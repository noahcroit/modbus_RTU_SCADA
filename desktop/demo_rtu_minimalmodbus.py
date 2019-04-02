#!/usr/bin/env python
import minimalmodbus
import time

# Object configuration for modbus device : PSA-03-50 as modbus RTU
device_address_psa0350 = 0x01
psa0350 = minimalmodbus.Instrument(port='COM13', slaveaddress=device_address_psa0350, mode='rtu')

# UART parameters configuration for modbus RTU
com_port_modbus = 'COM13'
psa0350.serial.port = com_port_modbus
psa0350.serial.baudrate = 9600
psa0350.serial.bytesize = 8
psa0350.serial.parity   = minimalmodbus.serial.PARITY_NONE
psa0350.serial.stopbits = 1
psa0350.serial.timeout  = 0.2   # seconds

# Debug mode config
psa0350.debug = False
# print(psa0350)

# Open serial port
if not psa0350.serial.is_open:
    psa0350.serial.open()

# Control loop 
try:
    stopFlag = 0
    while stopFlag == 0:
         # prompt user input from keyboard for percentage power setting of PSA-03-50
        userInput = input("Enter write value or 'q' for exit : ")

        if userInput != 'q':
            
            # Saturation block for user input : range only 0-99
            write_value = int(userInput)
            if write_value > 99:
                print(str(write_value) + " -> " + str(99))
                write_value = 99

            elif write_value < 0:
                print(str(write_value) + " -> " + str(0))
                write_value = 0
            else:
                print(write_value)    

            # Send modbus RTU command to PSA-03-50
            register_addr_psa0350 = 0x0000
            function_code_request_to_write_psa0350 = 0x06
            
            psa0350.write_register(registeraddress=register_addr_psa0350, 
                                           value=write_value, 
                                           numberOfDecimals=0, 
                                           functioncode=function_code_request_to_write_psa0350,
                                           signed=False)
            
        else:
            stopFlag = 1

except Exception as e:
    print("Exception : {}".format(e))

# Close serial port
if psa0350.serial.is_open:
    psa0350.serial.close()