import os
from utils.config import config
import utils.wpa_cli as wpa_cli

__all__ = ["get_wifi_ipaddress", "get_ethernet_ipaddress", "get_ssid", "get_mac", "is_connected"]

interface = wpa_cli.interface()

def get_wifi_ipaddress():
	fields = os.popen("ifconfig "+interface+ " | grep 'inet '").read().strip().split(" ")
	ipaddress = None
	if len(fields) >= 2:
	    ipaddress = fields[1]
	return ipaddress

def get_ethernet_ipaddress():
	fields = os.popen("ifconfig "+interface+" | grep 'inet '").read().strip().split(" ")
	ipaddress = None
	if len(fields) >= 2:
		ipaddress = fields[1]
	return ipaddress

def get_ssid():
	ssid = os.popen("iwconfig "+interface+ " | grep 'ESSID'| awk '{print $4}' | awk -F\\\" '{print $2}'").read().strip()
	if ssid == "":
		ssid = None
	return ssid

def get_mac():
	mac = os.popen("cat /sys/class/net/"+interface+"/address").read().strip()
	return mac

def is_connected():
	return (get_ssid() and get_wifi_ipaddress())
