from fastapi import APIRouter

from controllers.topic import Topics


topics_router = APIRouter( prefix='/v1/topic', tags=['chat'] )


@topics_router.get('/list')
async def get_topics_name():
	return {
		'topics': list(Topics.keys())
	}

@topics_router.get('/state')
def get_topics_state():
	'''
	Retorna el estado de todos los topics desde la base de datos
	'''
	return {
		'Topic1':{
			'state': 'Indexed', 	# No indexed, Indexed, Indexing
			'last_update': 'Date' 	#
		},
		'Topic2':{
			'state': 'Indexing', 	# No indexed, Indexed, Indexing
			'last_update': 'Date' 	#
		},
		'Topic2':{
			'state': 'No indexed', 	# No indexed, Indexed, Indexing
			'last_update': 'Date' 	#
		},
	}

@topics_router.get('/state/{topic}')
def get_topic_state( topic: str ):
	'''
	Retorna el estado de un topic desde la base de datos
	'''

	return {
		'Topic1':{
			'state': 'Indexed', 	# No indexed, Indexed, Indexing
			'last_update': 'Date' 	#
		},
	}


@topics_router.post('/update')
async def update_topics():
	'Actualiza los vectorstore de cada topic'

	pass