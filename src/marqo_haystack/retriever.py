from typing import Any, Dict, List, Optional
from haystack.preview import Document, component
from marqo_haystack import MarqoDocumentStore


@component
class MarqoRetriever:
    """
    A component for retrieving documents from an MarqoDocumentStore with multiple queries.
    """

    def __init__(self, document_store: MarqoDocumentStore, filters: Optional[Dict[str, Any]] = None, top_k: int = 10):
        """Create an retriever component. Usually you pass some basic configuration
        parameters to the constructor.

        Args:
            document_store (MarqoDocumentStore): An instance of a MarqoDocumentStore
            filters (Optional[Dict[str, Any]], optional): A dictionary with filters to narrow down the search space. Defaults to None.
            top_k (int, optional):
        """
        self.filters = filters
        self.top_k = top_k
        self.document_store = document_store

    @component.output_types(documents=List[List[Document]])
    def run(self, queries: List[str], filters: Optional[Dict[str, Any]] = None, top_k: Optional[int] = None):
        """Run the retriever on the given list of queries.

        Args:
            queries (List[str]): An input list of queries
            filters (Optional[Dict[str, Any]], optional): A dictionary with filters to narrow down the search space. Defaults to None.
            top_k (Optional[int], optional): The maximum number of documents to retrieve. Defaults to None.
        """

        if not top_k:
            top_k = self.top_k

        if not filters:
            filters = self.filters

        return {"documents": self.document_store.search(queries, top_k, filters=filters)}


@component
class MarqoSingleRetriever(MarqoRetriever):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @component.output_types(documents=List[Document])
    def run(self, query: str, filters: Optional[Dict[str, Any]] = None, top_k: Optional[int] = None):
        """Run the retriever on a single query.

        Args:
            query (str): An input query
            filters (Optional[Dict[str, Any]], optional): A dictionary with filters to narrow down the search space. Defaults to None.
            top_k (Optional[int], optional): The maximum number of documents to retrieve. Defaults to None.
        """
        return {"documents": super().run([query], filters, top_k)["documents"][0]}
