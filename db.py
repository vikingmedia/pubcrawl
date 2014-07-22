'''
Created on Jul 22, 2014

@author: zking
'''

import sqlite3
import config
import datetime
import logging

class Db(object):
    '''
    '''
    
    _data_type_map = {
        None: 'NULL',
        int: 'INTEGER',
        long: 'INTEGER',
        float: 'REAL',
        str: 'TEXT',
        unicode: 'TEXT',
        buffer: 'BLOB',
        datetime.datetime: 'TEXT',
        datetime.date: 'TEXT',
    }
    
    def __init__(self, db=config.DB):
        
        # connect to db
        self.conn = sqlite3.connect(db)
        
    
    def init(self, item_class): 
        '''
        @param item_class: class of an item type to save
        '''
        columns = []
        for k,v in sorted(item_class._fields.items(), key=lambda x: x[0]):
            field = k+' '+self._data_type_map[v['type']]
            if k == 'id': field += ' PRIMARY KEY'
            columns.append(field)
        
        query = 'CREATE TABLE IF NOT EXISTS %s (%s)' % (item_class.__name__, ', '.join(columns))
        
        logging.info(query)
        
        self.conn.execute(query)
    
        
    def save(self, item):
        
        query = 'INSERT INTO %s VALUES (%s)' % (item.__class__.__name__, ','.join(['?' for x in item._fields.keys()]))
        logging.info(query)
        values = [v['value'] if v.has_key('value') else None for k,v in sorted(item._fields.items(), key=lambda x: x[0])]
        logging.info(', '.join([unicode(x)[:16] for x in values]))
        result = self.conn.execute(query,tuple(values))
        self.conn.commit()
        return result
         
        
    
    
    