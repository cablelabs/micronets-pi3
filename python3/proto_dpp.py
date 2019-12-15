import os, time
import threading
from threading import Timer

#import json
from Tkinter import *

from utils.syslogger import SysLogger
from proto_config import *

# Frames
from tk.tk_status import TKStatus 
from tk.tk_main import TKMain 
from tk.tk_header import TKHeader 

# Logfile is /tmp/<argv[0]>.log
logger = SysLogger().logger()

window = Tk()
window.title("ProtoDPP")

full_w = 320
full_h = 240
main_w = 280
main_h = 160
banner_h = 40
icon_l = 282
icon_t = banner_h + 2
iconframe_size = 40
icon_size = 36
do_shutdown = False
shutting_down = False
shutdown_timer = None
last_message_time = 0.0
mode_icon = None
mode_label = None
reset_label = None
settings = None
settings_visible = False
onboard_button = None
refresh_button = None
settings_button = None
shutdown_button = None
qrcode_frame = None
qrcode_image = None
#config = {}
onboard_active = False
qrcode_data = None
demo_mode = False
demo_status = None
demo_ssid = None
demo_wifi_ip = None
connected_frame = None
not_connected_frame = None
frame_count = 0
splash_image = None
fireworks_image = None

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

logger.info("Screen: "+str(screen_width) + " x " + str(screen_height))

main_x = 0
main_y = 0

if screen_width >= 640 and screen_height >= 480:

    # External monitor/VNC
    main_x = 40
    main_y = 40

window.geometry("320x240+" + str(main_x) + "+" +str(main_y))

main_window = TKMain(window, 0, 0, full_w, full_h, True)
status_window = TKStatus(main_window.frame, 0, banner_h, main_w, main_h, True)

def enableExit():
    global canExit
    canExit  = True

t = threading.Timer(3.0, enableExit)
t.start()

count = 0
def updateTimer():
	global count
	window.after(4000,updateTimer)
	if count == 1:
		pass
		status_frame.hide()
	count += 1

updateTimer()

window.mainloop()
