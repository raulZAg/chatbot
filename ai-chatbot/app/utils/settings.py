import os

from pydantic_settings import BaseSettings
from pydantic import DirectoryPath
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
	index_folder: DirectoryPath = os.getenv('INDEX_FOLDER')
	local_datasources_folder: DirectoryPath = os.getenv( 'DATASOURCE_FOLDER' )
	openai_api_key:str = os.getenv('OPENAI_API_KEY')


class GuiSettings(BaseSettings):
	backend_address:str = os.getenv( 'BACKEND_ADDRESS', 'http://localhost' )
	backend_port:int = os.getenv('BACKEND_PORT', 8000)
	backend_api:str = backend_address+':' + str(backend_port) + '/v1'

