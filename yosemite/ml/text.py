import spacy
from spacy.cli import download
from typing import List, Tuple, Union

def ensure_model(model: str):
    try:
        spacy.load(model)
    except OSError:
        download(model)

class Chunker:
    """
    A class to chunk text into individual sentences or chunks.

    Example:
        ```python
        from yosemite.ml.text import Chunker
        chunker = Chunker()
        text = "This is a long text. It consists of multiple sentences. The Chunker class will split it into individual sentences or chunks."
        sentences = chunker.chunk_text(text)
        for sentence in sentences:
            print(sentence)
        ```

        ```bash
        This is a long text.
        It consists of multiple sentences.
        The Chunker class will split it into individual sentences or chunks.
        ```

    Attributes:
        nlp: A spaCy NLP model to process text.
    """

    def __init__(self, model: str = "en_core_web_sm"):
        ensure_model(model)
        self.nlp = spacy.load(model)

    def chunk(self, text: Union[str, List[str], Tuple[str], List[Tuple[str]]]) -> List[str]:
        """
        Chunk text into individual sentences or chunks.

        Example:
            ```python
            Chunker.chunk_text("This is a long text. It consists of multiple sentences.")
            ```

        Args:
            text: A string, list of strings, tuple of strings, or list of tuples of strings to chunk.

        Returns:
            A list of strings representing individual sentences or chunks.
        """

        if not text:
            return []

        if isinstance(text, str):
            doc = self.nlp(text)
            if len(doc) > 500: # Adjust the threshold as needed
                return [chunk.text.strip() for chunk in doc.sents if len(chunk) > 1]
            else:
                return [sent.text.strip() for sent in doc.sents]
        elif isinstance(text, (list, tuple)):
            if all(isinstance(item, str) for item in text):
                return [self.chunk_text(item) for item in text]
            elif all(isinstance(item, (list, tuple)) for item in text):
                return [self.chunk_text(subitem) for item in text for subitem in item]
            else:
                raise ValueError("Invalid input type. Expected str, list, tuple, or list of tuples.")

if __name__ == "__main__":
    chunker = Chunker()

    # Example with a single string
    text1 = "This is a long text. It consists of multiple sentences. The Chunker class will split it into individual sentences."
    sentences1 = chunker.chunk(text1)
    print("Chunker Example 1:")
    for sentence in sentences1:
        print(sentence)

    # Example with a list of strings
    text2 = ["This is the first text.", "This is the second text. It has multiple sentences."]
    sentences2 = chunker.chunk(text2)
    print("\nChunker Example 2:")
    for sentence_list in sentences2:
        for sentence in sentence_list:
            print(sentence)

    # Example with a list of tuples
    text3 = [("This is a tuple.", "It has two sentences."), ("Another tuple.", "With two more sentences.")]
    sentences3 = chunker.chunk(text3)
    print("\nChunker Example 3:")
    for sentence_list in sentences3:
        for sentence in sentence_list:
            print(sentence)