import modbus_umodbus
import time
import signal

_TWIDO_PLC_START_ADDRESS_DISCRETE_INPUT_READ_1 = 0
_TWIDO_PLC_START_ADDRESS_COIL_READ  = 0
_TWIDO_PLC_START_ADDRESS_COIL_WRITE = 8
_TWIDO_PLC_START_ADDRESS_ANALOG_INPUT_READ  = 2

class light_controller_twido_plc():

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
        number_of_lightbulb = 1
        plc_outputpin_for_lightbulb = 2
        read = self.port.read_coils(start_coil_address=_TWIDO_PLC_START_ADDRESS_COIL_READ + plc_outputpin_for_lightbulb, number_of_coils=number_of_lightbulb)
        if type(read) == list:
            read = read[0]

        if read > 0:
            return True
        else:
            return False
    
    def light_on(self):
        self.port.write_coil(coil_address=_TWIDO_PLC_START_ADDRESS_COIL_WRITE + 2, write_value=1)
    
    def light_off(self):
        self.port.write_coil(coil_address=_TWIDO_PLC_START_ADDRESS_COIL_WRITE + 2, write_value=0)



def main():

    # Device initialize
    device = light_controller_twido_plc(port_type='modbus_tcp')
    device.config(socket_ip='192.168.2.77', socket_port=502, device_id=0x01)

    """
        Test read/write an output coil of Twido PLC. 
        User input a coil number (from 0 to 7) to toggle the status of the selected coil.
    """
    try:
        print("Enter PLC's coil number (from 0-7) to toggle, or 'q' for exit")
        exit_flag = 0
        while exit_flag == 0:
            selected_coil = input(" : ")
            if selected_coil != 'q':
                selected_coil = int(selected_coil)
                tmp = device.read_coil(coil=selected_coil)
                tmp = tmp[0]
                if tmp == 0:
                    device.write_coil(coil=selected_coil, write_value=1)
                else:
                    device.write_coil(coil=selected_coil, write_value=0)
            else:
                exit_flag = 1
        
    except KeyboardInterrupt:
        print("Exit demo program : Write coil")
    


    """
        Test read switch state, analog input & light bulb state from PLC 
    """
    try:
        while True:
            #discrete_inputs = twido_plc.read_holding_registers(start_register_address=plc_modbus_address_discrete_input_1, number_of_registers=2)
            switch_value = device.read_switch_array()
            analog_value = device.read_analog()
            tmp = device.is_light_on()
            if tmp:
                light_state = 'ON'
            else:
                light_state = 'OFF'

            print("switch={},\tanalog={},\tlight bulb={}".format(switch_value, analog_value, light_state))
            time.sleep(1)

    except KeyboardInterrupt:
        print("Exit demo program : Read status data")
        exit(0)



if __name__ == '__main__':
    main()
    exit(0)