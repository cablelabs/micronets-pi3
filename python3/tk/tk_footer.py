from tkinter import *
from .tk_widget import TKWidget

import utils.globals as globals

class TKFooter(TKWidget):

	def __init__(self,parent,l=0, t=200, w=320, h=40, show=True):

		TKWidget.__init__(self)

		font = self.font1

		self.parent = parent

		# main frame
		self.frame = Label(parent.frame, fg="white", bg='gray20')
		self.place_widget(self.frame,l, t, w, h, show)
		self.frame.config(font=font)

	def clear(self):
		self.frame.config(text="")

	def set_text(text):
		self.frame.config(text=text)

	def set_font(font):
		self.frame.config(font=font)

	def update():
		pass

	'''
		TODO: based on parent.state & globals.sparse_mode, choose what to show
			            #if not self.sparse_mode:
		                #footer.config(text=str(wifi_ip))
		                

		            if not config.get('comcast'):
		            	
		                #footer.config(text="NO IP ADDRESS")
	'''
