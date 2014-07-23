#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jul 22, 2014

@author: zking
'''
import datetime
import pprint

class Item(object):
    '''
    Item
    '''
    
    _fields = {
        'id': {'type': str, 'serializer': lambda x: str(x)},
    }
    

    def __init__(self):
        pass

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
################################################################################ 

class FlohmarktItem(Item):
    
    _fields = {
        'id': {'type': unicode},
        'title': {'type': unicode},
        'timestamp': {'type': datetime.datetime},
        'url': {'type': unicode},
        'text': {'type': unicode, 'hash': True},
    }