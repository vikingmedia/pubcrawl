#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Jul 22, 2014

@author: zking
'''
import argparse
import config
import spiders
import mail
import db
import logging


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
        
    if new_items:
        lines = []
        for item in new_items:
            for k,v in item._fields.iteritems():
                if v.has_key('value') and v['value'] and unicode(v['value']).startswith('http'): 
                    v['value'] = '<a href="%s">%s</a>' % (v['value'],v['value'])
                
                lines.append('<b>%s:</b><br />%s<br /><br />' % (k,unicode(v['value']).encode('utf-8') if v.has_key('value') and v['value'] else 'n.a.'))
            lines.append('<hr /><br /><br />')
        
        # send email with new items    
        mail_text = '<html><head><meta http-equiv="content-type" content="text/html; charset=utf-8"> <!-- HTML 4.x --> <meta charset="utf-8"><!-- HTML 5 --></head><body>%s</body></html>' % ('\n'.join(lines))
        
        try: mail.Email(config.EMAIL_HOST, config.EMAIL_USER, config.EMAIL_PWD, config.EMAIL_SENDER, config.EMAIL_USE_TLS).send(config.EMAIL_RECEIVER, config.EMAIL_SUBJECT % {'spider': spider.__class__.__name__,'items': len(new_items)}, mail_text)
        
        except AttributeError: pass
        
        except: logging.exception('Email couldn\'t be sent!')
        