'''
Created on Jul 22, 2014

@author: zking
'''

import urllib2
import BeautifulSoup
import re
import items
import logging
from dateutil.parser import parse as parse_date
import urlparse




class Spider (object):
    '''
    Spider base class - extend for your own spider
    '''
    
    def urlopen(self, request):
        '''
        Retrieving the contents of an url
        @param request: string or urllib2.Request
        @return: unicode
        '''
        logging.info('GET %s', request)
        return urllib2.urlopen(request).read()
    
    
    def order_soup(self, request):
        '''
        Open an url, process relative image sources and links and return the soup
        @param request: string or urllib2.Request
        @return: BeautifulSoup.BeautifulSoup
        '''
        
        base_url = self.get_base_url(request)
        
        soup = BeautifulSoup.BeautifulSoup(self.urlopen(request))
        
        # handle relative links and image references
        self.add_base_url(soup.findAll('img'), base_url, 'src')
        self.add_base_url(soup.findAll('a'), base_url)
        
        return soup
    
    
    def add_base_url(self, iterator, base_url, attribute='href'):
        '''
        add http://domain.at to relative urls like /pictures/bla.jpg
        @param iterator: Iterator of soup chunks
        @param base_url: base url eg. 'http://domain.at'
        @param attribute: attribute of the DOM object to alter  
        '''
        base_url = base_url.strip('/')
        
        for element in iterator:
            
            try: element[attribute] = urlparse.urljoin(base_url, element[attribute]) 
            except: logging.exception(element)
            
    
    def get_base_url(self, request):
        '''
        get the base url, either from string or Request object
        @param request: string or urllib2.Request
        @return: string
        '''
        try:
            split_url = urlparse.urlsplit(request)
            base_url = split_url.scheme + '://' + split_url.netloc
            
        # request is not a string
        except AttributeError:
            base_url = request.get_type() + '://' + request.get_host()
            
        return base_url 



################################################################################
# YOUR SPIDERS HERE
################################################################################    


class Flohmarkt(Spider):
    
    start_url = 'http://www.flohmarkt.at/php/inserat_topsuche.php?such_kategorie=immobilien-wien&region=&q=&biete=ok'
    
    def crawl(self, url=None):
        
        if not url: url = self.start_url
        
        soup = self.order_soup(url)
                
        for add in soup.findAll('div', {'class': 'pMitte'}):
            detail_link = add.find('a', href=re.compile('detail\/[0-9]+$'))
            
            if not detail_link: continue
            item = self.parse_detail(self.urlopen(detail_link['href']))
            item['url'] = detail_link['href']
            yield item
            
        next = soup.find('a', href=re.compile('inserat_topsuche'))

        if next: 
            for item in self.crawl('http://www.flohmarkt.at/php/'+next['href']):
                yield item                    
            
    
    def parse_detail(self, soup):
        '''
        parse detail view
        '''
        #remove tags
        for tag in soup.findAll('script'):
            tag.replaceWith('')
            
        for tag in soup.findAll('iframe'):
            tag.replaceWith('')
            
        for tag in soup.findAll('div', id='adunit'):
            tag.replaceWith('')
        
        item = items.FlohmarktItem()
        
        item['id'] = soup.find('input', {'name': 'inserat_id'})['value']
        item['title'] = soup.find('title').text
        item['timestamp'] = parse_date(str(soup.find('div', text=re.compile('\(zuletzt aktualisiert\)'))).replace('(zuletzt aktualisiert)', ''))
        item['text'] = unicode(soup.find('div', style=None, id=None))
        
        return item
            
# ----------------------------------------------------------------------------------------------------            
            
import json
import time
            
class Leerstandsmelder(Spider):
    
    URL = 'http://www.leerstandsmelder.de/Wien/all_places.json?_=%(ts)s'  #ts == unix timestamp, can be ommitted
    
    def crawl(self):
        
        for json_item in json.loads(self.urlopen(self.URL % {'ts': int(time.time())}))['places']:
            item = items.LeerstandItem(**json_item['place'])
            yield item
        
                
# ----------------------------------------------------------------------------------------------------            
            
class Edikte(Spider):
    
    #url = 'http://www.edikte.justiz.gv.at/edikte/ex/exedi3.nsf/suche?OpenForm&subf=e&query=([VKat]=MH | [VKat]=MW | [VKat]=MSH | [VKat]=GGH | [VKat]=BBL | [VKat]=LF | [VKat]=GL | [VKat]=SO) AND [BL]=0'
    url = 'http://www.edikte.justiz.gv.at/edikte/ex/exedi3.nsf/suche?OpenForm&subf=e&query=%28%5BVKat%5D%3DEH%20%7C%20%5BVKat%5D%3DZH%20%7C%20%5BVKat%5D%3DMH%20%7C%20%5BVKat%5D%3DMW%20%7C%20%5BVKat%5D%3DMSH%20%7C%20%5BVKat%5D%3DGGH%20%7C%20%5BVKat%5D%3DRH%20%7C%20%5BVKat%5D%3DHAN%20%7C%20%5BVKat%5D%3DWE%20%7C%20%5BVKat%5D%3DEW%20%7C%20%5BVKat%5D%3DMAI%20%7C%20%5BVKat%5D%3DDTW%20%7C%20%5BVKat%5D%3DDGW%20%7C%20%5BVKat%5D%3DGA%20%7C%20%5BVKat%5D%3DGW%20%7C%20%5BVKat%5D%3DUL%20%7C%20%5BVKat%5D%3DBBL%20%7C%20%5BVKat%5D%3DLF%20%7C%20%5BVKat%5D%3DGL%20%7C%20%5BVKat%5D%3DSE%20%7C%20%5BVKat%5D%3DSO%29%20AND%20%5BBL%5D%3D0'
    detail_url = 'http://www.edikte.justiz.gv.at/edikte/ex/exedi3.nsf/0/%s?OpenDocument&f=1&bm=2' # insert document hash
    js_regex = "subOpen\('(?P<hash>[0-9a-z]{32})'\)"
    url_regex = ''
    
    def crawl(self, url=None):
        
        soup = self.order_soup(self.url)
        
        base_url = self.get_base_url(self.url)
                
        for link in soup.findAll('a', {'href': re.compile(self.js_regex)}):

            hash = re.search(self.js_regex, link['href']).groupdict()['hash']
            detail_link = self.detail_url % (hash,)

            detail_soup = self.order_soup(detail_link)
            
            content = detail_soup.find('div', {'class': 'edibg'})
            
            item = items.EdiktItem()
            
            #replace javascript links
            for element in detail_soup.findAll('a', href=re.compile('javascript')):
                try: 
                    element['href'] = urlparse.urljoin(base_url, re.search('imgwin\(\'(.+?)\'', element['onclick']).group(1))
                
                except: 
                    try:
                        element['href'] = urlparse.urljoin(base_url, re.search('helpwin\(\'(.+?)\'', element['href']).group(1))
                        
                    except: pass
            
            item['url'] = detail_link
            item['id'] = hash
            item['title'] = detail_soup.find('title').text
            item['text'] = unicode(content)           
            
            yield item

        
        
        
    