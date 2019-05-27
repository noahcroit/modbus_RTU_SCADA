#!/usr/bin/env python3
import modbus_umodbus


""" Modbus address list for device LX2E_1212 and LX2E_0806 """
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
# Discrete Output : Read/Write (Use Auxillary Relay : M0, M1, ...)
_MODBUS_ADDRESS_WRITE_DISCRETE_OUTPUT_1 = 0
_MODBUS_ADDRESS_WRITE_DISCRETE_OUTPUT_2 = _MODBUS_ADDRESS_WRITE_DISCRETE_OUTPUT_1 + 1
_MODBUS_ADDRESS_WRITE_DISCRETE_OUTPUT_3 = _MODBUS_ADDRESS_WRITE_DISCRETE_OUTPUT_1 + 2
_MODBUS_ADDRESS_WRITE_DISCRETE_OUTPUT_4 = _MODBUS_ADDRESS_WRITE_DISCRETE_OUTPUT_1 + 3
# Analog Input : Read only (AI0, AI1, AI2, ...)
# Note : This cannot be used in device LX2E_0806
_MODBUS_ADDRESS_ANALOG_INPUT_1 = 0
_MODBUS_ADDRESS_ANALOG_INPUT_2 = _MODBUS_ADDRESS_ANALOG_INPUT_1 + 1
_MODBUS_ADDRESS_ANALOG_INPUT_3 = _MODBUS_ADDRESS_ANALOG_INPUT_1 + 2
_MODBUS_ADDRESS_ANALOG_INPUT_4 = _MODBUS_ADDRESS_ANALOG_INPUT_1 + 3

# LEDs (Write)
_MODBUS_ADDRESS_LED_WRITE_1 = _MODBUS_ADDRESS_WRITE_DISCRETE_OUTPUT_2
_MODBUS_ADDRESS_LED_WRITE_2 = _MODBUS_ADDRESS_WRITE_DISCRETE_OUTPUT_4
# LEDs (Read)
_MODBUS_ADDRESS_LED_READ_1 = _MODBUS_ADDRESS_READ_DISCRETE_OUTPUT_2
_MODBUS_ADDRESS_LED_READ_2 = _MODBUS_ADDRESS_READ_DISCRETE_OUTPUT_4
# Buttons (Read only)
_MODBUS_ADDRESS_BUTTON_1 = _MODBUS_ADDRESS_DISCRETE_INPUT_1
_MODBUS_ADDRESS_BUTTON_2 = _MODBUS_ADDRESS_DISCRETE_INPUT_3
# Potentiometer (Read only)
# Note : This cannot be used in device LX2E_0806
_MODBUS_ADDRESS_POTENTIOMETER_1 = _MODBUS_ADDRESS_ANALOG_INPUT_1
_MODBUS_ADDRESS_POTENTIOMETER_2 = _MODBUS_ADDRESS_ANALOG_INPUT_2
_MODBUS_ADDRESS_POTENTIOMETER_3 = _MODBUS_ADDRESS_ANALOG_INPUT_3
_MODBUS_ADDRESS_POTENTIOMETER_4 = _MODBUS_ADDRESS_ANALOG_INPUT_4
# Remote Control Enable
_MODBUS_ADDRESS_REMOTE_ENABLE = 50





""" Class : Wecon's PLC, LX2E_1212 with ADC Adaptor board """ 
class device_lx2e_1212():

    def __init__(self, port_type=None):
        self.port_type = port_type
    
    def config(self, socket_ip='192.168.2.99', socket_port=502, comport='COM5', baud=9600, device_id=0x01):
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
        
    def read_led_status(self, led=1):
        """
            @Argument :
                led (int) : LED number. (led1 = 1, led2 = 2)
            @Return :
                read_value (int) : LED status (on = 1, off = 0)
        """
        if led == 1:
            read_value = self.port.read_coils(start_coil_address=_MODBUS_ADDRESS_LED_READ_1, number_of_coils=1)
        elif led == 2:
            read_value = self.port.read_coils(start_coil_address=_MODBUS_ADDRESS_LED_READ_2, number_of_coils=1)

        if type(read_value) == list:
            read_value = read_value[0]
        return read_value
    
    def read_potentiometer(self, channel=1):
        """
            @Argument :
                channnel (int) : Potentiometer number. (channnel = 1,2,3,4)
            @Return :
                read_value (int) : analog value of potentiometer
        """
        if channel == 1:
            read_value = self.port.read_holding_registers(start_register_address=_MODBUS_ADDRESS_POTENTIOMETER_1, number_of_registers=1)
        elif channel == 2:
            read_value = self.port.read_holding_registers(start_register_address=_MODBUS_ADDRESS_POTENTIOMETER_2, number_of_registers=1)
        elif channel == 3:
            read_value = self.port.read_holding_registers(start_register_address=_MODBUS_ADDRESS_POTENTIOMETER_3, number_of_registers=1)
        elif channel == 4:
            read_value = self.port.read_holding_registers(start_register_address=_MODBUS_ADDRESS_POTENTIOMETER_4, number_of_registers=1)

        if type(read_value) == list:
            read_value = read_value[0]
        return read_value

    def write_led_status(self, led=1, led_value=0):
        """
            @Argument :
                led (int) : LED number. (led1 = 1, led2 = 2)
                led_value (int) : LED value (1 = ON, 0 = OFF)
            @Return :
                No return
        """
        if led == 1:
            self.port.write_coil(coil_address=_MODBUS_ADDRESS_LED_WRITE_1, write_value=led_value)
        elif led == 2:
            self.port.write_coil(coil_address=_MODBUS_ADDRESS_LED_WRITE_2, write_value=led_value)
    
    def remote_control_enable(self):
        self.port.write_coil(coil_address=_MODBUS_ADDRESS_REMOTE_ENABLE, write_value=1)
    
    def remote_control_disable(self):
        self.port.write_coil(coil_address=_MODBUS_ADDRESS_REMOTE_ENABLE, write_value=0)





""" Class : Wecon's PLC, LX2E_0806 """ 
class device_lx2e_0806():

    def __init__(self, port_type=None):
        self.port_type = port_type
    
    def config(self, socket_ip='192.168.2.99', socket_port=502, comport='COM5', baud=9600, device_id=0x01):
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
        
    def read_led_status(self, led=1):
        """
            @Argument :
                led (int) : LED number. (led1 = 1, led2 = 2)
            @Return :
                read_value (int) : LED status (on = 1, off = 0)
        """
        if led == 1:
            read_value = self.port.read_coils(start_coil_address=_MODBUS_ADDRESS_LED_READ_1, number_of_coils=1)
        elif led == 2:
            read_value = self.port.read_coils(start_coil_address=_MODBUS_ADDRESS_LED_READ_2, number_of_coils=1)

        if type(read_value) == list:
            read_value = read_value[0]
        return read_value

    def write_led_status(self, led=1, led_value=0):
        """
            @Argument :
                led (int) : LED number. (led1 = 1, led2 = 2)
                led_value (int) : LED value (1 = ON, 0 = OFF)
            @Return :
                No return
        """
        if led == 1:
            self.port.write_coil(coil_address=_MODBUS_ADDRESS_LED_WRITE_1, write_value=led_value)
        elif led == 2:
            self.port.write_coil(coil_address=_MODBUS_ADDRESS_LED_WRITE_2, write_value=led_value)
    
    def remote_control_enable(self):
        self.port.write_coil(coil_address=_MODBUS_ADDRESS_REMOTE_ENABLE, write_value=1)
    
    def remote_control_disable(self):
        self.port.write_coil(coil_address=_MODBUS_ADDRESS_REMOTE_ENABLE, write_value=0)