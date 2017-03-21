# -*- coding: utf-8 -*-
import urllib2, urllib, xbmcgui, xbmcplugin, xbmc, re, sys, os, base64, dandy, xbmcaddon
import urlresolver
import requests
from addon.common.addon import Addon
s = requests.session() 
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
addon_id='plugin.video.fineanddandy'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
addon_name = selfAddon.getAddonInfo('name')
ART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/icons/'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
BASEURL = 'http://www.mydownloadtube.com/'
BASEURL2 = 'http://www.mydownloadtube.tv/'


def Main_menu():
    addDir('[B][COLOR white]Most Popular Movies[/COLOR][/B]',BASEURL+'movies/most_popular',5,ART + 'mostpop.jpg',FANART,'')
    addDir('[B][COLOR white]Recently Added Movies[/COLOR][/B]',BASEURL+'movies/recent',5,ART + 'recent.jpg',FANART,'')
    addDir('[B][COLOR white]Most Downloaded Movies[/COLOR][/B]',BASEURL+'movies/most_download',5,ART + 'mostdown.jpg',FANART,'')
    addDir('[B][COLOR white]All Movies[/COLOR][/B]',BASEURL+'movies/all',5,ART + 'allmovies.jpg',FANART,'')
    addDir('[B][COLOR white]Animation Movies[/COLOR][/B]',BASEURL+'genres/movies/animation',5,ART + 'animate.jpg',FANART,'')
    addDir('[B][COLOR white]Movie Genres[/COLOR][/B]','',3,ART + 'genres.jpg',FANART,'')
    addDir('[B][COLOR white]Search Movies[/COLOR][/B]','url',6,ART + 'search.jpg',FANART,'')
    addDir('[B][COLOR white]TV Shows Menu[/COLOR][/B]','',2,ART + 'tv_menu.jpg',FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

    
def tv_menu():
    addDir('[B][COLOR white]Most Popular Series[/COLOR][/B]',BASEURL2+'series/most_popular',4,ART + 'pop_tv.jpg',FANART,'')
    addDir('[B][COLOR white]Recently Added Series[/COLOR][/B]',BASEURL2+'series/recent',4,ART + 'recent_tv.jpg',FANART,'')
    addDir('[B][COLOR white]Featured Series[/COLOR][/B]',BASEURL2+'series/featured_series',4,ART + 'feat_tv.jpg',FANART,'')
    addDir('[B][COLOR white]Most Watched Series[/COLOR][/B]',BASEURL2+'series/most_watched',4,ART + 'mw_tv.jpg',FANART,'')
    addDir('[B][COLOR white]Upcoming Series[/COLOR][/B]',BASEURL2+'series/up_coming',4,ART + 'up_tv.jpg',FANART,'')
    addDir('[B][COLOR white]TV Genres[/COLOR][/B]','',8,ART + 'genre_tv.jpg',FANART,'')
    #addDir('[B][COLOR white]Search TV Series[/COLOR][/B]','url',6,ART + 'search.jpg',FANART,'')

def Get_Genres():
    OPEN = Open_Url('http://www.mydownloadtube.com/')
    Regex = re.compile('>Hollywood Movies</a>(.+?)</ul>',re.DOTALL).findall(OPEN)
    Regex2 = re.compile('href="(.+?)">(.+?)</a>',re.DOTALL).findall(str(Regex))
    for url,name in Regex2:
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,5,ART + 'genres.jpg',FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
    
def TV_Genres():
    OPEN = Open_Url('http://www.mydownloadtube.tv/')
    Regex = re.compile('class="mega-hdr-a sub-cat" href="#">Series</a>(.+?)</ul>',re.DOTALL).findall(OPEN)
    Regex2 = re.compile('href="(.+?)">(.+?)</a>',re.DOTALL).findall(str(Regex))
    for url,name in Regex2:
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,4,ART + 'genre_tv.jpg',FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def Get_content(url):
    referer = url
    headers = {'Host': 'www.mydownloadtube.com', 'User-Agent': User_Agent, 'Referer': referer}
    OPEN = Open_Url(url)
    Regex = re.compile('<ul class="pop-lists pop"(.+?)</ul>',re.DOTALL).findall(OPEN)[0]
    Regex = Regex.replace('\r','').replace('\n','').replace('\t','')
    Regex2 = re.compile('<li>.+?href="(.+?)".+?data.+? src="(.+?)" alt="(.+?)"').findall(str(Regex))
    for url,icon,name in Regex2:
            name = name.replace('Free Download','').replace('\\','').replace('poster','')
            icon = icon.replace('listing_thumb','detail_page_poster')
            icon = icon + '|' + urllib.urlencode(headers)
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,BASEURL+url,10,icon,FANART,'')

    np = re.compile('<a rel="(.+?)" href="(.+?)"',re.DOTALL).findall(OPEN)
    for name,url in np:
            if 'next' in name:
                    addDir('[B][COLOR blue]Next Page>>>[/COLOR][/B]',url,5,ART + 'nextpage.jpg',FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def Get_tv_content(url):
    referer = url
    headers = {'Host': 'www.mydownloadtube.tv', 'User-Agent': User_Agent, 'Referer': referer}
    OPEN = Open_Url(url)
    Regex = re.compile('<ul class="pop-lists pop">(.+?)</ul>',re.DOTALL).findall(OPEN)[0]
    Regex = Regex.replace('\r','').replace('\n','').replace('\t','')
    Regex2 = re.compile('<li>.+?href="(.+?)".+?data.+? src="(.+?)" alt="(.+?)"').findall(str(Regex))
    for url,icon,name in Regex2:
            name = name.replace('Watch ','').replace('online free.','').replace('Full series download HD','').replace(' poster','')
            icon = icon.replace('listing_thumb','detail_page_poster')
            icon = icon + '|' + urllib.urlencode(headers)
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,BASEURL2+url,7,icon,FANART,'')

    np = re.compile('<a rel="(.+?)" href="(.+?)"',re.DOTALL).findall(OPEN)
    for name,url in np:
            if 'next' in name:
                    addDir('[B][COLOR blue]Next Page>>>[/COLOR][/B]',url,4,ART + 'nextpage.jpg',FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
    
def Get_tv_episodes(url):
    referer = url
    headers = {'Host': 'www.mydownloadtube.tv', 'User-Agent': User_Agent, 'Referer': referer}
    OPEN = Open_Url(url)
    Regex = re.compile('<div class=".+?-box-wrp">(.+?)</div>',re.DOTALL).findall(OPEN)
    Regex2 = re.compile('<td><strong><a href="(.+?)">(.+?)</a></strong></td>.+?<td><strong>.+?</strong></td>.+?<td>(.+?)</td>').findall(str(Regex))
    for url,epis,airdate in Regex2:
            name = epis + '[COLOR red] ' + airdate
            name = name.replace('"',' - ').replace('\\','')
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,9,iconimage,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
    
def Get_links(name,url,iconimage):
    nono = name.replace('[B][COLOR white]','').replace('[/COLOR][/B]','')
    nono2 = name.partition('(')[0].replace('[B][COLOR white]','').replace('[/COLOR][/B]','')
    OPEN = Open_Url(url)
    Regex = re.compile("'Downloads-Server', '(.+?)'.+?>(.+?)</a>.+?value=\"(.+?)\"",re.DOTALL).findall(OPEN)
    for name2, name3, url in Regex:
            name2 = name2.replace('b - Bit - ','').replace('c - Bit - ','').replace('d - Bit - ','').replace('e - Bit - ','').replace('Download Server (factory)','FileFactory').strip()
            name3 = name3.replace('\n','').replace('\t','').replace(nono,'').replace(nono2,'').replace('-','[COLOR red]|[/COLOR]')
            if 'Movie Promo Host' not in name2:
                    if 'Multi' not in name2:
                            addDir('[B][COLOR red]%s [/COLOR][COLOR white]%s[/COLOR][/B]' %(name2,name3),url,100,iconimage,FANART,name)
    for name4, name5, url in Regex:
            name5 = name5.replace('\n','').replace('\t','').replace(nono,'').replace(nono2,'').replace('-','[COLOR red]|[/COLOR]')
            if 'Multi' in name4:
                    addDir('[B][COLOR red]Click Here For Multi Debrid [COLOR white]%s[/COLOR] Links[/COLOR][/B]' %name5,url,11,iconimage,FANART,name)
    xbmc.executebuiltin('Container.SetViewMode(50)')

def Get_tv_links(name,url,iconimage):
    OPEN = Open_Url(url)
    Regex = re.compile('<td>&nbsp;</td>.+?<img src="(.+?)".+?<a href="(.+?)"',re.DOTALL).findall(OPEN)
    for name2,url in Regex:
        if 'multiUp-org' not in name2:
            if 'Full_Speed_' not in name2:
                name2 = name2.split('_')[2].replace('logo.png','').replace('Logo.png','').replace('.jpg','').title()
                addDir('[B][COLOR red]%s[/COLOR][/B]' %name2,url,100,iconimage,FANART,name)
    for name2,url in Regex:
            if 'multiUp-org' in name2:
                name2 = name2.split('_')[2].replace('.png','').title()
                addDir('[B][COLOR red]Click Here For Multi Debrid [COLOR white]%s[/COLOR] Links[/COLOR][/B]' %name2,url,11,iconimage,FANART,name)
    xbmc.executebuiltin('Container.SetViewMode(50)')

def Get_multi_links(name,url,iconimage,description):
        name = description
        if 'bit.ly' in url:
                headers = {'User-Agent': User_Agent}
                r = requests.get(url,headers=headers,allow_redirects=False)
                url = r.headers['location']
        url=url.replace('https://www.multiup.org/en/mirror/','http://www.multiup.org/en/mirror/').replace('https://www.multiup.org/download/','http://www.multiup.org/en/mirror/')
        OPEN = Open_Url(url)
        Regex = re.compile('nameHost="(.+?)".+?validity=(.+?)dateLastChecked=.+?href="(.+?)"',re.DOTALL).findall(OPEN)
        for name2, validity, url in Regex:
                if 'invalid' not in validity:
                        if urlresolver.HostedMediaFile(url):
                                addDir('[B][COLOR red]%s[/COLOR][/B]' %name2,url,100,iconimage,FANART,name)


def Search():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','-')
                url = BASEURL + 'search/movies/' + search
                Get_content(url)
    
#def Search_TV():
 #       keyb = xbmc.Keyboard('', 'Search')
 #       keyb.doModal()
  #      if (keyb.isConfirmed()):
  #              search = keyb.getText().replace(' ','%20')
   #             url = BASEURL2 + 'search/series/' + search
   #             Get_tv_content(url)
########################################


def Open_Url(url):
    headers = {}
    headers['User-Agent'] = User_Agent
    link = s.get(url, headers=headers).text
    link = link.encode('ascii', 'ignore')
    return link


def addDir(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
	liz.setProperty('fanart_image', fanart)
	if mode==100:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok


def resolve(url):
    if 'bit.ly' in url:
            headers = {'User-Agent': User_Agent}
            r = requests.get(url,headers=headers,allow_redirects=False)
            url = r.headers['location'] 
    if 'adf.ly' in url:
            adfly_data = requests.get(url).content
            ysmm = adfly_data.split("ysmm = \'")[1].split("\';")[0]
            url = crack(ysmm)
    url=urlresolver.HostedMediaFile(url).resolve()
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": description})
    liz.setProperty("IsPlayable","true")
    liz.setPath(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)


def crack(code):
        #Function written by D4Vinci
        zeros = ''
        ones = ''
        for n,letter in enumerate(code):
                if n%2 == 0:
                        zeros += code[n]
                else:
                        ones =code[n] + ones
        key = zeros + ones
        key = base64.b64decode(key.encode("utf-8"))
        return key[2:]
		


def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2: 
                params=sys.argv[2] 
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}    
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
        
params=get_params()
url=None
name=None
iconimage=None
mode=None
fanart=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        
        

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
#########################################################
	
if mode == None: Main_menu()
elif mode == 2 : tv_menu()
elif mode == 3 : Get_Genres()
elif mode == 8 : TV_Genres()
elif mode == 5 : Get_content(url)
elif mode == 4 : Get_tv_content(url)
elif mode == 7 : Get_tv_episodes(url)
elif mode == 6 : Search()
#elif mode == 12 : Search_TV()
elif mode == 9 : Get_tv_links(name,url,iconimage)
elif mode == 10 : Get_links(name,url,iconimage)
elif mode == 11 : Get_multi_links(name,url,iconimage,description)
elif mode == 100 : resolve(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
