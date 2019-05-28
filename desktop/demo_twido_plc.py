from lightbulb_ctrl_twido import lightbulb_plc
import time
import signal



def main():

    # Device initialize
    device = lightbulb_plc(port_type='modbus_tcp')
    device.config(socket_ip='192.168.2.77', socket_port=502, device_id=0x01)

    """
        Test read/write an output coil of Twido PLC. 
        User input a coil number (from 0 to 7) to toggle the status of the selected coil.
    """
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



    """
        Test lightbulb control by using turn on/off function
    """
    try:
        print("Enter \"1\" to turn on, \"0\" to turn off or 'q' for exit.")
        exit_flag = 0
        while exit_flag == 0:
            user_input = input(" : ")
            if user_input != 'q':
                if user_input == '1':
                    device.light_on()
                elif user_input == '0':
                    device.light_off()
            else:
                exit_flag = 1
        
    except KeyboardInterrupt:
        print("Exit demo program : CTRL lightbulb")



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