#!/usr/bin/env python3
import wecon_plc_minipanel
import time
import signal



""" PLC Object config """
device_1 = wecon_plc_minipanel.device_lx2e_1212(port_type='modbus_tcp')
device_1.config(socket_ip='192.168.2.88', socket_port=8899, device_id=0x01)




"""
    This section is used to test how to read analog from PLC. 
"""

print("Test read analog function... Enter CTRL+C for exit.")
time.sleep(3)
try:
    while True:
        # Sample discrete input : M0 for each 0.1 sec
        volume = []
        analog_read = device_1.read_potentiometer(channel=1)
        volume.append(analog_read)
        analog_read = device_1.read_potentiometer(channel=2)
        volume.append(analog_read)
        analog_read = device_1.read_potentiometer(channel=3)
        volume.append(analog_read)
        analog_read = device_1.read_potentiometer(channel=4)
        volume.append(analog_read)

        
        print("value={}".format(volume))
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Exit demo program : Read analog input") 

