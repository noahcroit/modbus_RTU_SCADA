#!/usr/bin/env python3
import modbus_umodbus


# Address for modbus
_TWIDO_PLC_START_ADDRESS_DISCRETE_INPUT_READ_1 = 0
_TWIDO_PLC_START_ADDRESS_COIL_READ  = 0
_TWIDO_PLC_START_ADDRESS_COIL_WRITE = 8
_TWIDO_PLC_START_ADDRESS_ANALOG_INPUT_READ  = 2

# Address for object : lightbulb_plc
_LIGHTBULB_1_READ_ADDRESS  = _TWIDO_PLC_START_ADDRESS_COIL_READ  + 3
_LIGHTBULB_1_WRITE_ADDRESS = _TWIDO_PLC_START_ADDRESS_COIL_WRITE + 3

class lightbulb_plc():

    def __init__(self, port_type=None):
        self.port_type = port_type
    
    def config(self, socket_ip='192.168.2.77', socket_port=502, comport='COM5', baud=9600, device_id=0x01):
        if self.port_type == 'modbus_tcp':
            self.socket_ip = socket_ip
            self.socket_port = socket_port
            self.device_id = device_id
            self.port = modbus_umodbus.device_tcp()
            self.port.config(device_id=self.device_id, socket_ip=self.socket_ip, socket_port=self.socket_port, signed_type=True)
        
        elif self.port_type == 'modbus_rtu':
            self.comport = comport
            self.baud = baud
            self.device_id = device_id
            self.port = modbus_umodbus.device_rtu()
        
    def read_switch_array(self):
        return self.port.read_holding_registers(start_register_address=_TWIDO_PLC_START_ADDRESS_DISCRETE_INPUT_READ_1, number_of_registers=1)
    
    def read_coil(self, coil=0, number_of_coil=1):
        return self.port.read_coils(start_coil_address=_TWIDO_PLC_START_ADDRESS_COIL_READ + coil, number_of_coils=number_of_coil)

    def write_coil(self, coil=0, write_value=0):
        self.port.write_coil(coil_address=_TWIDO_PLC_START_ADDRESS_COIL_WRITE + coil, write_value=write_value)
    
    def read_analog(self):
        return self.port.read_holding_registers(start_register_address=_TWIDO_PLC_START_ADDRESS_ANALOG_INPUT_READ, number_of_registers=2)
    
    def is_light_on(self):
        read = self.port.read_coils(start_coil_address=_LIGHTBULB_1_READ_ADDRESS, number_of_coils=1)
        if type(read) == list:
            read = read[0]

        if read > 0:
            return True
        else:
            return False
    
    def light_on(self):
        self.port.write_coil(coil_address=_LIGHTBULB_1_WRITE_ADDRESS, write_value=1)
    
    def light_off(self):
        self.port.write_coil(coil_address=_LIGHTBULB_1_WRITE_ADDRESS, write_value=0)