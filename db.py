'''
Created on Jul 22, 2014

@author: zking
'''

import sqlite3
import config
import datetime
import logging
import hashlib

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
        
        columns.extend(['created TEXT', 'updated TEXT', 'hash TEXT'])
        
        query = 'CREATE TABLE IF NOT EXISTS %s (%s)' % (item_class.__name__, ', '.join(columns))
        
        logging.info(query)
        
        self.conn.execute(query)
    
        
    def save(self, item):
        '''
        @return: result (int), new (boolean)
        '''
        
        hash = self.hash(item)
        logging.debug('Hash of item %s: %s', item, hash)
        
        print item['id'].__class__, item.__class__.__name__, item['id']
        
        for row in self.conn.execute('SELECT hash FROM %s WHERE id=?;' % (item.__class__.__name__,), (item['id'],)):
            if row[0] != hash:
                query = 'UPDATE %s SET %s,`updated`=?,`hash`=? WHERE `id`=?' % (item.__class__.__name__, ','.join(['`%s`=?' % (x,) for x in item._fields.keys() if x != 'id']))
                logging.info(query)
                values = [v['value'] if v.has_key('value') else None for k,v in sorted(item._fields.items(), key=lambda x: x[0]) if k != 'id']
                values.extend([datetime.datetime.now(), hash, item['id']])
                logging.info(', '.join([unicode(x)[:16] for x in values]))
                result = self.conn.execute(query,tuple(values))
                self.conn.commit()
                return result, False
        
        query = 'INSERT INTO %s VALUES (%s,?,?,?)' % (item.__class__.__name__, ','.join(['?' for x in item._fields.keys()]))
        logging.info(query)
        values = [v['value'] if v.has_key('value') else None for k,v in sorted(item._fields.items(), key=lambda x: x[0])]
        values.extend([datetime.datetime.now(), datetime.datetime.now(), hash])
        logging.info(', '.join([unicode(x)[:16] for x in values]))
        result = self.conn.execute(query,tuple(values))
        self.conn.commit()
                
        return result, True
         
         
    def hash(self, item):
        m = hashlib.md5()
        
        for k,v in sorted(item._fields.items(), key=lambda x: x[0]):
            
            if v.has_key('hash'): 
                
                try: s = str(v)
                except: pass
                
                try: s = v.decode('utf-8')
                except: pass
                
                try: m.update(s)
                except: logging.warning('Couldn\'t digest %s [%s]',k,v.__class__.__name__)
                
        return m.hexdigest()
        
    
    
    