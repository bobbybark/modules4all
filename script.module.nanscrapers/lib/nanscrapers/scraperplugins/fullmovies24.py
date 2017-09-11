import re
import requests
import xbmc
import urllib
from ..scraper import Scraper

requests.packages.urllib3.disable_warnings()

s = requests.session()
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

class fullmovies24(Scraper):
    domains = ['http://fullmovies24.net']
    name = "Fullmovies24"
    sources = []

    def __init__(self):
        self.base_link = 'http://fullmovies24.net'
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            search_id = urllib.quote_plus(title.lower())
            movie_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            
            headers = {'User_Agent':User_Agent}
            link = requests.get(movie_url,headers=headers,verify=False).content

            links = link.split('class="title"')[1]
            
            m_url = re.compile('href="(.+?)"',re.DOTALL).findall(links)[0]
            m_title = re.compile('title="(.+?)"',re.DOTALL).findall(links)[0]
            if title.lower() in m_title.lower():
                if year in m_title:
                    headers={'User-Agent':User_Agent}
        
                    content = requests.get(m_url,headers=headers).content

                    frame = re.compile('<iframe src="(.+?)"',re.DOTALL).findall(content)[0]
                    
                    holder = requests.get(frame).content
                    
                    vid = re.compile('type:"video/mp4",src:"(.+?)",height:(.+?),',re.DOTALL).findall(holder)
                    for url,qual in vid:
                        self.sources.append({'source': 'Streamango', 'quality': qual, 'scraper': self.name, 'url': 'http:'+url,'direct': True})                   
            return self.sources
        except Exception, argument:
            return self.sources


