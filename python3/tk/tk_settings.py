import os, time
from tkinter import *
from .tk_widget import TKWidget
from .tk_button import TKTextButton
from .tk_label import TKLabel 
from utils.config import config


import utils.network as network

class TKSettings(TKWidget):

	CB_DONE = 0
	CB_RESET = 1
	CB_REBOOT = 2

	def __init__(self,parent, callback=None, l=0, t=40, w=280, h=160, show=False):

		TKWidget.__init__(self, parent)

		self.callback = callback if callback else self.null_callback

		self.frame = Frame(parent.frame, background='light goldenrod yellow', borderwidth=0, relief="solid")
		self.place_widget(self.frame, l, t, w, h, show)

		self.mode = config.get('mode')

		self.configure_ui()
		self.will_restart = False

	def configure_ui(self):
		# Fixed settings buttons
		left = 0
		top = 0
		height = 40
		button_width = 120
		label_width = 160

		self.mode_button = TKTextButton(self, left, top, button_width, height, "Mode", self.toggle_mode)
		self.mode_label = TKLabel(self, button_width, top, label_width, height-1, self.mode.upper(), "black", TKWidget.font3, "light goldenrod yellow")

		self.mode_warning_label = TKLabel(self, button_width, top+26, label_width, height/2-1, "- device will restart -", "red", TKWidget.font5, "light goldenrod yellow", False)


		top += height

		self.reset_button = TKTextButton(self, left, top, button_width, height, "Reset", self.reset)
		self.reset_label = TKLabel(self, button_width, top, label_width, height-1, "Remove Wifi Keys", "black", TKWidget.font3, "light goldenrod")

		top += height

		self.reboot_button = TKTextButton(self, left, top, button_width, height, "Reboot", self.reboot)
		self.reboot_label = TKLabel(self, button_width, top, label_width, height-1, "Reboot Device", "black", TKWidget.font3, "light goldenrod yellow")

		top += height

		self.reset_button = TKTextButton(self, left, top, button_width, height, "Done", self.done)
		self.reset_label = TKLabel(self, button_width, top, label_width, height-1, "Exit Settings", "black", TKWidget.font3, "light goldenrod")

	def null_callback(self, arg1, arg2):
		pass

	def reset(self, null_arg=0):
		self.callback(TKSettings.CB_RESET)

	def done(self, null_arg=0):
		if self.will_restart:
			config.set('mode', self.mode)
			config.save_config()
		self.callback(TKSettings.CB_DONE, self.will_restart)

	def reboot(self, null_arg=0):
		self.callback(TKSettings.CB_REBOOT)

	def toggle_mode(self, null_arg=0):
		if self.mode == 'dpp':
			self.mode = 'clinic'
		else:
			self.mode = 'dpp'

		self.mode_label.set_text(self.mode.upper())

		if self.mode != config.get('mode'):
			self.will_restart = True
			self.mode_warning_label.show()
		else:
			self.will_restart = False
			self.mode_warning_label.hide()

