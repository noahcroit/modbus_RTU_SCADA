#!/usr/bin/env python3
import modbus_umodbus
import time
import signal



# modbus TCP
slave_ip = '192.168.2.88'
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
_ADDRESS_OFFSET_ANALOG_INPUT = 0

# Modbus address list for device 1
# Discrete Input : Read only (X0, X1, ...)
_MODBUS_ADDRESS_DISCRETE_INPUT_1 = 63488
_MODBUS_ADDRESS_DISCRETE_INPUT_2 = _MODBUS_ADDRESS_DISCRETE_INPUT_1 + 1
_MODBUS_ADDRESS_DISCRETE_INPUT_3 = _MODBUS_ADDRESS_DISCRETE_INPUT_1 + 2
_MODBUS_ADDRESS_DISCRETE_INPUT_4 = _MODBUS_ADDRESS_DISCRETE_INPUT_1 + 3
# Discrete Output : Read only (Y0, Y1, ...)
_MODBUS_ADDRESS_READ_DISCRETE_OUTPUT_1 = 64512
_MODBUS_ADDRESS_READ_DISCRETE_OUTPUT_2 = _MODBUS_ADDRESS_READ_DISCRETE_OUTPUT_1 + 1
_MODBUS_ADDRESS_READ_DISCRETE_OUTPUT_3 = _MODBUS_ADDRESS_READ_DISCRETE_OUTPUT_1 + 2
_MODBUS_ADDRESS_READ_DISCRETE_OUTPUT_4 = _MODBUS_ADDRESS_READ_DISCRETE_OUTPUT_1 + 3
# Discrete Output : Write (Use Auxillary Relay : M0, M1, ...)
_MODBUS_ADDRESS_WRITE_DISCRETE_OUTPUT_1 = 0
_MODBUS_ADDRESS_WRITE_DISCRETE_OUTPUT_2 = _MODBUS_ADDRESS_WRITE_DISCRETE_OUTPUT_1 + 1
_MODBUS_ADDRESS_WRITE_DISCRETE_OUTPUT_3 = _MODBUS_ADDRESS_WRITE_DISCRETE_OUTPUT_1 + 2
_MODBUS_ADDRESS_WRITE_DISCRETE_OUTPUT_4 = _MODBUS_ADDRESS_WRITE_DISCRETE_OUTPUT_1 + 3
# Analog Input : Read only (AI0, AI1, AI2, ...)
_MODBUS_ADDRESS_ANALOG_INPUT_1 = 0
_MODBUS_ADDRESS_ANALOG_INPUT_2 = _MODBUS_ADDRESS_ANALOG_INPUT_1 + 1
_MODBUS_ADDRESS_ANALOG_INPUT_3 = _MODBUS_ADDRESS_ANALOG_INPUT_1 + 2
_MODBUS_ADDRESS_ANALOG_INPUT_4 = _MODBUS_ADDRESS_ANALOG_INPUT_1 + 3



"""
    This section is used to test how to read dicrete input from PLC. 
"""
"""
print("Test read discrete function... Enter CTRL+C for exit.")
time.sleep(3)
try:
    while True:
        # Sample discrete input : M0 for each 0.1 sec
        m = my_plc.read_discrete_inputs(start_discrete_address=_MODBUS_ADDRESS_DISCRETE_INPUT_1, number_of_inputs=4)

        print("value={}".format(m))
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Exit demo program : Read discrete input")
"""


"""
    This section is used to test how to write coil from PLC. 
"""

try:
    print("Enter PLC's coil number (from 0-3) to toggle, CTRL+C and Enter to exit")
    while True:
        selected_coil = input(" : ")
        selected_coil = int(selected_coil)

        tmp = my_plc.read_coils(start_coil_address=selected_coil + _MODBUS_ADDRESS_READ_DISCRETE_OUTPUT_1, number_of_coils=1)
        time.sleep(0.1)
        if type(tmp) is list and len(tmp) == 1:
            tmp = tmp[0]
        print("read={}".format(tmp))
        if tmp == 0:
            #my_plc.write_coils(coil_start_address=selected_coil + _ADDRESS_OFFSET_COIL, write_values=[1])
            my_plc.write_coil(coil_address=selected_coil + _MODBUS_ADDRESS_WRITE_DISCRETE_OUTPUT_1, write_value=1)
        else:
            #my_plc.write_coils(coil_start_address=selected_coil + _ADDRESS_OFFSET_COIL, write_values=[0])
            my_plc.write_coil(coil_address=selected_coil + _MODBUS_ADDRESS_WRITE_DISCRETE_OUTPUT_1, write_value=0)
    
except KeyboardInterrupt:
    print("Exit demo program : Write coil")
    exit(0)




"""
    This section is used to test how to read analog from PLC. 
"""
"""
print("Test read analog function... Enter CTRL+C for exit.")
time.sleep(3)
try:
    while True:
        # Sample discrete input : M0 for each 0.1 sec
        volume = []
        volume_0 = my_plc.read_input_registers(start_register_address=_MODBUS_ADDRESS_ANALOG_INPUT_1, number_of_registers=1)
        volume.append(volume_0)
        volume_1 = my_plc.read_input_registers(start_register_address=_MODBUS_ADDRESS_ANALOG_INPUT_2, number_of_registers=1)
        volume.append(volume_1)
        volume_2 = my_plc.read_input_registers(start_register_address=_MODBUS_ADDRESS_ANALOG_INPUT_3, number_of_registers=1)
        volume.append(volume_2)
        volume_3 = my_plc.read_input_registers(start_register_address=_MODBUS_ADDRESS_ANALOG_INPUT_4, number_of_registers=1)
        volume.append(volume_3)

        
        print("value={}".format(volume))
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Exit demo program : Read analog input")  
"""



