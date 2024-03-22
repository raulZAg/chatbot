import requests

from schema.chat import ChatQuestion
#from ..models.chat_question import ChatQues	tion
from schema.chat import LenguajeModel

q = ChatQuestion()
q.llm = LenguajeModel.OpenAI.name, 
q.data_source = 'Clients'
q.ask = 'Quien es Jose Guerra?'

print(q.json())
params = {
	'llm': "OpenAI",
	"data_source": q.data_source,
	'ask': q.ask,
}

print(params)
ret = requests.post( "http://127.0.0.1:8000/v1/chat/answer",json=params )
print('-------------')
print(ret)
print('-------------')

print(ret.text)
