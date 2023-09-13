from typing import Any, Dict, List, Optional
from haystack.preview import Document, component
from marqo_haystack import MarqoDocumentStore


@component
class MarqoDenseRetriever:
    """
    A component for retrieving documents from an MarqoDocumentStore.
    """

    def __init__(self, document_store: MarqoDocumentStore, filters: Optional[Dict[str, Any]] = None, top_k: int = 10):
        """
        Create an ExampleRetriever component. Usually you pass some basic configuration
        parameters to the constructor.

        :param filters: A dictionary with filters to narrow down the search space (default is None).
        :param top_k: The maximum number of documents to retrieve (default is 10).
        """
        self.filters = filters
        self.top_k = top_k
        self.document_store = document_store

    @component.output_types(documents=List[List[Document]])
    def run(
        self,
        queries: List[str],
        _: Optional[Dict[str, Any]] = None,  # filters not yet supported
        top_k: Optional[int] = None,
    ):
        """
        Run the retriever on the given input data.

        :param queries: The input data for the retriever. In this case, a list of queries.
        :param filters: The filters to apply during the search process, applied to all queries.
        :return: The retrieved documents.

        :raises ValueError: If the specified document store is not found or is not a MemoryDocumentStore instance.
        """

        if not top_k:
            top_k = self.top_k

        return {"documents": self.document_store.search(queries, top_k)}
