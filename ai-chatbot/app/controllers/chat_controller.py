from glob import glob
import os
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
#from langchain.chains import ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import (
	ChatOpenAI,
#	AzureChatOpenAI,
)
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
#from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import (
	CharacterTextSplitter,
	MarkdownTextSplitter,
	TokenTextSplitter,
)

from langchain.document_loaders import (
	DirectoryLoader,
	PyPDFLoader,
	TextLoader,
	UnstructuredMarkdownLoader,
	UnstructuredRTFLoader,
	UnstructuredWordDocumentLoader,
)

from langchain.vectorstores import (
	VectorStore,
	FAISS
)

from langchain.memory import (
	ConversationSummaryMemory,
	ConversationBufferMemory,
	ConversationBufferWindowMemory,
	)
from langchain.chains import ConversationalRetrievalChain
from pydantic import DirectoryPath

#from models.chat_question import ChatQuestion
from schema.chat import LanguageModel
from schema.chat import ChatMemoryModel
from utils.settings import Settings

settings = Settings()

__ai_links = dict()

INDEX_FOLDER = settings.index_folder


class LinkAI(object):
	'UserAi Class'
	IndexFolder: DirectoryPath = INDEX_FOLDER

	def __init__(self, ll_model:LanguageModel = LanguageModel.OpenAI, topic: str = 'default', memory :ChatMemoryModel = ChatMemoryModel.SUMMARY, memory_buffer_size:int = 10 ) -> None:
		self._llm = ll_model
		self._memory_model = memory
		self._topics = os.listdir( self.IndexFolder )
		self._active_topic = topic
		self._memory_buffer_size = memory_buffer_size # only for Buffer Window Memory
		self.reload()



	@property
	def chat_model(self):
		return self._llm
	
	@chat_model.setter
	def chat_model(self, new_llm: LanguageModel):
		self._llm = new_llm

	@property
	def topics(self):
		return self._topics
	
	@property
	def active_topic(self):
		return self._active_topic
	
	@active_topic.setter
	def active_topic(self, new_topic:str):
		self._active_topic = new_topic
	
	def reload(self):
		'''Recarga toda la configuración para la comunicación con la IA'''

		# Carga el LLM correspondiente
		if self._llm == LanguageModel.OpenAI:
			self._llm_r = ChatOpenAI(model_name="gpt-4", temperature=0, openai_api_key=settings.openai_api_key) 
			#self._llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0) 
		elif self._llm == LanguageModel.AzureOpenAI:
			self._llm_r = ChatOpenAI(
				model_name="gpt-4", 
				temperature=0, 
				openai_api_key=settings.openai_api_key) 
		
		folder_path = self.IndexFolder.as_posix() + '/'+ self._active_topic
		print(folder_path)
#		os.system('sleep 2000')
		self._vectorstore = FAISS.load_local(folder_path, OpenAIEmbeddings(chunk_size=512))

		retriever = self._vectorstore.as_retriever(
			search_type="mmr", # Also test "similarity"
    		search_kwargs={"k": 8},)
		
		# Carga el tipo de memoria correspondiente
		
		if self._memory_model == ChatMemoryModel.SUMMARY:
			self._memory = ConversationSummaryMemory(llm=self._llm_r,memory_key="chat_history",return_messages=True)
		elif self._memory_model == ChatMemoryModel.WINDOW:
			self._memory = ConversationBufferWindowMemory( memory_key="chat_history", return_messages=True, k=self._memory_buffer_size )
		elif self._memory_model == ChatMemoryModel.ALL_CHAT:
			self._memory = ConversationBufferMemory( memory_key="chat_history", return_messages=True )
		elif self._memory_model == ChatMemoryModel.NO_MEMORY:
			self._memory = ConversationBufferWindowMemory( memory_key="chat_history", return_messages=True, k=0 )
		self._qa = ConversationalRetrievalChain.from_llm(self._llm_r, retriever=retriever, memory=self._memory)

	def initialize(self):
		'''
		Do all initialization process.
		'''
		pass
		
	def ask_to_ai(self, question: str):	
		'''
		Send a message to AI llm.

		Args: 
			question: message to send
		
		Return:
			Answer returned by AI LLM
		'''

		result = self._qa(question)
		print(result)
		return result


#llm_azure_openai = UserAI( index_folder=INDEX_FOLDER, chat_model = AzureChatOpenAI(model_name="gpt-4", temperature=0))



def update_link_ai( user_id: str, link: LinkAI ):
	__ai_links[user_id] = link
	__ai_links[user_id].reload()


def answer_question( ask: str, user_id: str ):
	return __ai_links[user_id].ask_to_ai(question=ask) 

