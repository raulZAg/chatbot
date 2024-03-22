from glob import glob
import os
from pydantic import (
	DirectoryPath,
	FilePath,
)

from langchain.embeddings import (
	OpenAIEmbeddings
)
from langchain.embeddings.base import Embeddings

from langchain.document_loaders import (
	DirectoryLoader,
	PyPDFLoader,
	TextLoader,
	UnstructuredMarkdownLoader,
	UnstructuredRTFLoader,
	UnstructuredWordDocumentLoader,
	GoogleDriveLoader,
	CSVLoader
)


from langchain.text_splitter import (
	CharacterTextSplitter
)

from langchain.vectorstores import FAISS 


class DataSource(object):
	'''
	Base class for data sources (Topics)
	'''

	EXTENSION_TO_LOADER = {
		'*.pdf': PyPDFLoader,
		'*.txt': TextLoader,
		'*.md' : UnstructuredMarkdownLoader,
		'*.rtf': UnstructuredRTFLoader,
		'*.doc': UnstructuredWordDocumentLoader,
		'*.csv': CSVLoader
	}


	def __init__(self, name:str, embedding: Embeddings, extensions: "list[str]" ) -> None:
		self._name = name
		self._embedding = embedding
		self._extensions = extensions
		self._vector_store = None

	@property
	def name(self):
		return self._name
	
	@name.setter
	def name(self, new_name):
		self._name = new_name

	@property
	def extensions(self):
		return self._extensions
	
	@extensions.setter
	def extensions(self, new_ext: "list[str]"):
		self._extensions = new_ext

	@property
	def vector_store(self):
		return self._vector_store

	def update_vector_store(self, verbose:bool = True):
		print('Base implementation')
		pass

	def save_vector_store(self, folder: DirectoryPath):
		print('Base implementation')
		pass


class LocalDataSource(DataSource):

	def __init__(self, name: str, embedding: Embeddings, folder: DirectoryPath, extensions: "list[str]" ) -> None:
		super().__init__(name, embedding, extensions)
		self._folder = folder


	@property
	def folder(self):
		return self._folder

	@folder.setter
	def folder(self, new_folder: DirectoryPath):
		self._folder = new_folder
	
	def update_vector_store(self, verbose: bool = True):
		'''
		Build a vector store with documents in "folder".
		First split docs in chucks
		Then use "embedding" and "VectorStoreGen" for create the vector store.
		'''
		splitted_documents = []
		if verbose:
			print(f'Updating {self.name} from {self.folder}',)
		for ext in self._extensions:
			
			if verbose:
				print(f'\t Loading {ext} files')
			loader = DirectoryLoader(
    			self._folder, glob="**/"+ext, loader_cls=DataSource.EXTENSION_TO_LOADER[ext]
			)

			splitter = CharacterTextSplitter(
				separator="\n\n", chunk_size=400, chunk_overlap=100, length_function=len
			)
			#text_splitter = TokenTextSplitter(chunk_size=400, chunk_overlap=50)
			splitted_documents.extend(loader.load_and_split(splitter))
			
		if len(splitted_documents) > 0:
			self._vector_store = FAISS.from_documents( splitted_documents,  embedding=self._embedding(chunk_size=512) )
			if verbose:
				print(f'\t Vector generated for {self.name}')

	def save_vector_store(self, folder: DirectoryPath):
		self._vector_store.save_local( folder + '/' + self._name )
	
	def load_vector_store( self, folder: DirectoryPath ):
		self._vector_store = FAISS.load_local(folder + '/' + self._name, self._embedding(chunk_size=512))


class GoogleDataSource(DataSource):
	def __init__(self, name: str, embedding: Embeddings, folder_link: str, extensions: "list[str]" = ["document", "sheet", "pdf"]) -> None:
		super().__init__(name, embedding, extensions)
		self._folder_id = self._link2folder_id(folder_link)

	
	def _link2folder_id(self, link: str):
		''' Extract the 'folder id' form 'folder link' '''
		return link.split('/')[-1]
	
	def update_vector_store(self):
		loader = GoogleDriveLoader(
    		folder_id=self._folder_id,
    		# Optional: configure whether to recursively fetch files from subfolders. Defaults to False.
    		recursive=True,
		)
		splitter = CharacterTextSplitter(
			separator="\n\n", chunk_size=400, chunk_overlap=100, length_function=len
		)
		#text_splitter = TokenTextSplitter(chunk_size=400, chunk_overlap=50)
		splitted_documents = loader.load_and_split(splitter)

		if len(splitted_documents) > 0:
			self._vector_store = FAISS.from_documents( splitted_documents,  embedding=self._embedding(chunk_size=512) )


#class MicrosoftSharePointDataSource(DataSource):
#	def __init__(self, name: str, embedding: Embeddings, extensions: "list[str]") -> None:
#		super().__init__(name, embedding, extensions)

def gen_datasource_from_folder(docs_folder:str) -> "list[DataSource]":
	directories = os.listdir( docs_folder )

	Topics = [LocalDataSource( 
					name=d, 
					folder=docs_folder + d, 
					extensions=[ "*.pdf","*.txt", "*.md", "*.rtf" ], 
					embedding=OpenAIEmbeddings ) for d in directories ]

	for i in range(len(Topics)):
		Topics[i].update_vector_store()
		print( f"topic({i}): {Topics[i].name}" )

	return Topics

def load_datasource(index_folder:str,docs_folder:str='') -> "list[DataSource]":
	directories = os.listdir( index_folder )
	Topics = [LocalDataSource( 
					name=d, 
					folder=docs_folder + d, 
					extensions=[ "*.pdf","*.txt", "*.md", "*.rtf" ], 
					embedding=OpenAIEmbeddings ) for d in directories ]

	for i in range(len(Topics)):
		Topics[i].load_vector_store(index_folder)
		print( f"topic({i}): {Topics[i].name}" )
	
	return Topics
