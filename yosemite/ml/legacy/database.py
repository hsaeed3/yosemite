from typing import Optional, List, Dict
import pathlib as pl
import uuid
from whoosh import index as whoosh_index
from whoosh.analysis import StandardAnalyzer, FancyAnalyzer, LanguageAnalyzer, KeywordAnalyzer
from whoosh.fields import Schema, TEXT, ID, KEYWORD
from whoosh.qparser import QueryParser, QueryParserError, MultifieldParser
import pandas as pd
from PyPDF2 import PdfReader
from ebooklib import epub

class Database:
    """
    A class for creating simple databases with Whoosh. Old.

    ```python
    from yosemite.ml.legacy.database import Database
    ```

    Attributes:
        ix: The Whoosh index object.
        schema: The Whoosh schema object.
        index_dir: The directory path to the index.

    Args:
        dir (str): The directory path to the index.
        schema (Schema): A Whoosh Schema to define the index structure.
        analyzer (str): The type of analyzer to use. Options are "standard", "fancy", "language", and "keyword".

    Methods:
        load: Loads an existing index.
        create: Creates a new index.
        load_dataset: Adds documents to an index, by reading a dataset.
        load_docs: Adds documents to an index, by reading text files from a directory.
        add: Adds documents to an index.
        search: Searches the index.
    """
    def __init__(self):
        self.ix = None
        self.schema = None
        self.index_dir = None

    def load(self, dir: str):
        """
        Loads an existing index.

        Example:
            ```python
            db = Database()
            db.load("./databases/db")
            ```

        Args:
            dir (str): Path to the index directory.
        """
        self.index_dir = dir
        if not pl.Path(self.index_dir).exists():
            return print(f"Index directory {self.index_dir} does not exist.")
        if not whoosh_index.exists_in(self.index_dir):
            return print(f"Index does not exist in directory {self.index_dir}.")
        self.ix = whoosh_index.open_dir(self.index_dir)

    def create(self, dir: Optional[str] = None, schema: Optional[Schema] = None, analyzer: Optional[str] = "standard"):
        """
        Creates a new index.

        Example:
            ```python
            db = Database()
            db.create()
            ```

        Args:
            dir (Optional[str]): Path to the index directory.
            schema (Optional[Schema]): A Whoosh Schema to define the index structure.
            analyzer (Optional[str]): The type of analyzer to use. Options are "standard", "fancy", "language", and "keyword".
        """
        if schema is None and analyzer == "standard":
            self.schema = Schema(id=ID(stored=True), content=TEXT(analyzer=StandardAnalyzer(), stored=True))
        elif schema is None and analyzer == "fancy":
            self.schema = Schema(id=ID(stored=True), content=TEXT(analyzer=FancyAnalyzer(), stored=True))
        elif schema is None and analyzer == "language":
            self.schema = Schema(id=ID(stored=True), content=TEXT(analyzer=LanguageAnalyzer(), stored=True))
        elif schema is None and analyzer == "keyword":
            self.schema = Schema(id=ID(stored=True), content=KEYWORD(analyzer=KeywordAnalyzer(), stored=True))
        else:
            self.schema = schema
        if dir is None:
            self.index_dir = "./databases/db"
            if not pl.Path(self.index_dir).exists():
                pl.Path(self.index_dir).mkdir(parents=True, exist_ok=True)
        else:
            self.index_dir = dir
            if not pl.Path(self.index_dir).exists():
                pl.Path(self.index_dir).mkdir(parents=True, exist_ok=True)
        self.ix = whoosh_index.create_in(self.index_dir, self.schema)

    def load_dataset(self, path: str, id_column: str, content_column: str):
        """
        Adds documents to an index, by reading a dataset.

        Example:
            ```python
            db = Database()
            db.load_dataset("dataset.csv", "id", "content")
            ```

        Args:
            path (str): The path to the dataset.
            id_column (str): The name of the column containing the document IDs.
            content_column (str): The name of the column containing the document content.
        """
        if not self.ix:
            self.create()
        df = pd.read_csv(path)
        writer = self.ix.writer()
        for i, row in df.iterrows():
            writer.add_document(id=row[id_column], content=row[content_column])
        writer.commit()

    def load_docs(self, dir: str):
        """
        Adds documents to an index, by reading text files from a directory.

        Args:
            dir (str): The path to the directory containing the text files.

        Returns:
            None
        """
        self.ix = None
        if not self.ix:
            self.create(schema=Schema(id=ID(stored=True), title=TEXT(stored=True), content=TEXT(stored=True)))
        if not pl.Path(dir).exists():
            return print(f"Directory {dir} does not exist.")

        writer = self.ix.writer()
        for file_path in pl.Path(dir).glob("*"):
            if file_path.suffix == ".txt":
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    writer.add_document(id=str(uuid.uuid4()), title=file_path.stem, content=content)
            elif file_path.suffix == ".pdf":
                with open(file_path, "rb") as file:
                    reader = PdfReader(file)
                    content = " ".join(page.extract_text() for page in reader.pages)
                    writer.add_document(id=str(uuid.uuid4()), title=file_path.stem, content=content)
            elif file_path.suffix == ".epub":
                book = epub.read_epub(file_path)
                content = " ".join(item.get_content().decode("utf-8") for item in book.get_items_of_type(9))
                writer.add_document(id=str(uuid.uuid4()), title=book.get_metadata("DC", "title")[0][0], content=content)
        writer.commit()

    def add(self, documents: List[Dict[str, str]], shared_id: Optional[bool] = False):
        """
        Adds documents to an index.

        Example:
            ```python
            db = Database()
            db.add([{"content": "This is a test document."}, {"content": "This is another test document."}])
            ```

        Args:
            documents (List[Dict[str, str]]): A list of documents to add to the index.
            shared_id (Optional[bool]): Whether to use a shared ID for all documents.
        """
        if shared_id:
            if not self.ix:
                self.create()
            writer = self.ix.writer()
            for doc in documents:
                writer.add_document(id="shared", content=doc["content"])
            writer.commit()
        if not self.ix:
            self.create()
        writer = self.ix.writer()
        for doc in documents:
            if 'id' not in doc:
                id = str(uuid.uuid4())
            else:
                id = doc['id']
            writer.add_document(id=id, content=doc["content"])
        writer.commit()

    def search(self, query: str, fields: Optional[List[str]] = None):
        """
        Searches the index.

        Example:
            ```python
            db = Database()
            db.create()
            db.add([{"content": "This is a test document."}, {"content": "This is another test document."}])
            results = db.search("test")
            print(results)
            ```

        Args:
            query (str): The query to search for.
            fields (Optional[List[str]]): A list of fields to search in.

        Returns:
            List[Dict[str, str]]: A list of search results.
        """
        if not self.ix:
            self.create()
        with self.ix.searcher() as searcher:
            if fields is None:
                parser = QueryParser("content", schema=self.schema)
            else:
                parser = MultifieldParser(fields, schema=self.schema)
            try:
                q = parser.parse(query)
                results = searcher.search(q)
                return [{"id": hit["id"], "content": hit["content"]} for hit in results]
            except QueryParserError as e:
                return print(f"QueryParserError: {e}")
    
#==============================================================================#
    
if __name__ == "__main__":

    db = Database()
    db.create()
    db.add([{"content": "This is a test document."}, {"content": "This is another test document."}])
    results = db.search("test")
    print(results)