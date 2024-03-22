
from controllers.data_source import load_datasource
from utils.settings import Settings

settings = Settings()

__topics = load_datasource( settings.index_folder.as_posix() )

d = dict()

for t in __topics:
	d.update( { t.name : t } )

Topics = d