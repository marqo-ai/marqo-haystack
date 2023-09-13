import logging
from typing import Any, Dict, List, Optional, Union

import marqo
from haystack.preview.dataclasses import Document
from haystack.preview.document_stores.decorator import document_store
from haystack.preview.document_stores.protocols import DuplicatePolicy

from marqo_haystack.errors import MarqoDocumentStoreFilterError

logger = logging.getLogger(__name__)


@document_store
class MarqoDocumentStore:
    """
    We use the `collection.get` API to implement the document store protocol,
    the `collection.search` API will be used in the retriever instead.
    """

    def __init__(
        self,
        collection_name: str = "documents",
        url: str = "http://localhost:8882",
        api_key: Optional[str] = None,
        settings_dict: Optional[Dict[str, Any]] = None,
        client_batch_size: int = 4,
    ):
        """
        Initializes the store.
        """

        # marqo.set_log_level("WARN")

        self._marqo_client = marqo.Client(url=url, api_key=api_key)

        self._collection = collection_name

        indexes = {idx.index_name for idx in self._marqo_client.get_indexes()["results"]}
        if self._collection not in indexes:
            self._marqo_client.create_index(self._collection, settings_dict=settings_dict)
        else:
            print(f"Index {self._collection} already exists, skipping index creation.")

        self._index = self._marqo_client.index(self._collection)

        self.client_batch_size = client_batch_size

    def count_documents(self) -> int:
        """
        Returns how many documents are present in the document store.
        """
        return self._index.get_stats()["numberOfDocuments"]

    def count_vectors(self) -> int:
        """
        Returns how many documents are present in the document store.
        """
        return self._index.get_stats()["numberOfVectors"]

    def filter_documents(self, filters: Optional[Dict[str, Any]] = None) -> List[Document]:
        """
        Not recommended to use. At most 10000 documents are returned.

        Returns the documents that match the filters provided.

        :param filters: the filters to apply to the document list.
        :return: a list of Documents that match the given filters.
        """

        if not isinstance(filters, dict) and filters is not None:
            msg = "Filters must be a dictionary or None"
            raise MarqoDocumentStoreFilterError(msg)

        filter_string = self._convert_filters(filters)
        results = self._index.search("", filter_string=filter_string, limit=10000)
        hits = []
        for r in results["hits"]:
            r.pop("_score")
            hits.append(r)

        return self._get_result_to_documents(hits)

    def _escape_special_filter(self, filter_value: Union[str, List[str]]) -> Union[str, List[str]]:
        """
        Escape special characters in filter values
        """
        special_chars = {"+", "-", "&&", "||", "!", "(", ")", "{", "}", "[", "]", "^", '"', "~", "*", "?", ":", "\\"}
        if isinstance(filter_value, list):
            return [self._escape_special_filter(v) for v in filter_value]

        if not isinstance(filter_value, str):
            return filter_value

        if any(c in filter_value for c in special_chars):
            for c in special_chars:
                filter_value = filter_value.replace(c, f"\\{c}")
        return filter_value

    def _convert_filters(self, filters: Optional[Dict[str, Any]] = None, boolean_op: str = "AND") -> str:
        """
        Convert haystack filters to marqo filterstring capturing all boolean operators
        """

        if not filters:
            return None

        filter_statements = []

        if isinstance(filters, list):
            for f in filters:
                filter_statements.append(self._convert_filters(f))
            return f" {boolean_op} ".join(filter_statements)

        for k in filters:
            if k in {"$and", "$or", "$not"}:
                filter_statements.append(f"({self._convert_filters(filters[k], k[1:].upper())})")
                continue

            if k in {"id", "text", "mime_type", "metadata", "id_hash_keys", "score", "embedding"}:
                doc_key = k
            else:
                doc_key = "__metadata_" + k

            # get the child of the filter for the key
            child = filters[k]

            # if the child is a dict then we go deeper
            if isinstance(child, dict):
                for op in child:
                    # if logical operator
                    if op in {"$and", "$or", "$not"}:
                        if isinstance(child[op], list):
                            new_op = {}
                            for v in child[op]:
                                new_op |= v
                            child[op] = new_op
                        filter_statements.append(f"({self._convert_filters({k: child[op]}, op[1:].upper())})")
                        continue

                    value = child[op]

                    # if comparison operator
                    if op == "$eq":
                        filt = f"{doc_key}:({value})"
                    elif op == "$ne":
                        filt = f"NOT {doc_key}:({value})"
                    elif op == "$in":
                        filts = []
                        for v in value:
                            filts.append(f"{doc_key}:({v})")
                        filt = f"({' OR '.join(filts)})"
                    elif op == "$nin":
                        filts = []
                        for v in value:
                            filts.append(f"NOT {doc_key}:{v}")
                        filt = f"({' AND '.join(filts)})"
                    elif op == "$gt":
                        # marqo doesn't have an exclusing range so we use a magic number
                        if type(value) not in {int, float}:
                            msg = f"Filter value {value} of type {type(value)} is not supported for range filters, must be of type int or float"
                            raise MarqoDocumentStoreFilterError(msg)
                        filt = f"{doc_key}:[{value + value*1e-16} TO *]"
                    elif op == "$gte":
                        if type(value) not in {int, float}:
                            msg = f"Filter value {value} of type {type(value)} is not supported for range filters, must be of type int or float"
                            raise MarqoDocumentStoreFilterError(msg)
                        filt = f"{doc_key}:[{value} TO *]"
                    elif op == "$lt":
                        if type(value) not in {int, float}:
                            msg = f"Filter value {value} of type {type(value)} is not supported for range filters, must be of type int or float"
                            raise MarqoDocumentStoreFilterError(msg)
                        # marqo doesn't have an exclusing range so we use a magic number
                        filt = f"{doc_key}:[* TO {value - value*1e-16}]"
                    elif op == "$lte":
                        if type(value) not in {int, float}:
                            msg = f"Filter value {value} of type {type(value)} is not supported for range filters, must be of type int or float"
                            raise MarqoDocumentStoreFilterError(msg)
                        filt = f"{doc_key}:[* TO {value}]"
                    else:
                        msg = f"Operator {op} is not supported with MarqoDocumentStore or is not a valid operator"
                        raise MarqoDocumentStoreFilterError(msg)
                    filter_statements.append(filt)
                    continue
            # if the child is a list then we apply the implict OR
            elif isinstance(child, list):
                filts = []
                for v in child:
                    filts.append(f"{doc_key}:({v})")
                filt = f"({' OR '.join(filts)})"
                filter_statements.append(filt)
            # otherwise the child is a literal value
            else:
                filter_statements.append(f"{doc_key}:({child})")

        return f" {boolean_op} ".join(filter_statements)

    def get_documents_by_id(self, ids: List[str]) -> List[Document]:
        """
        Returns documents with given ids.
        """
        results = self._index.get_documents(document_ids=ids)["results"]
        results = [r for r in results if r["_found"]]
        return self._get_result_to_documents(results)

    def write_documents(self, documents: List[Document], policy: DuplicatePolicy = DuplicatePolicy.FAIL) -> None:
        """
        Writes (or overwrites) documents into the store.

        :param documents: a list of documents.
        :param policy: not supported at the moment
        :raises DuplicateDocumentError: Exception trigger on duplicate document if `policy=DuplicatePolicy.FAIL`
        :return: None
        """

        if not isinstance(documents, list):
            msg = "Documents must be a list"
            raise ValueError(msg)

        marqo_docs = []
        for d in documents:
            if not isinstance(d, Document):
                msg = "Documents must be of type Document"
                raise ValueError(msg)
            d = self._prepare_document(d)

            if d["text"] is None:
                logger.warn(
                    f"Document {d['_id']} has no text, "
                    "therefor Marqo has nothing to create an embedding for. This document will be skipped"
                )
                continue

            marqo_docs.append(d)

        self._index.add_documents(
            documents=marqo_docs, client_batch_size=self.client_batch_size, tensor_fields=["text"]
        )

    def delete_documents(self, document_ids: List[str]) -> None:
        """
        Deletes all documents with a matching document_ids from the document store.
        Fails with `MissingDocumentError` if no document with this id is present in the store.

        :param object_ids: the object_ids to delete
        """
        self._index.delete_documents(ids=document_ids)

    def search(self, queries: List[Union[str, Dict[str, float]]], top_k: int) -> List[List[Document]]:
        """
        Perform vector search on the stored documents
        """
        results = []
        for query in queries:
            result = self._index.search(q=query, limit=top_k)
            results.append(result)

        return self._query_result_to_documents(results)

    def _prepare_document(self, d: Document) -> Dict[str, Any]:
        """
        Change the document in a way we can better store it into Marqo.
        """
        marqo_doc_meta = {}

        for k in d.metadata:
            new_k = "__metadata_" + k
            marqo_doc_meta[new_k] = d.metadata[k]

        document = {
            "_id": d.id,
            "id": d.id,
            "text": d.text,
            "mime_type": d.mime_type,
        }

        document |= marqo_doc_meta
        return document

    def _get_result_to_documents(self, marqo_documents: List[Dict[str, Any]]) -> List[Document]:
        """
        Helper function to convert Marqo results into Haystack Documents
        """
        documents = []
        for marqo_doc in marqo_documents:
            # prepare metadata
            metadata: Dict[str, Any] = {}
            for k in marqo_doc:
                if k.startswith("__metadata_"):
                    new_k = k.replace("__metadata_", "")
                    metadata[new_k] = marqo_doc[k]

            mime_type = marqo_doc.get("mime_type")
            document = Document(
                id=marqo_doc["_id"],
                text=marqo_doc["text"],
                metadata=metadata,
                mime_type=mime_type,
                score=marqo_doc.get("_score"),
            )

            documents.append(document)

        return documents

    def _query_result_to_documents(self, result: Dict[str, Any]) -> List[List[Document]]:
        """
        Helper function to convert Marqo results into Haystack Documents
        """
        retrievals = []

        for r in result:
            converted_hits = self._get_result_to_documents(r["hits"])
            retrievals.append(converted_hits)
        return retrievals
