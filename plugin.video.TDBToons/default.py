##########################################################################################################
#																										 #
#								TDB Wizard Video Add-On Base Code                                        #
# 																										 #
# This addon is a modified base code taken from the Evolve addon.                                        #
# The original base code was coded by Mettle Ketal for use by Team Evolve.                               # 
# The base code was then adapted for use by Evolve Team members Trapper and Slim.                        # 
# During my development with Trapper and Slim I had to make some substantial modifications               # 
# To the code to allow certain things to work. Kodi as a platform is constantly changing                 # 
# and due to this things change, this can mean certain base codes become outdated and no longer          #
# Function as intended. I have since had approval from Trapper to modify the base code and release       #
# it for public use.           																			 #
# This base code was originaly from MK and has since been edited by TDB Wizard.                          # 
# Any questions regarding this addon please contact TDB Wizard @TDBWizard on Twitter                     # 
# E-Mail - tdbwizard@gmail.com or online at www.tdbwizard.co.uk/forum                                    #
#																										 #
##########################################################################################################

##########################################################################################################
#									IMPORT REQUIRED PYTHON MODULES										 #
##########################################################################################################
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,shutil,urlresolver,random,liveresolver
import requests
import time
import downloader
import zipfile
from resources.libs.common_addon import Addon
import base64
from metahandler import metahandlers

##########################################################################################################
#					            DEFINE VERIABLES NEEDED BY THE PLUGIN								     #
##########################################################################################################
## MUST BE CHANGED TO REPRESENT THE ADDON BEING USED
## -------------------------------------------------
addon_id        = 'plugin.video.TDBToons'
## -------------------------------------------------
addon           = Addon(addon_id, sys.argv)
selfAddon       = xbmcaddon.Addon(id=addon_id)
searchicon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
icon            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanarts         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'fanart.jpg'))
F4MTESTER       = xbmc.translatePath(os.path.join('special://home/addons/', 'plugin.video.f4mTester'))
AddonTitle      = "[COLOR dodgerblue][B]TDB[/B][/COLOR] [COLOR white]Toons[/COLOR]"
## MUST BE CHANGED TO REPRESENT THE ADDON BEING USED
## This is the URL to the main menu list.
## -------------------------------------------------
USER_AGENT      = base64.b64decode(b'VGhlV2l6YXJkSXNIZXJl')
## DEFAULT USER AGENT IS - TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgNi4xKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNDEuMC4yMjI4LjAgU2FmYXJpLzUzNy4zNg==
## -------------------------------------------------
## MUST BE CHANGED TO REPRESENT THE ADDON BEING USED
## This is the URL to the message disaplyed when the addon launches.
## -------------------------------------------------
messagetext     = base64.b64decode(b'aHR0cDovL3d3dy5sZWUtdHYubmV0L3Rvb25zcG9wdXAudHh0')
## -------------------------------------------------
## MUST BE CHANGED TO REPRESENT THE ADDON BEING USED
## This is the URL that contains all the search <link> items.
## -------------------------------------------------
## -------------------------------------------------

## VERIABLES FOR THE YOUTUBE API - DO NOT CHANGE
ytpl            = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId='
ytpl2           = '&maxResults=50&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA'
ytplpg1         = 'https://www.googleapis.com/youtube/v3/playlistItems?pageToken='
ytplpg2         = '&part=snippet&playlistId='
ytplpg3         = '&maxResults=50&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA'

##########################################################################################################
#					         IF YOU WOULD LIKE A POPUP HERE IS THE CODE FOR IT						     #
##########################################################################################################

try:
	baseurl = base64.b64decode(b'aHR0cDovL3d3dy50ZGJ3aXphcmQuY28udWsvYWRkb25zL2xlZS90ZGJ0b29ucy9tYWlubGlzdC54bWw=')
	req = urllib2.Request(baseurl)
	req.add_header('User-Agent', USER_AGENT)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	link=link.replace('\n','').replace('\r','').replace('<title></title>','<title>x</title>').replace('<link></link>','<link>x</link>').replace('<fanart></fanart>','<fanart>x</fanart>').replace('<thumbnail></thumbnail>','<thumbnail>x</thumbnail>').replace('<utube>','<link>https://www.youtube.com/watch?v=').replace('</utube>','</link>')#.replace('></','>x</')
	match= re.compile('<item>(.+?)</item>').findall(link)
	for item in match:
		url = baseurl
except:
	baseurl = base64.b64decode(b'aHR0cDovL3d3dy50ZGJ3aXphcmRidWlsZHMuY28udWsvYWRkb25zL2xlZS90ZGJ0b29ucy9tYWlubGlzdC54bWw=')

def popup():
 
	message=open_url(messagetext)
	if len(message)>1:
		path = xbmcaddon.Addon().getAddonInfo('path')
		comparefile = os.path.join(os.path.join(path,''), 'compare.txt')
#               if not os.path.isfile(comparefile):
#                    open(comparefile, "w")
		r = open(comparefile)
		compfile = r.read()       
		if compfile == message:pass
		else:
			f = requests.get(messagetext)
			TextBoxesPlain("%s" % f.text)
			text_file = open(comparefile, "w")
			text_file.write(message)
			text_file.close()
	
##########################################################################################################
#					  			      PLUGIN MAIN MENU FUNCTION							         	     #
##########################################################################################################
					
def GetMenu():
		#Set the url variable to the baseurl defined in the addon variables.
		url = baseurl
		# Add the Directory for the Search Function.
		#addDir("[COLOR dodgerblue][B]TDB[/COLOR] [COLOR white]Toons Search[/B][/COLOR]",url,5,searchicon,fanarts)
		# Open the baseurl to start getting the main menu list.
		link=open_url(baseurl)
		# Pull all data contained within the <item> tags.
		match= re.compile('<item>(.+?)</item>').findall(link)
		
		# This functions sends a loop for every <item> you have in  the list.
		for item in match:
			# Try the following, if there is an error it will pass and not show any errors.
			try:

				# Check if the item is a <folder>
				if '<poster>'in item:
					data=re.compile('<title>(.+?)</title>.+?poster>(.+?)</poster>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
					for name,url,iconimage,fanart in data:
						addDir("[B][COLOR white]" + name + "[/B][/COLOR]",url,1,iconimage,fanart)

				# If the item is not picked up by the sportsdevil or folder function do the following.
				else:
					links=re.compile('<link>(.+?)</link>').findall(item)
					# Count the number of <links> in the item.
					# If a single link do the following.
					if len(links)==1:
						data=re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>').findall(item)
						lcount=len(match)
						for name,url,iconimage in data:
							if 'youtube.com/playlist' in url:
								addDir("[B][COLOR white]" + name + "[/B][/COLOR]",url,2,iconimage,fanarts)
							else:
								addLink("[B][COLOR white]" + name + "[/B][/COLOR]",url,2,iconimage,fanarts)
					# If a multi link do the following.
					elif len(links)>1:
						name=re.compile('<title>(.+?)</title>').findall(item)[0]
						iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
						addLink("[B][COLOR white]" + name + "[/B][/COLOR]",url2,3,iconimage,fanarts)
			# If there are any errors pass without warning.
			except:pass
		addItem("[COLOR white][B]Clear Cache[/COLOR][/B]",url,10,icon,fanarts)
		addDir("[COLOR dodgerblue][B]Search[/B][/COLOR]",url,5,searchicon,fanarts)
		view(link)

##########################################################################################################
#					      FUNCTION TO GET THE CONTECNT IN AN XML LIST								     #
##########################################################################################################

def GetContent(name,url,iconimage,fanart):

		url2=url
		link=open_url(url)
		match= re.compile('<item>(.+?)</item>').findall(link)
		# This functions sends a loop for every <item> you have in  the list.
		for item in match:
			# Try the following, if there is an error it will pass and not show any errors.
#			try:
			
			# Check if the item is a <folder>
			if '<poster>'in item:
				data=re.compile('<title>(.+?)</title>.+?poster>(.+?)</poster>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
				for name,url,iconimage,fanart in data:
					addDir("[B][COLOR white]" + name + "[/B][/COLOR]",url,1,iconimage,fanart)
	
			# If the item is not picked up by the sportsdevil or folder function do the following.
			else:
				links=re.compile('<link>(.+?)</link>').findall(item)
				# Count the number of <links> in the item.
				# If a single link do the following.
				if len(links)==1:
					data=re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>').findall(item)
					lcount=len(match)
					for name,url,iconimage in data:
						if 'youtube.com/playlist' in url:
							addDir("[B][COLOR white]" + name + "[/B][/COLOR]",url,2,iconimage,fanarts)
						else:
							addLink("[B][COLOR white]" + name + "[/B][/COLOR]",url,2,iconimage,fanarts)
				# If a multi link do the following.
				elif len(links)>1:
					name=re.compile('<title>(.+?)</title>').findall(item)[0]
					iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
					addItem("[B][COLOR white]" + name + "[/B][/COLOR]",url2,3,iconimage,fanarts)
		# If there are any errors pass without warning.
#			except:pass
			
		view(link)

##########################################################################################################
#					            FUNCTION TO SEARCH THE PLUGIN										     #
##########################################################################################################

def SEARCH():

	try:
		SEARCH_LIST     = base64.b64decode(b'aHR0cDovL3d3dy50ZGJ3aXphcmQuY28udWsvYWRkb25zL2xlZS90ZGJ0b29ucy9zZWFyY2gvc2VhcmNoLnhtbA==')
		link=open_url(SEARCH_LIST)
		slist=re.compile('<link>(.+?)</link>').findall(link)
		for url in slist:
			SEARCH_LIST     = base64.b64decode(b'aHR0cDovL3d3dy50ZGJ3aXphcmQuY28udWsvYWRkb25zL2xlZS90ZGJ0b29ucy9zZWFyY2gvc2VhcmNoLnhtbA==')
	except:
			SEARCH_LIST     = base64.b64decode(b'aHR0cDovL3d3dy50ZGJ3aXphcmRidWlsZHMuY28udWsvYWRkb25zL2xlZS90ZGJ0b29ucy9zZWFyY2gvc2VhcmNoLnhtbA==')

	found = 0
	i = 0
	url2  = "Null"
	keyb = xbmc.Keyboard('', AddonTitle)
	keyb.doModal()
	if (keyb.isConfirmed()):
		searchterm=keyb.getText()
	else:quit()
	addItem("[COLOR white][B]You searched for - [/COLOR] [COLOR dodgerblue]" + searchterm + "[/COLOR][/B]",url2,999,icon,fanarts)			
	addItem("[B][COLOR yellow]------------------------------------------------[/COLOR][/B]",url2,999,icon,fanarts)			
	searchterm=searchterm.upper()
	link=open_url(SEARCH_LIST)
	slist=re.compile('<link>(.+?)</link>').findall(link)
	for url in slist:
		try:
			link=open_url(url)
			entries= re.compile('<item>(.+?)</item>').findall(link)
			for item in entries:
				match=re.compile('<title>(.+?)</title>').findall(item)
				for title in match:
					title=title.upper()
					if searchterm in title:
						i = i + 1
						# This functions sends a loop for every <item> you have in  the list.
						# Try the following, if there is an error it will pass and not show any errors.
						try:

							# Check if the item is a <folder>
							if '<poster>'in item:
								found = 1
								data=re.compile('<title>(.+?)</title>.+?poster>(.+?)</poster>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
								for name,url,iconimage,fanart in data:
									name2 = name
									name = "[COLOR white][B]" + name2 + "[/B][/COLOR]"
									addDir(name,url,1,iconimage,fanart)

							# If the item is not picked up by the sportsdevil or folder function do the following.
							else:
								links=re.compile('<link>(.+?)</link>').findall(item)
							# Count the number of <links> in the item.
							# If a single link do the following.
								if len(links)==1:
									found = 1
									data=re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>').findall(item)
									lcount=len(match)
									for name,url,iconimage in data:
										name2 = name
										name = "[COLOR white][B]" + name2 + "[/B][/COLOR]"
										if 'youtube.com/playlist' in url:
											addDir(name,url,2,iconimage,fanarts)
										else:
											addLink(name,url,2,iconimage,fanarts)
								# If a multi link do the following.
								elif len(links)>1:
									found = 1
									name=re.compile('<title>(.+?)</title>').findall(item)[0]
									iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
									name2 = name
									name = "[COLOR white][B]" + name2 + "[/B][/COLOR]"
									addLink(name,url2,3,iconimage,fanarts)

							# If there are any errors pass without warning.
						except:pass

		except: pass

	if found == 0:
		addItem("[COLOR dodgerblue][B]Sorry! [/COLOR][COLOR white]No Results Found![/COLOR][/B]",url,999,icon,fanarts)			
	else:
		addItem("[COLOR dodgerblue][I]Results Found - [/COLOR][COLOR dodgerblue]" + str(i) + "[/COLOR][/I]",url,999,icon,fanarts)			

##########################################################################################################
#					            FUNCTION TO PLAY SINGLE LINKS										     #
##########################################################################################################

def PLAYLINK(name,url,iconimage):

        if not'http'in url:url='http://'+url
        if 'youtube.com/playlist' in url:
                searchterm = url.split('list=')[1]
                ytapi = ytpl + searchterm + ytpl2
                req = urllib2.Request(ytapi)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                link = link.replace('\r','').replace('\n','').replace('  ','')     
                match=re.compile('"title": "(.+?)".+?"videoId": "(.+?)"',re.DOTALL).findall(link)
                try:
                        np=re.compile('"nextPageToken": "(.+?)"').findall(link)[0]
                        ytapi = ytplpg1 + np + ytplpg2 + searchterm + ytplpg3
                        addDir('Next Page >>',ytapi,2,nextpage,fanart)
                except:pass

                for name,ytid in match:
                        url = 'https://www.youtube.com/watch?v='+ytid
                        iconimage = 'https://i.ytimg.com/vi/'+ytid+'/hqdefault.jpg'
                        if not 'Private video' in name:
                                if not 'Deleted video' in name:
                                        addLink(name,url,2,iconimage,fanart)
                
        if 'https://www.googleapis.com/youtube/v3' in url:
                searchterm = re.compile('playlistId=(.+?)&maxResults').findall(url)[0]
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                link = link.replace('\r','').replace('\n','').replace('  ','')     
                match=re.compile('"title": "(.+?)".+?"videoId": "(.+?)"',re.DOTALL).findall(link)
                try:
                        np=re.compile('"nextPageToken": "(.+?)"').findall(link)[0]
                        ytapi = ytplpg1 + np + ytplpg2 + searchterm + ytplpg3
                        addDir('Next Page >>',ytapi,2,nextpage,fanart)
                except:pass


                
                for name,ytid in match:
                        url = 'https://www.youtube.com/watch?v='+ytid
                        iconimage = 'https://i.ytimg.com/vi/'+ytid+'/hqdefault.jpg'
                        if not 'Private video' in name:
                                if not 'Deleted video' in name:
                                        addLink(name,url,2,iconimage,fanart)

                
                                     
        if urlresolver.HostedMediaFile(url).valid_url(): stream_url = urlresolver.HostedMediaFile(url).resolve()
        elif liveresolver.isValid(url)==True: stream_url=liveresolver.resolve(url)
        else: stream_url=url
        liz = xbmcgui.ListItem(name,iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setPath(stream_url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)			
		
##########################################################################################################
#					            FUNCTION FOR MULTI LINKS            								     #
##########################################################################################################

def GETMULTI(name,url,iconimage):
	
	streamurl=[]
	streamname=[]
	streamicon=[]
	link=open_url(url)
	urls=re.compile('<title>'+re.escape(name)+'</title>(.+?)</item>',re.DOTALL).findall(link)[0]
	iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(urls)[0]
	links=re.compile('<link>(.+?)</link>').findall(urls)
	i=1
	for sturl in links:
                sturl2=sturl
                if '(' in sturl:
                        sturl=sturl.split('(')[0]
                        caption=str(sturl2.split('(')[1].replace(')',''))
                        streamurl.append(sturl)
                        streamname.append(caption)
                else:
                        streamurl.append( sturl )
                        streamname.append( 'Link '+str(i) )
                i=i+1
	name='[COLOR red]'+name+'[/COLOR]'
	dialog = xbmcgui.Dialog()
	select = dialog.select(name,streamname)
	if select < 0:
		quit()
	else:
		url = streamurl[select]
		print url
		if urlresolver.HostedMediaFile(url).valid_url(): stream_url = urlresolver.HostedMediaFile(url).resolve()
                elif liveresolver.isValid(url)==True: stream_url=liveresolver.resolve(url)
                else: stream_url=url
                liz = xbmcgui.ListItem(name,iconImage='DefaultVideo.png', thumbnailImage=iconimage)
                liz.setPath(stream_url)
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

##########################################################################################################
#				GENERAL FUNCTIONS NEEDED FOR THE ADDON TO FUNCTION      							     #
##########################################################################################################

def open_url(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', USER_AGENT)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		link=link.replace('\n','').replace('\r','').replace('<title></title>','<title>x</title>').replace('<link></link>','<link>x</link>').replace('<fanart></fanart>','<fanart>x</fanart>').replace('<thumbnail></thumbnail>','<thumbnail>x</thumbnail>').replace('<utube>','<link>https://www.youtube.com/watch?v=').replace('</utube>','</link>')#.replace('></','>x</')
		return link
	except: pass

def open_url2(url):
		req = urllib2.Request(url)
		req.add_header('User-Agent', USER_AGENT)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link
 
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
	
def addDir(name,url,mode,iconimage,fanart,description=''):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)+"&fanart="+urllib.quote_plus(fanart)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
    liz.setProperty('fanart_image', fanart)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name, url, mode, iconimage, fanart, description=''):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)+"&fanart="+urllib.quote_plus(fanart)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setProperty('fanart_image', fanart)
    liz.setProperty("IsPlayable","true")
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

def addItem(name,url,mode,iconimage,fanart, description=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty( "Fanart_Image", fanart )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

#######################################################################
#						Maintenance Functions
#######################################################################

class cacheEntry:
    def __init__(self, namei, pathi):
        self.name = namei
        self.path = pathi	

def setupCacheEntries():
    entries = 5 #make sure this refelcts the amount of entries you have
    dialogName = ["WTF", "4oD", "BBC iPlayer", "Simple Downloader", "ITV"]
    pathName = ["special://profile/addon_data/plugin.video.whatthefurk/cache", "special://profile/addon_data/plugin.video.4od/cache",
					"special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache","special://profile/addon_data/script.module.simple.downloader",
                    "special://profile/addon_data/plugin.video.itv/Images"]
                    
    cacheEntries = []
    
    for x in range(entries):
        cacheEntries.append(cacheEntry(dialogName[x],pathName[x]))
    
    return cacheEntries

#######################################################################
#						Clear Cache
#######################################################################

def clearCache():
   
    thumbnailPath = xbmc.translatePath('special://userdata/Thumbnails');
    cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
    tempPath = xbmc.translatePath('special://temp')

    if os.path.exists(cachePath)==True:    
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Kodi Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        try:
							if (f.endswith(".log")): continue
							os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if os.path.exists(tempPath)==True:    
        for root, dirs, files in os.walk(tempPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Kodi Temp Files", str(file_count) + " files found", "Do you want to delete them?"):
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'Other'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'LocalAndRental'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass    
                
    cacheEntries = setupCacheEntries()
                                         
    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:

                    dialog = xbmcgui.Dialog()
                    if dialog.yesno(AddonTitle,str(file_count) + "%s cache files found"%(entry.name), "Do you want to delete them?"):
                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))
                            
                else:
                    pass
                

    dialog = xbmcgui.Dialog()
    dialog.ok(AddonTitle, "Done Clearing Cache files")

def find_single_match(text,pattern):

    result = ""
    try:    
        single = re.findall(pattern,text, flags=re.DOTALL)
        result = single[0]
    except:
        result = ""

    return result

def TextBoxesPlain(announce):
	class TextBox():
		WINDOW=10147
		CONTROL_LABEL=1
		CONTROL_TEXTBOX=5
		def __init__(self,*args,**kwargs):
			xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
			self.win=xbmcgui.Window(self.WINDOW) # get window
			xbmc.sleep(500) # give window time to initialize
			self.setControls()
		def setControls(self):
			self.win.getControl(self.CONTROL_LABEL).setLabel('[COLOR smokewhite][B]TDB Wizard[/B][/COLOR]') # set heading
			f=open(announce); text=f.read()
			self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
			return
	TextBox()
	while xbmc.getCondVisibility('Window.IsVisible(10147)'):
		time.sleep(.5)

def view(link):
        try:
                match= re.compile('<layouttype>(.+?)</layouttype>').findall(link)[0]
                if layout=='thumbnail': xbmc.executebuiltin('Container.SetViewMode(500)')              
                else:xbmc.executebuiltin('Container.SetViewMode(50)')  
        except:pass

params=get_params(); url=None; name=None; mode=None; site=None; iconimage=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: fanart=urllib.unquote_plus(params["fanart"])
except: pass
 
if mode==None or url==None or len(url)<1: GetMenu()
elif mode==1:GetContent(name,url,iconimage,fanart)
elif mode==2:PLAYLINK(name,url,iconimage)
elif mode==3:GETMULTI(name,url,iconimage)
elif mode==5:SEARCH()
elif mode==7:PLAYVIDEO(url)
elif mode==10:clearCache()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
