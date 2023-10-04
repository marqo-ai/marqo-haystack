# Marqo Document Store for Haystack

[![PyPI - Version](https://img.shields.io/pypi/v/marqo-haystack.svg)](https://pypi.org/project/marqo-haystack)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/marqo-haystack.svg)](https://pypi.org/project/marqo-haystack)
[![test](https://github.com/marqo-ai/marqo-haystack/actions/workflows/test.yml/badge.svg)](https://github.com/marqo-ai/marqo-haystack/actions/workflows/test.yml)

-----

**Table of Contents**

- [Marqo Document Store for Haystack](#marqo-document-store-for-haystack)
  - [Installation](#installation)
  - [About](#about)
  - [Examples](#examples)
  - [Usage](#usage)
    - [Using Locally](#using-locally)
    - [Using with Marqo Cloud](#using-with-marqo-cloud)
  - [License](#license)

## Installation

```console
pip install marqo-haystack
```

## About

This is a document store integration for [Marqo](https://github.com/marqo-ai/marqo) with [haystack](https://github.com/deepset-ai/haystack). 

Marqo is an end-to-end vector search engine which includes preprocessing and inference to generate vectors from your data. You can use pre-trained models or bring finetuned ones.

Haystack is an end-to-end NLP framework that enables you to build applications powered by LLMs, with haystack you can build end-to-end NLP applications solving your use case using state-of-the-art models.

## Examples

```python
from marqo_haystack import MarqoDocumentStore
 
document_store = MarqoDocumentStore()
```

You can find a code example showing how to use the Document Store and the Retriever under the `example/` folder of this repo.

## Usage

For documentation on Marqo itself, please [refer to the documentation](https://docs.marqo.ai/latest/).

You can use the `MarqoDocumentStore` in your haystack pipelines for single queries like so:

```python
from marqo_haystack import MarqoDocumentStore
from marqo_haystack.retriever import MarqoSingleRetriever

document_store = MarqoDocumentStore()

querying = Pipeline()
querying.add_component("retriever", MarqoSingleRetriever(document_store))
results = querying.run({"retriever": {"query": "Is black and white text boring?", "top_k": 3}})
```

Or for a list of queries:

```python
from marqo_haystack import MarqoDocumentStore
from marqo_haystack.retriever import MarqoRetriever

document_store = MarqoDocumentStore()

querying = Pipeline()
querying.add_component("retriever", MarqoRetriever(document_store))
results = querying.run({"retriever": {"queries": ["Is black and white text boring?"], "top_k": 3}})
```

### Using Locally

If you specify a `collection_name` that doesn't exist as a Marqo index then one will be created for you.

```python
from marqo_haystack import MarqoDocumentStore

# Use an existing index (if my-index does exist)
document_store = MarqoDocumentStore(collection_name="my-index")

# Create a new index (called 'documents' by default)
document_store = MarqoDocumentStore()
```

You can also pass in settings for the index created by the API by passing a dictionary to the `settings_dict` parameter. For details on the settings object please [refer to the Marqo docs](https://docs.marqo.ai/latest/API-Reference/indexes/#body-parameters)

In this example we specify that the index should use the `e5-large-v2` model and increase the `ef_construction` parameter to 512 for the HNSW graph construction.

```python
from marqo_haystack import MarqoDocumentStore

index_settings = {
    "index_defaults": {
        "model": "hf/e5-large-v2",
        "ann_parameters" : {
            "parameters": {
                "ef_construction": 512
            }
        }
    }
}

document_store = MarqoDocumentStore(settings_dict=index_settings)
```

### Using with Marqo Cloud

This integration can also be used with Marqo Cloud. You can sign up or access you Marqo Cloud account [here](https://cloud.marqo.ai/).

To use Marqo Cloud with this integration you will need to pass the `collection_name` (index name), `url` (`https://api.marqo.ai`), and `api_key` into the constructor.

```python
from marqo_haystack import MarqoDocumentStore
 
document_store = MarqoDocumentStore(
    url="https://api.marqo.ai",
    api_key="XXXXXXXXXXXXX",
    collection_name="my-cloud-index"
)
```

## License

`marqo-haystack` is distributed under the terms of the [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html) license.
