# Superpowered AI Python SDK

This Python SDK provides an interface to interact with Superpowered AI, a knowledge base as a service for LLM applications. The SDK allows you to create, update, and delete knowledge bases, as well as directly query a knowledge base. You can also create and delete documents in a knowledge base.

## Installation

To install the Superpowered AI Python SDK you can use pip

```bash
pip install superpowered-sdk
```

## Usage

### Import all, and then initialize with API key and secret
```python
from superpowered import *

# initialize with API key
api_key_id = "INSERT_API_KEY_ID_HERE"
api_key_secret = "INSERT_API_KEY_SECRET_HERE"
init(api_key_id=api_key_id, api_key_secret=api_key_secret)
```

### KnowledgeBase class

The `KnowledgeBase` class is used to create, update, and delete knowledge bases. It can also be used to directly query a knowledge base.

```python
kb = KnowledgeBase(title="My Knowledge Base", supp_id="123", description="A sample knowledge base")
```

#### Methods

- `create()`: Creates a new knowledge base with the given title, supp_id, and description.
- `add_document(content, title=None, link_to_source=None, supp_id=None, description=None)`: Adds a document to the knowledge base.
- `get_documents()`: Retrieves all documents in the knowledge base.
- `query(query, retriever_top_k=100, reranker_top_k=5)`: Directly queries the knowledge base.
- `delete()`: Deletes the knowledge base.

### KnowledgeBaseDocument class

The `KnowledgeBaseDocument` class is used to create and delete documents in a knowledge base.

```python
doc = KnowledgeBaseDocument(kb_id="kb_id", content="Sample content", title="Sample document", link_to_source="https://example.com", supp_id="123", description="A sample document")
```

#### Methods

- `create()`: Creates a new document in the knowledge base with the given content, title, link_to_source, supp_id, and description.
- `delete()`: Deletes the document from the knowledge base.

### Utility functions

- `create_knowledge_base(title, supp_id=None, description=None)`: Creates a new knowledge base with the given title, supp_id, and description.
- `get_knowledge_base(title)`: Retrieves a knowledge base object for an existing knowledge base, given its title.
- `list_knowledge_bases(verbose=True)`: Lists all knowledge bases for an account.
- `list_documents_in_kb(kb_title, verbose=True)`: Lists all documents in a knowledge base, given its title.
- `add_file_to_kb(kb_title, file_path, file_type=None)`: Adds a file to a knowledge base.
- `add_directory_to_kb(kb_title, directory_path, verbose=False)`: Adds all supported files in a directory to a knowledge base.

## Examples

### Creating a knowledge base

```python
create_knowledge_base(title="My Knowledge Base", supp_id="123", description="A sample knowledge base")
```

### Getting an existing knowledge base
```python
kb = get_knowledge_base(title="My Knowledge Base")
```

### Adding a document to a knowledge base

```python
kb.add_document(content="Sample content", title="Sample document", link_to_source="https://example.com", supp_id="123", description="A sample document")
```

### Querying a knowledge base

```python
results = kb.query(query="What is the capital of France?", retriever_top_k=100, reranker_top_k=5)
```

### Deleting a knowledge base

```python
kb.delete()
```

### Listing all knowledge bases

```python
list_knowledge_bases(verbose=True)
```

### Listing all documents in a knowledge base

```python
documents = list_documents_in_kb(kb_title="My Knowledge Base", verbose=True)
```

### Adding a file to a knowledge base

```python
add_file_to_kb(kb_title="My Knowledge Base", file_path="path/to/file.txt")
```

### Adding all files in a directory to a knowledge base

```python
add_directory_to_kb(kb_title="My Knowledge Base", directory_path="path/to/directory")
```
