import modbus_umodbus
import time
import signal



psa0350_dimmer = modbus_umodbus.device_rtu()
psa0350_dimmer.config(device_id=0x01, port='COM13', baudrate=9600, signed_type=False)

print(psa0350_dimmer.device_id)
print(psa0350_dimmer.serialport)

"""
    This section is used to demo output percentage control of psa0350_dimmer using device_rtu.write_register()
    User need to enter the percentage from terminal
"""
print("Test write function...")
stopFlag = 0
while stopFlag == 0:
    userInput = input("Enter write value or 'q' for exit : ")

    if userInput != 'q':
        write_value = int(userInput)
        
        """
        if write_value > 99:
            print(str(write_value) + " -> " + str(99))
            write_value = 99

        elif write_value < 0:
            print(str(write_value) + " -> " + str(0))
            write_value = 0
        else:
            print(write_value)    
        """

        # Send modbus RTU command
        psa0350_dimmer.write_register(register_address=0x00, write_value=write_value)
        time.sleep(0.1)
    else:
        stopFlag = 1
        print("Demo program for modbus exit")

#################################################################################################
"""
    This section is used to demo output percentage control of psa0350_dimmer using device_rtu.read_register()
    User need to trim the trimpot (potentiometer) on device to control output percentage manually.
"""

print("Test read function... Enter CTRL+C for exit.")
time.sleep(3)
try:
    while True:
        # Sample input register value for each 0.1 sec
        trimpot_value = psa0350_dimmer.read_input_registers(start_register_address=0x01, number_of_registers=2)

        # Refer to the datasheet of psa0350 device
        output_percentage  = trimpot_value[0]    # at address 0x01
        softstart_duration = trimpot_value[1]    # at address 0x02

        psa0350_dimmer.write_register(register_address=0x00, write_value=output_percentage)
        print("output_percentage={}%, softstart_duration={} sec".format(output_percentage, softstart_duration))

        time.sleep(0.1)
except KeyboardInterrupt:
    print("Demo program for modbus exit")
    exit(0)