'''
    hdmovieswatch_mvs.py
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common


class hdmovieswatch(MovieSource):
    implements = [MovieSource]
    
    name = "hdmovieswatch"
    display_name = "hdmovieswatch"

    base_url='http://www.hdmovieswatch.net/'
    
    source_enabled_by_default = 'true'
    
    
    def GetFileHosts(self, url, list, lock, message_queue,ref,res):
        import re,json
        from entertainment.net import Net

        
        net = Net(cached=False)
        

        THE_URL=url


        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.3'}
       
        content = net.http_GET(THE_URL,headers=headers).content
      
        URL=re.compile('<iframe src="(.+?)"').findall(content)[0]
        self.AddFileHost(list, res, URL)            
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        import re
        from entertainment.net import Net

        
        net = Net(cached=False)
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)

        search='http://www.hdmovieswatch.net/?s=' + name.replace(' ','+')

        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.3','Referer':'http://www.hdmovieswatch.net/'}
     
        html = net.http_GET(search,headers=headers).content

        html=html.split('Results:',1)[1]

        r ='href="(.+?)">.+?alt="(.+?)".+?class="calidad2">(.+?)<' 
        match=re.compile(r,re.DOTALL).findall(html)
      

        for URL ,TITLE ,res in match:
            ref=URL
            NAME = name.lower()
            if NAME in self.CleanTextForSearch(TITLE.lower()):

                if year in TITLE:
 
                    self.GetFileHosts(URL, list, lock, message_queue,ref,res.upper())

                        

    #def Resolve(self, url):

        
       
            
        #return url

