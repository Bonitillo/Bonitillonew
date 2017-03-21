'''
    9movies
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment.xgoogle.search import GoogleSearch

class onetwothree(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "9MoviesTv"
    display_name = "9MoviesTv"
    base_url = 'http://9movies.tv/'
    
    source_enabled_by_default = 'true'

    
    def GetFileHosts(self, url, list, lock, message_queue, season, episode,type,year):

        from entertainment.net import Net
        import re
        net = Net(cached=False,user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko')

        REF=url

        #print REF

        LINK=net.http_GET(url).content
        try:
            res=re.compile('class="quality">(.+?)<').findall(LINK)[0].strip().lower()     
        except:
            res='HD'
        
        hosts = re.search('<ul id="ip_server">(.+?)</ul>', LINK, re.DOTALL)

        if hosts:
            hosts = re.compile('<li>(.+?)</li>',re.DOTALL).findall(hosts.group(1))
            for host in hosts:
                
                if type == 'tv_episodes':
                    data_name = episode
                else:
                    data_name = re.search('data-name="([^"]+?)"', host)
                    if data_name:
                        data_name = data_name.group(1)
                
                data_film = re.search('data-film="([^"]+?)"', host)
                if data_film:
                    data_film = data_film.group(1)
                    
                data_server = re.search('data-server="([^"]+?)"', host)
                if data_server:
                    data_server = data_server.group(1)
                    
                data_source = re.search('>(.+?)<', host)
                if data_source:
                    data_source = data_source.group(1)
                    
                if data_source.lower() == 'putlocker':
                    data_source = self.display_name
                    
                if data_name and data_film and  data_server:
                    self.AddFileHost(list, res.upper(), data_name+'|'+data_film+'|'+data_server+'|'+REF,host=data_source.upper())
        
                
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):  
    
        from entertainment.net import Net
        
        import re

        net = Net(cached=False)        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)
        
        if type == 'tv_episodes':
            name = name + ' season ' + season
        
        url = 'http://9movies.tv/search/'   + name.replace(' ','+')  + '.html'         
        LINK=net.http_GET(url).content
        match=re.compile('<div class="ml-item">(.+?)</div>',re.DOTALL).findall(LINK)
        
        found_item_url = ''
        for item in match:                      
             item_info = re.search('<a href="([^"]+?)".+?title="([^"]+?)">', item)
             if item_info:
                item_url = item_info.group(1)
                item_title = item_info.group(2).lower()
                
                names = name.lower().split(' ')
                names_count = len(names)
                names_match_count = 0
                for names_item in names:
                    if names_item in item_title:
                        names_match_count = names_match_count + 1
                if names_match_count / names_count * 100 >= 85:
                    found_item_url = item_url
                    break;

        if found_item_url:
            self.GetFileHosts(found_item_url, list, lock, message_queue,season,episode,type,year)
    
            
    def Resolve(self, url):
            #print url
            import urllib

            if '|' in url:
                splits = url.split('|')
                data_name = splits[0]
                data_film = splits[1]
                data_server = splits[2]
                REF = splits[3]
                
                from entertainment.net import Net
                import time,json,re

                net = Net(cached=False,user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko')    
                
                headers = {'X-Requested-With': 'XMLHttpRequest','Referer':REF}

                query = {'ipplugins': '1', 'ip_film':data_film, 'ip_server':data_server, 'ip_name':data_name}
                
                url = 'http://9movies.tv/ip.temp/swf/plugins/ipplugins.php'
                #print url
                result = net.http_POST(url, query, headers=headers).content

                result = json.loads(result)
                #print result

                if 'error' in result:
                    return ''
               
                try:
                    plugin_s = result['s']
                    url = 'http://9movies.tv/ip.temp/swf/ipplayer/ipplayer.php?u=%s&w=%s&h=%s&s=%s' % (result['s'], '100%25', '500', data_server)
                    headers = {'X-Requested-With': 'XMLHttpRequest','Referer':REF}
                    result = net.http_GET(url, headers=headers).content
                    result = json.loads(result)
                    
                    if result["type"] == 3:
                        url = result["data"].replace('\/','/')
                    elif result["type"] == 1:
                        url = result["data"][0]["files"]
                        
                    
                    if 'redirector' in url:
                        url = urllib.urlopen(url).geturl()
                        if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
                        else: url = url.replace('https://', 'http://')
                    else:
                        from entertainment import istream
                        url = istream.ResolveUrl(url)
                except:
                    pass

            else:
                from entertainment import istream
                url = istream.ResolveUrl(url)                     
                        

            return url
            
                
                
