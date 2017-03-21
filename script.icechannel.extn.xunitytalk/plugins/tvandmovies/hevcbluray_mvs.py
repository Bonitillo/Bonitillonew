'''
    Cartoon HD Extra   
    Copyright (C) 2013 Mikey1234
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin



class hevec(MovieSource):
    implements = [MovieSource]
    
    name = "HevcBluray"
    display_name = "HevcBluray"

    source_enabled_by_default = 'true'
    BASE ='http://www.300mbmoviesdl.com'



        
    def GetFileHosts(self, url, list, lock, message_queue):

    
        import re
        from entertainment.net import Net
        net = Net(cached=False)


        headers={'Host':'www.300mbmoviesdl.com',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
                   


        LINK = net.http_GET(url,headers=headers).content
 
        RES=re.compile('Quality:(.+?)<').findall(LINK)[0]
        link=LINK.split('<h3 style="text-align: center;">')
                
        uniques=[]
        for p in link:
           
            try:
                URL=re.compile('<a href="(.+?)"').findall(p)[0]
                

            

                if 'HDCAM' in RES.upper():
                    res='CAM'
                    
                elif 'CAM' in RES.upper():
                    res='CAM'
                elif 'HD' in RES.upper():
                    res='HD'
                elif 'DVD' in RES.upper():
                    res='DVD'
                elif '720' in RES:
                    res='720P'                   
                elif '1080' in RES:
                    res='1080P'
                else:
                    res='720P'
                
                FINAL_URL=URL.split('//')[1]
                FINAL_URL=FINAL_URL.split('/')[0]
                if not '300mbmoviesdl' in URL:
                    if not 'amazon' in URL:
                        self.AddFileHost(list, res, URL,host=FINAL_URL.upper())

            except:pass   
                    
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
    
        import re
        from entertainment.net import Net
        net = Net(cached=False)


        name=self.CleanTextForSearch(name.lower())
        

        headers={'Host':'www.300mbmoviesdl.com',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
                   

        new_url='http://www.300mbmoviesdl.com/?s='+name.replace(' ','+')
        
        LINK = net.http_GET(new_url,headers=headers).content
        link=LINK.split('<div class="cover">')
   
        for p in link:
            try:
                item_url=re.compile(' href="(.+?)"').findall(p)[0]
                if not 'http' in item_url:
                    item_url='http://'+item_url
                TITLE=re.compile(' title="(.+?)"').findall(p)[0]
                xbmc.log(TITLE)
                xbmc.log(item_url)
                if name.lower() in self.CleanTextForSearch(TITLE.lower()):
                    if year in TITLE.lower():
                        
                        self.GetFileHosts(item_url, list, lock, message_queue)

            except:pass              




                
    




            
