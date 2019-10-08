#main imports
import os
import time
import csh_ldap
import requests
import pygame
import vlc
from pygame import mixer
import RPi.GPIO as GPIO

#import the config file
import config

#set config password
sudoPassword = config.SUDO_PASSWORD

#setup I-Button paths
os.system('echo %s|sudo modprobe wire timeout=1 slave_ttl=5' % (sudoPassword))
os.system('echo %s|sudo modprobe w1-gpio' % (sudoPassword))
os.system('echo %s|sudo modprobe w1-smem' % (sudoPassword))
os.system('echo %s|sudo chmod a+w /sys/devices/w1_bus_master1/w1_master_slaves' % (sudoPassword))
os.system('echo %s|sudo chmod a+w /sys/devices/w1_bus_master1/w1_master_remove' % (sudoPassword))
os.system('echo %s|sudo chmod a+w /sys/devices/w1_bus_master1/w1_master_search' % (sudoPassword))
base_dir = '/sys/devices/w1_bus_master1/w1_master_slaves'
delete_dir = '/sys/devices/w1_bus_master1/w1_master_remove'

#create an instance
instance = csh_ldap.CSHLDAP("uid=nfatkhiyev,cn=users,cn=accounts,dc=csh,dc=rit,dc=edu", config.PASSWORD)

#authentication config file
HAROLD_AUTH = config.harold_auth

pygame.mixer.init()

timeNow = time.localtime()

#main function
def main():
    ID = ""
    volume = 0.0
    #keep the whole program running so it doesn't play one song and stop
    while True:
        #while loop per song
        while True:
            if 23 >= timeNow.tm_hour >= 7:
                volume = 0.5
            else:
                volume = 0.15
            #read the file and set the ID to the I-Button that was read 
            time.sleep(0.5)
            f = open(base_dir, "r")
            ID = f.readline()
            time.sleep(0.1)
            f.close()
            #if I-Button is found play music
            if ID != 'not found.\n':
                print(ID)
                pygame.mixer.music.load("scanComplete")
                pygame.mixer.music.play()
                time.sleep(3)
                pygame.mixer.music.set_volume(volume)
                #add the found I-Button to the base directory
                while True:
                    f2 = open(base_dir, "r")
                    test = f2.readline()
                    f2.close()
                    if test != 'not found.\n':
                        d = open(delete_dir, "w")
                        d.write(test)
                        continue
                    else:
                        print("iButton read file is clean")
                        break
                break
            else:
                print("Waiting")

        #play the music from the I-Button that currently exists in the base directory
        ID = "*" + ID[3:].strip() + "01"
        gets3Link(getAudiophiler(getUID(ID)))
        #try to play music and if you can't play the music then quit the vlc process
        try:
            #load the music
            pygame.mixer.music.load("music")
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(volume)
            #play the music for thirty seconds
            while True:
                if pygame.mixer.music.get_busy() == False or pygame.mixer.music.get_pos()/1000 > 30:
                    break
            #stop the music
            pygame.mixer.music.stop()
            #delete the music file from the root directory
            deleteMusic()
        except Exception as e:
            #os.system('vlc --stop-time 30 music --sout-al vlc://quit')
            print(e)
            player2 = vlc.MediaPlayer("/home/pi/Harold/music")
            player2.play()
            time.sleep(30)
            player2.stop()
            deleteMusic()

        #reset variables
        ID = ""
        print("FINISHED")

#getUID with the I-Button as an arg
def getUID(iButtonCode):
    user = instance.get_member_ibutton(iButtonCode)
    UID = user.uid
    return UID

#getAudiophiler with UID as an arg
def getAudiophiler(UID):
    getHaroldURL = "https://audiophiler.csh.rit.edu/get_harold/" + UID
    params = {
        'auth_key':HAROLD_AUTH
    }
    try:
        s3Link = requests.post(url = getHaroldURL, json = params)
        print(s3Link.text)
        return s3Link.text
    except Exception as e:
        print(e)
        getDefaultURL = "https://audiophiler.csh.rit.edu/get_harold/nfatkhiyev" 
        paramsD = {
            'auth_key':HAROLD_AUTH
        }
        defaultLink = requests.post(url = getDefaultURL, json = paramsD)
        return defaultLink.text

#gets3Link with the Link as an arg
def gets3Link(link):
    try:
        music = requests.get(link, allow_redirects=True)
        open('music', 'wb').write(music.content)
    except:
        music = requests.get(getAudiophiler("nfatkhiyev"), allow_redirects=True)
        open('music', 'wb').write(music.content)

#remove the music file from the directory
def deleteMusic():
    os.remove("music")

#run main
if __name__ == '__main__':
    main()
