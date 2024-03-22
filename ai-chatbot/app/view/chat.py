from typing import Any, List, Optional, Union
import asyncio
import flet as ft
from flet import (
	Row,
	Column
)
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, CrossAxisAlignment, MainAxisAlignment, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue, ScrollMode
from enum import Enum

class MessageSenderType(str, Enum):
	HUMAN = 'Human',
	AI = 'AI'

class Message():
	def __init__(self, user: str, sms: str, sender: MessageSenderType) -> None:
		self.user = user
		self.sms = sms
		self.type = sender
	

class ChatMessage(Row):
	def __init__(self, message: Message):
		super().__init__(self)
		self.vertical_alignment = CrossAxisAlignment.START
		self.message = message

		self.text = ft.TextField(
			value=message.sms, 
			multiline=True, 
			expand=True, 
			read_only=True,
			border_width=0,
			border_radius=ft.border_radius.all( 20 ),
			)
		
		if message.type == MessageSenderType.AI:
			self.alignment = MainAxisAlignment.START
			
			self.text.bgcolor=ft.colors.GREY_300
			self.text.text_style=ft.TextStyle(color=ft.colors.BLACK )
			self.text.border_radius.top_left = 0

			self.controls = [
				ft.CircleAvatar(
					bgcolor=ft.colors.GREEN,
					content=ft.Icon(name=ft.icons.FACE_ROUNDED)
				),
				self.text
			]

		elif message.type == MessageSenderType.HUMAN:
			self.alignment = MainAxisAlignment.END

			self.text.bgcolor=ft.colors.BLUE_300
			self.text.text_style=ft.TextStyle(color=ft.colors.WHITE )
			self.text.border_radius.top_right = 0
			
			self.controls = [
				self.text,
				ft.CircleAvatar(
					bgcolor=ft.colors.BLUE_200,
					content=ft.Icon(name=ft.icons.PERSON_ROUNDED)
				),
			]

class Chat(ft.UserControl):
	def __init__(self, on_submit):
		super().__init__(self)
		self.expand = True
		self.on_submit_message = on_submit
	
	async def clean_history(self):
		await self.history.clean_async()
		await self.update_async()
	
	def get_chat_history(self, n: int) -> list:
		ans = []
		start = max(0, len(self.history.controls)-n )
		end = len(self.history.controls)
		
		for i in range( start, end ):
			m = self.history.controls[i]
			ans.append( ( m.message.type.value, m.message.sms) )

		return ans


	def build(self):

		async def submit_cb(e: ft.Control):
			await self.on_submit_message( self, self.inputbox.new_message, self.inputbox.btn, self.history )

		self.history = ft.ListView(
					expand=True,
					auto_scroll=True,
					spacing=10,
					padding=20,
				)
		self.expand = True
		self.inputbox = InputBox( submit_func=submit_cb )

		return ft.Column(
				controls=[
					ft.Container(
						#border=ft.border.all(2, ft.colors.OUTLINE),
						border_radius = ft.border_radius.all( 10 ),
						expand=True,
						content=self.history
					),
					self.inputbox,
				]
			)
		


class InputBox( ft.UserControl ):
	def __init__(self, submit_func):
		super().__init__(self)
		#self.expand = True
		self.on_submit = submit_func


	def build(self):
		async def btn_onclick(e:ft.ControlEvent):
			e.control = self.new_message
			await self.on_submit(e)

		self.btn = ft.IconButton( 
			ft.icons.SEND_ROUNDED, 
			on_click=btn_onclick, 
			disabled=True,
			icon_color=ft.colors.BLUE_700,
		)
		
		async def update_btn(e: ft.Control):
			if len(self.new_message.value) > 0:
				self.btn.disabled = False
				self.btn.icon_color = ft.colors.BLUE_700
			else:
				self.btn.disabled = True
				self.btn.icon_color = ft.colors.GREY_300
			await self.update_async()


		self.new_message = ft.TextField( 
			border_width=0,
#			label='Message: ', 
			hint_text="Write a message...",
        	autofocus=True,
        	shift_enter=True,
        	min_lines=1,
        	max_lines=5,
        	expand=True,
			on_submit=self.on_submit,
			on_change = update_btn, 
			on_focus = update_btn,
		)

		return ft.Container(
			border=ft.border.all(1, ft.colors.OUTLINE),
			border_radius=ft.border_radius.all( 15 ),
			content = ft.Row(
			#expand=True,
			controls=[
				self.new_message,
				self.btn
			]),

		)

#
#
#def main( page: ft.Page):
#
#	page.title = 'Bot Assistant'
#
#	async def submit_action( box: ft.TextField, btn: ft.IconButton, history: ft.ListView ):
#		if box.value == '':
#			return
#		
#		history.controls.append( ChatMessage(Message( 'Yo', box.value, MessageSenderType.HUMAN ) ) )
#		history.controls.append( ChatMessage(Message( 'IA', box.value*10, MessageSenderType.AI ) ) )
#		box.value = ''
#		await box.focus_async()
#		await box.update_async()
#		await chat.update_async()
#
#	chat = Chat(submit_action)
#
#	page.theme = ft.Theme( color_scheme_seed=ft.colors.BLUE_500 )
#	page.appbar = ft.AppBar(
#		leading=ft.Icon(ft.icons.EMOJI_OBJECTS_SHARP),
#		leading_width=40,
#		color=ft.colors.BLUE,
#		elevation=10,
#		title=ft.Text(page.title),
#		center_title=False,
#		actions=[ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),]
#	)
#
#
#
#	page.padding = ft.padding.only(top=0, left=10, right=10, bottom=10)
#	page.add_async(
#		chat,
#	)
#
#
#if __name__ == "__main__":
#	ft.app(port=8550, target=main, view=ft.WEB_BROWSER)
#	#ft.app( target=main, view=ft.FLET_APP)
#		
#
#
#