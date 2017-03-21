'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common


class plex(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "Plex"
    display_name = "Plex"
    source_enabled_by_default = 'true'

        
    servers   =['http://23.94.101.170:32400',
				'http://98.191.86.177:32400',
				'http://64.130.117.2:32400',
				'http://173.164.3.18:32400']
    


    def OPEN_URL(self,url):
        import urllib2
        response = urllib2.urlopen(url, timeout = 3)
        link=response.read()
        response.close()
        return link    
    
    def GetFileHosts(self, url, list, lock, message_queue,res):

            
        self.AddFileHost(list, res, url,host='PLEX')

        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        #import re
        #from entertainment.net import Net
        
        #net = Net(cached=False)
        
        import re,urllib
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)
        name=name.lower()
        
        for s in self.servers:
            if type == 'tv_episodes':
                try:
                    url=s+'/search?local=1&query='+name.replace(' ','%20')
                    link=self.OPEN_URL(url)
                    title=re.compile('title="(.+?)"').findall(link)[0]
                    title=title.lower()
                    title=title.replace('the ','')
                    name=name.replace('the ','')                  
                    if name.lower() == self.CleanTextForSearch(title.lower()):
                        child=re.compile('key="(.+?)"').findall(link)[0]
                        LINK=self.OPEN_URL(s+child)
                        SEASONS=re.compile('ratingKey=".+?" key="(.+?)".+?title="(.+?)"').findall(LINK)
                        for CHILDREN ,SEASON in SEASONS:

                            if season in SEASON:

                                content=self.OPEN_URL(s+CHILDREN)
                                MATCHED=re.compile('ratingKey=".+?" key="(.+?)".+?index="(.+?)".+?videoResolution="(.+?)"',re.DOTALL).findall(content)
                    
                                for KEY , ep, res in MATCHED:
        
                                    if ep == episode:
      
                                        path=s+'/video/:/transcode/universal/start?path='+urllib.quote(s)+urllib.quote(KEY)

                                       
                                        if res.isdigit():
                                            res= res+'P'
                                        else:
                                            res=res.upper()
                                            
                                        self.GetFileHosts(path, list, lock, message_queue,res)
                                        break
                except:pass
            else:    
                try:
                    url=s+'/search?local=1&query='+name.replace(' ','%20')
                    link=self.OPEN_URL(url)
                    title=re.compile('title="(.+?)"').findall(link)[0]
                    YEAR=re.compile('year="(.+?)"').findall(link)[0]
                    title=title.lower()
                    title=title.replace('the ','')
                    name=name.replace('the ','')
                    if name.lower() == title.lower():
                        if year in YEAR:
                            key=re.compile('key="(.+?)"').findall(link)[0]
                            path=s+'/video/:/transcode/universal/start?path='+urllib.quote(s)+urllib.quote(key)
                            res=re.compile('videoResolution="(.+?)"').findall(link)[0].upper()
                            if res.isdigit():
                                res =res+'P'
                                
                            self.GetFileHosts(path, list, lock, message_queue,res)
                            break
                except:pass

            


    def Resolve(self, url):
        import random,string
        random1 = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])   
        random = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])
        MOVIE_URL=url+'&mediaIndex=0&partIndex=0&protocol=http&offset=0&fastSeek=1&directPlay=0&directStream=1&subtitleSize=100&audioBoost=100&maxVideoBitrate=4000&videoQuality=100&session='+random+'&subtitles=burn&copyts=1&Accept-Language=en&X-Plex-Chunked=1&X-Plex-Product=Plex+Web&X-Plex-Version=2.4.23&X-Plex-Client-Identifier='+random1+'&X-Plex-Platform=Chrome&X-Plex-Platform-Version=47.0&X-Plex-Device=Windows&X-Plex-Device-Name=Plex+Web+(Chrome)'        
        return MOVIE_URL
 
        
