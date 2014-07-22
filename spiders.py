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



class Spider (object):
    '''
    Spider base class - extend for your own spider
    '''
    
    def urlopen(self, request):
        logging.info('GET %s', request)
        return BeautifulSoup.BeautifulSoup(urllib2.urlopen(request).read())



################################################################################
# YOUR SPIDERS HERE
################################################################################    


class Flohmarkt(Spider):
    
    start_url = 'http://www.flohmarkt.at/php/inserat_topsuche.php?such_kategorie=immobilien-wien&region=&q=&biete=ok'
    
    def crawl(self, url=None):
        
        if not url: url = self.start_url
        
        soup = self.urlopen(url)
        
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
        item = items.FlohmarktItem()
        
        item['id'] = int(soup.find('input', {'name': 'inserat_id'})['value'])
        item['title'] = soup.find('title').text
        item['timestamp'] = parse_date(str(soup.find('div', text=re.compile('\(zuletzt aktualisiert\)'))).replace('(zuletzt aktualisiert)', ''))
        item['text'] = unicode(soup.find('div', style=None, id=None))
        
        return item
            
            
            
        
        
        
    