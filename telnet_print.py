import getpass
import sys
import time
import paramiko
import telnetlib
import re



def read_switch_ip_list(path):
#	Function to read hosts IP addresses from file
	try:
		hosts_file = open(path, "r")
		hosts_list = hosts_file.readlines()
		hosts_file.close()
		#	Strip EOL symbols
		for i in range(0, len(hosts_list)):
			hosts_list[i]=hosts_list[i].rstrip()
		return hosts_list
	except:
		print('Error opening hosts file')
		return('ERROR')

def wipe_results_file(path):
	results_file = open(path, "w")
	results_file.close()

def append_to_results_file(path, data_to_append):
	results_file = open(path, "a")
	results_file.writelines(str(data_to_append).lstrip("('").rstrip("')") + "\n")
	results_file.close()

def try_telnet(ip):
	host_telnet_object = telnetlib.Telnet()
	try:
		host_telnet_object.open(ip, 23, timeout=3)
		host_telnet_object.read_very_lazy()
		host_telnet_object.close()
		return 'OK'
	except:
		return 'FAILED'

def telnet_send_command(host_telnet_object, cli_command):
	cli_command_bytes = bytes(cli_command, encoding='ASCII')
	host_telnet_object.write(cli_command_bytes + b'\n')
	time.sleep(2)
	return(host_telnet_object.read_very_eager())

def telnet_open_connection(ip):
	host_telnet_object = telnetlib.Telnet()
	host_telnet_object.open(ip, 23, timeout=3)
	return(host_telnet_object)

def telnet_send_username_password(host_telnet_object, usr, passwd, old_session=''):
	if old_session == '':
		try:
			session = host_telnet_object.read_until(b"Username: ", timeout=5)
		except Exception as e:
			return(str(e))
	else:
		session = old_session
		
	if "Username:" in str(session) and not "Screen" in str(session):
		print('*** Received username prompt. Trying username and password.')	
		try:
			host_telnet_object.write(usr.encode('ascii') + b"\n")
			time.sleep(1)
			host_telnet_object.read_until(b'Password: ', 5)
			host_telnet_object.write(passwd.encode('ascii') + b"\n")
			time.sleep(4)
			print('*** Checking answer from the device.')
			session = host_telnet_object.read_very_eager()
			return(session)
		except Exception as e:
			return(str(e))
	else:
		print('*** No correct prompt received')
		return('NO PROMPT')


switch_ip_file = 'trylist.txt'
result_file = 'inventory.csv'
separator = ';'
result_list = list()

print('Enter RADIUS username')
radius_username = input('Username: ')
print('Enter RADIUS password (username:' + radius_username + ')')
radius_password = getpass.getpass()
""" # Local switch credentials to try if RADIUS credentials fail:
print('Enter LOCAL username')
local_username = input('Username: ')
print('Enter LOCAL password: (username:' + local_username + ')')
local_password = getpass.getpass()
# Password to access priv mode
print('Enter ENABLE password')
enable_password = getpass.getpass()
# Simple password, for switches that don't have user accounts configured
print('Enter SIMPLE password')
simple_password = getpass.getpass() """


switch_ip_list = read_switch_ip_list(switch_ip_file)


wipe_results_file(result_file)


for switch_ip in switch_ip_list:
    current_host = telnet_open_connection(switch_ip)
    current_session_output = telnet_send_username_password(current_host, radius_username, radius_password)
    current_session_output = telnet_send_command(current_host, 'show mac address-table')
    
    