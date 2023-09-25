# SPDX-FileCopyrightText: 2023-present John Doe <jd@example.com>
#
# SPDX-License-Identifier: Apache-2.0
from haystack.preview.document_stores.errors import DocumentStoreError
from haystack.preview.errors import FilterError


class MarqoDocumentStoreError(DocumentStoreError):
    pass


class MarqoDocumentStoreFilterError(FilterError):
    pass


class MarqoDocumentStoreConfigError(MarqoDocumentStoreError):
    pass
