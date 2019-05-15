# main.py -- put your code here!
import pyb
import machine
import time
from network import WLAN
from lib.uModbus.serial import Serial
from lib.uModBus.tcp    import TCP


""" Initialize hardware object """
# user switch
user_button = pyb.Switch()

# user LED
led_red = pyb.LED(1)
led_green = pyb.LED(2)

"""
    Pycom's WiFi config function
    @Argument
    : config_mode
        - config_mode = "STA" -> To set a connection of LoPy as station mode or "STA" mode.
        - config_mode = "AP"  -> To set a connection of LoPy as access-point mode or "AP" mode. 
                                 SSID='wipy-wlan', auth=(WLAN.WPA2,'www.wipy.io'), channel=7, antenna=WLAN.INT_ANT
"""
class wifi_pyboard():
    
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
                else :
                    # If SSID is not "USR-WIFI232-604_27BC", Do nothing.
                    pass

            except Exception as e:
                print("Maybe, access point is not avialable.")
                print("Exception : {}".format(e))


def main():
        led_red.on()
        led_green.off()
        wifi = wifi_pyboard()
        wifi.connect()
        led_red.off()
        led_green.on()
                

if __name__ == '__main__':
        main()


 