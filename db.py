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
    pubcrawl safes items in an sqlite db, mainly to decide wether items are new or have changed  
    '''
    
    # mapping python data types to sqlite data types
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
        '''
        connect to sqlite db
        '''
        
        # connect to db
        self.conn = sqlite3.connect(db)
        
    
    def init(self, item_class): 
        '''
        try to create a table with the item classes name and fields
        @param item_class: class of an item type to save
        '''
        columns = []
        
        for k,v in sorted(item_class.fields.items(), key=lambda x: x[0]):
            
            field = k+' '+self._data_type_map[v['type']]
            if k == 'id': field += ' PRIMARY KEY'
            columns.append(field)
        
        # add fields for created and updated timestamps as well as for the hash
        columns.extend(['created TEXT', 'updated TEXT', 'hash TEXT'])
        
        query = 'CREATE TABLE IF NOT EXISTS %s (%s)' % (item_class.__name__, ', '.join(columns))
        
        logging.info(query)
        
        self.conn.execute(query)
    
        
    def save(self, item):
        '''
        save an item to the database
        @return: result (int), new (boolean)
        '''
        
        # get hash of the item
        hash = self.hash(item)
        logging.debug('Hash of item %s: %s', item, hash)
        
        # try to select the item from the database
        for row in self.conn.execute('SELECT hash FROM %s WHERE id=?;' % (item.__class__.__name__,), (item['id'],)):
            
            # if the hash value from the database is not equal to the calculated hash value,
            # the item's content has changed and therefor has to be updated in the database  
            if row[0] != hash:
                
                query = 'UPDATE %s SET %s,`updated`=?,`hash`=? WHERE `id`=?' % (item.__class__.__name__, ','.join(['`%s`=?' % (x,) for x in item._fields.keys() if x != 'id']))
                logging.info(query)
                values = [v['value'] if v.has_key('value') else None for k,v in sorted(item._fields.items(), key=lambda x: x[0]) if k != 'id']
                values.extend([datetime.datetime.now(), hash, item['id']])
                logging.info(', '.join([unicode(x)[:16] for x in values]))
                result = self.conn.execute(query,tuple(values))
                self.conn.commit()
                return result, False
            
            # the item hasn't changed, so do nothing
            else: return 0, False
        
        # the item seems to be new, add it to the database
        query = 'INSERT INTO %s VALUES (%s,?,?,?)' % (item.__class__.__name__, ','.join(['?' for x in item._fields.keys()]))
        logging.info(query)
        values = [v['value'] if v.has_key('value') else None for k,v in sorted(item._fields.items(), key=lambda x: x[0])]
        values.extend([datetime.datetime.now(), datetime.datetime.now(), hash])
        logging.info(', '.join([unicode(x)[:16] for x in values]))
        result = self.conn.execute(query,tuple(values))
        self.conn.commit()
                
        return result, True
         
         
    def hash(self, item):
        '''
        calculate the items hash value based on the fields marked as part of the hash
        '''
        m = hashlib.md5()
        
        for k,v in sorted(item._fields.items(), key=lambda x: x[0]):
            
            if v.has_key('hash'): 
                
                # try to make a string out of the value
                try: s = str(v['value'])
                except: pass
                
                # maybe it's a unicode object?
                try: s = v['value'].encode('utf-8')
                except: pass
                
                try: m.update(s)
                except: logging.warning('Couldn\'t digest %s [%s]',k,v.__class__.__name__)
                
        return m.hexdigest()
        
    
    
    