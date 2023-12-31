# Autogenerated by nbdev

d = { 'settings': { 'branch': 'main',
                'doc_baseurl': '/nanorag',
                'doc_host': 'https://antoni0z.github.io',
                'git_url': 'https://github.com/antoni0z/nanorag',
                'lib_path': 'nanorag'},
  'syms': { 'nanorag.base': { 'nanorag.base.BaseNode': ('base.html#basenode', 'nanorag/base.py'),
                              'nanorag.base.BaseNode.__init__': ('base.html#basenode.__init__', 'nanorag/base.py'),
                              'nanorag.base.BaseNode.__repr__': ('base.html#basenode.__repr__', 'nanorag/base.py'),
                              'nanorag.base.BaseNode.__set_id': ('base.html#basenode.__set_id', 'nanorag/base.py'),
                              'nanorag.base.BaseNode.create_embedding': ('base.html#basenode.create_embedding', 'nanorag/base.py'),
                              'nanorag.base.BaseNode.get_embedding': ('base.html#basenode.get_embedding', 'nanorag/base.py'),
                              'nanorag.base.Document': ('base.html#document', 'nanorag/base.py'),
                              'nanorag.base.Document.__calculate_hash': ('base.html#document.__calculate_hash', 'nanorag/base.py'),
                              'nanorag.base.Document.__call__': ('base.html#document.__call__', 'nanorag/base.py'),
                              'nanorag.base.Document.__chunk_text': ('base.html#document.__chunk_text', 'nanorag/base.py'),
                              'nanorag.base.Document.__init__': ('base.html#document.__init__', 'nanorag/base.py'),
                              'nanorag.base.Document.__repr__': ('base.html#document.__repr__', 'nanorag/base.py'),
                              'nanorag.base.Document.__set_id': ('base.html#document.__set_id', 'nanorag/base.py'),
                              'nanorag.base.Document.create_nodes_from_doc': ( 'base.html#document.create_nodes_from_doc',
                                                                               'nanorag/base.py'),
                              'nanorag.base.Document.get_embedding': ('base.html#document.get_embedding', 'nanorag/base.py'),
                              'nanorag.base.TextNode': ('base.html#textnode', 'nanorag/base.py'),
                              'nanorag.base.TextNode.__calculate_hash': ('base.html#textnode.__calculate_hash', 'nanorag/base.py'),
                              'nanorag.base.TextNode.__init__': ('base.html#textnode.__init__', 'nanorag/base.py'),
                              'nanorag.base.TextNode.__repr__': ('base.html#textnode.__repr__', 'nanorag/base.py'),
                              'nanorag.base.TextNode.create_embedding': ('base.html#textnode.create_embedding', 'nanorag/base.py'),
                              'nanorag.base.TextNode.get_embedding': ('base.html#textnode.get_embedding', 'nanorag/base.py')},
            'nanorag.context': { 'nanorag.context.ModelContext': ('context.html#modelcontext', 'nanorag/context.py'),
                                 'nanorag.context.ModelContext.__init__': ('context.html#modelcontext.__init__', 'nanorag/context.py'),
                                 'nanorag.context.ModelContext.set_default': ( 'context.html#modelcontext.set_default',
                                                                               'nanorag/context.py')},
            'nanorag.llm': { 'nanorag.llm.LLM': ('llm.html#llm', 'nanorag/llm.py'),
                             'nanorag.llm.LLM.__call__': ('llm.html#llm.__call__', 'nanorag/llm.py'),
                             'nanorag.llm.LLM.__init__': ('llm.html#llm.__init__', 'nanorag/llm.py'),
                             'nanorag.llm.PromptTemplate': ('llm.html#prompttemplate', 'nanorag/llm.py'),
                             'nanorag.llm.PromptTemplate.__call__': ('llm.html#prompttemplate.__call__', 'nanorag/llm.py'),
                             'nanorag.llm.PromptTemplate.__init__': ('llm.html#prompttemplate.__init__', 'nanorag/llm.py')},
            'nanorag.loaders': { 'nanorag.loaders.DocumentBridge': ('loaders.html#documentbridge', 'nanorag/loaders.py'),
                                 'nanorag.loaders.DocumentBridge.__init__': ('loaders.html#documentbridge.__init__', 'nanorag/loaders.py'),
                                 'nanorag.loaders.DocumentBridge.to_doc': ('loaders.html#documentbridge.to_doc', 'nanorag/loaders.py'),
                                 'nanorag.loaders.DocumentBridge.to_nodes': ('loaders.html#documentbridge.to_nodes', 'nanorag/loaders.py'),
                                 'nanorag.loaders.DocumentBridge.to_subdocuments': ( 'loaders.html#documentbridge.to_subdocuments',
                                                                                     'nanorag/loaders.py'),
                                 'nanorag.loaders.PDFLoader': ('loaders.html#pdfloader', 'nanorag/loaders.py'),
                                 'nanorag.loaders.PDFLoader.__generate_id': ('loaders.html#pdfloader.__generate_id', 'nanorag/loaders.py'),
                                 'nanorag.loaders.PDFLoader.__init__': ('loaders.html#pdfloader.__init__', 'nanorag/loaders.py'),
                                 'nanorag.loaders.PDFLoader.get_documents': ('loaders.html#pdfloader.get_documents', 'nanorag/loaders.py'),
                                 'nanorag.loaders.PDFLoader.get_images': ('loaders.html#pdfloader.get_images', 'nanorag/loaders.py'),
                                 'nanorag.loaders.PDFLoader.load_pdf': ('loaders.html#pdfloader.load_pdf', 'nanorag/loaders.py'),
                                 'nanorag.loaders.PDFLoader.load_random_pdf': ( 'loaders.html#pdfloader.load_random_pdf',
                                                                                'nanorag/loaders.py'),
                                 'nanorag.loaders.PDFLoader.pdf_validator': ('loaders.html#pdfloader.pdf_validator', 'nanorag/loaders.py')},
            'nanorag.store': { 'nanorag.store.BaseDocumentStore': ('store.html#basedocumentstore', 'nanorag/store.py'),
                               'nanorag.store.BaseDocumentStore.__call__': ('store.html#basedocumentstore.__call__', 'nanorag/store.py'),
                               'nanorag.store.BaseDocumentStore.__init__': ('store.html#basedocumentstore.__init__', 'nanorag/store.py'),
                               'nanorag.store.BaseDocumentStore.add': ('store.html#basedocumentstore.add', 'nanorag/store.py'),
                               'nanorag.store.BaseDocumentStore.delete': ('store.html#basedocumentstore.delete', 'nanorag/store.py'),
                               'nanorag.store.BaseDocumentStore.get': ('store.html#basedocumentstore.get', 'nanorag/store.py'),
                               'nanorag.store.BaseDocumentStore.ids': ('store.html#basedocumentstore.ids', 'nanorag/store.py'),
                               'nanorag.store.DocumentStore': ('store.html#documentstore', 'nanorag/store.py'),
                               'nanorag.store.DocumentStore.__call__': ('store.html#documentstore.__call__', 'nanorag/store.py'),
                               'nanorag.store.DocumentStore.__init__': ('store.html#documentstore.__init__', 'nanorag/store.py'),
                               'nanorag.store.DocumentStore.add': ('store.html#documentstore.add', 'nanorag/store.py'),
                               'nanorag.store.DocumentStore.delete': ('store.html#documentstore.delete', 'nanorag/store.py'),
                               'nanorag.store.DocumentStore.get': ('store.html#documentstore.get', 'nanorag/store.py'),
                               'nanorag.store.DocumentStore.group_by_source_id': ( 'store.html#documentstore.group_by_source_id',
                                                                                   'nanorag/store.py'),
                               'nanorag.store.DocumentStore.ids': ('store.html#documentstore.ids', 'nanorag/store.py')},
            'nanorag.utils': {'nanorag.utils.hash_input': ('utils.html#hash_input', 'nanorag/utils.py')}}}
