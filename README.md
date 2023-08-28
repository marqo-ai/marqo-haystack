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

## License

`marqo-haystack` is distributed under the terms of the [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html) license.
