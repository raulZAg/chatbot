
#import controllers.data_source as data_sources
from controllers import data_source
from dotenv import load_dotenv
import os
load_dotenv()

DOCS_FOLDER = os.getenv( 'DATASOURCE_FOLDER' )
INDEX_FOLDER = os.getenv('INDEX_FOLDER')

Topics = data_source.gen_datasource_from_folder(docs_folder=DOCS_FOLDER)

for t in Topics:
	t.update_vector_store()
	print(t.name)
	t.save_vector_store( folder=INDEX_FOLDER )
