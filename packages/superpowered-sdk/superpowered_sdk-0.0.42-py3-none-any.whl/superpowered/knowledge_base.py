from superpowered.main import BASE_URL, _format_http_response, get_headers
import requests
import random
import string
import os
#from llama_index import download_loader
from pathlib import Path

class KnowledgeBase:
    """
    The KnowledgeBase class is used to create, update, and delete knowledge bases. It can also be used to directly query a knowledge base.
    """
    def __init__(self, title: str, supp_id: str = None, description: str = None, kb_id: str = None):
        self.title = title
        self.supp_id = supp_id
        self.description = description
        self.kb_id = kb_id
        self.is_deployed = self.kb_id is not None

    def create(self):
        if self.is_deployed:
            raise Exception('This knowledge base has already been deployed: ' + self.kb_id)
        url = BASE_URL + 'knowledge_bases'
        payload = {
            'title': self.title
        }
        if self.supp_id is not None:
            payload['supp_id'] = self.supp_id
        if self.description is not None:
            payload['description'] = self.description
        resp = _format_http_response(requests.post(url, headers=get_headers(), json=payload))
        self.kb_id = resp['body']['id']
        self.is_deployed = True
        return resp['body']

    def add_document(self, content: str, title: str = None, link_to_source: str = None, supp_id: str = None, description: str = None):
        kb_document = KnowledgeBaseDocument(kb_id=self.kb_id, content=content, title=title, link_to_source=link_to_source, supp_id=supp_id, description=description)
        resp_body = kb_document.create()
        return resp_body

    def get_documents(self):
        url = BASE_URL + f'knowledge_bases/{self.kb_id}/documents'
        resp = _format_http_response(requests.get(url, headers=get_headers()))
        documents = {}
        for document in resp['body']:
            kb_document = KnowledgeBaseDocument(
                kb_id=document['id'],
                content=document['content'],
                title=document['title'],
                link_to_source=document['link_to_source'],
                supp_id=document['supp_id'],
                description=document['description'],
            )
            documents[document['id']] = kb_document
        return documents

    def query(self, query: str, retriever_top_k: int = 100, reranker_top_k: int = 5):
        """
        directly query a knowledge base
        """
        url = BASE_URL + f'knowledge_bases/{self.kb_id}/query'
        payload = {
            'query': query,
            'retriever_top_k': retriever_top_k,
            'reranker_top_k': reranker_top_k,
        }
        resp = _format_http_response(requests.post(url, headers=get_headers(), json=payload))
        return resp["body"]

    def delete(self):
        url = BASE_URL + f'knowledge_bases/{self.kb_id}'
        resp = _format_http_response(requests.delete(url, headers=get_headers()))
        return resp


class KnowledgeBaseDocument:
    """
    The KnowledgeBaseDocument class is used to create and delete documents in a knowledge base.
    """
    def __init__(self, kb_id: str, content: str, title: str = None, link_to_source: str = None, supp_id: str = None, description: str = None, doc_id: str = None):
        self.kb_id = kb_id
        self.content = content # content is a string
        self.title = title
        self.link_to_source = link_to_source
        self.supp_id = supp_id
        self.description = description
        self.doc_id = doc_id

    def create(self):
        url = BASE_URL + f'knowledge_bases/{self.kb_id}/documents'
        payload = {
            'content': self.content
        }
        if self.title is not None:
            payload['title'] = self.title
        if self.link_to_source is not None:
            payload['link_to_source'] = self.link_to_source
        if self.supp_id is not None:
            payload['supp_id'] = self.supp_id
        if self.description is not None:
            payload['description'] = self.description
        resp = _format_http_response(requests.post(url, headers=get_headers(), json=payload))
        return resp['body']

    def delete(self):
        url = BASE_URL + f'knowledge_bases/{self.kb_id}/documents/{self.doc_id}'
        resp = _format_http_response(requests.delete(url, headers=get_headers()))
        return resp


def get_knowledge_bases():
    knowledge_bases = {}
    url = BASE_URL + 'knowledge_bases'
    resp = requests.get(url, headers=get_headers())
    resp = _format_http_response(resp)
    for knowledge_base in resp['body']:
        kb = KnowledgeBase(
            title=knowledge_base['title'],
            kb_id=knowledge_base['id'],
            supp_id = knowledge_base['supp_id'],
            description=knowledge_base['description']
        )
        knowledge_bases[knowledge_base['id']] = kb
    return knowledge_bases

def create_knowledge_base(title: str, supp_id: str = None, description: str = None):
    """
    create_knowledge_base() is a convenience function that creates a KnowledgeBase object and then calls its create() method
    """
    kb = KnowledgeBase(title, supp_id, description)
    resp = kb.create()
    return kb

def get_knowledge_base(title: str):
    """
    get_knowledge_base() is a convenience function that returns a KnowledgeBase object for an existing knowledge base, given its title
    """
    knowledge_bases = get_knowledge_bases()
    # create knowledge base name to id map - knowledge_bases is a dict of knowledge base objects keyed on knowledge_base_id
    kb_from_title = {}
    for kb_id in knowledge_bases.keys():
        kb = knowledge_bases[kb_id] # get the KnowledgeBase object
        if kb.title not in kb_from_title:
            kb_from_title[kb.title] = kb
        else:
            print ('WARNING: Duplicate knowledge base title: ' + kb.title)
            #raise Exception('Duplicate knowledge base title: ' + kb.title)
    
    # if the title we're looking for is in the map, return the KnowledgeBase object
    if title in kb_from_title:
        return kb_from_title[title]
    else:
        raise Exception('Knowledge base title not found: ' + title)

def list_knowledge_bases(verbose=True):
    """
    list_knowledge_bases() is a convenience function that returns a dictionary of all KnowledgeBase objects for an account
    """
    knowledge_bases = get_knowledge_bases()
    if verbose:
        print ("\nKnowledge bases:")
        for kb_obj in knowledge_bases.values():
            print (f"id: {kb_obj.kb_id}\ntitle: {kb_obj.title}\n")
    return knowledge_bases

def list_documents_in_kb(kb_title: str, verbose=True):
    """
    list_documents_in_kb() is a convenience function that returns a dictionary of KnowledgeBaseDocument objects for an existing knowledge base, given its title
    """
    kb = get_knowledge_base(kb_title)
    documents = kb.get_documents()
    if verbose:
        print ("\nDocuments:")
        for document_obj in documents.values():
            print (f"title: {document_obj.title}\ncontent: {document_obj.content[:100]}\n\n")
    return documents

def read_file(file_path: str, file_type: str = None):
    """
    read a file and return its contents as a string
    """
    if file_type is None:
        file_type = file_path.split(".")[-1]

    reader_names = {
        "pdf": "PDFReader",
        "csv": "SimpleCSVReader",
        "docx": "DocxReader",
        "md": "MarkdownReader"
    }

    """elif file_type in list(reader_names.keys()):
        Reader = download_loader(reader_names[file_type])
        loader = Reader()
        documents = loader.load_data(file=Path(file_path))
        content = documents[0].text
        return content"""
    
    if file_type == "txt":
        with open(file_path, 'r') as f:
            # read the file and convert it to a string
            content = f.read()
            return content
    else:
        return None

def add_file_to_kb(kb_title: str, file_path: str, file_type: str = None):
    """
    add a file to a knowledge base - currently supports .txt, .pdf, .csv, .docx, and .md files
    """
    kb = get_knowledge_base(kb_title)
    if file_type is None:
        file_type = file_path.split(".")[-1]
    
    content = read_file(file_path, file_type)

    if content is None:
        raise Exception("File type not supported: " + file_type)
    
    # make the title a random string
    title = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    kb.add_document(content=content, title=title)

def add_directory_to_kb(kb_title: str, directory_path: str, verbose=False):
    """
    add all the supported files in a directory to a knowledge base
    """
    # TODO: add support for other file types
    # TODO: make sure this works for all different kinds of subdirectory structures - currently it's only been tested for one level of subdirectories
    # get all the txt files in the directory, and all subdirectories
    all_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".txt"):
                all_files.append(os.path.join(root, file))

    # add each file to the knowledge base
    for file in all_files:
        if verbose: print("Adding:", file)
        add_file_to_kb(kb_title, file_path=file)