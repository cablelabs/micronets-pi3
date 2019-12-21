# This is the launch script for the Gen2 prototype (Pi 3 & PiTFT screen). 
import sys
from utils.config import config

if sys.version_info[0] < 3:
    raise Exception("Python 3 Required")

if config.get('mode') == 'dpp':
	from proto_dpp import ProtoDPP
	ProtoDPP().run()
else:
	from proto_clinic import ProtoClinic
	ProtoClinic().run()
