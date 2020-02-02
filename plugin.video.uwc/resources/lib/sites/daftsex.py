'''
    Ultimate Whitecream
    Copyright (C) 2016 Whitecream, hdgdl
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib2
import re

import xbmc
import xbmcplugin
import xbmcgui
from resources.lib import utils

@utils.url_dispatcher.register('610')
def Main():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','https://daftsex.com/categories',614,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','https://daftsex.com/video/',613,'','')
    utils.addDir('[COLOR red]Random TV[/COLOR]','https://daftsex.com/',615,'','')
    List('https://daftsex.com/hot')

def FindServer(video, vp, encrypted_server):
    srvs = {'SM':'1','iM':'2','yM':'3','CN':'4','SN':'5',
            'cTM':'17','AjM':'20','MDN':'43','UDN':'45','YDN':'46','cDN':'47','gDN':'48','ATN':'50','ETN':'51','ITN':'52','QTN':'54','MjN':'63',
            'QjN':'64','UjN':'65','YjN':'66','cjN':'67', 'gjN':'68','kjN':'69','AzN':'70','EzN':'71'}

    if encrypted_server.startswith('1JnLkV3bsNWe6Fmcj5'):
        srv = 'https://psv' + srvs[encrypted_server[21:24]] + '-' + srvs[encrypted_server[18:20]] + '.crazycloud.ru'
        utils.kodilog(srv + '/videos/' + video)
        return srv + '/videos/' + video
        
    if encrypted_server.startswith('=02bj5iYhhXYk5'):
        srv = 'https://psv' + srvs[encrypted_server[17:20]] + '-' + srvs[encrypted_server[14:16]] + '.daxab.com'
        utils.kodilog(srv + '/videos/' + video)
        return srv + '/videos/' + video

    # crazycloud_list = ['17-1','17-2','17-3','20-1','20-2','20-3']
    # daxab_list = ['12-1','17-4','20-5','32-1','33-1','43-1','45-1','46-1','47-1','48-1','50-1','51-1','52-1','53-1','54-1','55-1','56-1','57-1','58-1','59-1','60-1','63-1','64-1','65-1','66-1','67-1','68-1','68-2','69-1','69-2','69-3','69-4']
    
    # if len(encrypted_server)>25:
        # i = 1
        # for srv in crazycloud_list:
            # server = 'https://psv' + srv + '.crazycloud.ru'
            # vp.progress.update(25 + i, "", "Searching on crazycloud.ru ... " + srv, "")
            # try:
                # code = urllib2.urlopen(server + '/videos/' + video, timeout = 1).getcode()
                # if code == 200:
                    # with open(server_txt, 'a') as f:
                        # f.write(encrypted_server + '#' + server +'\r\n')
                    # return (server + '/videos/' + video)
            # except:
                # i = i+1
    # else:
        # i = 1
        # for srv in daxab_list:
            # server = 'https://psv' + srv + '.daxab.com'
            # vp.progress.update(25 + i, "", "Searching on daxab.com ... " + srv, "")
            # try:
                # code = urllib2.urlopen(server + '/videos/' + video, timeout = 0.5).getcode()
                # if code == 200:
                    # with open(server_txt, 'a') as f:
                        # f.write(encrypted_server + '#' + server +'\n')
                    # return (server + '/videos/' + video)
            # except:
                # i = i+1
    utils.kodilog('not found ' + video)


@utils.url_dispatcher.register('611', ['url'], ['page'])
def List(url, page=0):
    try:
        postRequest = {'page' : str(page)}
        response = utils.postHtml(url, form_data=postRequest,headers={},compression=False)
    except:
        return None
    match = re.compile('<div class="video-item">.*?a href="([^"]+)".*?<img src="([^"]+)" alt="([^"]+)".*?<span class="video-time">([^<]+)', re.DOTALL | re.IGNORECASE).findall(response)
    for video, img, name, length in match:
        video = 'https://daftsex.com' + video
        name = '[COLOR hotpink]' + length + '[/COLOR] ' + utils.cleantext(name)
        utils.addDownLink(name, video, 612, img, '')
    npage = page + 1
    utils.addDir('Next Page (' + str(npage) + ')', url, 611, '', npage)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('612', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    vp = utils.VideoPlayer(name, download = download)
    vp.progress.update(25, "", "Loading video page", "")
    vidsite = utils.getHtml(url, 'https://daftsex.com/')

    videourl = re.compile('<iframe.+?src="(https://da{0,1}xa{0,1}b\.[ct]om{0,1}/[^"]+)"', re.DOTALL | re.IGNORECASE).findall(vidsite)[0]
    videopage = utils.getHtml(videourl, 'https://daftsex.com/')
    if utils.addon.getSetting('daftsexresolver') == '0':
        server =''
        try:	
            match = re.compile('id: "([^"]+)_([^"]+)".+:"(\d+)\.([^"]+)"}.+?server:\s*?"([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)[0]
            (id1, id2, res, extra, server) =  match
            video =  id1 + '/' + id2 + '/' + res + '.mp4?extra=' + extra
            fserver = FindServer(video, vp, server)
            vp.play_from_direct_link(fserver)
            return
        except:
            pass
    video = 'https://vk.com/video' + re.compile("Fav.Toggle\(this, '([^']+)'", re.DOTALL | re.IGNORECASE).findall(vidsite)[0]
    vp.play_from_link_to_resolve(video)

@utils.url_dispatcher.register('613', ['url'], ['keyword'])
def Search(url, keyword=None):
    searchUrl = url
    xbmc.log("Search: " + searchUrl)
    if not keyword:
        utils.searchDir(url, 613)
    else:
        title = keyword.replace(' ','_')
        searchUrl = searchUrl + title
        xbmc.log("Search: " + searchUrl)
        List(searchUrl)

@utils.url_dispatcher.register('614', ['url'])
def Categories(url):
    response = utils.getHtml(url, 'https://daftsex.com/')
    match = re.compile('<div class="video-item">.*?a href="([^"]+)">.*?<img src="([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(response)
    for caturl, img, name in sorted(match, key=lambda x: x[2]):
        caturl = 'https://daftsex.com' + caturl
        img = 'https://daftsex.com' + img
        utils.addDir(name, caturl, 611, img, 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)

@utils.url_dispatcher.register('615', ['url'])
def Random(url):
    response = utils.getHtml(url, 'https://daftsex.com/')
    match = re.compile('title="RandomTV" href="([^"]+)" class="randomQuery"', re.DOTALL | re.IGNORECASE).findall(response)
    title = match[0].replace('/video/','')
    utils.addDir('[COLOR red]' + title + '[/COLOR]', url, 615,'','')
    List('https://daftsex.com' + match[0])