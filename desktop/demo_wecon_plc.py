#!/usr/bin/env python3
import modbus_umodbus
import time
import signal



# modbus TCP
slave_ip = '192.168.2.66'
slave_port = 8899

my_plc = modbus_umodbus.device_tcp()
my_plc.config(device_id=0x01, socket_ip=slave_ip, socket_port=slave_port, signed_type=True)

print(my_plc.device_id)
print(my_plc.tcp_socket)
print(my_plc.socket_ip)
print(my_plc.socket_port)

"""     
# modbus RTU
my_plc = modbus_umodbus.device_rtu()
my_plc.config(device_id=0x01, port='COM13', baudrate=9600, signed_type=False)

print(my_plc.device_id)
print(my_plc.serialport)
"""

_ADDRESS_OFFSET_COIL = 64512     # %Y of wecon PLC
_ADDRESS_OFFSET_DISCRETE_INPUT = 63488  # %X of wecon PLC
_ADDRESS_OFFSET_ANALOG_INPT = 0

"""
    This section is used to test how to read dicrete input from PLC. 
"""
"""
print("Test read discrete function... Enter CTRL+C for exit.")
time.sleep(3)
try:
    while True:
        # Sample discrete input : M0 for each 0.1 sec
        m = my_plc.read_discrete_inputs(start_discrete_address=0 + _ADDRESS_OFFSET_DISCRETE_INPUT, number_of_inputs=8)

        print("value={}".format(m))
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Exit demo program : Read discrete input")
"""


"""
    This section is used to test how to write coil from PLC. 
"""
"""
try:
    print("Enter PLC's coil number (from 0-7) to toggle")
    while True:
        selected_coil = input(" : ")
        selected_coil = int(selected_coil)

        tmp = my_plc.read_coils(start_coil_address=selected_coil + _ADDRESS_OFFSET_COIL, number_of_coils=1)
        time.sleep(0.1)
        if type(tmp) is list and len(tmp) == 1:
            tmp = tmp[0]
        print("read={}".format(tmp))
        if tmp == 0:
            #my_plc.write_coils(coil_start_address=selected_coil + _ADDRESS_OFFSET_COIL, write_values=[1])
            my_plc.write_coil(coil_address=selected_coil + _ADDRESS_OFFSET_COIL, write_value=1)
        else:
            #my_plc.write_coils(coil_start_address=selected_coil + _ADDRESS_OFFSET_COIL, write_values=[0])
            my_plc.write_coil(coil_address=selected_coil + _ADDRESS_OFFSET_COIL, write_value=0)
    
except KeyboardInterrupt:
    print("Exit demo program : Write coil")
    exit(0)
"""



"""
    This section is used to test how to read analog from PLC. 
"""

print("Test read analog function... Enter CTRL+C for exit.")
time.sleep(3)
try:
    while True:
        # Sample discrete input : M0 for each 0.1 sec
        volume = []
        volume_0 = my_plc.read_input_registers(start_register_address=_ADDRESS_OFFSET_ANALOG_INPT + 0, number_of_registers=1)
        volume.append(volume_0)
        volume_1 = my_plc.read_input_registers(start_register_address=_ADDRESS_OFFSET_ANALOG_INPT + 1, number_of_registers=1)
        volume.append(volume_1)
        volume_2 = my_plc.read_input_registers(start_register_address=_ADDRESS_OFFSET_ANALOG_INPT + 2, number_of_registers=1)
        volume.append(volume_2)
        volume_3 = my_plc.read_input_registers(start_register_address=_ADDRESS_OFFSET_ANALOG_INPT + 3, number_of_registers=1)
        volume.append(volume_3)

        
        print("value={}".format(volume))
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Exit demo program : Read analog input")  




