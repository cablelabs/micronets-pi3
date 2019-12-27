# clinic variant of proto-pi demo
import os, time, atexit
import threading
from threading import Timer
from enum import Enum

from utils.syslogger import SysLogger
from utils.config import config
import utils.globals as globals
import utils.network as network
import utils.wpa_cli as wpa_cli
import pyscreenshot as ImageGrab

from tkinter import *
from tk.tk_app import TKApp
from tk.tk_header import TKHeader
from tk.tk_widget import TKWidget
from tk.tk_footer import TKFooter
from tk.tk_status import TKStatus
from tk.tk_buttons import TKButtons
from tk.tk_messages import TKMessages
from tk.tk_settings import TKSettings
from tk.tk_animation import TKAnimation

import onboard_clinic as onboard

# TODO: 
#   -  Implement utils/layouts.py instead of passing l,t,w,h in widget constructors
#      Widgets can look up the default values from utils/layouts.py by their class name.
#	   Add 'layout' to config.py, default: '320x240'
#   -  Add new "logfile" window. Add icon to messages window that will toggle. Shows contents of syslogger logfile, small font.

class AppState(Enum):
	SPLASH = 0
	STATUS = 1
	FIREWORKS = 2
	MESSAGES = 3
	SETTINGS = 4

# Logfile is /tmp/<argv[0]>.log
logger = SysLogger().logger()

class ProtoClinic(TKApp):

	def __init__(self):
		TKApp.__init__(self)

		# User interface
		self.configure_ui()

		# Wifi state
		self.ssid = None
		self.wifi_ipaddress = None
		self.eth_ipaddress = None
		self.ssid_psk = None

		# Application state
		self.state = None
		self.last_state = None
		self.shutting_down = False

		# Start with splash screen
		self.set_state(AppState.SPLASH)

		# Start the main application interval timer
		self.main_timer()

		#^ __init__ ^#

	# Configure user interface and state management
	def configure_ui(self):

		# Sparse mode hides most connection details on the status window (available on message window w/tap). (Comcast)
		self.sparse_mode = True
		title = "MICRONETS"
		font = TKWidget.font1

		# Build the UI (main_window already exists, created by TKApp)
		self.header_window = TKHeader(self.main_window, 'clinic', title, font)
		self.status_window = TKStatus(self.main_window)
		self.message_window = TKMessages(self.main_window)
		self.footer_window = TKFooter(self.main_window)
		self.settings_window = TKSettings(self.main_window, self.settings_event)

		# Buttons panel
		self.buttons_window = TKButtons(self.main_window)

		# Buttons
		self.onboard_button = self.buttons_window.add_button(0, 'onboard.png', self.click_onboard)
		self.cancel_button = self.buttons_window.add_button(0, 'cancel.png', self.click_onboard, None, False)
		self.countdown_button = self.buttons_window.add_button(0, None, self.click_onboard, None, False)
		self.refresh_button = self.buttons_window.add_button(1, 'refresh.png', self.click_cycle_wifi)
		self.settings_button = self.buttons_window.add_button(2, 'settings.png', self.click_settings)
		self.shutdown_button = self.buttons_window.add_button(3, 'shutdown.png', self.click_power, self.release_power)
		self.countdown_button.set_text("", "white", TKWidget.font1)

		# Hardware buttons
		self.hardware_button(0, self.click_onboard)
		self.hardware_button(1, self.click_cycle_wifi)
		self.hardware_button(2, self.click_settings)
		self.hardware_button(3, self.click_power, self.release_power)

		# Animations
		self.splash_window = TKAnimation(self.main_window, 'earth.gif', 6, self.splash_end_event)
		self.fireworks_window = TKAnimation(self.main_window, 'fireworks.gif', 2, self.fireworks_end_event)

		## UI state management ##

		# Dispatch vectors for state initialize/clear
		self.dispatch = {
			AppState.SPLASH: [self.display_splash, self.end_splash],
			AppState.FIREWORKS: [self.display_fireworks, None],
			AppState.STATUS: [self.display_status, None],
			AppState.SETTINGS: [None, None],
			AppState.MESSAGES: [None, None]
		}

		# Window visibility vectors
		self.base_windows = [self.header_window, self.footer_window, self.buttons_window]
		self.all_windows = self.base_windows + [self.splash_window, self.settings_window, self.status_window, self.message_window, self.fireworks_window]

		self.visible_windows = {
			AppState.SPLASH: self.base_windows + [self.splash_window],
			AppState.STATUS: self.base_windows + [self.status_window],
			AppState.SETTINGS: self.base_windows + [self.settings_window],
			AppState.FIREWORKS: self.base_windows + [self.fireworks_window],
			AppState.MESSAGES: self.base_windows + [self.message_window]
		}

		# Button visibility vectors
		self.standard_buttons = [self.onboard_button, self.refresh_button, self.settings_button, self.shutdown_button]
		self.all_buttons = self.standard_buttons + [self.countdown_button]

		self.visible_buttons = {
			AppState.SPLASH: self.standard_buttons,
			AppState.STATUS: self.standard_buttons,
			AppState.SETTINGS: [self.shutdown_button],
			AppState.FIREWORKS: self.standard_buttons,
			AppState.MESSAGES: self.standard_buttons
		}

		# Window click events
		self.status_window.register_click(self.click_status_window)
		self.message_window.register_click(self.restore_state)
		self.header_window.mode_icon.register_click(self.take_screenshot)
		self.header_window.register_click(self.toggle_backlight)

	# Revert to prior state. Mainly used for returning from message window
	def restore_state(self, null_arg=0):
		self.set_state(self.last_state)

	# Update the status window and underlying message window (connection details)
	def update_status(self):
		self.status_window.update()
		self.message_window.display_connection_info()

	def cancel_animations(self):
		self.splash_window.cancel()
		self.fireworks_window.cancel()

	# Window initialization routines. These are declared in self.dispatch_vectors. They are executed after UI reconfiguration
	def display_splash(self):
		logger.info("display splash")
		self.splash_window.start()
		try:
			ethernet_ip = network.get_ethernet_ipaddress()
			if ethernet_ip:
				self.footer_window.set_text(ethernet_ip)
		except:
			pass

	def end_splash(self):
		logger.info("end splash")
		self.footer_window.set_text("")
		self.splash_window.unload()

	def display_status(self):
		self.update_status()

	def display_fireworks(self):
		logger.info("display fireworks")
		self.fireworks_window.start()

	def end_fireworks(self):
		logger.info("end fireworks")
		self.fireworks_window.unload()

	def reset_wifi(self):
		wpa_cli.remove_networks()
		# add default "clinic" network(s)
		folder = os.path.dirname(os.path.realpath(__file__))
		filename = os.path.join(folder, '../config/networks.json')

		try:
			with open(filename, 'r') as infile:  
				file_data = infile.read()
				networks = json.loads(file_data)

				for net in networks:
					wpa_cli.add_network()

				wpa_cli.reconfigure()
		except:
			pass
		finally:
			self.set_state(AppState.STATUS)

	def cycle_wifi(self):
		wpa_cli.reconfigure()
		#wpa_cli.reassociate()

		Timer(2.0, self.set_state,[AppState.STATUS]).start()

	def end_onboard(self, error):
		if not error:
			self.set_state(AppState.FIREWORKS)
		else:
			pass
			self.message_window.add_message(error)
			# leave message window showing.
			# On message window tap, change status to STATUS (error messages erased)

	# Timer events

	# Animation complete events
	def fireworks_end_event(self, canceled):
		logger.info("fireworks ended. canceled: "+ str(canceled))
		if not canceled:
			self.set_state(AppState.STATUS)

	def splash_end_event(self, canceled):
		logger.info("splash ended. canceled: "+ str(canceled))
		if not canceled:
			self.set_state(AppState.STATUS)

	def wait_end_event(self, canceled):
		logger.info("wait ended. canceled: "+ str(canceled))
		if not canceled:
			self.set_state(AppState.STATUS)

	# Settings window callbacks
	def settings_event(self, reason, param=None):
		if reason == TKSettings.CB_DONE:
			if param == True:
				# Mode changed.
				self.message_window.clear()
				self.message_window.add_message("Restarting Application..")
				self.set_state(AppState.MESSAGES)

				logger.info("Restarting Application..")
				Timer(2.0, self.restart).start()
			else:
				self.set_state(AppState.STATUS)

		elif reason == TKSettings.CB_REBOOT:
			self.message_window.clear()
			self.message_window.add_message("Rebooting Device..")
			self.set_state(AppState.MESSAGES)

			logger.info("Rebooting Device..")
			Timer(2.0, self.reboot).start()

		elif reason == TKSettings.CB_RESET:
			self.message_window.clear()
			self.message_window.add_message("Clearing Wifi Credentials..")
			self.set_state(AppState.MESSAGES)

			logger.info("Clearing Wifi Credentials....")
			Timer(2.0, self.reset_wifi).start()


	# Shutdown timer fired
	def check_shutdown_event(self):
		self.shutdown_timer = None

		if (self.can_shutdown):
			self.shutting_down = True
			logger.info("Shutting Down..")
			self.message_window.clear()
			self.message_window.add_message("Shutting Down..")
			self.set_state(AppState.MESSAGES)
			Timer(2.0, self.shutdown).start()

	# Button events
	def click_onboard(self, nullArg=0):
		logger.info("click_onboard")
		self.cancel_animations()
		
		# todo, toggle betweek onboard and cancel

		# temp
		self.message_window.clear()
		self.message_window.add_message("Begin Onboard..")
		onboard.start(self.end_onboard, self.message_window)
		self.set_state(AppState.MESSAGES)


	def click_cycle_wifi(self, nullArg=0):
		self.cancel_animations()
		logger.info("click_cycle_wifi")
		self.message_window.clear()
		self.message_window.add_message("Cycling wifi..")
		self.set_state(AppState.MESSAGES)
		logger.info("Cycling wifi..")
		self.cycle_wifi()

	def click_settings(self, nullArg=0):
		self.cancel_animations()
		logger.info("click_setting")
		self.set_state(AppState.SETTINGS)

	def click_power(self, nullArg=0):
		self.cancel_animations()
		logger.info("click_power")

		self.can_shutdown = True
		self.shutdown_timer = threading.Timer(3.0, self.check_shutdown_event).start()

	def release_power(self, nullArg=0):
		logger.info("release_power")
		self.can_shutdown = False
		if self.shutdown_timer != None:
			self.shutdown_timer.cancel()
			self.shutdown_timer = None

		if not self.shutting_down:

			if self.canExit:
				self.message_window.clear()
				self.message_window.add_message("Restarting Application..")
				self.set_state(AppState.MESSAGES)
				logger.info("Restarting Application..")
				Timer(2.0, os.popen, self.restart).start()

	# Window click events
	def click_status_window(self, nullArg=0):
		self.set_state(AppState.MESSAGES)

	# UI updates
	def main_timer(self):

		try:
			# check for change in wifi connection
			if self.state == AppState.STATUS or self.state == AppState.MESSAGES:
				self.update_status()

			threading.Timer(2.0, self.main_timer).start()

		except:
			pass

if __name__ == '__main__':
	app = ProtoClinic()
	app.run()
