#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jul 22, 2014

@author: zking
'''
import datetime
import pprint
from copy import deepcopy

################################################################################
# ITEM BASE CLASS
# Define your own item classes below
################################################################################ 


class Item(object):
    '''
    Item base class. Extend this class to build your own item types
    
    Define the fields you want to use
    items need to have an 'id' field, which serves as a unique identifier in the database
    the field names 'created', 'updated' and 'hash' may not be used, because these names
    are used internally 
    
    field types may be
    
        * int
        * long
        * float
        * str
        * unicode
        * buffer
        * datetime.datetime
        * datetime.date
        
    Fields are defines as dictionary
    keys are the field names, values are dictionaries defining a "type"
    
        fields = {
            'id': {'type': int},
        }
        
    fields may also have 'hash' set to True, resulting in the field's contents being part of the 
    items hash:
    
        fields = {
            'id': {'type': int, 'hash': True},
        }
      
     
    '''
    
    # field definitions
    fields = {
        'id': {'type': int},
    }
    
    def __init__(self, **kwargs):
        '''
        the constructor deepcopies the fields for use in the actual instances
        '''
        #deepcopy fields for each instance
        self._fields = {}
        for k,v in self.fields.iteritems(): 
            self._fields[k] = deepcopy(v)
            if kwargs.has_key(k): self[k] = kwargs[k]

    ########################
    # DICTIONARY INTERFACE #
    ########################
    
    def __str__(self):
        d = dict([(k,v['value'] if v.has_key('value') else None) for k,v in self._fields.iteritems()])
        return pprint.pformat(d)

    def __len__(self):
        return len(self._fields)

    def __setitem__(self, name, value):
        if not self._fields.has_key(name): raise KeyError(name)
        if value.__class__ != self._fields[name]['type']: raise ValueError('Type mismatch: %s: %s, %s' % (name, value.__class__.__name__, self._fields[name]['type'].__name__))
        self._fields[name]['value'] = value

    def __getitem__(self, name):
        if not self._fields.has_key(name): raise KeyError(name)
        try: return self._fields[name]['value']
        except KeyError: return None

    def __delitem__(self, name):
        if not self._fields.has_key(name): raise KeyError(name)
        try: del self._fields[name]['value']
        except KeyError: pass
        
    def __iter__(self):
        for k,v in self._fields.iteritems():
            try: value = v['value']
            except KeyError: value = None
            yield k, value           

    def __contains__(self, name):
        return self._fields.has_key(name)
    
    
    
################################################################################
# YOUR ITEM CLASSES HERE
# EXTEND "Item" class and define your fields
################################################################################ 

class FlohmarktItem(Item):
    
    fields = {
        'id':       {'type': unicode},
        'title':    {'type': unicode},
        'timestamp':{'type': datetime.datetime},
        'url':      {'type': unicode},
        'text':     {'type': unicode, 'hash': True},
    }
    
# ----------------------------------------------------------------------------------------------------            

class LeerstandItem(Item):
    
    fields = {
        'id':       {'type': unicode},
        'name':     {'type': unicode},
        'link':     {'type': unicode},
        'inactive': {'type': unicode, 'hash': True},
        'address':  {'type': unicode},
        'author':   {'type': unicode},
        'comments': {'type': unicode, 'hash': True},       
    }