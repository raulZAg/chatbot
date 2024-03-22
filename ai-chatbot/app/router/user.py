from fastapi import APIRouter

from schema.user import UserSettings
from controllers import user

user_router = APIRouter( prefix='/v1/user', tags=['user'] )

@user_router.post( "/{user_id}/settings/set" ) 
def settings_set( user_id: str, user_settings: UserSettings ):
	print(f'{user_id}: {user_settings.data_source}')
	user.user_settings_set( user_id, user_settings )
	return user.user_settings_get(user_id)

@user_router.get( '/{user_id}/settings/get' )
def settings_get( user_id ):
	return user.user_settings_get( user_id )





