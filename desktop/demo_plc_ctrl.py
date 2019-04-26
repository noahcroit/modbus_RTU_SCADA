import modbus_umodbus
import time
import signal

plc_modbus_address_coil_write   = 1
plc_modbus_address_discrete_input = 0
plc_modbus_address_analog_input = 1

# For modbus RTU
#twido_plc = modbus_umodbus.device_rtu()
#twido_plc.config(device_id=0x01, port='COM16', baudrate=9600, signed_type=False)

# For modbus TCP
slave_ip = '192.168.2.77'
slave_port = 502
twido_plc = modbus_umodbus.device_tcp()
twido_plc.config(device_id=0x01, socket_ip=slave_ip, socket_port=slave_port, signed_type=True)

# Test write coil to PLC
try:
    while True:
        userInput = input("Enter 1 or 0 value to open or close PLC output %Q0.7: ")
        if userInput == '1':
            twido_plc.write_coil(coil_address=plc_modbus_address_coil_write, write_value=1)
        elif userInput == '0':
            twido_plc.write_coil(coil_address=plc_modbus_address_coil_write, write_value=0)
            
        time.sleep(1)

except KeyboardInterrupt:
    print("Exit demo program : Write coil")

# Test read PLC status data (read holding register & coil)
count = 0
read_coil = []
read_holding = []
try:
    while True:
        read_switch, read_potentiometer = twido_plc.read_holding_registers(start_register_address=plc_modbus_address_discrete_input, number_of_registers=2)
        time.sleep(0.1)
        if count == 5:
            read_coil = twido_plc.read_coils(start_coil_address=0, number_of_coils=2)
            count = 0
            time.sleep(0.1)

        time.sleep(1)
        count += 1
        print("")

except KeyboardInterrupt:
    print("Exit demo program : Read status data")
    exit(0)