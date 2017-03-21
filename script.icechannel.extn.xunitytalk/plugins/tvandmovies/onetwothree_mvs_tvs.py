'''
    Ice Channel
    buzzfilms.co
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
import os



class onetwothree(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "123Movies"
    display_name = "123Movies"
    #base_url = 'https://123movies.is'

    UA ='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    
    profile_path = common.profile_path
    cookie_file = os.path.join(profile_path, 'cookies', '123moviesNEW.cookies')

    source_enabled_by_default = 'true'
    

    def random_generator(self,size=16):
            import random,string
            chars=string.ascii_lowercase + string.digits
            return ''.join(random.choice(chars) for x in range(size))


    def GetFileHosts(self, url, list, lock, message_queue, season, episode,type,year,query,base_url):

        key = '87wwxtp3dqii'
        key2 = '7bcq9826avrbi6m49vd7shxkn985mhod'
        key3 = '7bcq9826avrbi6m4'

        REF=url

        from entertainment.net import Net

        import re,json,hashlib,urllib
        
        net = Net(cached=False)
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36','Referer':base_url + ''}
        
      
        LINK = net.http_GET(url,headers=headers).content
        #net.save_cookies(self.cookie_file)

        
        try:movie_id = re.compile('name="movie_id" value="(.+?)"').findall(LINK)[0]
        except:movie_id = re.compile('id: "(.+?)"').findall(LINK)[0]
        
        coookie_1 = hashlib.md5(movie_id+key).hexdigest()

        
        sneaky = re.compile('src="(.+?)" class="hidden"').findall(LINK)[0]

        headers = {'Accept': 'image/webp,image/*,*/*;q=0.8', 'Accept-Encoding':'gzip, deflate, sdch, br',
                   'Accept-Language': 'en-US,en;q=0.8', 'Referer': REF, 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        FIRSTCOOKIE = self.FirstCookie(sneaky,REF)

        
        #net.set_cookies(self.cookie_file)
        LOAD =net.http_GET(base_url + 'ajax/v2_get_episodes/%s'%(movie_id),headers=headers).content
        LOAD=LOAD.replace('Episode 0','Episode ')
        link=LOAD.split('<div id="server-')
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36','Referer':base_url + ''}
      
        for p in link:

            #try:
                
                res ='720P'
               
                    

                if type == 'tv_episodes':
                        
                        HTML=p.split('<a title="')
                        
                        for d in HTML:
                            try:
                           
                                if ' '+episode+':' in d.lower():
                                    
                                    #token = re.compile('hash="(.+?)"').findall(d)[0]
                                    SERVER=d.split('loadEpisode(')[1]
                                    server=SERVER.split(',')[0]
                                    episodeid=re.compile(',(.+?)\)').findall(SERVER)[0]
                                    key_gen = self.random_generator()
                                    COOKIE =  FIRSTCOOKIE +'; ' +hashlib.md5(episodeid + key).hexdigest() + '=%s' %key_gen
                                    a= episodeid + key2
                                    b= key_gen
                                    token = urllib.quote(self.__uncensored(a, b)).encode('utf8')

                                    HEADERS={'Accept-Encoding':'gzip, deflate, sdch','x-requested-with':'XMLHttpRequest','Cookie':COOKIE,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36','Referer':REF}
               
                                    if int(server) > 11:
                                        try:
                                            URL=base_url + '/ajax/load_embed/%s' % (episodeid)
                                            HTML1=net.http_GET(URL,headers=HEADERS).content
                                            HTML2 = json.loads(HTML1)
                                            FINAL_URL = HTML2['embed_url']
                                            if '720p' in FINAL_URL.lower():
                                                res='720P'
                                            if '1080p' in FINAL_URL.lower():
                                                res='1080P'
                                            else:
                                                res='720P'                                                

                                            self.AddFileHost(list, res, FINAL_URL)
                                        except:pass
                                    else:
                                        URL=base_url + 'ajax/v2_get_sources/%s?hash=%s' % (episodeid,token)
                                        try:
                                            HTML1=net.http_GET(URL,headers=HEADERS).content
                                            HTML2 = json.loads(HTML1)
                                            DATA=HTML2['playlist'][0]['sources']
                                            for field in DATA:
                                                FINAL_URL= field['file']
                                                res= field['label']#.upper()
                                            
                           
                                                if not '.srt' in FINAL_URL:
                                                    res=res.replace('p','').replace('P','').replace('CAM','360')
                                                    if not res.isdigit():
                                                        res='720'

                                                    if res =='360':
                                                        res='SD'
                                                    if res =='480':
                                                        res='DVD'
                                                    if res =='720':
                                                        res='720P'
                                                    if res =='1080':
                                                        res='1080P'
                                                      

                                                    HOST=FINAL_URL.split('//')[1]
                                                    HOST=HOST.split('/')[0]  
                                                    

                                                    

                                                    self.AddFileHost(list, res, FINAL_URL,host=HOST.upper())                            
                                        except:pass

                            except:pass                                    
                else:
                        HTML=p.split('<a title="')
                        
                        for d in HTML:
                            try:

                                YEAR=re.compile('Release:</strong>(.+?)<').findall(LINK)[0].strip()
                                THETITLE=re.compile('"og:title" content="(.+?)"').findall(LINK)[0].strip()
                                if not year:
                                    if query.lower() in THETITLE.lower():
                                        PASS=True
                                else:        
                                    if year == YEAR:
                                        PASS=True
                                if PASS==True:
                                    
                                    SERVER=d.split('loadEpisode(')[1]
                                    server=SERVER.split(',')[0]
                                    episodeid=re.compile(',(.+?)\)').findall(SERVER)[0]
                                    key_gen = self.random_generator()
                                    COOKIE =  FIRSTCOOKIE +'; ' +hashlib.md5(episodeid + key).hexdigest() + '=%s' %key_gen
                           
                                    a= episodeid + key2
                                    b= key_gen
                                    token = urllib.quote(self.__uncensored(a, b)).encode('utf8')

                                    
                                    HEADERS={'Accept-Encoding':'gzip, deflate, sdch',
                                             'x-requested-with':'XMLHttpRequest',
                                             'Cookie':COOKIE,
                                             'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                                             'Referer':REF}
                             
                                    
                                    if int(server) > 11:
                                        
                                        URL=base_url + 'ajax/load_embed/%s' % (episodeid)

                                        EMBEDHTML=net.http_GET(URL,headers=HEADERS).content
                                        THEEMBED=json.loads(EMBEDHTML)
                                        FINAL_URL = THEEMBED['embed_url']
                                       
                                        if '720p' in FINAL_URL.lower():
                                            res='720P'
                                        elif '1080p' in FINAL_URL.lower():
                                            res='1080P'
                                        else:
                                            res='HD'                                                

                                        self.AddFileHost(list, res, FINAL_URL)
                                    else:
                                        URL=base_url + 'ajax/v2_get_sources/%s?hash=%s' % (episodeid,token)
                                        


                                        

                                        
                                        #net.set_cookies(self.cookie_file)
                                        HTML=net.http_GET(URL,headers=HEADERS).content
                                        try:  

                                             
                                            HTML2 = json.loads(HTML)
                                            DATA=HTML2['playlist'][0]['sources']
                                            for field in DATA:
                                                FINAL_URL= field['file']
                                                res= field['label']#.upper()
                                            
                                            #if 'google' in FINAL_URL or 'blogspot' in FINAL_URL or '123movies.ru' in FINAL_URL:                             
                                                if not '.srt' in FINAL_URL:
                                                    res=res.replace('p','').replace('P','').replace('CAM','360')
                                                    if not res.isdigit():
                                                        res='720'
                                                    #print res
                                                    #res=int(res)
                                                    #print res
                                                    if res =='360':
                                                        res='SD'
                                                    if res =='480':
                                                        res='DVD'
                                                    if res =='720':
                                                        res='720P'
                                                    if res =='1080':
                                                        res='1080P'
                                                      

                                                    HOST=FINAL_URL.split('//')[1]
                                                    HOST=HOST.split('/')[0]  
                                                    

                                                    

                                                    self.AddFileHost(list, res, FINAL_URL,host=HOST.upper()) 
                                        except:pass 
                            except:pass

    def FirstCookie(self,sneaky,referer):
        
            import urllib2
            
            req = urllib2.Request(sneaky)
            req.add_header('User-Agent' , 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
            req.add_header('Accept-Encoding' , "gzip, deflate, sdch, b")
            req.add_header('Accept-Language' , "Accept-Language")
            req.add_header('Referer' , referer)
            response = urllib2.urlopen(req)
            headers=response.info()
            response.close()
            THEHEADERS=str(headers['Set-Cookie'])
            if 'HttpOnly,' in THEHEADERS:
                THEHEADERS=THEHEADERS.split('HttpOnly,')[1].strip()
            return THEHEADERS



    def __jav(self, a):
            b = str(a)
            code = ord(b[0])
            if 0xD800 <= code and code <= 0xDBFF:
                c = code
                if len(b) == 1:
                    return code
                d = ord(b[1])
                return ((c - 0xD800) * 0x400) + (d - 0xDC00) + 0x10000

            if 0xDC00 <= code and code <= 0xDFFF:
                return code
            return code

    def __uncensored(self,a, b):
            import base64
            c = ''
            i = 0
            for i, d in enumerate(a):
                e = b[i % len(b) - 1]
                d = int(self.__jav(d) +self. __jav(e))
                c += chr(d)

            return base64.b64encode(c)
        
             

    def GetDomain(self):                 
        
        from entertainment.net import Net
        net = Net(cached=False)

        headers={'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4',}
        url = ['https://123movie.tech/',
               'https://123movies.center/',
               'https://123movies.group/',
               'https://123moviesbackup.ru/',
               'https://123movies.is/',
               'https://123movies.ru/',
               'https://123movies.gs/',
               'https://123movies.vc/',
               'https://123movies.cz/',
               'https://123movies.ag/',
               'https://123movies-proxy.ru/',
               'https://123movies.net.ru/',
               'https://123movie.space/',
               'http://123-movie.ru/',
               'https://123movies.moscow',
               'https://123movies.cloud']
        
        for URL in url:
            HOST=URL.split('//')[1]

            try:
               hello = net.http_GET(URL,headers=headers).content
               if HOST in hello:
                   return URL
            except:pass 

            
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):  
    
        from entertainment.net import Net

        import re

        base_url = self.GetDomain()
        net = Net(cached=False)        
        title = self.CleanTextForSearch(title) 
        query = self.CleanTextForSearch(name)
        #print ':::::::::::::::::::::::::::::::::'
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36','Referer':base_url}
                
        url=base_url + 'movie/search/' + str(query).replace(' ','+')

        #net.set_cookies(self.cookie_file)
        LINK=net.http_GET(url,headers=headers).content

                              
        LINK = LINK.split('"ml-item">')
        for p in LINK:
            try:
               movie_url=re.compile('a href="(.+?)"',re.DOTALL).findall(p)[0]
               name=re.compile('title="(.+?)"',re.DOTALL).findall(p)[0]
               iconimage=re.compile('img data-original="(.+?)"',re.DOTALL).findall(p)[0]           

               movie_url=movie_url+'watching.html'
               if type == 'tv_episodes':
                   if query.lower() in self.CleanTextForSearch(name.lower()):                
                       if 'Season '+season in name:
                           self.GetFileHosts(movie_url, list, lock, message_queue,season, episode,type,year,query,base_url)
                        
               else:
                   if query.lower() in self.CleanTextForSearch(name.lower()):
                       self.GetFileHosts(movie_url, list, lock, message_queue,season, episode,type,year,query,base_url)

            except:pass

                    
            
    def Resolve(self, url):
       url=url.replace('amp;','')
       if 'streaming.fshare' in url or 'redirector.googlevideo' in url or 'googleusercontent' in url:
          import urllib2 
          headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
          req = urllib2.Request(url, headers=headers) 
          url = urllib2.urlopen( req )  .geturl()    
          return url
       else:  
            from entertainment import istream
            return istream.ResolveUrl(url)
            
                
                
