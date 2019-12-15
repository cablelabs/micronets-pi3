from tkinter import *

from .tk_widget import TKWidget
from .tk_icon import TKIcon
from .tk_label import TKLabel

import lib.wpa_supplicant as wpa_supplicant
import utils.globals as globals
import utils.network as network

class TKStatus(TKWidget):

	def __init__(self,parent,l=0, t=40, w=280, h=160, show=True):

		TKWidget.__init__(self)

		self.parent = parent

		# main frame
		self.frame = Frame(parent.frame, background="white", borderwidth=0, relief="solid")
		self.place_widget(self.frame,l, t, w, h, show)

		# center of frame
		l = (w - 64) / 2
		t = (h - 64) / 2

		# Status icons
		self.connected_icon = TKIcon(self, l, t, 64, 64, 'green-check.png', False)
		self.not_connected_icon = TKIcon(self, l, t, 64, 64, 'no-connection.png', False)

		# SSID label
		self.ssid_label = TKLabel(self, 4, t+64+10, w-8, 24, "NOT CONNECTED", "DodgerBlue4", TKWidget.font3)

	def clear(self):
		self.connected_icon.hide()
		self.not_connected_icon.hide()
		self.ssid_label.set_text("")

	# MAYBE: change TKWidget show/hide to check winfo_ismapped()
	# only change icons if status changed (avoid flicker)
	def set_connected(self, connected):
		if connected:
			#if not self.connected_icon.frame.winfo_ismapped():
			self.connected_icon.show()
			#if self.not_connected_icon.frame.winfo_ismapped():
			self.not_connected_icon.hide()
		else:
			#if self.connected_icon.frame.winfo_ismapped():
			self.connected_icon.hide()
			#if not self.not_connected_icon.frame.winfo_ismapped():
			self.not_connected_icon.show()

	# only change text if status changed (avoid flicker)
	def set_ssid_text(self, text):
		if self.ssid_label.frame.cget("text") != text:
			self.ssid_label.set_text(text)

	def update(self):

		#self.connected_icon.show()
		#self.not_connected_icon.show()
		#self.ssid_label.set_text("flerb")

		#return

		#self.clear()
		ssid = network.get_ssid()
		wifi_ip = network.get_wifi_ipaddress()
		is_provisioned = wpa_supplicant.has_network()

		if ssid:
			if not globals.sparse_mode:
				self.set_ssid_text(ssid)
			else:
				self.set_ssid_text("CONNECTED")
				
			if wifi_ip:
				self.set_connected(True)
			else:
				self.set_connected(False)
		else:
			self.set_connected(False)

			if is_provisioned:
				self.set_ssid_text("NOT CONNECTED")
			else:
				if globals.sparse_mode:
					self.set_ssid_text("NOT CONNECTED")
				else:
					self.set_ssid_text("NOT PROVISIONED")

	def register_click(self, callback):

		# overloaded TKWidget because we need to respond if child windows are clicked as well
		self.frame.bind("<Button-1>",callback)
		self.connected_icon.frame.bind("<Button-1>",callback)
		self.not_connected_icon.frame.bind("<Button-1>",callback)
		self.ssid_label.frame.bind("<Button-1>",callback)






