from yosemite.ml.text.util import Chunker, SentenceTransformer
from yosemite.ml.text.cross_encode import CrossEncoder as CrossEncode
from typing import Union, List, Tuple, Optional, Dict
import os
import uuid
from annoy import AnnoyIndex
from whoosh import index as whoosh_index
from whoosh.analysis import StandardAnalyzer, FancyAnalyzer, LanguageAnalyzer, KeywordAnalyzer
from whoosh.fields import Schema, TEXT, ID, KEYWORD, STORED
from whoosh.qparser import QueryParser, QueryParserError, MultifieldParser
import pandas as pd
from PyPDF2 import PdfReader
from ebooklib import epub

class YosemiteDatabase:
    """
    A Unified & Local Database with no backend services required. Built using Whoosh & Annoy. Combines the power of Whoosh for text search and Annoy for vector search, to deliver incredibly easy to use and powerful search capabilities.

    ```python
    from yosemite.ml.database import YosemiteDatabase
    ```

    Attributes:
        dimension (int): The dimension of the vectors.
        model_name (str): The name of the SentenceTransformer model to be used.
        schema (Schema): The schema to be used for the Whoosh index.
        index_dir (str): The directory where the Whoosh index is stored.
        analyzer (str): The type of analyzer to be used for the Whoosh index.

    Args:
        dimension (int, optional): The dimension of the vectors. Defaults to None.
        model_name (str, optional): The name of the SentenceTransformer model to be used. Defaults to "all-MiniLM-L6-v2".
        schema (Schema, optional): The schema to be used for the Whoosh index. Defaults to None.
        analyzer (str, optional): The type of analyzer to be used for the Whoosh index. Defaults to "standard".

    Methods:
        load: Load an existing Whoosh index.
        create: Create a new Whoosh index.
        load_dataset: Load a dataset into the Whoosh index.
        load_docs: Load documents from a directory into the Whoosh index.
        add: Add documents to the Whoosh index.
        search: Search the Whoosh index.
        search_and_rank: Search and rank the Whoosh index.
    """
    def __init__(self, dimension: Optional[int] = None, model_name: str = "all-MiniLM-L6-v2", 
                 schema: Optional[Schema] = None, analyzer: Optional[str] = "standard"):
        self.index = None
        self.dimension = dimension
        self.model_name = model_name
        self.ix = None
        self.schema = schema
        self.index_dir = None
        self.analyzer = analyzer

    def load(self, dir: str):
        """
        A method to load an existing Whoosh index.

        Example:
            ```python
            db = YosemiteDatabase()
            db.load("./databases/db")
            ```

        Args:
            dir (str): The directory where the Whoosh index is stored.
        """
        self.index_dir = dir
        if not os.path.exists(self.index_dir):
            raise FileNotFoundError(f"Index directory {self.index_dir} does not exist.")
        if not whoosh_index.exists_in(self.index_dir):
            raise FileNotFoundError(f"Index does not exist in directory {self.index_dir}.")
        self.ix = whoosh_index.open_dir(self.index_dir)

    def create(self, dir: Optional[str] = None):
        """
        A method to create a new Whoosh index.

        Example:
            ```python
            db = YosemiteDatabase()
            db.create()
            ```

        Args:
            dir (str, optional): The directory where the Whoosh index will be stored. Defaults to None.
        """
        if self.schema is None:
            if self.analyzer == "standard":
                self.schema = Schema(id=ID(stored=True), content=TEXT(analyzer=StandardAnalyzer(), stored=True), 
                                     chunks=TEXT(stored=True), vectors=STORED)
            elif self.analyzer == "fancy":
                self.schema = Schema(id=ID(stored=True), content=TEXT(analyzer=FancyAnalyzer(), stored=True), 
                                     chunks=TEXT(stored=True), vectors=STORED)
            elif self.analyzer == "language":
                self.schema = Schema(id=ID(stored=True), content=TEXT(analyzer=LanguageAnalyzer(), stored=True), 
                                     chunks=TEXT(stored=True), vectors=STORED)
            elif self.analyzer == "keyword":
                self.schema = Schema(id=ID(stored=True), content=KEYWORD(analyzer=KeywordAnalyzer(), stored=True), 
                                     chunks=TEXT(stored=True), vectors=STORED)

        if dir is None:
            self.index_dir = "./databases/db"
        else:
            self.index_dir = dir
        os.makedirs(self.index_dir, exist_ok=True)
        self.ix = whoosh_index.create_in(self.index_dir, self.schema)

    def load_dataset(self, path: str, id_column: str, content_column: str):
        """
        A method to load a CSV dataset into the Whoosh index.

        Example:
            ```python
            db = YosemiteDatabase()
            db.create()
            db.load_dataset("data.csv", "id", "content")
            ```

        Args:
            path (str): The path to the CSV dataset.
            id_column (str): The name of the column containing the document IDs.
            content_column (str): The name of the column containing the document content.
        """
        if not self.ix:
            self.create()
        df = pd.read_csv(path)
        writer = self.ix.writer()
        chunker = Chunker()
        embedder = SentenceTransformer(self.model_name)
        for _, row in df.iterrows():
            doc_id = str(row[id_column])
            doc_content = row[content_column]
            chunks = chunker.chunk_text(doc_content)
            vectors = [embedder.embed([chunk])[0][1] for chunk in chunks]
            writer.add_document(id=doc_id, content=doc_content, chunks="\n".join(chunks), vectors=vectors)
        writer.commit()

    def load_docs(self, dir: str):
        """
        A very powerful method to load documents from a directory into the Whoosh index. Supports .txt, .pdf, and .epub files.

        Example:
            ```python
            db = YosemiteDatabase()
            db.create()
            db.load_docs("documents")
            ```

        Args:
            dir (str): The directory containing the documents.
        """
        if not self.ix:
            self.create()
        if not os.path.exists(dir):
            raise FileNotFoundError(f"Directory {dir} does not exist.")

        writer = self.ix.writer()
        chunker = Chunker()
        embedder = SentenceTransformer(self.model_name)
        for file_path in os.listdir(dir):
            file_path = os.path.join(dir, file_path)
            if file_path.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
            elif file_path.endswith(".pdf"):
                with open(file_path, "rb") as file:
                    reader = PdfReader(file)
                    content = " ".join(page.extract_text() for page in reader.pages)
            elif file_path.endswith(".epub"):
                book = epub.read_epub(file_path)
                content = " ".join(item.get_content().decode("utf-8") for item in book.get_items_of_type(9))
            else:
                continue

            doc_id = str(uuid.uuid4())
            chunks = chunker.chunk_text(content)
            vectors = [embedder.embed([chunk])[0][1] for chunk in chunks]
            writer.add_document(id=doc_id, content=content, chunks="\n".join(chunks), vectors=vectors)
        writer.commit()

    def add(self, documents: List[Dict[str, str]], shared_id: Optional[bool] = False):
        """
        A method to add documents to the Whoosh index.

        Example:
            ```python
            db = YosemiteDatabase()
            db.create()
            documents = [
                {"content": "This is a test document."},
                {"content": "This is another test document."}
            ]
            db.add(documents)
            ```

        Args:
            documents (List[Dict[str, str]]): A list of dictionaries containing the document content.
            shared_id (Optional[bool], optional): Whether to use a shared ID for all documents. Defaults to False.
        """
        if not self.ix:
            self.create()
        writer = self.ix.writer()
        chunker = Chunker()
        embedder = SentenceTransformer(self.model_name)
        for doc in documents:
            if shared_id:
                doc_id = "shared"
            else:
                doc_id = doc.get("id", str(uuid.uuid4()))
            doc_content = doc["content"]
            chunks = chunker.chunk_text(doc_content)
            vectors = [embedder.embed([chunk])[0][1] for chunk in chunks]
            writer.add_document(id=doc_id, content=doc_content, chunks="\n".join(chunks), vectors=vectors)
        writer.commit()

    def search(self, query: str, fields: Optional[List[str]] = None, k: int = 5) -> List[Tuple[str, str, List[float]]]:
        """
        A method to search the Whoosh & Annoy index.

        Example:
            ```python
            db = YosemiteDatabase()
            db.load("./databases/db")
            results = db.search("test")
            for doc_id, chunk, vector in results:
                print(f"Document ID: {doc_id}")
                print(f"Chunk: {chunk}")
                print(f"Vector: {vector}")
                print("---")
            ```

            ```bash
            Document ID: 1
            Chunk: This is a test document.
            Vector: [0.1, 0.2, 0.3, ...]
            ---
            Document ID: 2
            Chunk: This is another test document.
            Vector: [0.4, 0.5, 0.6, ...]
            ---
            ```

        Args:
            query (str): The search query.
            fields (Optional[List[str]], optional): The fields to search in. Defaults to None.
            k (int, optional): The number of results to return. Defaults to 5.

        Returns:
            List[Tuple[str, str, List[float]]]: A list of tuples containing the document ID, chunk, and vector.
        """
        if not self.ix:
            raise ValueError("Index has not been built or loaded.")

        with self.ix.searcher() as searcher:
            if fields is None:
                parser = QueryParser("content", schema=self.schema)
            else:
                parser = MultifieldParser(fields, schema=self.schema)
            try:
                q = parser.parse(query)
                results = searcher.search(q, limit=k)
                embedder = SentenceTransformer(self.model_name)
                query_vector = embedder.embed([query])[0][1]
                ranked_results = []
                for hit in results:
                    doc_id = hit["id"]
                    doc_content = hit["content"]
                    doc_vectors = hit["vectors"]
                    if not self.dimension:
                        self.dimension = len(doc_vectors[0])
                    index = AnnoyIndex(self.dimension, 'angular')
                    for i, vector in enumerate(doc_vectors):
                        index.add_item(i, vector)
                    index.build(10)
                    indices = index.get_nns_by_vector(query_vector, k, include_distances=False)
                    for idx in indices:
                        chunk = hit["chunks"].split("\n")[idx]
                        ranked_results.append((doc_id, chunk, doc_vectors[idx]))
                return ranked_results
            except QueryParserError as e:
                print(f"QueryParserError: {e}")
                return []
            
    def search_and_rank(self, query: str, k: int = 5) -> List[Tuple[str, str, float]]:
        """
        A method to search and rank the Whoosh & Annoy index.

        Example:
            ```python
            db = YosemiteDatabase()
            db.load("./databases/db")
            results = db.search_and_rank("test")
            for doc_id, chunk, score in results:
                print(f"Document ID: {doc_id}")
                print(f"Chunk: {chunk}")
                print(f"Score: {score}")
                print("---")
            ```

            ```bash
            Document ID: 1
            Chunk: This is a test document.
            Score: 0.9
            ---
            Document ID: 2
            Chunk: This is another test document.
            Score: 0.8
            ---
            ```

        Args:
            query (str): The search query.
            k (int, optional): The number of results to return. Defaults to 5.

        Returns:
            List[Tuple[str, str, float]]: A list of tuples containing the document ID, chunk, and score.
        """
        if not self.ix:
            raise ValueError("Index has not been built or loaded.")
        with self.ix.searcher() as searcher:
            parser = QueryParser("content", schema=self.schema)
            try:
                q = parser.parse(query)
                whoosh_results = searcher.search(q, limit=k)
                whoosh_chunks = [hit["chunks"] for hit in whoosh_results]
            except QueryParserError as e:
                print(f"QueryParserError: {e}")
                whoosh_chunks = []
        embedder = SentenceTransformer(self.model_name)
        query_vector = embedder.embed([query])[0][1]
        vector_results = []
        for doc_id, doc_chunks, doc_vectors in zip(self.document_ids, self.sentences, self.vectors):
            if not self.dimension:
                self.dimension = len(doc_vectors[0])
            index = AnnoyIndex(self.dimension, 'angular')
            for i, vector in enumerate(doc_vectors):
                index.add_item(i, vector)
            index.build(10)
            indices = index.get_nns_by_vector(query_vector, k, include_distances=False)
            for idx in indices:
                vector_results.append((doc_id, doc_chunks[idx]))

        combined_results = whoosh_chunks + [chunk for _, chunk in vector_results]
        cross_encode = CrossEncode()
        ranked_results = cross_encode.rank(query, combined_results, [])
        return [(doc_id, chunk, score) for (doc_id, chunk), score in ranked_results]

if __name__ == "__main__":
    db = YosemiteDatabase()
    db.create()
    documents = [
        {"content": "This is a test document."},
        {"content": "This is another test document."}
    ]
    db.add(documents)
    results = db.search("test")
    for doc_id, chunk, vector in results:
        print(f"Document ID: {doc_id}")
        print(f"Chunk: {chunk}")
        print(f"Vector: {vector}")
        print("---")