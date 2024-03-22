from schema.user import UserSettings
from schema.user import User
from controllers.chat_controller import LinkAI
from controllers.chat_controller import update_link_ai

__users = dict()


def _check_user(user_id: str):
	if user_id not in __users:
		usr = User(user_id=user_id)
		__users[user_id] = usr
		update_link_ai( 
			user_id = user_id, 
			link = LinkAI( 
				ll_model=usr.settings.llm,
				topic=usr.settings.data_source,
				memory=usr.settings.chat_memory_model ) )
		

def user_get( user_id: str ) -> User:
	_check_user(user_id=user_id)
	return __users[user_id]

def user_settings_get( user_id: str ) -> UserSettings:
	_check_user(user_id=user_id)
	
	return __users[user_id].settings

def user_settings_set( user_id: str, sett: UserSettings ) -> None:
	_check_user(user_id=user_id)	
	__users[user_id].settings = sett
	usr = __users[user_id]

	update_link_ai( 
		user_id = user_id, 
		link = LinkAI( 
			ll_model=usr.settings.llm,
			topic=usr.settings.data_source,
			memory=usr.settings.chat_memory_model,
			memory_buffer_size=usr.settings.memory_buffer_size
			)
	)

