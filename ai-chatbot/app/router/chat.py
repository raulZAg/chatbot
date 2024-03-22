from fastapi import APIRouter

from schema.chat import ChatQuestion

import controllers.chat_controller as chat_driver

chat_router = APIRouter( prefix='/v1/chat', tags=['chat'] )

@chat_router.post( "/answer" ) 
def answer( question: ChatQuestion, user_id: str ):
	print( f" Q: {question}" )
	ans = chat_driver.answer_question( 
		ask = question.ask,
		user_id = user_id )
	return ans







