import math
from glob import glob
from .cleaner import clean
import os
from .documents import Document

class Index:
    '''
        inverted index class : 

        attributes : 
            1. index 
            2. documents ( aka IDs )
            3. index_path_indx - to store positions where tokens occur in a document

        methods : 
            1. buildIndex : indexes all the files in the folder
            1. search : does boolean search
            2. update : updates a document in index
            3. delete : deletes a document in index
            4. phase_search : searches a phase in index 
    '''
    def __init__(self):
        self.index = {}            # inverted index
        self.documents = {}        # stores actual document to be retrieved using document's path ( i.e. document's ID )
        self.index_path_indx = {}  # used to store positions for phase search
    
    def buildIndex(self,path='data'):
        '''
            build the inverted index for files in folder path
        '''
        self.add_folder(path)
    
    def index_document(self,document):
        '''
            will index the document
            self.document stores the actual document using document.path as key/id
        '''
        self.documents[document.path] = document

        for ind,token in enumerate(clean(document.text)):
            # for boolean search , standard index formulation for index
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(document.path)

            # for phase search , store the positon of this token in the document
            if token not in self.index_path_indx:
                self.index_path_indx[token] = {document.path : set()}
            if document.path not in self.index_path_indx[token]:
                self.index_path_indx[token][document.path]= set()                    
            self.index_path_indx[token][document.path].add(ind)
                

    def document_frequency(self, token):
        '''
            return TF of token
        '''
        return len(self.index.get(token, set()))

    def inverse_document_frequency(self, token):
        '''
            return IDF of token
        '''
        return math.log10(len(self.documents) / self.document_frequency(token))

    def result(self, cleaned_query):
        return [self.index.get(token, set()) for token in cleaned_query]
        
    def search(self, query, search_type='AND', rank=False):
        """
        Search; this will return documents that contain words from the query,
        and rank them if requested (sets are fast, but unordered).

        Parameters:
          - query: the query string
          - search_type: ('AND', 'OR','Not')
          - search_type AND : all terms needed
          - search_type OR  : any term needed
          - search_type NOT : all files exluding the terms in query
          - score: (True, False) if True, rank results based on TF-IDF score
        """
        if search_type not in ('AND', 'OR' , 'NOT'):
            return []

        cleaned_query = clean(query)
        results = self.result(cleaned_query)
        
        if search_type == 'AND':
            # all tokens must be in the document
            documents = [self.documents[path] for path in set.intersection(*results)]
        if search_type == 'OR':
            # only one token has to be in the document
            documents = [self.documents[path] for path in set.union(*results)]
        if search_type == 'NOT':
            documents = [self.documents[path] for path in self.documents.keys() if path not in set.union(*results)]
        if rank:
            return self.rank(cleaned_query, documents)
        return documents

    def rank(self, cleaned_query, documents):
        '''
            rank the results using TF-IDF
        '''
        results = []
        if not documents:
            return results
        for document in documents:
            score = 0.0
            for token in cleaned_query:
                tf = document.term_frequency(token)
                idf = self.inverse_document_frequency(token)
                score += tf * idf
            results.append((document, score))
        return sorted(results, key=lambda doc: doc[1], reverse=True)



    def add_folder(self, path):
        '''
            add a new folder from path
        '''
        files_in_folder = glob(os.path.join(path, "*.txt"))
        for txtfile in files_in_folder:
            try:
                with open(txtfile, 'r') as f:
                    txt = f.read()
                    self.index_document(Document(path=txtfile, text=txt)) # index this document obj
            except FileNotFoundError:
                print(f"The file '{txtfile}' was not found.")
            except Exception as e:
                print(f"error happened while adding folder'{txtfile}':", e)

    def add_document(self,path):
        '''
            add a new document to the index
        '''
        try:
            doc_path = os.path.normpath(path)
            with open(doc_path, 'r') as f:
                txt = f.read()
                self.index_document(Document(path=doc_path, text=txt))
        except FileNotFoundError:
            print(f"The file '{doc_path}' was not found while updating.")
        except Exception as e:
            print(f"error happened while updating'{doc_path}':", e)

    def update_document(self, full_file_path):
        '''
            update a document to the index
        '''
        file_path = os.path.normpath(full_file_path)
        if file_path in self.documents.keys():
            self.delete_document(full_file_path)  #1st remove it from index
        try:
            with open(file_path, 'r') as f:
                txt = f.read()
                self.index_document(Document(path=file_path, text=txt)) # now add it to index
        except FileNotFoundError:
            print(f"The file '{file_path}' was not found.")
        except Exception as e:
            print(f"error happened while updating'{file_path}':", e)

    def delete_document(self, full_file_path):
        '''
            delete a document from the index
        '''
        doc_path = os.path.normpath(full_file_path)
        if doc_path in self.documents.keys():
            self.documents.pop(doc_path)
            for token, doc_set in self.index.items():
                if doc_path in doc_set:
                    doc_set.remove(doc_path)
            for token , doc_dict in self.index_path_indx.items():
                if doc_path in doc_dict.keys():
                    self.index_path_indx[token].pop(doc_path)
        else:
            print(f"The file '{doc_path}' was not found. for deleting")


    def phrase_search(self, text): 
        '''
            phrase search for query text
        '''
        cleaned_query = clean(text)
        positions = []
        first_token = cleaned_query[0]
        if first_token in self.index:
            positions = self.index[first_token]
            positions = [(_path,self.index_path_indx[first_token][_path]) for _path in positions] #contains file path & possible indexes
        
        # Find positions for subsequent tokens and ensure they are adjacent
        for i in range(1, len(cleaned_query)):
            token = cleaned_query[i]
            if token in self.index:
                new_positions = []
                for doc_path in self.index[token]:
                    pos_set = self.index_path_indx[token][doc_path]
                    for prev_doc_path, prev_pos_set in positions:
                        if doc_path == prev_doc_path :
                            possible_position = set()
                            for x in pos_set:
                                if x-1 in prev_pos_set:#this will ensure adjacency
                                    possible_position.add(x)
                            if len(possible_position)>=1:
                                new_positions.append((doc_path,possible_position))
                positions = new_positions
        return [self.documents[doc_id] for doc_id, _ in positions]

 
