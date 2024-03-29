from yosemite.ml import RAG
from yosemite.llms import Serve

def rag(document_directory: str = "rag_documents", provider: str = "openai", api_key: str = None):
    if api_key:
        rag = RAG(provider=provider, api_key=api_key)
    else:
        rag = RAG(provider=provider)

    rag.build()
    rag.db.load_docs(document_directory)
    
    serve = Serve(rag)
    serve.serve()
    
if __name__ == "__main__":
    rag()