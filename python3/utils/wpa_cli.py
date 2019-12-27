# wrapper for communicating with wpa_supplicant via wpa_cli
# To run without sudo requires adding netdev group
import os, sys
from .config import *
from .syslogger import SysLogger

__all__ = ["dpp_uri"]

# Logfile is /tmp/<argv[0]>.log
logger = SysLogger().logger()

chan_freqs = {1:2412, 2:2417, 3:2422, 4:2427, 5:2432, 6:2437, 7:2442, 8:2447, 9:2452, 10:2457, 11:2462, 12:2467, 13:2472, 14:2484}

def dpp_bootstrap_gen(mac, channel_class, channel, key, vendor):

	cmd = "dpp_bootstrap_gen type=qrcode mac={} chan={}/{} key={} info={}".format(
		mac, channel_class, channel, key, vendor)

	lines = exec_cli(cmd, 1)
	id = lines[0][0]

	cmd = "dpp_bootstrap_get_uri {}".format(id)

	lines = exec_cli(cmd, 1)
	uri = lines[0][0]

	return uri

def dpp_listen():
	cmd = "dpp_listen {}".format(chan_freqs[config.get('channel')])
	exec_cli(cmd, 1)

def dpp_stop_listen():
	exec_cli("dpp_stop_listen", 1)

def reconfigure():
	exec_cli("reconfigure")

def reassociate():
	exec_cli("reassociate")

def set(param, value):
	exec_cli("set {} {}".format(param,value), 0, False)

def list_networks():
	lines = exec_cli("list_networks", 2, False)
	return lines

def remove_networks(ssid=None):

	lines = exec_cli("list_networks", 2, False)

	for fields in lines:
		if ssid == None or ssid == fields[1]:
			cmd = "remove_network {}".format(fields[0])
			exec_cli(cmd, 1)

# check to see if we have been provisioned onto a micronets network (clinic mode only) for display purposes
def get_provisioned():
	lines = exec_cli("list_networks", 2, False)

	for fields in lines:
		network = fields[0]
		cmd = "get_network {} {}".format(network, "identity")
		lines2 = exec_cli(cmd, 1, False)
		if lines2[0][0] == '"micronets"':
			cmd = "get_network {} {}".format(network, "ssid")
			lines3 = exec_cli(cmd, 1, False)
			return lines3[0][0]
	return None

# check to see if we have ANY networks provisioned (dpp mode only) for display purposes
def has_network():
	lines = exec_cli("list_networks", 2, False)
	return len(lines) > 0

# get psk for an ssid (display purposes)
def get_ssid_psk(ssid):
	lines = exec_cli("list_networks", 2, False)

	for fields in lines:
		network = fields[0]
		if ssid == fields[1]:
			cmd = "get_network {} {}".format(network, "psk")
			lines2 = exec_cli(cmd, 1, False)
			return lines2[0][0]

# create a new network definition from dictionary of key/value pairs

def add_network(params):

	try:
		lines = exec_cli("add_network", 1)
		index = lines[0][0]

		for key, value in params.items():
			# double quoted strings need to be wrapped in single quotes.
			if isinstance(value, str) and value[0] == '"':
				value = '\''+value+'\''
			cmd = "set_network {} {} {}".format(index, key, value)
			exec_cli(cmd, 1)

		cmd = "enable_network {}".format(index)
		exec_cli(cmd, 1)
	except:
		raise()

# required after add_network(s) are done
def save_config():
	exec_cli("save_config", 1)
		
def interface(iface=None):
	try:
		if iface:
			cmd = "interface ".format(iface)
		else:
			cmd = "interface"

		lines = exec_cli(cmd,0,False)

		fields = lines[0]
		if fields[0] == 'Selected' and fields[1] == 'interface' and fields[2] != None:
			return fields[2].replace("'","")
		return None
	except:
		logger.error("Unable to parse result")
		return None

# Execute the command, and then return a 2-D array of lines and fields
def exec_cli(cmd, skip=0, log=True):
	cmd = "wpa_cli {}".format(cmd)
	if log:
		logger.info("** "+cmd+" **")
	result = os.popen(cmd).read().strip()

	ret = []
	lines = result.split('\n')
	i = 0
	for line in lines:
		line = line.strip()
		i += 1
		if i > skip:
			if log:
				logger.info(line)
			ret.append(line.split())
	#if log:
	#	logger.info("** ^^^^^^^^^^^^ **")


	return ret

logger.info("Interface: "+ str(interface()))

if __name__ == '__main__':

	iface = interface()
	mac = os.popen("cat /sys/class/net/"+iface+"/address").read().strip()
	
	dpp_bootstrap_gen(mac)
	dpp_listen()
	dpp_stop_listen()

	list_networks()
	remove_networks()

	network = {'ssid': '"visitors"', 'psk': '"rockymountain"', 'key_mgmt': 'WPA-PSK WPA-PSK-SHA256', 'ieee80211w': 1}
	add_network(network)

	network = {'ssid': '"googie"', 'psk': '"flerb"', 'key_mgmt': 'WPA-PSK WPA-PSK-SHA256', 'ieee80211w': 1, 'identity': '"micronets"'}
	add_network(network)

	network = {'ssid': '"micronets-hs"', 'psk': '"secblanket"', 'key_mgmt': 'WPA-PSK WPA-PSK-SHA256', 'ieee80211w': 1}
	add_network(network)

	save_config()

	list_networks()

	logger.info("get_provisioned: "+ str(get_provisioned()))



