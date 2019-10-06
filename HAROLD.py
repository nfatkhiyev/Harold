import os
import time
import csh_ldap
import requests
import pygame
import RPi.GPIO as GPIO

#from urllib import urlencode
import config

sudoPassword = config.SUDO_PASSWORD

os.system('echo %s|sudo modprobe wire timeout=1 slave_ttl=5' % (sudoPassword))
os.system('echo %s|sudo modprobe w1-gpio' % (sudoPassword))
os.system('echo %s|sudo modprobe w1-smem' % (sudoPassword))
os.system('echo %s|sudo chmod a+w /sys/devices/w1_bus_master1/w1_master_slaves' % (sudoPassword))
os.system('echo %s|sudo chmod a+w /sys/devices/w1_bus_master1/w1_master_remove' % (sudoPassword))
os.system('echo %s|sudo chmod a+w /sys/devices/w1_bus_master1/w1_master_search' % (sudoPassword))
base_dir = '/sys/devices/w1_bus_master1/w1_master_slaves'
delete_dir = '/sys/devices/w1_bus_master1/w1_master_remove'

instance = csh_ldap.CSHLDAP("uid=nfatkhiyev,cn=users,cn=accounts,dc=csh,dc=rit,dc=edu", config.PASSWORD)

HAROLD_AUTH = config.harold_auth

pygame.mixer.init()

def main():
    ID = ""
    while True:
        while True: 
            time.sleep(0.5)
            f = open(base_dir, "r")
            ID = f.read()
            f.close()
            if ID != 'not found.\n':
                print(ID)
                d = open(delete_dir, "w")
                d.write(ID)
                break
            else:
                print("Waiting")

        ID = "*" + ID[3:].strip() + "01"
        print(ID)
        gets3Link(getAudiophiler(getUID(ID)))
        pygame.mixer.music.load("music")
        pygame.mixer.music.play()
        while True:
            if pygame.mixer.get_busy() != True:
                break
            else:
                print("busy")
        pygame.mixer.music.stop()
        deleteMusic()
        ID =""
        print("FINISHED")


def getUID(iButtonCode):
    user = instance.get_member_ibutton(iButtonCode)
    UID = user.uid
    return UID

def getAudiophiler(UID):
    getHaroldURL = "https://audiophiler.csh.rit.edu/get_harold/" + UID
    params = {
        'auth_key':HAROLD_AUTH
    }
    try:
        s3Link = requests.post(url = getHaroldURL, json = params)
        print(s3Link.text)
        return s3Link.text
    except:
        print(e)
        getDefaultURL = "https://audiophiler.csh.rit.edu/get_harold/nfatkhiyev" 
        paramsD = {
            'auth_key':HAROLD_AUTH
        }
        defaultLink = requests.post(url = getDefaultURL, json = paramsD)
        return defaultLink.text

def gets3Link(link):
    music = requests.get(link, allow_redirects=True)
    open('music', 'wb').write(music.content)

def deleteMusic():
    os.remove("music")

if __name__ == '__main__':
    main()
        
