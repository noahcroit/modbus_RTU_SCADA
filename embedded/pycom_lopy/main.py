import pycom
import os
import time
import machine

from machine import ADC
from machine import Pin
from network import WLAN
from lib.uModbus.serial import Serial
from lib.uModBus.tcp    import TCP



"""
    Pycom's WiFi config function
    @Argument
    : config_mode
        - config_mode = "STA" -> To set a connection of LoPy as station mode or "STA" mode.
        - config_mode = "AP"  -> To set a connection of LoPy as access-point mode or "AP" mode. 
                                 SSID='wipy-wlan', auth=(WLAN.WPA2,'www.wipy.io'), channel=7, antenna=WLAN.INT_ANT
"""
def modbus_tcp_connection_init():

    # initialize lopy wifi object
    lopy_wlan = WLAN() 

    # config as station-mode 
    lopy_wlan.init(mode=WLAN.STA)
    lopy_wlan.ifconfig(id=0)

    # Scan for an available wifi and connect to "USR-WIFI232-604_27BC"
    ssid_usr_wifi232 =  "USR-WIFI232-604_27BC"  # ssid of usr-wifi module
    network_list = lopy_wlan.scan()
    for net in network_list:
        try:
            if net.ssid == ssid_usr_wifi232 :
                print("USR-WIFI232 founded! Connecting...")
            
                lopy_wlan.connect(ssid_usr_wifi232, timeout=5000)
                # wait for connection
                while not lopy_wlan.isconnected():
                    # do nothing or save power by idle using machine.idle()
                    machine.idle()

                print("Connection succeeded!")
                print(lopy_wlan.ifconfig())

                # lid LED to green color
                pycom.rgbled(0xFF00)
            else :
                # If SSID is not "USR-WIFI232-604_27BC", Do nothing.
                pass

        except Exception as e:
            print("Maybe, USR-WIFI232 access point is not avialable.")
            print("Exception : {}".format(e))

class modbus_pycom:
    def __init__(self, server_ssid="USR-WIFI232-604_27BC", connection_timeout=10):
        self.server_ssid = server_ssid
        self.timeout = connection_timeout
        self.wlan = WLAN()
    
    def connect(self):
         # config as station-mode 
        self.wlan.init(mode=WLAN.STA)
        self.wlan.ifconfig(id=0)

        # Scan for an available wifi and connect to server
        network_list = self.wlan.scan()
        for net in network_list:
            try:
                if net.ssid == self.server_ssid :
                    print("Server founded! Connecting...")
                
                    self.wlan.connect(self.server_ssid, timeout=5000)
                    # wait for connection
                    while not self.wlan.isconnected():
                        # do nothing or save power by idle using machine.idle()
                        machine.idle()

                    print("Connection succeeded!")
                    print(self.wlan.ifconfig())

                    # lid LED to green color
                    pycom.rgbled(0xFF00)
                else :
                    # If SSID is not "USR-WIFI232-604_27BC", Do nothing.
                    pass

            except Exception as e:
                print("Maybe, access point is not avialable.")
                print("Exception : {}".format(e))
        
    
############################################################# Main script #################################################################

# Disable heart beat LED and lid LED to red color
pycom.heartbeat(False)
pycom.rgbled(0x7f0000)

modbus = modbus_pycom()
modbus.connect()
#modbus_tcp_connection_init()

######################### RTU TCP MODBUS Initialize #########################
slave_ip = '10.10.100.254'
slave_port = 8899
timeout = 10
modbus_obj = TCP(slave_ip=slave_ip, slave_port=slave_port, timeout=timeout)

"""
    For Modbus RTU communication with PSA-03-50 Dimmer.


    Request to read status from input register,
    : Functional Code  = 0x04
    : Register address = 0x00 - 0x02
"""

#print("Send modbus request : Read input register...")
###################### READ INPUT REGISTERS ##################
#slave_addr=0x01
#starting_address=0x00
#register_quantity=2
#signed=True

#register_value = modbus_obj.read_input_registers(slave_addr, starting_address, register_quantity, signed)
#print('Input register value: ' + ' '.join('{:d}'.format(x) for x in register_value))
#print("Read finish.")

#print("Send modbus request : Write input register...")
###################### WRITE SINGLE REGISTER ##################
#slave_addr=0x01
#register_address=0x00
#register_value=0
#signed=True

#return_flag = modbus_obj.write_single_register(slave_addr, register_address, register_value, signed)
#output_flag = 'Success' if return_flag else 'Failure'
#print('Writing single coil status: ' + output_flag)

############################ Light Dimmer Trimpot Control ###############################
# LED state => dimmer loop
pycom.rgbled(0x0000FF)

# Initialize user button
user_button = Pin('P10', mode=Pin.IN, pull=Pin.PULL_UP)

# Initialize ADC
adc = ADC(id=0)
adc.init(bits=12)
adc_c = adc.channel(pin='P13', attn=ADC.ATTN_11DB)

while(user_button() == 1):
    # ADC sample
    adc_sample = adc_c.value()

    # ADC sample to percentage output conversion
    percentage = int(adc_sample/4096*100)
    if percentage > 100:
        percentage = 100

    time.sleep(0.1)

    # MODBUS write
    slave_addr=0x01
    register_address=0x00
    register_value = percentage
    signed=True
    
    return_flag = modbus_obj.write_single_register(slave_addr, register_address, register_value, signed)
    output_flag = 'Success' if return_flag else 'Failure'
    print('Writing single coil status: ' + output_flag + ": percentage output = {}".format(percentage))

pycom.rgbled(0x000000)
print("End task")