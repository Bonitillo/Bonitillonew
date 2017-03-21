'''
    9movies
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
import os

class streamlord(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "Streamlord"
    display_name = "Streamlord"
    base_url = 'http://streamlord.com/'
    
    source_enabled_by_default = 'true'
    profile_path = common.profile_path
    cookie_file = os.path.join(profile_path, 'cookies', '%s.cookies') % name
    
    def GetFileHosts(self, url, list, lock, message_queue, season, episode,type,year):

        self.AddFileHost(list, '720P', url,host='STREAMLORD')

            
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):  
    
        from entertainment.net import Net

        from entertainment import bing

        
        net = Net(cached=False,user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')        

        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)
        #print ':::::::::::::::::::::::::::::::::'
         
        if type == 'tv_episodes':
            if len(episode)<2:
              episode = "0%s"%episode
            if len(season)<2:
              season = "0%s"%season              
            search_term ='%s s%se%s' %(name,season,episode)
            RESULT_TERM ='%s s%se%s' %(name,season,episode)
            try:GOOGLED = self.GoogleSearch('streamlord.com', search_term)
            except:GOOGLED = bing.Search('streamlord.com', search_term)
            RETURN = 'watch %s' % RESULT_TERM.lower()
                      
           
        else:
            search_term = name + ' '+year
            RESULT_TERM = name.lower()           
            try:GOOGLED = self.GoogleSearch('streamlord.com', search_term)
            except:GOOGLED = bing.Search('streamlord.com', search_term)
                
            RETURN = 'watch %s' % RESULT_TERM.lower()
                      
            
        uniques =[]
        for result in GOOGLED:          
            movie_url= result['url']
            TITLE = result['title']
       
            if '?' in movie_url:
                movie_url=movie_url.split('?')[0]

                 
            #if not '/watching.html' in movie_url:
                #movie_url = movie_url + '/watching.html'
                #movie_url =movie_url.replace('//watching.html','/watching.html')

                


            if RETURN.lower() in TITLE.lower():
                if movie_url not in uniques:

                    uniques.append(movie_url)

                    self.GetFileHosts(movie_url, list, lock, message_queue,season, episode,type,year)
                    break

    def __get_array(self, array, html):
        import re
        pattern = 'var\s+%s\s*=\s*\[([^\]]+)' % (array)
        match = re.search(pattern, html)
        if match:
            return self.__do_join(match.group(1))
    
    def __get_fragment(self, span, html):
        import re
        r='id=%s>(.+?)<' % span
        match=re.compile(r).findall(html)[0]
        return match


    def __do_join(self, array):
        import re
        array = re.sub('[" ]', '', array)
        array = array.replace('\/', '/')
        return ''.join(array.split(','))

    def __decode(self, result):
        import re
        match = re.compile('return\(\[(.+?)\].+?\+ (.+?)\.join.+?document\.getElementById\("(.+?)"\)', re.DOTALL).findall(result)
        url = match[0][0]
        array = match[0][1]
        span = match[0][2]     
        url = self.__do_join(url)
        array = self.__get_array(array, result)
        span = self.__get_fragment(span, result)
        if url and array and span:
            return url + array + span


            
    def Resolve(self, url):
        
            from entertainment.net import Net
            from entertainment import cloudflare 
            import re
            #print url

            UA='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
            net = Net(cached=False,user_agent=UA)
     
            try:
                net.set_cookies(self.cookie_file)                
                result = net.http_GET(url).content
                net.save_cookies(self.cookie_file)                 
            except:result = cloudflare.solve(url,self.cookie_file,UA)
            #print result.encode('ascii','ignore')
            stream=re.compile('return\("(.+?)"').findall(result)[0]
            final=stream.split('://')[1]
            host=final.split('/')[0]
            
            #cf_clearance=re.compile('cf_clearance=(.+?);').findall(open(self.cookie_file).read())[0]
            #cfduid=re.compile('cfduid=(.+?);').findall(open(self.cookie_file).read())[0]
            
            #AND='|Host=%s&User-Agent=%s&Referrer=%s&Connection=keep-alive&Cookie=cfduid=%s;' %(host,UA,url,cfduid)           

            return stream#+AND
            
                
                
