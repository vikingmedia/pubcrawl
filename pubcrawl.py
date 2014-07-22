#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Jul 22, 2014

@author: zking
'''
import argparse
import sqlite3
import config
import spiders
import items
import db

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
    
    for item in spider.crawl():
        if idx == 0: database.init(item.__class__)
        idx += 1
        try: database.save(item)
        except sqlite3.IntegrityError: pass