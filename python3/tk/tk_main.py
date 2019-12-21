
# Main (empty) window serves as a parent window for everything else
from tkinter import *

from .tk_widget import TKWidget

class TKMain(TKWidget):

	def __init__(self,parent,l, t, w, h, show):

		TKWidget.__init__(self, parent)

		# main frame
		self.frame = Frame(parent, background="gray80", borderwidth=0, relief="solid")
		self.place_widget(self.frame,l, t, w, h, show)
