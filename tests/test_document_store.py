from typing import List
from haystack.preview.dataclasses import Document
from haystack.preview.document_stores import DocumentStore

import pytest
from haystack.preview import Document
from haystack.preview.testing.document_store import DocumentStoreBaseTests

from marqo_haystack.document_store import MarqoDocumentStore


class TestDocumentStore(DocumentStoreBaseTests):
    """
    Common test cases will be provided by `DocumentStoreBaseTests` but
    you can add more to this class.
    """

    @pytest.fixture
    def docstore(self) -> MarqoDocumentStore:
        """
        This is the most basic requirement for the child class: provide
        an instance of this document store so the base class can use it.
        """
        import marqo

        mq = marqo.Client()
        test_index = "test-haystack-document-store"
        mq.delete_index(test_index)
        return MarqoDocumentStore(collection_name=test_index)

    @pytest.mark.unit
    def test_delete_empty(self, docstore: MarqoDocumentStore):
        """
        Deleting a non-existing document should not raise with Marqo
        """
        docstore.delete_documents(["test"])

    @pytest.mark.unit
    def test_delete_not_empty_nonexisting(self, docstore: MarqoDocumentStore):
        """
        Deleting a non-existing document should not raise with Marqo
        """
        doc = Document(text="test doc")
        docstore.write_documents([doc])
        docstore.delete_documents(["non_existing"])
        assert docstore.get_documents_by_id(ids=[doc.id])[0].id == doc.id
        docstore.delete_documents([doc.id])

    @pytest.mark.unit
    def test_get_existing(self, docstore: MarqoDocumentStore):
        """
        Deleting an existing document
        """
        doc = Document(text="test doc")
        docstore.write_documents([doc])

        gotten_docs = docstore.get_documents_by_id(ids=[doc.id])
        assert len(gotten_docs) == 1

        docstore.delete_documents([doc.id])

    @pytest.mark.unit
    def test_delete_existing(self, docstore: MarqoDocumentStore):
        """
        Deleting an existing document
        """
        doc = Document(text="test doc")
        docstore.write_documents([doc])
        docstore.delete_documents([doc.id])
        assert len(docstore.get_documents_by_id(ids=[doc.id])) == 0

    @pytest.mark.unit
    def test_search_documents(self, docstore: MarqoDocumentStore):
        """
        Searching documents
        """
        doc = Document(id="mydoc", text="test1 test2")
        docstore.write_documents([doc])

        documents = docstore.search(queries=["test1", "test2"], top_k=10)
        assert len(documents) == 2
        assert len(documents[0]) <= 10
        assert len(documents[1]) <= 10
        docstore.delete_documents([doc.id])

    @pytest.mark.skip(reason="Filter on embedding value is not supported.")
    @pytest.mark.unit
    def test_eq_filter_embedding(self, docstore: MarqoDocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Filter on embedding value is not supported.")
    @pytest.mark.unit
    def test_in_filter_embedding(self, docstore: MarqoDocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Filter on embedding value is not supported.")
    @pytest.mark.unit
    def test_ne_filter_embedding(self, docstore: MarqoDocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Filter on embedding value is not supported.")
    @pytest.mark.unit
    def test_nin_filter_embedding(self, docstore: MarqoDocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Filter on embedding value is not supported.")
    @pytest.mark.unit
    def test_gt_filter_embedding(self, docstore: MarqoDocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Filter on embedding value is not supported.")
    @pytest.mark.unit
    def test_gte_filter_embedding(self, docstore: MarqoDocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Filter on embedding value is not supported.")
    @pytest.mark.unit
    def test_lt_filter_embedding(self, docstore: MarqoDocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Filter on embedding value is not supported.")
    @pytest.mark.unit
    def test_lte_filter_embedding(self, docstore: MarqoDocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Filter on table value is not supported.")
    @pytest.mark.unit
    def test_eq_filter_table(self, docstore: MarqoDocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Filter on table value is not supported.")
    @pytest.mark.unit
    def test_in_filter_table(self, docstore: MarqoDocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Filter on table value is not supported.")
    @pytest.mark.unit
    def test_ne_filter_table(self, docstore: MarqoDocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Filter on table value is not supported.")
    @pytest.mark.unit
    def test_nin_filter_table(self, docstore: MarqoDocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Filter on table value is not supported.")
    @pytest.mark.unit
    def test_gt_filter_table(self, docstore: MarqoDocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Filter on table value is not supported.")
    @pytest.mark.unit
    def test_gte_filter_table(self, docstore: MarqoDocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Filter on table value is not supported.")
    @pytest.mark.unit
    def test_lt_filter_table(self, docstore: MarqoDocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Filter on table value is not supported.")
    @pytest.mark.unit
    def test_lte_filter_table(self, docstore: MarqoDocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Range query on non-numeric value is not supported.")
    @pytest.mark.unit
    def test_gt_filter_non_numeric(self, docstore: MarqoDocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Range query on non-numeric value is not supported.")
    @pytest.mark.unit
    def test_gte_filter_non_numeric(self, docstore: MarqoDocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Range query on non-numeric value is not supported.")
    @pytest.mark.unit
    def test_lt_filter_non_numeric(self, docstore: MarqoDocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Range query on non-numeric value is not supported.")
    @pytest.mark.unit
    def test_lte_filter_non_numeric(self, docstore: MarqoDocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Duplicate policy not supported.")
    @pytest.mark.unit
    def test_write_duplicate_fail(self, docstore: MarqoDocumentStore):
        pass

    @pytest.mark.skip(reason="Duplicate policy not supported.")
    @pytest.mark.unit
    def test_write_duplicate_skip(self, docstore: MarqoDocumentStore):
        pass

    @pytest.mark.skip(reason="Duplicate policy not supported.")
    @pytest.mark.unit
    def test_write_duplicate_overwrite(self, docstore: MarqoDocumentStore):
        pass

    @pytest.mark.skip(reason="Filter on array contents is not supported.")
    @pytest.mark.unit
    def test_filter_document_array(self, docstore: DocumentStore, filterable_docs: List[Document]):
        pass

    @pytest.mark.skip(reason="Filter on dataframe is not supported.")
    @pytest.mark.unit
    def test_filter_document_dataframe(self, docstore: DocumentStore, filterable_docs: List[Document]):
        pass
