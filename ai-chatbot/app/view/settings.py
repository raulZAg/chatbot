
from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
import requests
#from app.v1.controllers.chat_controller import UserAI


from schema.chat import ChatMemoryModel
from schema.chat import LanguageModel
from schema.user import UserSettings
from utils.settings import GuiSettings

from controllers.topic import Topics


class Spinner( ft.UserControl ):
	def __init__(self, controls: List[Control] = None, ref: Ref = None, key: str = None, width: OptionalNumber = None, height: OptionalNumber = None, left: OptionalNumber = None, top: OptionalNumber = None, right: OptionalNumber = None, bottom: OptionalNumber = None, expand: int = None, col: ResponsiveNumber = None, opacity: OptionalNumber = None, rotate: RotateValue = None, scale: ScaleValue = None, offset: OffsetValue = None, aspect_ratio: OptionalNumber = None, animate_opacity: AnimationValue = None, animate_size: AnimationValue = None, animate_position: AnimationValue = None, animate_rotation: AnimationValue = None, animate_scale: AnimationValue = None, animate_offset: AnimationValue = None, on_animation_end=None, visible: bool = None, disabled: bool = None, data: Any = None, clip_behavior: ClipBehavior = None, minim:int = 0, maxim:int = 100):
		super().__init__(controls, ref, key, width, height, left, top, right, bottom, expand, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, clip_behavior)
		self._min_value = minim
		self._max_value = maxim

	@property
	def value(self):
		n = 0
		if self.text_field.current.value.isdecimal():
			n = int(self.text_field.current.value)
		return n

	@value.setter
	async def value(self, n: int):
		# poner limites de min y max
		n = max( n, self.min_value )
		n = min( n, self.max_value )
		self.text_field.current.value = str(n)
		await self.text_field.current.update_async()
		await self.update_async()

	@property
	def max_value(self):
		return self._max_value
	
	@property
	def min_value(self):
		return self._min_value
	
	@max_value.setter
	def max_value(self, val: int):
		self._max_value = val
	
	@min_value.setter
	def min_value(self, val: int):
		self._min_value = val


	def build(self):
		self.increase = ft.Ref[ ft.IconButton ]()
		self.decrease = ft.Ref[ ft.IconButton ]()
		self.text_field = ft.Ref[ ft.TextField ]()


		def increase_onclick(e):
			n = self.value
			n += 1
			self.value = n

		def decrease_onclick(e):
			n = self.value
			n -= 1
			self.value = n

		def on_blur(e):
			n = self.value
			self.value = n

		return ft.Row( 
			controls=[
				#ft.Text('Size of Window:'),
				ft.IconButton( 
					icon = ft.icons.REMOVE_CIRCLE_OUTLINED, 
					ref = self.decrease,
					on_click=decrease_onclick ),
				ft.TextField( 
					ref = self.text_field,
					on_blur=on_blur),
				ft.IconButton( 
					icon = ft.icons.ADD_CIRCLE_OUTLINED, 
					ref = self.decrease ,
					on_click=increase_onclick ),
			] )

gui_settings = GuiSettings()		

class SettingsWindows( ft.UserControl ):
	def __init__(self ):
		super().__init__()

		async def on_change_cb(e: ft.ControlEvent):
			await e.control.update_async()

		self.select_llm = ft.Dropdown(
					label = "Select LLM:",
					options = [
						ft.dropdown.Option( LanguageModel.OpenAI.value ),
						ft.dropdown.Option( LanguageModel.AzureOpenAI.value ),
						ft.dropdown.Option( LanguageModel.Llama2.value, disabled=True ),
					],
					value = LanguageModel.OpenAI.value,
					on_change = on_change_cb,
				)

		self.select_topic = ft.Dropdown(
					label="Select topic:",
					options=[],
					on_change = on_change_cb,
				)


		async def memory_on_change(e):
			if e.control.value == ChatMemoryModel.WINDOW.value:
				self.memory_window.visible = True
				#print('show')
			else:
				self.memory_window.visible = False
				#print('hide')
			
			await self.memory_window.update_async()
			await self.select_memory.update_async()
			await self.update_async()

		self.select_memory = ft.Dropdown(
					label = "Memory type:",
					options = [
						ft.dropdown.Option( ChatMemoryModel.SUMMARY.value ),
						ft.dropdown.Option( ChatMemoryModel.ALL_CHAT.value ),
						ft.dropdown.Option( ChatMemoryModel.WINDOW.value ),
						ft.dropdown.Option( ChatMemoryModel.NO_MEMORY.value ),
					],
					on_change = memory_on_change,
					value = ChatMemoryModel.SUMMARY.value,
				)
		
		self.memory_window = Spinner(
			visible = False,
			minim = 1,
			maxim = 30)


	async def apply_new_settings(self, user:str):
		sett = self.get_settings()
		#print(f'sett: {sett.json()}')
		params = {
			'data_source': sett.data_source,
			'chat_memory_model': sett.chat_memory_model.value,
			'llm': sett.llm,
			'memory_buffer_size': sett.memory_buffer_size
		}
		print(f'params: {params}')
		from  router.user import settings_set as user_settings_set
		ret = user_settings_set( user_id=user, user_settings=sett )
		#ret = await requests.post(gui_settings.backend_api +  f'/user/{user}/settings/set', json=params)
		#print(ret)
		await self.update_async()

	def build(self):

		topics = list(Topics.keys()) #requests.get( 'http://localhost:8000/v1/topic/list' )
		#topics = topics.json()
		for t in topics:
			self.select_topic.options.append(ft.dropdown.Option( t )) 
		self.select_topic.value = topics[0]

		self.settings = ft.Column(
			controls=[
				ft.Row( controls = [
					ft.Icon(name=ft.icons.SETTINGS, color=ft.colors.GREY),
					ft.Text(value="Settings", style=ft.TextThemeStyle.TITLE_LARGE)
				] ),
				
				ft.Divider(),
				self.select_llm,
				self.select_topic,
				self.select_memory,
				self.memory_window

			],
			expand=True
		)

		return self.settings

	def get_settings(self) -> UserSettings:
		sett = UserSettings( 
			data_source=self.select_topic.value,
			llm=LanguageModel(self.select_llm.value),
			chat_memory_model=self.select_memory.value,
			memory_buffer_size=self.memory_window.value
			)
		
		return sett
