#!/usr/bin/env python3
'''This file is to preconfigure new switch devices for migration'''
import netmiko.exceptions
import banner
import netmiko
import json
import getpass as gp
from datetime import datetime
import time
import threading

start = time.time()

netmiko_exceptions = (netmiko.exceptions.NetMikoTimeoutException,
                      netmiko.exceptions.NetMikoAuthenticationException)

#username = gp.getuser("admin")
username = "admin"
password = gp.getpass()
sitecode = input("Enter site code: ")
count = 0


with open("devices.json") as dev_file:
    devices = json.load(dev_file)

#Create an empty list (it will store the threads)

threads = list()

for device in devices:
    device["username"] = username
    device["password"] = password
    count += 1
   
    try:
        connection = netmiko.ConnectHandler(**device)      
        print("=" * 79)
        print("Connecting to Core Switch "+ connection.base_prompt +" " + device["ip"])
        print("=" * 79)
        #CONFIGURE HOSTNAME FOR EACH DEVICE
        hostname = connection.send_config_set(f'hostname bs0{count}.{sitecode}-new')
        print(hostname)
        border = str(hostname)
        print(border)
        #CHECK HOSTNAME AND ENTER SPECIFIC COMMAND FOR EACH DEVICE
        if "bs01" in border:
            print("*" * 79)
            print(f'Sending commands to Core Switch {connection.base_prompt}')
            print("*" * 79)
            #print(connection.send_config_from_file('precon_core1.txt'))
            time.sleep(2)

        if "bs02" in border:
            print("*" * 79)
            print(f'Sending commands to Core Switch {connection.base_prompt}')
            print("*" * 79)
            #print(connection.send_config_from_file('precon_core2.txt'))
            time.sleep(2)
            print("*" * 79)
        #HARDENING COMMANDS         
        print("*" * 79)
        print(f'Sending hardening commands to {connection.base_prompt}')
        print("*" * 79)
        #print(connection.send_config_from_file('coreswitch_hardening.txt'))

    except netmiko_exceptions as e:
        print("Failed to connect " + connection.base_prompt +" " + device["ip"])

connection.disconnect()

# starting the threads
for th in threads:
    th.start()
# waiting for the threads to finish
for th in threads:
    th.join()

end = time.time()

print(f'Total execution time:{end-start}')