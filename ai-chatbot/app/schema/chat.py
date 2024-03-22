from pydantic import BaseModel
from enum import Enum

class LanguageModel(str, Enum):
	OpenAI = "OpenAI"
	AzureOpenAI = "AzureOpenAI"
	Llama2 = "Llama2"

class ChatMemoryModel(str, Enum):
	SUMMARY = 'Summary',
	ALL_CHAT = 'All chat',
	WINDOW = 'Window',
	NO_MEMORY = 'No memory'


class ChatQuestion(BaseModel):
	ask: str = 'tellme'
	