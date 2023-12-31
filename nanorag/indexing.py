# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/06_indexing.ipynb.

# %% auto 0
__all__ = ['context', 'store', 'VectorIndex']

# %% ../nbs/06_indexing.ipynb 2
from .base import *
from .store import *
from .context import *
from .llm import *
from .loaders import *
from typing import Union, List, Dict, Tuple, Optional, Any
import numpy as np

# %% ../nbs/06_indexing.ipynb 3
#| eval: false
context = ModelContext()
context.set_default()
store = DocumentStore()

# %% ../nbs/06_indexing.ipynb 6
class VectorIndex: #Compatible with TextNode right now
    def __init__(self, context): #May not be needed in postgres. 
        self.node_to_idx = {}
        self.idx_to_node = {}
        self.idx = np.array([], dtype=np.int64)
        self.context = context
        #This line below accepts huggingface embeddings format. 
        self.embedding_dim = self.context.embedding[1].word_embedding_dimension
        if self.embedding_dim is not None:
            self.embeddings = np.empty((0, self.embedding_dim))
        else:
            self.embeddings = np.array([])

    def add(self, nodes: Union[TextNode, List[TextNode]]):
        if isinstance(nodes, TextNode):
            nodes = [nodes]
        elif isinstance(nodes, list):
            new_embeddings = np.vstack([node.embedding for node in nodes])
            if self.embeddings.size == 0:
                self.embeddings = new_embeddings
            else:
                self.embeddings = np.append(self.embeddings, new_embeddings, axis=0)
            node_idx = np.arange(len(self.idx), self.embeddings.shape[0])
            for node, idx in zip(nodes, node_idx):
                self.node_to_idx[node.id] = idx
                self.idx_to_node[idx] = node.id
                node.idx = idx
            self.idx = np.concatenate((self.idx, node_idx))

    def get_embedding(self, ids: Union[List[int], int]):
        if isinstance(ids, np.int64) or isinstance(ids, int):
            ids = np.array([ids], dtype = np.int64)
        if isinstance(ids, list):
            ids = np.array(ids)
        if isinstance(ids, np.ndarray):
            return self.embeddings[ids]

#TODO: Integration with the DocumentBridge and Document Object. 
#TODO: Try querying the Index with some text converted to embeddings.
