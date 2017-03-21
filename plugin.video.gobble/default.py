import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,net,json,base64,random

AddonID ='plugin.video.gobble'
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID, 'icon.png'))
setting = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID + '/resources/','setting.xml'))
swift = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID + '/resources/','swift.png'))
sport = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID + '/resources/','sport.png'))
live = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID + '/resources/','live.png'))
dialog = xbmcgui.Dialog()
selfAddon = xbmcaddon.Addon(id=AddonID)
net = net.Net()
setting = open(setting, "r")
r=setting.read()
setting.close()
uas=re.compile('<>(.+?)<>').findall(r)
selfAddon.setSetting('ADDONAGENT',random.choice(uas))
aua=selfAddon.getSetting('ADDONAGENT')

def INDEX():
	addDir('Swift Streams','url',3,swift,fanart)
	addDir('Sports TV','url',4,sport,fanart)
	xbmc.executebuiltin('Container.SetViewMode(500)')
    
def SportsTVMain():
	headers={'User-Agent':aua}
	page=net.http_GET('http://sportstv.club/',headers).content
	channels=re.compile('<td><a href="(.+?)"><center><img src="(.+?)" width="150" height="55"/></a></td>').findall(page)
	for url,iconimage in channels:
		if 'tvhistories' in url and not '/channel/' in url:
			name=url.split('/')[-1].replace('.php','').title()
			iconimage='http://sportstv.club'+iconimage
			addLink(name,url,5,iconimage,fanart)
	xbmc.executebuiltin('Container.SetViewMode(500)')
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_LABEL)

def SportsTVGetLinks(name,url,iconimage):
	hstring='|User-Agent=%s'%'hellosamaam'
	headers={'User-Agent':aua}
	page=net.http_GET(url,headers).content
	links=re.compile('<li><a href="(.+?)" align="center">.+?</a>').findall(page)
	if len(links)>1:
		streamurl=[]
		streamname=[]
		i=1
		for url in links:
			streamname.append('Link '+str(i))
			streamurl.append(url)
			i=i+1
		select = dialog.select(name,streamname)
		if select == -1:return
		else:
			url=streamurl[select]+hstring
	else:url=links[0]+hstring
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	xbmc.Player().play(url, liz, False)
	return ok

def SwiftMain():
	hstring='|User-Agent=%s&Host=swiftstreamz.com&Accept-Encoding=gzip&Connection=Keep-Alive'%aua
	headers={'Authorization':'Basic U3dpZnRUZWM6QFN3aWZ0VGVjQA==',
		 'User-Agent':aua,
		 'Host':'swiftstreamz.com',
		 'Connection':'Keep-Alive',
		 'Accept-Encoding':'gzip'}
	data=net.http_GET('http://swiftstreamz.com/SwiftStream/swiftdata.php',headers).content
        loginUrl=re.compile('"loginUrl":"(.+?)"').findall(data)[0] #http://173.212.202.101/token001.php
	selfAddon.setSetting('loginUrl',loginUrl)
	Password=re.compile('"Password":"(.+?)"').findall(data)[0] #QFN3aWZ0MTEjOkBTd2lmdDExIw==
	selfAddon.setSetting('Password',base64.b64encode(Password))
	
        loginUrlNew=re.compile('"loginUrlNew":"(.+?)"').findall(data)[0] #http://173.212.202.101/token003.php
	selfAddon.setSetting('loginUrlNew',loginUrlNew)
	PasswordNew=re.compile('"PasswordNew":"(.+?)"').findall(data)[0] #QFN3aWZ0MTMjOkBTd2lmdDEzIw==
	selfAddon.setSetting('PasswordNew',base64.b64encode(PasswordNew))
	
	HelloLogin=re.compile('"HelloLogin":"(.+?)"').findall(data)[0] #http://173.212.202.101/token004.php
	selfAddon.setSetting('HelloLogin',HelloLogin)
        HelloUrl=re.compile('"HelloUrl":"(.+?)"').findall(data)[0] #http://51.15.137.107:8081/ .... token4
	selfAddon.setSetting('HelloUrl',HelloUrl)
        HelloUrl1=re.compile('"HelloUrl1":"(.+?)"').findall(data)[0] #http://51.15.57.159:8081/ .... token4
	selfAddon.setSetting('HelloUrl1',HelloUrl1)
	PasswordHello=re.compile('"PasswordHello":"(.+?)"').findall(data)[0] #QFN3aWZ0MTQjOkBTd2lmdDE0Iw==
	selfAddon.setSetting('PasswordHello',base64.b64encode(PasswordHello))

	LiveTvUrl=re.compile('"LiveTvUrl":"(.+?)"').findall(data)[0] #http://51.15.47.194:8081/ .... token2
	selfAddon.setSetting('LiveTvUrl',LiveTvUrl)
	LiveTvLogin=re.compile('"LiveTvLogin":"(.+?)"').findall(data)[0] #http://173.212.202.101/token002.php
	selfAddon.setSetting('LiveTvLogin',LiveTvLogin)
	PasswordLiveTv=re.compile('"PasswordLiveTv":"(.+?)"').findall(data)[0] #QFN3aWZ0MTIjOkBTd2lmdDEyIw==
	selfAddon.setSetting('PasswordLiveTv',base64.b64encode(PasswordLiveTv))

	nexgtvUrl=re.compile('"nexgtvUrl":"(.+?)"').findall(data)[0] #http://51.15.57.108:8081/ .... token5
	selfAddon.setSetting('nexgtvUrl',LiveTvUrl)
	nexgtvToken=re.compile('"nexgtvToken":"(.+?)"').findall(data)[0] #http://173.212.202.101/token005.php
	selfAddon.setSetting('nexgtvToken',nexgtvToken)
	nexgtvPass=re.compile('"nexgtvPass":"(.+?)"').findall(data)[0] #QFN3aWZ0MTUjOkBTd2lmdDE1Iw==
	selfAddon.setSetting('nexgtvPass',base64.b64encode(nexgtvPass))

	Agent=re.compile('"Agent":"(.+?)"').findall(data)[0] #123new
	selfAddon.setSetting('Agent',Agent)

	api=net.http_GET('http://swiftstreamz.com/SwiftStream/api.php',headers).content
	api=json.loads(api)
	api=api['LIVETV']
	for resp in api:
		iconimage='http://swiftstreamz.com/SwiftStream/images/thumbs/'+resp['category_image']+hstring
		name=resp['category_name']
		url='http://swiftstreamz.com/SwiftStream/api.php?cat_id='+resp['cid']
		if not 'MOVIES' in name and not 'IRAN' in name and not 'INDON' in name:
			addDir(name,url,1,iconimage,fanart)
	xbmc.executebuiltin('Container.SetViewMode(500)')

def SwiftGetChannels(url):
	hstring='|User-Agent=%s&Host=swiftstreamz.com&Accept-Encoding=gzip&Connection=Keep-Alive'%aua
	headers={'Authorization':'Basic %s'%selfAddon.getSetting('Password'),'User-Agent':aua,'Host':'swiftstreamz.com','Connection':'Keep-Alive','Accept-Encoding':'gzip'}
	data=net.http_GET(url,headers).content
	data=json.loads(data)
	data=data['LIVETV']
	for channel in data:
		iconimage='http://swiftstreamz.com/SwiftStream/images/thumbs/'+channel['channel_thumbnail']+hstring
		name=channel['channel_title']
		url=channel['channel_url']
		addLink(name,url,2,iconimage,fanart)
	xbmc.executebuiltin('Container.SetViewMode(500)')
		    
def SwiftPlayStream(name,url,iconimage):
        if '51.15.47.194:8081' in url:
                tokenurl=selfAddon.getSetting('LiveTvLogin')
                password=selfAddon.getSetting('PasswordLiveTv')
        elif '51.15.57.108:8081' in url:
                tokenurl=selfAddon.getSetting('nexgtvToken')
                password=selfAddon.getSetting('nexgtvPass')
        else:
                tokenurl=selfAddon.getSetting('HelloLogin')
                password=selfAddon.getSetting('PasswordHello')
        passw='Basic '+password
        headers={'Authorization':passw,
                 'User-Agent':'Dalvik/1.6.0 (Linux; U; Android 4.4.2; SM-G900F Build/KOT49H)',
                 'Host':'173.212.202.101'}
        token=net.http_GET(tokenurl,headers).content.replace('eMeeea/1.0.0.','')
	hstring='|User-Agent=%s'%selfAddon.getSetting('Agent')        
        url=url+token+hstring
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	xbmc.Player().play(url, liz, False)
	return ok

def addLink(name,url,mode,iconimage,fanart):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': '' } )
	liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def addDir(name,url,mode,iconimage,fanart):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	if not 'gobble'in u:quit()
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': '' } )
	liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:mode=int(params["mode"])
except:pass
try:iconimage=urllib.unquote_plus(params["iconimage"])
except:pass

if mode==None or url==None or len(url)<1:SwiftMain()#INDEX()
elif mode==1:SwiftGetChannels(url)
elif mode==2:SwiftPlayStream(name,url,iconimage)
elif mode==3:SwiftMain()
elif mode==4:SportsTVMain()
elif mode==5:SportsTVGetLinks(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
