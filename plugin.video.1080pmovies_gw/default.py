# -*- coding: utf-8 -*-
import urllib2, urllib, xbmcgui,xbmcaddon, xbmcplugin, xbmc, re, sys, os
import urlresolver
from addon.common.addon import Addon
import requests
s = requests.session() 
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
addon_id='plugin.video.1080pmovies_gw'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
addon_name = selfAddon.getAddonInfo('name')
ADDON      = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo('path')
ICON = ADDON.getAddonInfo('icon')
FANART = ADDON.getAddonInfo('fanart')
PATH = '1080pmovies_gw'
VERSION = ADDON.getAddonInfo('version')
ART = ADDON_PATH + "/resources/icons/"
BASEURL = 'http://1080pmovies.org/'
ART = ADDON_PATH + "/resources/icons/"

def Main_menu():
    addDir('[B][COLOR white]Latest Added[/COLOR][/B]',BASEURL,5,ART + 'latest.jpg',FANART,'')
    addDir('[B][COLOR white]Top Movies[/COLOR][/B]',BASEURL + '?tag=top',5,ART + 'top.jpg',FANART,'')
    addDir('[B][COLOR white]2016[/COLOR][/B]',BASEURL + '?tag=2016',5,ART + '2016.jpg',FANART,'')
    addDir('[B][COLOR white]2015[/COLOR][/B]',BASEURL + '?tag=2015',5,ART + '2015.jpg',FANART,'')
    addDir('[B][COLOR red]Search Movies[/COLOR][/B]','url',6,ART + 'search.jpg',FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def Get_content(url):
    referer = url
    headers = {'Host': '1080pmovies.org', 'User-Agent': User_Agent, 'Referer': referer}
    OPEN = Open_Url(url)
    Regex = re.compile('<div class="post-thumbnail">.+?<img width="420" height="636" src="(.+?)".+?<h1 class="entry-title"><a href="(.+?)".+?>(.+?)</a></h1>',re.DOTALL).findall(OPEN)
    for icon,url,name in Regex:
            name = name.replace('&#8217;','\'').replace('&#8211;','-').replace('&#039;','\'')
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,'')
    np = re.compile("<link rel='next' href='(.+?)'",re.DOTALL).findall(OPEN)
    for url in np:
        url=url.replace('#038;','')
        addDir('[B][COLOR blue]Next Page>>>[/COLOR][/B]',url,5,ART + 'nextpage.jpg',FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def Search():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = BASEURL + '?s=' + search + '&submit=Search'
                Get_content(url)
    
	
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


def resolve(name,url,iconimage,description): 
    OPEN = Open_Url(url)
    try:
        url = re.compile('<iframe src="https://openload.co/(.+?)"',re.DOTALL).findall(OPEN)[0]
        url = 'https://openload.co/' + url
        stream_url=urlresolver.resolve(url)
        liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={"Title": description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(stream_url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:
        url = re.compile('<iframe src="https://drive.google.com/file/d/(.+?)/preview"',re.DOTALL).findall(OPEN)[0]
        url = 'https://drive.google.com/file/d/' + url + '/edit' 
        stream_url=urlresolver.resolve(url)
        liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={"Title": description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(stream_url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

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
        
        
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
#########################################################
	
if mode == None: Main_menu()
elif mode == 5 : Get_content(url)
elif mode == 6 : Search()
elif mode == 100 : resolve(name,url,iconimage,description)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
