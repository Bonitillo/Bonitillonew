'''
    Ice Channel    
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common

class yify(MovieSource):
    implements = [MovieSource]
    
    name = "Niter.tv"
    display_name = "Niter Tv"
    base_url = 'http://niter.co/'
    source_enabled_by_default = 'true'

    icon = common.notify_icon
    
    
    def GetFileHosts(self, url, list, lock, message_queue): 
        
        import re
        
        from entertainment.net import Net

        net = Net(cached=False)
        content = net.http_GET(url,{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}).content



        match=re.compile('(pic|emb|emb2|dir|tsf)=(.+?)&').findall (content.replace('</div>','&'))
        for one, pic in match:
            if '//' in pic:
                HOST=pic.split('//')[1]
                HOST=HOST.split('/')[0]
     
                self.AddFileHost(list, 'HD', pic,host=HOST.upper())

                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from entertainment.net import Net
        import re
        net = Net(cached=False)        
        
        name = self.CleanTextForSearch(name) 

            
        search_term = self.base_url+'search?q='+name.lower().replace(' ','+')

        html=   net.http_GET(search_term,{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}).content
        
        match=re.compile('<figcaption title="(.+?)">.+?href="(.+?)">',re.DOTALL).findall(html)

        for NAME , URL  in match:
            
            if name.lower() == NAME.lower():

                self.GetFileHosts(URL, list, lock, message_queue)
        
        


