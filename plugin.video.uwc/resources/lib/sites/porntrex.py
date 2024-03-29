'''
    Ultimate Whitecream
    Copyright (C) 2015 Whitecream

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

import re

import xbmc
import xbmcplugin
import xbmcgui
from resources.lib import utils


@utils.url_dispatcher.register('50')    
def PTMain():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://www.porntrex.com/categories/',53,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://www.porntrex.com/search/',54,'','')
    PTList('http://www.porntrex.com/latest-updates/1/',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('51', ['url'], ['page'])
def PTList(url, page=1, onelist=None):
    if onelist:
        url = url.replace('/1/','/'+str(page)+'/')
    try:
        listhtml = utils.getHtml(url, '')
    except:
        utils.notify('Oh oh','It looks like this website is down.')
        return None
    match = re.compile('class="video-item.*?href="([^"]+)" title="([^"]+)".*?original="([^"]+)"(.*?)clock-o"></i>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, name, img, hd, duration in match:
        name = utils.cleantext(name)
        if hd.find('HD') > 0:
            hd = " [COLOR orange]HD[/COLOR] "
        else:
            hd = " "
        name = name + hd + "[COLOR deeppink]" + duration + "[/COLOR]"
        utils.addDownLink(name, videopage, 52, img, '')
    if not onelist:
        if re.search('<li class="next">', listhtml, re.DOTALL | re.IGNORECASE):
            npage = page + 1        
            url = url.replace('/'+str(page)+'/','/'+str(npage)+'/')
            utils.addDir('Next Page ('+str(npage)+')', url, 51, '', npage)
        xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('52', ['url', 'name'], ['download'])
def PTPlayvid(url, name, download=None):
    videopage = utils.getHtml(url, '')
    match = re.compile("video_alt_url2: '([^']+)'", re.DOTALL | re.IGNORECASE).findall(videopage)
    match2 = re.compile("video_alt_url: '([^']+)'", re.DOTALL | re.IGNORECASE).findall(videopage)
    try: videourl = match[0]
    except: videourl = match2[0]

    if download == 1:
        utils.downloadVideo(videourl, name)
    else:
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        xbmc.Player().play(videourl, listitem)


@utils.url_dispatcher.register('53', ['url'])
def PTCat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<a class="item" href="([^"]+)" title="([^"]+)".*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name, img in match:
        utils.addDir(name, catpage, 51, img, 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('54', ['url'], ['keyword'])  
def PTSearch(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 54)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title + '/'
        print "Searching URL: " + searchUrl
        PTList(searchUrl, 1)
