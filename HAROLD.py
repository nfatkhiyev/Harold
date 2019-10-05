import os
import time
import RPi.GPIO as GPIO

os.system('modprobe wire timeout=1 slave_ttl=5')
os.system('modprobe w1-gpio')
os.system('modprobe w1-smem')
os.system('chmod a+w /sys/devices/w1_bus_master1/w1_master_slaves')
os.system('chmod a+w /sys/devices/w1_bus_master1/w1_master_remove')
os.system('chmod a+w /sys/devices/w1_bus_master1/w1_master_search')
base_dir = '/sys/devices/w1_bus_master1/w1_master_slaves'
delete_dir = '/sys/devices/w1_bus_master1/w1_master_remove'

def main():
    while True:
        f = open(base_dir, "r")
        ID = f.read()
        f.close()
        time.sleep(1)
        if ID != 'not found.\n':
            print(ID)
            d = open(delete_dir, "w")
            d.write(ID)
            break
        else:
            print("Waiting")

    print("FINISHED")

if __name__ == '__main__':
    main()
        