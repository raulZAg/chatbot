import flet as ft
import time
from dotenv import load_dotenv
import os
import requests
import sys
import asyncio

import view.chat as chat
from view.chat import Chat
from view.settings import SettingsWindows
from view.settings import ChatMemoryModel

from utils.settings import GuiSettings

from router.chat import answer as chat_answer
from schema.chat import ChatQuestion


load_dotenv()

print(os.environ)

gui_settings = GuiSettings()
BACKEND_API = gui_settings.backend_api
#DOCS_FOLDER = './uploads/'
#INDEX_FOLDER = './vector_store_index'


async def main_test(page: ft.Page):
	page.title = 'Bot Assistant test'

	async def submit_action( own: Chat, box: ft.TextField, btn: ft.IconButton, history: ft.ListView ):
		"""
		Callback to perform on Send Message action.

		Args:
			own: reference to Chat object.
			box: reference to TextField with the message.
			btn: reference to send button.
			history: reference to chat history.

		Returns:
			None

		"""

		if box.value == '':
			return
		question = box.value
		box.value = ''

#		if settings_windows.select_memory.current.value == ChatMemoryType.WINDOW.value:
#			page.chat_history = own.get_chat_history(settings_windows.memory_window.value)
		
		history.controls.append( chat.ChatMessage(chat.Message( 'Yo', question, chat.MessageSenderType.HUMAN ) ) )
		await box.update_async()
		history.controls.append( chat.ChatMessage(chat.Message( 'IA', 'Thinking...', chat.MessageSenderType.AI ) ) )    
		index = len(history.controls) -1
		await history.update_async()

		json_params = {
			'ask' : question,
		}
		params = {
			'user_id': page.session_id
		}

#		print(params)
#		print('------------------')
		ret = await requests.post( BACKEND_API + '/chat/answer', json=json_params, params=params )

		ret = ret.json()
		answer = ret['answer']
		page.chat_history = ret['chat_history']

		history.controls[index] = chat.ChatMessage(chat.Message( 'IA', answer, chat.MessageSenderType.AI ) )
#		history.controls.append(  )
		await box.focus_async()
		await own.update_async()

	chat_space = Chat(on_submit=submit_action)
	
	settings_windows = SettingsWindows( )
	
	async def on_save(e):
		await settings_windows.apply_new_settings(page.session_id)
		settings.open = False
		await chat_space.clean_history()

		await settings.update_async()
		await chat_space.update_async()

	settings = ft.BottomSheet(

		ft.Container(
			content = ft.Column(
				controls=[
					ft.Divider(thickness=0,opacity=0),
					settings_windows,
					ft.ElevatedButton(
						text = "Save",
						disabled = False,
						on_click = on_save,
					),
				],
				alignment=ft.MainAxisAlignment.START,
				horizontal_alignment=ft.CrossAxisAlignment.END,
        	),
			padding=10,
		),
        open=False,

	)


	page.overlay.append(settings)

	await page.add_async(
		ft.Row(
			[
				ft.Column([ chat_space], alignment=ft.MainAxisAlignment.START, expand=True),			
			],
			expand=True
		)
	)

	await settings_windows.apply_new_settings(page.session_id)

	await page.update_async()



async def main(page: ft.Page):
	page.title = 'Bot Assistant'


	#page.theme = ft.Theme( color_scheme_seed=ft.colors.BLUE_500 ),
	#ai_link =add_async UserAI( index_folder=INDEX_FOLDER, chat_model = ChatOpenAI(model_name="gpt-4", temperature=0))


	async def submit_action( own: Chat, box: ft.TextField, btn: ft.IconButton, history: ft.ListView ):
		"""
		Callback to perform on Send Message action.

		Args:
			own: reference to Chat object.
			box: reference to TextField with the message.
			btn: reference to send button.
			history: reference to chat history.

		Returns:
			None

		"""

		if box.value == '':
			return 
		question = box.value
		box.value = ''

#		if settings_windows.select_memory.current.value == ChatMemoryType.WINDOW.value:
#			page.chat_history = own.get_chat_history(settings_windows.memory_window.value)
		
		history.controls.append( chat.ChatMessage(chat.Message( 'Yo', question, chat.MessageSenderType.HUMAN ) ) )
		await box.update_async()
		history.controls.append( chat.ChatMessage(chat.Message( 'IA', 'Thinking...', chat.MessageSenderType.AI ) ) )    
		index = len(history.controls) -1
		await history.update_async()
		await asyncio.sleep(1)

#		print(params)
#		print('------------------')
		ret = chat_answer( ChatQuestion( ask=question ), user_id=page.session_id )
#		ret = await requests.post( BACKEND_API + '/chat/answer', json=json_params, params=params )

		#ret = ret.json()
		answer = ret['answer']
		page.chat_history = ret['chat_history']

		history.controls[index] = chat.ChatMessage(chat.Message( 'IA', answer, chat.MessageSenderType.AI ) )
#		history.controls.append(  )
		await box.focus_async()
		await own.update_async()

	chat_space = Chat(on_submit=submit_action)
	
	settings_windows = SettingsWindows( )

	async def on_save(e):
		await settings_windows.apply_new_settings(page.session_id)
		settings.open = False
		await chat_space.clean_history()

		await settings.update_async()
		await chat_space.update_async()

	settings = ft.BottomSheet(

		ft.Container(
			content = ft.Column(
				controls=[
					ft.Divider(thickness=0,opacity=0),
					settings_windows,
					ft.ElevatedButton(
						text = "Save",
						disabled = False,
						on_click = on_save,
					),
				],
				alignment=ft.MainAxisAlignment.START,
				horizontal_alignment=ft.CrossAxisAlignment.END,
        	),
			padding=10,
		),
        open=True,
		
#        on_dismiss=bs_dismissed,
	)

	async def show_settings(e):
		settings.open = True
		await settings.update_async()

	page.appbar = ft.AppBar(
		leading=ft.Icon(ft.icons.EMOJI_OBJECTS_SHARP),
		leading_width=40,
		color=ft.colors.BLUE,
		elevation=10,
		title=ft.Text(page.title),
		center_title=False,
		actions=[
			ft.IconButton(
				ft.icons.PLAYLIST_REMOVE, 
				on_click=lambda _: chat_space.clean_history()
			),
			ft.IconButton(
				ft.icons.SETTINGS, 
				on_click=show_settings
			),
		]
	)

	page.overlay.append(settings)
	await page.add_async(
		ft.Row(
			[
				ft.Column([ chat_space], alignment=ft.MainAxisAlignment.START, expand=True),			
			],
			expand=True
		)
	)

	await settings_windows.apply_new_settings(page.session_id)

	await page.update_async()


#if __name__ == '__main__':
#	ft.app(target=main, view=None, port=5555, assets_dir='assets')
	#ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=5555, assets_dir='assets')

