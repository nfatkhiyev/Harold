#main imports
import os
import time
import csh_ldap
import requests
import pygame
import vlc
import serial
from pygame import mixer
import RPi.GPIO as GPIO

#import the config file
import config

#set config password
sudoPassword = config.SUDO_PASSWORD

#setup Serial Coms
ser = serial.Serial('/dev/ttyACM0',9600)

#create an instance
instance = csh_ldap.CSHLDAP(config.LDAP_BIND_DN, config.PASSWORD)

#authentication config file
HAROLD_AUTH = config.harold_auth

pygame.mixer.init()

time_now = time.localtime()

max_counter = 0
#main function
def main():
    ID = ""
    #keep the whole program running so it doesn't play one song and stop
    while True:
        #while loop per song
        while True:
            if 23 >= time_now.tm_hour >= 7:
                os.system("amixer set Master 73%")
            else:
                os.system("amixer set Master 20%")
            
            #if I-Button is found play scanComplete
            if ser.in_waiting > 6:
                ID = ser.readline().decode('ascii')
                ser.flushInput()
                if ID is None or 'ready' in ID:
                    print("Waiting")
                    continue
                print(ID)
                #Strip the read id of the family code and replaces it with star
                ID = "*" + ID[2:].strip()
                if get_uid(ID) == "mom":
                    pygame.mixer.music.load("aaa")
                    pygame.mixer.music.play()
                    time.sleep(15)
                    pygame.mixer.music.stop()
                    break
                pygame.mixer.music.load("scanComplete")
                pygame.mixer.music.play()
                time.sleep(3)
                break
            else:
                print("Waiting")
                continue

        #Dwonload te song from the s3_link
        get_s3_link(get_audiophiler(get_uid(ID)))
        #try to play music and if you can't play the music then quit the vlc process
        try:
            #load the music
            pygame.mixer.music.load("music")
            pygame.mixer.music.play()
            #play the music for thirty seconds
            while True:
                if pygame.mixer.music.get_busy() == False or pygame.mixer.music.get_pos()/1000 > 30:
                    break
            #stop the music
            ser.flushInput()
            pygame.mixer.music.stop()
            #delete the music file from the root directory
            delete_music()
        except Exception as e:
            print(e)
            player2 = vlc.MediaPlayer("/home/pi/Harold/music")
            player2.play()
            time.sleep(30)
            ser.flushInput()
            player2.stop()
            delete_music()

        #reset variables
        ID = ""
        print("FINISHED")

#getUID with the I-Button as an arg
def get_uid(iButtonCode):
    user = instance.get_member_ibutton(iButtonCode)
    UID = user.uid
    return UID

#getAudiophiler with UID as an arg
def get_audiophiler(UID):
    get_harold_url = "https://audiophiler.csh.rit.edu/get_harold/" + UID
    params = {
        'auth_key':HAROLD_AUTH
    }
    try:
        s3_link = requests.post(url = get_harold_url, json = params)
        print(s3_link.text)
        return s3_link.text
    except Exception as e:
        print(e)
        return "getAudiophiler ERROR"

#gets3Link with the Link as an arg
def get_s3_link(link):
    try:
        music = requests.get(link, allow_redirects=True)
        open('music', 'wb').write(music.content)
    except Exception as e:
        print(e)
        return "gets3Link ERROR"

#remove the music file from the directory
def delete_music():
    os.remove("music")

#run main
if __name__ == '__main__':
    main()
