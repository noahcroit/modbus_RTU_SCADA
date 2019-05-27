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
print("Test read LED status.")
time.sleep(3)
try:
    while True:
        # Sample discrete input : M0 for each 0.1 sec
        led_status = []
        status = device_1.read_led_status(led=1)
        led_status.append(status)
        status = device_1.read_led_status(led=2)
        led_status.append(status)
        
        print("LED(s) status = {}".format(led_status))
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Exit demo program") 
