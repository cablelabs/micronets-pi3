import os, time
from tkinter import *
from .tk_widget import TKWidget

import utils.network as network
import utils.wpa_supplicant as wpa_supplicant

class TKMessages(TKWidget):

	def __init__(self,parent,l=0, t=40, w=280, h=160, show=False):

		TKWidget.__init__(self)

		self.parent = parent
		self.last_message_time = 0.0

		self.frame = Text(parent.frame, wrap=WORD, background='white', borderwidth=0, highlightthickness=0, relief="solid")
		self.place_widget(self.frame, l, t, w, h, show)

	def clear(self):
		self.frame.delete('1.0', END)

	def add_message(self, message):
		self.last_message_time = time.time()
		self.frame.insert(END, " " + message + '\n')

	def display_connection_info(self):

		# don't update connection info if messages currently displayed (flicker)
		if not self.frame.winfo_ismapped():

			self.clear()

			self.add_message("")
			self.add_message("")
			if network.is_connected():
				self.add_message("-- Connection Succeeded! --")
			else:
				self.add_message("-- Connection Failed! --")

			ssid = network.get_ssid()
			addr = network.get_wifi_ipaddress()
			pwd  = wpa_supplicant.get_ssid_psk(ssid) if ssid else None

			self.add_message("")
			self.add_message("   SSID: "+ str(ssid))
			self.add_message("")
			self.add_message("   PASS: "+ str(pwd))
			self.add_message("")
			self.add_message("   ADDR: "+ str(addr))


