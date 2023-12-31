# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_base.ipynb.

# %% auto 0
__all__ = ['BaseNode', 'TextNode', 'Document']

# %% ../nbs/00_base.ipynb 3
from abc import ABC, abstractmethod
import uuid
import sys
sys.path.append('..')
from .utils import *

# %% ../nbs/00_base.ipynb 5
#TODO: Implement Reference to Vector Indices. 
class BaseNode(ABC):
    """
    Lowest level abstraction for storing interrelated pieces of information, building block for other types of nodes. 
    """
    def __init__(self, metadata, model_context, prev_node=None, next_node=None, parent_node=None, child_node=[], embedding=[], id = None):
        self.metadata = metadata
        self.model_context = model_context
        self.prev_node = prev_node  # In llama index they have relationships in one dict. I can try it.
        self.next_node = next_node
        self.parent_node = parent_node
        self.child_node = child_node
        self.embedding = embedding
        if id == None:
            self.id = self.__set_id()
        else:
            self.id = id

    def __repr__(self):
        return f"BaseNode(id={self.id}, metadata={self.metadata}, prev_node={self.prev_node}, next_node={self.next_node}, parent_node={self.parent_node}, child_node={self.child_node})"

    def __set_id(self):
        return uuid.uuid4()

    def create_embedding(self):
        # Create embedding with the specific content inside.
        pass
    @abstractmethod
    def get_embedding(self):
        # Return the embeddings stored
        pass
    @abstractmethod
    def get_metadata_str(self):
        pass

# %% ../nbs/00_base.ipynb 6
class TextNode(BaseNode): #Add hash to verify content uniqueness
    """Class for creating chunks of Text that contain additional information like relationships of metadata, inheritance from
    BaseNode but geared specifically towards text"""
    #TODO: Include doc_id
    def __init__(self, text, model_context, metadata, prev_node = None, next_node = None, parent_node = None, 
                 child_node = [], embedding = [], auto_embed = True, doc_id = None, source_id = None, id = None,
                 idx_ref = None):
        super().__init__(metadata = metadata, model_context = model_context, 
                         prev_node = prev_node, next_node = next_node, parent_node = parent_node, 
                         child_node = child_node, embedding = embedding, id = id)
        self.text = text
        self.model_context = model_context
        self.embedding = None
        if auto_embed == True:
            self.create_embedding()
        self.hash = self.__calculate_hash()
        self.doc_id = doc_id
        self.source_id = source_id
        self.idx_ref = idx_ref

    def __repr__(self):
        return f"TextNode(id = {self.id},text = {self.text},metadata = {self.metadata}, prev_node = {self.prev_node}, next_node = {self.next_node}, parent_node = {self.parent_node}, child_node = {self.child_node})"
    
    def create_embedding(self):
        if self.embedding == None:
            self.embedding = self.model_context.embedding.encode([self.text], normalize_embeddings = True) #Huggingface sentence transformers. #TODO: Generalize this, create wrapper.Embedding model would have get and create embedding.
    def get_embedding(self):
        if self.embedding is None:
            raise ValueError("embedding not set.")
        return self.embedding
        #Embedding for text. Try one for image.
    def get_metadata_str(self, mode = None):
        return '\n'.join([DEFAULT_METADATA_TMPL.format(key=key, value=value) for key, value in self.metadata.items()])
    def __calculate_hash(self):
        return hash_input(f"{self.text}{self.metadata}{self.prev_node}{self.next_node}{self.parent_node}{self.child_node}")

# %% ../nbs/00_base.ipynb 7
class Document(BaseNode): 
    # A document is a collection of nodes. Add hash to verify content uniqueness.
    # Also can be the source of information.
    """
    Class that serves as a way to group information that comes from different sources intended to be stored or integrated with other services. It serves
    as the centralized source of truth of the information that is transformed into nodes. It can be used to store the information of a document, a webpage, pdf
    or any other source of information. The hash is recalculated once the info is changed and serves as an interface to docstore. 
    """
    def __init__(self, metadata = {}, name = None, text = None, prev_node = None, 
                 next_node = None, parent_node = None, child_node = [], 
                 embedding = [], source_id = None, doc_separator = None, 
                 id = None, nodes = [], store = None):
        self._initialized = False
        super().__init__(metadata = metadata, prev_node = prev_node, next_node = next_node, parent_node = parent_node, child_node = child_node, embedding = embedding, model_context=None, id = id) 
        self._text = text
        self._name = name
        self._metadata = metadata
        if source_id == None:
            self.source_id = self.__set_id()
        else:
            self.source_id = source_id
        self._source_id = self.source_id
        self.nodes = nodes
        self.doc_separator = doc_separator
        self.hash = self.__calculate_hash()
        self._initialized = True
        self.store = store

    @property
    def id_(self):
        return str(self.id)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        if self._initialized:
            self.hash = self.__update_hash()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        if self._initialized:
            self.hash = self.__update_hash()

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        self._metadata = value
        if self._initialized:
            self.hash = self.__update_hash()

    @property
    def source_id(self):
        return self._source_id
    
    @source_id.setter
    def source_id(self, value):
        self._source_id = value
        if self._initialized:
            self.hash = self.__update_hash()

    def __update_hash(self):
        """Recalculated if name, metadata, text or source id are modified."""
        return hash_input(f"{self._name}{self._metadata}{self._text}{self.source_id}")

    def __calculate_hash(self):
        """Calculated at the start with name, metadata, text and source id."""
        return hash_input(f"{self.name}{self.metadata}{self.text}{self.source_id}")
    
    def __repr__(self):
      return f"Document(id = {self.id}, name = {self.name}, metadata = {self.metadata}, source_id = {self.source_id})"

    def __set_id(self):
        return uuid.uuid4()

    def get_embedding(self):
        #Return the embedding of the nodes
        pass
    
    #TODO: Substitute func for class that manages the transformation into Nodes. 
    def create_nodes_from_doc(self,model_context, chunk_size = 1024): #TODO: Support adding new full metadata
        nodes = []
        chunked_text = self.__chunk_text(chunk_size)
        existing_metadata = self.metadata
        for i, text in enumerate(chunked_text):
            if i == 0:
                 node_metadata = {**existing_metadata,**{'node_height': 0, 'node_length':1}}
                 nodes.append(TextNode(text = text, metadata = node_metadata, model_context = model_context, doc_id=self.id, source_id=self.source_id))
            else:
                 node_metadata = {**existing_metadata,**{'node_height': 0, 'node_length':1}}
                 node = TextNode(text = text, metadata = node_metadata, model_context = model_context, prev_node =  nodes[i - 1].id, doc_id=self.id, source_id=self.source_id)
                 nodes.append(node)
                 nodes[i - 1].next_node = node.id
        return nodes
        
    def __chunk_text(self, chunk_size = 1024): #Make with other types of text representations like dataframes. Initial version.
        chunked_text = []
        text = self.text
        for i in range(0, len(text), chunk_size):
            chunked_text.append(text[i:chunk_size + i])
        return chunked_text
    
    def copy(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result
    def get_metadata_str(self, mode = None):
        return '\n'.join([DEFAULT_METADATA_TMPL.format(key=key, value=value) for key, value in self.metadata.items()])
    
    def save(self):
        self.store.add(self)

    def delete(self):
        self.store.delete(self)

