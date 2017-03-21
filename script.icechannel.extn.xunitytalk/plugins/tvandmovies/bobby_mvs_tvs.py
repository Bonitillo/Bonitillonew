'''
    Cartoon HD Extra   
    Copyright (C) 2013 Mikey1234
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin



class bobby(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "BobbyMovies"
    display_name = "Bobby Movies"

    source_enabled_by_default = 'true'
    BASE ='https://bobby.kohimovie.com/jp/2.1.0/'



        
    def GetFileHosts(self, url, list, lock, message_queue,type,episode):

    
        import re
        from entertainment.net import Net
        net = Net(cached=False)



        headers={'Host':'webapp.bobbyhd.com',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69',
                'Accept-Language':'en-gb',
                'Accept-Encoding':'gzip, deflate',
                'Connection':'keep-alive'}
        new_url='http://webapp.bobbyhd.com/player.php?alias='+url
        
        link = net.http_GET(new_url,headers=headers).content
        if type=='tv_episodes':
            match=re.compile('changevideo\(\'(.+?)\'\)".+?data-toggle="tab">(.+?)\..+?</a>').findall(link)
            print match
        else:
            match=re.compile('changevideo\(\'(.+?)\'\)".+?data-toggle="tab">(.+?)</a>').findall(link)

        for URL , RES in match:
            if 'webapp' in URL:
                URL=URL.split('embed=')[1]
            
            
            if '720' in RES:
                res='720P'
            elif 'CAM' in RES:
                res='CAM'                    
            elif '1080' in RES:
                res='1080P'
            elif 'HD' in RES:
                res='HD'
            else:
                res='720P'
            
            FINAL_URL=URL.split('//')[1]
            FINAL_URL=FINAL_URL.split('/')[0]
            
            if type=='tv_episodes':
              
                EPISODE=int(RES)

                if int(episode)==EPISODE:
                               
                    self.AddFileHost(list, res, URL,host=FINAL_URL.upper())                    
            else:    
                    self.AddFileHost(list, res, URL,host=FINAL_URL.upper())

        
                    
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
    
        import re
        from entertainment.net import Net
        net = Net(cached=False)


        name=self.CleanTextForSearch(name.lower())
        
        headers={'Host':'webapp.bobbyhd.com',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69',
                'Accept-Language':'en-gb',
                'Accept-Encoding':'gzip, deflate',
                'Connection':'keep-alive'}

        new_url='http://webapp.bobbyhd.com/search.php?keyword='+name.replace(' ','+')
        
        link = net.http_GET(new_url,headers=headers).content
     
        match=re.compile('alias=(.+?)\'">(.+?)</a>').findall(link)
        
        for id,TITLE in match:
         
            if type=='tv_episodes':
                if name.lower() in self.CleanTextForSearch(TITLE.lower()):
                      if season in TITLE:
                        
                        self.GetFileHosts(id, list, lock, message_queue,type,episode)
            else:
                if name.lower()==self.CleanTextForSearch(TITLE.lower()):                    
                    self.GetFileHosts(id, list, lock, message_queue,type,episode)


                

    def Resolve(self, url):                 
        url=url.replace('amp;','')
        if 'requiressl=yes' in url:
            url = url.replace('http://', 'https://')
        from entertainment import istream
        resolved =istream.ResolveUrl(url)
        return resolved  



                
    




            
