# Yosemite - RAG Module

**The provided notebook demonstrates the use of the RAG module in the Yosemite library.**

**You can try it yourself without cloning this entire repository using:**

```bash
git clone https://github.com/hsaeed3/yosemite-rag
```

## Example Code

In this example we will use a small the corpus of documents located in the documents/ directory. The corpus contains a paper and a couple movie scripts. The Quiet-STar paper was chosen specifically as one of the inputs as it's file type is a PDF with pictures and numberical information, it was also published on March 14, 2024 making it too recent for LLM's to have picked up in knowledge. The movie scripts were chosen for extreme varience in this small example.

### Install the Yosemite Library

```bash
pip install yosemite
```

### Initialize the RAG Module

```python
# Import the RAG Module
from yosemite.ml import RAG
```

The RAG Module is Built off several other Modules from this Library. These classes are built right on top of Whoosh, Annoy, sentence-transformers, spaCy, OpenAI (instructor) just to make using them a bit easier:

```python
# from yosemite.ml import Database
# from yosemite.llms import LLM
# from yosemite.ml import CrossEncoder, SentenceTransformer
# from yosemite.ml.text import Chunker
```

### Initialize the RAG Module

The RAG module will initialize the LLM module at the same time, which may require an API key if you dont have one set. The currently supported API's are: 

- OpenAI
- NVIDIA
- Anthropic

*HuggingFace transformers is planned for local models.*

```python
# Initialize the RAG Module
rag = RAG(
    provider = "YOUR API PROVIDER",
    api_key = "YOUR API KEY IF NEEDED",
    # model = "MODEL",
    # base_url = "FOR NVIDIA API",
)
```

### Create a Database

This stage will create a database from the documents in the directory. The documents will be indexed, chunked, cleaned, tokenized & vectored and then stored in the database with a comfy schema for later use.

```python
# Create a Database
rag.build(
    # db = 'Your Directory / Or a Yosemite Database
)

# Add Documents to the Database
rag.db.load_docs(
    dir = 'Your Directory'
)
```

### Customize Your RAG Agent

This stage is completely optional, but it makes it fun! These values are embedded into a prompt, along with the Database's
cross encoded results.

```python
rag.customize(
    name = "Lightning McQueen",
    role = "Racecar",
    tone = "friendly",
    additional_instructions= "Answer everything incorporating your signature keywords like 'KACHOW!'"
    # goal = """
)
```

### Query the Database

Now that we have a database, we can query it using the RAG module. The RAG module will use the LLM module to generate a query and then use the database to find the most relevant documents.

```python
rag.invoke(
    query = "What is Quiet-STar learning?"
)
```

```bash
# Output
Well, partner, Quiet-STar learning is a process that involves using machine learning algorithms to detect and analyze patterns in data that may not be readily visible to the human eye. It's all about uncovering hidden insights and making predictions based on the information provided. Looks like Quiet-STar is diving deep into the world of data and using those numbers to zoom down the digital highway. KACHOW!
```