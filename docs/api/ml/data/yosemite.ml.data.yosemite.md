# **YosemiteDatabase** (Unified '*Elastic*' and *Vector Searchable* DB)

### Quick Start

```python
from yosemite.ml.database import YosemiteDatabase

# Initialize the database, Create Empty Database
db = YosemiteDatabase()
db.create()

# Add Documents
documents = [
    {"content": "This is a test document."},
    {"content": "This is another test document."}
]

# Add Documents to Database
db.add(documents)

# Search for Documents, uses Whoosh text search & Annoy vector search; 
# both ran through a cross encoder and reranked.
results = db.search("test")
```

::: yosemite.ml.database