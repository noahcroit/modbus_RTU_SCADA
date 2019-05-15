import pyb
import machine
import time
import network
from lib.uModbus.serial import Serial
from lib.uModBus.tcp    import TCP


def main():
        
        wlan_ap = network.WLAN(network.AP_IF)
        wlan_ap.config(essid='pyboard_D')
        print(wlan_ap.config('authmode'))
        
        wlan_ap.active(True)

        
                

if __name__ == '__main__':
        main()