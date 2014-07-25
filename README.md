pubcrawl
========

Simple crawling engine in python

# Usage

Add your spiders at the end of *spiders.py*. The class name also servers as the spider's name. The spider class must extend the *Spider* class and must have a crawl function which will be evoked without parameters by the crawling engine.

**Example:**

    class MySpider(Spider):
	
	def crawl(self):
		pass
		# do something

This spider can then be run by 

    python pubcrawl.py MySpider

If a mail server has been configured in *config.py*, a mail containing the new items (i.e. items not yet saved in the database) will be sent to the specified email address. Pubcrawl uses *sqlite3* as a database.

# Configuration

Configuration can be done in *config.py*, which has to be in the PYTHONPATH and is fairly simple. Just look at the example_config.py file. 

# Items

User your own items by extending th *Item* class. Define the fields you want to use. Items need to have an 'id' field, which serves as a unique identifier in the database. The field names 'created', 'updated' and 'hash' may not be used, because these names are used internally. 
    
field types may be
    
* int
* long
* float
* str
* unicode
* buffer
* datetime.datetime
* datetime.date
        
Fields are defines as a dictionary. Keys are the field names, values are dictionaries defining a "type"
    
        fields = {
            'id': {'type': int},
        }
        
Fields may also have 'hash' set to True, resulting in the field's contents being part of the 
item's hash:
    
        fields = {
            'id': {'type': int, 'hash': True},
        }

