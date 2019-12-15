import os, sys
from .config import *
from .syslogger import SysLogger

__all__ = ["dpp_uri"]

# Logfile is /tmp/<argv[0]>.log
logger = SysLogger().logger()

chan_freqs = {1:2412, 2:2417, 3:2422, 4:2427, 5:2432, 6:2437, 7:2442, 8:2447, 9:2452, 10:2457, 11:2462, 12:2467, 13:2472, 14:2484}

def dpp_bootstrap_gen():

	logger.info("** generate_dpp_uri **")

	cmd = "sudo wpa_cli dpp_bootstrap_gen type=qrcode mac={} chan={}/{} key={} info={}".format(
		network.get_mac(),
		config.get('channelClass'),
		config.get('channel'),
		config.get('p256'),
		config.get('vendorCode'))

	logger.info("cmd: " + cmd)

	result = os.popen(cmd).read().strip()
	logger.info(result)

	id = result.split('\n')[1]

	cmd = "sudo wpa_cli dpp_bootstrap_get_uri {}".format(id)
	result = os.popen(cmd).read().strip()

	uri = result.split('\n')[1]
	logger.info("uri: " + uri)

	return uri

def dpp_listen():
	logger.info("** wpa_cli: dpp_listen **")
	cmd = "sudo wpa_cli dpp_listen {}".format(chan_freqs[config.get('channel')])
	result = os.popen(cmd).read().strip()
	logger.info(result)

def reconfigure():
	logger.info("** wpa_cli: reconfigure **")
	cmd = "sudo wpa_cli reconfigure"
	result = os.popen(cmd).read().strip()
	logger.info(result)

def reassociate():
	logger.info("** wpa_cli: reassociate **")
	cmd = "sudo wpa_cli reassociate"
	result = os.popen(cmd).read().strip()
	logger.info(result)

def dpp_stop_listen():
	logger.info("** wpa_cli: dpp_stop_listen **")
	cmd = "sudo wpa_cli dpp_stop_listen"
	result = os.popen(cmd).read().strip()
	logger.info(result)

def interface(iface=None):
	if iface:
		cmd = "sudo wpa_cli interface {}".format(iface)
	else:
		cmd = "sudo wpa_cli interface"

	result = os.popen(cmd).read().strip()
	lines = result.split('\n')
	fields = lines[0].split(' ')
	if fields[0] == 'Selected' and fields[1] == 'interface' and fields[2] != None:
		return fields[2].replace("'","")
	else:
		logger.ERROR("Unable to parse result: sudo wpa_cli interface \n{}".format(result))
		return None

logger.info("Interface: "+ interface())

