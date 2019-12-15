# This is the launch script for the Gen2 prototype (Pi 3 & PiTFT screen). 
import sys
from config import * 

if sys.version_info[0] < 3:
    raise Exception("Python 3 Required")

'''
if config.get('mode') == 'dpp':
	from proto_dpp import *  # TODO: rename this module
else:
	from proto_clinic import *

'''

from protodpp_app import ProtoDPP

app = ProtoDPP()
app.run()
