#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Jul 22, 2014

@author: zking
'''
import argparse
import config
import spiders
import items
import mail
import db
from HTMLParser import HTMLParser

__version__ = '0.0.1'


if __name__ == '__main__':
    
    p = argparse.ArgumentParser(
        description = 'Simple crawling engine by zking', 
        epilog = 'Keep on coding!' 
    )
    
    p.add_argument('spider')
    
    args = vars (p.parse_args())
    
    spider = eval('spiders.'+args['spider']+'()')
    idx = 0
    database = db.Db()
    
    new_items = []
    
    for item in spider.crawl():
        if idx == 0: database.init(item.__class__)
        idx += 1
        result, new = database.save(item)
        if new: new_items.append(item)
        
    lines = []
    for item in new_items:
        for k,v in item._fields.iteritems():
            lines.append('<p><b>%s:</b><br />%s</p><hr />' % (k,unicode(v) if v else 'n.a.'))
    
    # send email with new items    
    mail_text = '<html><head></head><body>%s</body></html>' % (''.join(lines))
    
    with open('test.html', 'wb') as f: f.write(mail_text)
    