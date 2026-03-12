# TMTVR
**TMTVR**: That Motherfucker TV Remote
TMTVR is a lightweight, intuitive Object-Document Mapper (ODM) for CouchDB written in Python. It’s designed to make interacting with your database as easy as changing channels—if you can find the remote, that is.

# 🛋️ The Origin Story
Why the name? Because CouchDB is a "Couch," and every couch has that one elusive, frustrating, yet essential object: That Motherfucker TV Remote (TMTVR).

You know the one. It’s never on the table. It’s always wedged between the cushions. You only find it when you accidentally sit on it and change the channel to a Finnish documentary at max volume.

This library is that remote. It’s the interface between you and the "Couch." We named it TMTVR because, much like the physical remote, it’s always right there where you (eventually) need it, making sure you don't have to get up and manually poke the database buttons.

# ✨ Features
- Simple Mapping: Map Python classes to CouchDB documents with zero friction.
- Field Types: Define your model schema with `StringField`, `IntegerField`, `FloatField`, and more.
- Views: Create and query CouchDB views with simple functions.
- Lightweight: No heavy dependencies—just you, your couch, and the remote.

# 🚀 Quick Start
## Installation
```bash
pip install tmtvr
```
## Basic Usage
```python
from tmtvr.db import Database
from tmtvr.models import Model
from tmtvr.fields import StringField, IntegerField

# Connect to your "Couch"
db = Database('localhost', 5984, 'admin', 'password')
db_instance = db.get_or_create('my_living_room')
Model.set_db(db_instance)

# Define your Document (The stuff you find under the cushions)
class LostItem(Model):
    name = StringField()
    value = IntegerField()

# Create and save a new item
item = LostItem(name='keys', value=1)
item.save()

# Retrieve an item
retrieved_item = LostItem.get(item._id)
print(retrieved_item.name) # Output: keys
```

## Views
```python
from tmtvr.views import create_view
from tmtvr.query import query_view

# Create a view to find items by name
map_fun = "function(doc) { emit(doc.name, doc); }"
create_view(db_instance, 'lost_items', 'by_name', map_fun)

# Query the view
results = query_view(db_instance, 'lost_items', 'by_name', key='keys')
for row in results:
    print(row.value)
```

# 🛠️ Development
We welcome contributors! If you find a bug, it’s probably just stuck between the cushions. Feel free to open an issue or a Pull Request.

# 📄 License
Distributed under the GPL License. See LICENSE for more information.

**Disclaimer**: No actual television remotes were harmed in the making of this library. We cannot be held responsible for any butt-dialed database queries.
