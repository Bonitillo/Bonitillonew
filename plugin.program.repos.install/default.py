#!/usr/bin/python
#coding=utf-8


import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import shutil
import urllib2,urllib
import re
import extract
import time
import downloader
import plugintools
import zipfile
import ntpath


ADDON=xbmcaddon.Addon(id='plugin.program.repos.install')
localString = ADDON.getLocalizedString
home = ADDON.getAddonInfo('path').decode ( "utf-8" )
local_wizard = xbmc.translatePath(os.path.join(home, 'resources', 'data', 'local_wizard.txt'))
online_wizard = xbmc.translatePath(os.path.join(home, 'resources', 'data', 'online_wizard.txt'))
kodi_zip = xbmc.translatePath(os.path.join(home, 'resources', 'zipfile', 'kodi.zip'))
image_file =  xbmc.translatePath(os.path.join(home, 'resources', 'data'))
source = ADDON.getSetting('source')
url_source = ADDON.getSetting('url')
dialog = xbmcgui.Dialog()    
VERSION = "1.0.0"
PATH = "ReposInstall"            


def categories():
    if source == 'Local':
        link = open_file(local_wizard).replace('\n','').replace('\r','')
    else:
        if len(url_source) < 1:
            ADDON.openSettings()
            sys.exit()
        link = open_file(online_wizard).replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        if url == 'use_url':
            url = url.replace('use_url', url_source)
        addDir(name,url,1,image_file+'/'+iconimage,image_file+'/'+fanart,description)
    setView('movies', 'MAIN')


def open_file(file):
    content = open(file, 'r')
    link = content.read()
    content.close()
    return link


def wizard(name,url,description):
    if url == 'use_local_file':
        dp = xbmcgui.DialogProgress()
        dp.create(localString(30001).encode('utf-8'), localString(30002).encode('utf-8'), '', '')
        lib=kodi_zip
    else:
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        dp = xbmcgui.DialogProgress()
        dp.create(localString(30001).encode('utf-8'), localString(30003).encode('utf-8'), '', '')
        lib=os.path.join(path, name+'.zip')
        try:
           os.remove(lib)
        except:
           pass
        downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", localString(30004).encode('utf-8'))
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    dialog = xbmcgui.Dialog()
    #dialog.ok(localString(30005).encode('utf-8'), localString(30006).encode('utf-8'), localString(30007).encode('utf-8'), localString(30008).encode('utf-8'))
    #killxbmc()
    dialog.ok(localString(30005).encode('utf-8'), localString(30022).encode('utf-8'), "", "")


def killxbmc():
    choice = xbmcgui.Dialog().yesno(localString(30009).encode('utf-8'), localString(30010).encode('utf-8'), localString(30011).encode('utf-8'), nolabel=localString(30012).encode('utf-8'), yeslabel=localString(30013).encode('utf-8'))
    if choice == 0:
        return
    elif choice == 1:
        pass
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok(localString(30014).encode('utf-8'), localString(30015).encode('utf-8'), localString(30016).encode('utf-8'),'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok(localString(30014).encode('utf-8'), localString(30015).encode('utf-8'), localString(30016).encode('utf-8'),'')
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass        
        dialog.ok(localString(30014).encode('utf-8'), localString(30017).encode('utf-8'), localString(30018).encode('utf-8'),localString(30019).encode('utf-8'))
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok(localString(30014).encode('utf-8'), localString(30015).encode('utf-8'), localString(30016).encode('utf-8'), localString(30020).encode('utf-8'))
    else: #ATV
        print "############   try atv force close  #################"
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok(localString(30014).encode('utf-8'), localString(30015).encode('utf-8'), localString(30016).encode('utf-8'), localString(30021).encode('utf-8'))


def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'


def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok


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
mode=None
iconimage=None
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


def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )


if mode==None or url==None or len(url)<1:
        categories()

elif mode==1:
        wizard(name,url,description)


xbmcplugin.endOfDirectory(int(sys.argv[1]))