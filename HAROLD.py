#main imports
import os
import time
import csh_ldap
import requests
import pygame
import vlc
import serial
import LIGHT_BAR
import AUDIO_PROCESSING
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

LIGHT_BAR.setup_light_bar_gpio()
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
                UID = get_uid(ID)
                if UID == "mom":
                    play_music_pygame("aaa", 17, False)
                    break
                play_music_pygame("scanComplete", 3, False)
                break
            else:
                print("Waiting")
                continue
        #Dwonload te song from the s3_link
        get_s3_link(get_audiophiler(UID))
        #try to play music with pygame and if you can't play the music then quit the vlc process
        try:
            #play the music file with pygame for max of 30 seconds and also flush serial
            play_music_pygame("music", 30, True)
        #if music is unplayable in pygame, use vlc
        except Exception as e:
            print(e)

            os.system("ffmpeg -i music music.wav")
            play_music_pygame("music.wav", 30, True)

        finally:
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

#plays music till done or limit t has been reached
#last parameter dictates wheter or not the serial line is flushed at the end of the song
def play_music_pygame(music, t, flush_serial):
    pygame.mixer.music.load(music)
    pygame.mixer.music.play()
    while True:
        time = pygame.mixer.music.get_pos() / 1000
        if time = AUDIO_PROCESSING.get_beat_times()[0]:
            LIGHT_BAR.set_light_bar(LIGHT_BAR.get_random_gpio_state, LIGHT_BAR.get_random_gpio_state, LIGHT_BAR.get_random_gpio_state)
        if pygame.mixer.music.get_busy() == False or pygame.mixer.music.get_pos()/1000 > t:
            break
    if flush_serial:
        ser.flushInput()
    pygame.mixer.music.stop()
    LIGHT_BAR.reset()

#remove the music file from the directory
def delete_music():
    os.remove("music")
    os.remove("music.wav")

#run main
if __name__ == '__main__':
    main()
