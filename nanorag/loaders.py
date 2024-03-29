# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/05_loaders.ipynb.

# %% auto 0
__all__ = ['PDFLoader', 'DocumentBridge']

# %% ../nbs/05_loaders.ipynb 2
from pathlib import Path
from pypdf import PdfReader
import random
from typing import List, Union
import uuid
from PIL import Image
from io import BytesIO
import sys, platform, os
from .context import ModelContext
from .base import Document, TextNode

# %% ../nbs/05_loaders.ipynb 5
#For simplicity lets start with accepting a List. 
class PDFLoader:
    """Accepts a dir or single path and converts its contents into documents that can be later used for storage and retrieval"""
    def __init__(self, path_dir: str, store = None):
        self.path_dir = Path(path_dir)
        if self.path_dir.is_dir():
            self.paths = [path for path in self.path_dir.iterdir() if path]
        else:
            self.paths = [self.path_dir]
        self.path = None
        self.store = store

    def get_tables(self, path = None):
        pass
        
    def pdf_validator(self, path):
        """Tries to read the pdf and returns a Bool value with the result"""
        try:
            reader = PdfReader(path)
            return True
        except Exception as e:
            return False

    def load_random_pdf(self):
        """Load a random pdf from the dataset. It loads pdfs until a valid one is found"""
        valid_pdf_found = False
        while not valid_pdf_found:  # Continue until a valid PDF is found
            pdf_path = random.choice(self.paths)
            is_valid = self.pdf_validator(pdf_path)
            if is_valid:
                reader = PdfReader(pdf_path)
                valid_pdf_found = True
                self.path = pdf_path
                return reader
            else:
                pdf_path.unlink()
                self.paths.remove(pdf_path)  # Remove the invalid path from the list
        
        if not valid_pdf_found:
            return None
    def load_pdf(self, path):
        reader = PdfReader(path)
        self.path = path
        return reader
    
    def format_reader_metadata(self, reader, include_local_path = True):
        #Format the metadata of the pdf. 
        keys_to_include = ["title", "author", "subject","creator", "producer","creation_date", "modification_date"]
        formatted_metadata = {}
        for key in keys_to_include:
            pdf_key = "/" + key.capitalize()
            formatted_metadata[pdf_key] = getattr(reader.metadata, key, '')
        if include_local_path:
            formatted_metadata['file_path'] = self.path
            formatted_metadata['file_name'] = self.path.name
            # Retrieve and add system information
            formatted_metadata['/SystemInfo'] = {
                'os_type': platform.system(),
                'working_directory': os.getcwd()
            }
        return formatted_metadata
    
    def get_documents(self, path = None):
        """Get a List of Text Documents from a pdf Path."""
        documents = []
        #Extracting text and storing it in documents
        source_id = self.__generate_id()
        if path == None:
            reader = self.load_random_pdf()
        else:
            reader = self.load_pdf(path)

        formatted_metadata = self.format_reader_metadata(reader)
        for i, page in enumerate(reader.pages):
            params = {"metadata": {**{"page": i + 1, "category": "PDF"}, **formatted_metadata}, "text": page.extract_text(), "source_id": source_id}
            #Add option to handle where it comes from
            if i == 0:
                title = formatted_metadata.get('/Title', None)
                if title is None:
                    title = params['text'].split('\n')[0]        
            if title is not None:
                params["name"] = title
            doc = Document(**params)
            doc.store = self.store
            documents.append(doc)
        return documents
    def get_images(self, path = None):
        #Can add some metadata like what page and location was found on. 
        #Create Image Node with that kind of info. 
        if path == None:
            reader = self.load_random_pdf()
        else:
            reader = self.load_pdf(path)
        images = []
        for count, page in enumerate(reader.pages):
            for image_file_object in page.images:
                image = Image.open(BytesIO(image_file_object.data))
                images.append(image)
        return images
    def __generate_id(self):
        return str(uuid.uuid4())

# %% ../nbs/05_loaders.ipynb 6
class DocumentBridge:
    """Class for connecting a list of documents into its corresponding Nodes and relationships"""
    def __init__(self, documents: Union[List[Document], Document], context: ModelContext):
        if isinstance(documents, List):
            self.documents = documents
        else:
            self.documents = [documents]
        self.context = context
    def to_nodes(self, chunk_size = 1024) -> List[TextNode]:
        """Brige a series of Documents into nodes linked by the end and start of the prev and next document. Great for linking together complex docs with structure
        such as pages or other info extracted first on a Document basis."""
        doc_nodes_list = [doc.create_nodes_from_doc(model_context = self.context, chunk_size = chunk_size) for doc in self.documents]
        if len(doc_nodes_list) > 1:
            for i, node_list in enumerate(doc_nodes_list):
                if i == 0:
                    node_list[-1].next_node = doc_nodes_list[i + 1][0].id
                else:
                    if i < len(doc_nodes_list) - 1:
                        node_list[-1].next_node = doc_nodes_list[i + 1][0].id
                    node_list[0].prev_node = doc_nodes_list[i - 1][-1].id
            nodes = [node for node_list in doc_nodes_list for node in node_list]
        elif len(doc_nodes_list) == 1:
            nodes = doc_nodes_list[0]
            for i, node in enumerate(nodes):
                if i == 0:
                    node.prev_node = None
                else:
                    node.prev_node = nodes[i - 1].id
                    if i < len(nodes) - 1:
                        node.next_node = nodes[i + 1].id
        return nodes
        
    def to_doc(self, include_children = False, 
               separator = '\n-----------------------------------------------------------------------------------------\n') -> Document:
        """Bridges a series of Documents into a single document. Great for storing sub-documents into a single one. Keeps some metadata of the documents into one. 
        Use documents with the same source id to be included here. """
        text = ''
        for i, doc in enumerate(self.documents):
            text += doc.text + separator
        metadata = self.documents[0].metadata;metadata.pop('page', None); metadata['pages'] = i + 1    
        document = Document(name = self.documents[0].name, text = text, metadata = metadata,
                            source_id = self.documents[0].source_id, doc_separator = separator, store = self.documents[0].store)
        if include_children:
            subdocument_ids = [subdoc.id for subdoc in self.documents] #This would be children.
            document.child_node= subdocument_ids
        return document
    def to_subdocs(self):
        """Split a document based on its separator. It will split them by pages by default. Each
        page ends with a specific separator."""
        if len(self.documents) == 1:
            single_document = self.documents[0]
        else:
            raise ValueError('Only one document can be converted to subdocuments')
        separator = single_document.doc_separator
        split_text = single_document.text.split(separator)
        split_text = [text for i, text in enumerate(split_text) if text != '']
        metadata = single_document.metadata
        documents = []
        for i, doc in enumerate(split_text):
            document = Document(text = doc, name = single_document.name + f': {i + 1}', metadata = metadata.copy(), source_id=single_document.source_id, store = single_document.store)
            document.metadata.pop('pages', None)
            document.metadata['page'] = i + 1
            if i != 0:
                document.prev_node = documents[i - 1].id
                documents[i - 1].next_node = document.id
            documents.append(document)
        return documents
