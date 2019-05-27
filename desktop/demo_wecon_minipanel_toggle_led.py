#!/usr/bin/env python3
import wecon_plc_minipanel
import time
import signal



""" PLC Object config """
device_1 = wecon_plc_minipanel.device_lx2e_1212(port_type='modbus_tcp')
device_2 = wecon_plc_minipanel.device_lx2e_0806(port_type='modbus_tcp')
device_3 = wecon_plc_minipanel.device_lx2e_0806(port_type='modbus_tcp')
device_4 = wecon_plc_minipanel.device_lx2e_0806(port_type='modbus_tcp')

device_1.config(socket_ip='192.168.2.88', socket_port=8899, device_id=0x01)
device_2.config(socket_ip='192.168.2.88', socket_port=8899, device_id=0x02)
device_3.config(socket_ip='192.168.2.88', socket_port=8899, device_id=0x03)
device_4.config(socket_ip='192.168.2.88', socket_port=8899, device_id=0x04)




"""
    This section is used to test how to toggle LED in minipanel. 
    There are 2 modbus functions used in this program.
        : write_coil, by calling "device_x.write_led_status()"
        : read_coil,  by calling "device_x.read_led_status()"
"""
device_1.remote_control_enable()
try:
    print("\n\nEnter LED's number (from 1-2) to toggle, CTRL+C and Enter to exit")
    while True:
        selected_led = input(" : ")
        selected_led = int(selected_led)

        tmp = device_1.read_led_status(led=selected_led)
        time.sleep(0.1)
        if type(tmp) is list and len(tmp) == 1:
            tmp = tmp[0]
        print("read={}".format(tmp))
        if tmp == 0:
            device_1.write_led_status(led=selected_led, led_value=1)
        else:
            device_1.write_led_status(led=selected_led, led_value=0)
    
except KeyboardInterrupt:
    device_1.remote_control_disable()
    print("Exit demo program")
    exit(0)
