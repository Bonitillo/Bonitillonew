'''
    Istream
    myvideolinks
    Copyright (C) 2013 Mikey1234

    version 0.2

'''


from entertainment.plugnplay import Plugin
from entertainment import common

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import MovieSource

class myvideolinks(MovieSource, TVShowSource):
    implements = [MovieSource, TVShowSource]
	
    name = "myvideolinks"
    source_enabled_by_default = 'false'
    display_name = "Myvideolinks"
    base_url = 'http://newmyvideolink.xyz/'
    
    def GetFileHosts(self, url, list, lock, message_queue):
        import re

        from entertainment.net import Net
        net = Net(cached=False,user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko')

        content = net.http_GET(url).content
        
        RES=match  = re.compile('<h1>(.+?)<').findall(content)[0]
        
        #r = '<li><a href="(http://.+?)">(.+?)</a></li>'
        match  = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(content)
        
        for url, host in match:
            
            if 'HDCAM' in RES.upper():
                res='CAM'
                
            if 'CAM' in RES.upper():
                res='CAM'
            elif 'DVD' in RES.upper():
                res='DVD'
            elif '720' in RES:
                res='720P'                   
            elif '1080' in RES:
                res='1080P'
            elif 'HD' in RES.upper():
                res='HD'
            else:
                res='720P'
            self.AddFileHost(list, res, url)
                
                

    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        import urllib2
        import re
        from entertainment.net import Net
        net = Net(cached=False,user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko')

        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)

        season_pull = "0%s"%season if len(season)<2 else season
        episode_pull = "0%s"%episode if len(episode)<2 else episode
        
        tv_url='http://newmyvideolink.xyz/index2/?s=%s+S%sE%s' %(name.replace(' ','+'),season_pull,episode_pull)
        movie_url='http://newmyvideolink.xyz/index2/?s=%s+%s' %(name.replace(' ','+'),year)

        if type == 'movies':
            html = net.http_GET(movie_url).content
            for item in re.finditer(r'<a href="(.+?)" rel="bookmark"',html,re.I):
                url = item.group(1)                
                self.GetFileHosts(url, list, lock, message_queue)

        elif type == 'tv_episodes':
            html = net.http_GET(tv_url).content
            
            for item in re.finditer(r'<a href="(.+?)" rel="bookmark"',html,re.I):              
                url = item.group(1)                
                self.GetFileHosts(url, list, lock, message_queue)

    '''
    def Resolve(self, url):
        import re
        from entertainment.net import Net
        net = Net(cached=False)
        #print "test#############################################################"
        content = net.http_GET(url).content
                       
        if 'http://adf.ly/' in url:
            
            try:
                import time
                content = net.http_GET(url).content
                time.sleep(9)
                encoded_url = re.compile("var ysmm = '(.+?)';").findall(content)[0]
                encoded_url_length = len(encoded_url)
                encdd_url_part_1 = ''
                encdd_url_part_2 = ''
                for x in range(0, encoded_url_length):
                    enc_char = encoded_url[x]
                    if not re.match("[a-zA-Z0-9\+/=]", enc_char):
                        break;
                    if x % 2 == 0:
                        encdd_url_part_1 = encdd_url_part_1 + enc_char
                    else:
                        encdd_url_part_2 = enc_char + encdd_url_part_2
                encoded_url = encdd_url_part_1 + encdd_url_part_2
                import base64
                url = (base64.b64decode(encoded_url))[2:]
            
            except:
                continue
        self.GetFileHosts(url)
    '''

        

                
                
