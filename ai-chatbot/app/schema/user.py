from pydantic import BaseModel
from enum import Enum

from schema.chat import (
	LanguageModel,
	ChatMemoryModel
)

class UserSettings(BaseModel):
	data_source: str = 'default'
	llm: LanguageModel = LanguageModel.OpenAI
	chat_memory_model: ChatMemoryModel = ChatMemoryModel.SUMMARY
	memory_buffer_size: int = 10


class User(BaseModel):
	user_id: str
	user_name: str = ''
	name: str = ''
	lastname: str = ''
	password_hash: str = ''
	settings: UserSettings = UserSettings()
	

	


