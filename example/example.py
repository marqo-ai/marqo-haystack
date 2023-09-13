# Colab: https://colab.research.google.com/drive/1YpDetI8BRbObPDEVdfqUcwhEX9UUXP-m?usp=sharing
import os
from pathlib import Path

from haystack.preview import Pipeline
from haystack.preview.components.file_converters import TextFileToDocument
from haystack.preview.components.writers import DocumentWriter

from marqo_haystack import MarqoDocumentStore
from marqo_haystack.retriever import MarqoDenseRetriever

HERE = Path(__file__).resolve().parent
file_paths = [HERE / "data" / Path(name) for name in os.listdir("data")]

# Marqo requires the docker container to be running.
# See here: https://docs.marqo.ai/latest/
document_store = MarqoDocumentStore(collection_name="test-haystack-document-store")

indexing = Pipeline()
indexing.add_component("converter", TextFileToDocument(id_hash_keys=["text"]))
indexing.add_component("writer", DocumentWriter(document_store))
indexing.connect("converter", "writer")
print("Indexing data...")
indexing.run({"converter": {"paths": file_paths}})

querying = Pipeline()
querying.add_component("retriever", MarqoDenseRetriever(document_store))
results = querying.run({"retriever": {"queries": ["Is black and white text boring?"], "top_k": 3}})

for d in results["retriever"]['documents'][0]:
    print(d.metadata, d.score)


# cleanup when done
import marqo

mq = marqo.Client()
mq.delete_index("test-haystack-document-store")
