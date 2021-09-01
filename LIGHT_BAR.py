import time
import RPi.GPIO as GPIO
import random

RED_GPIO = 17
GREEN_GPIO = 22
BLUE_GPIO = 27

def setup_light_bar_gpio():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(RED_GPIO, GPIO.OUT)
    GPIO.setup(GREEN_GPIO, GPIO.OUT)
    GPIO.setup(BLUE_GPIO, GPIO.OUT)

    GPIO.output(RED_GPIO, GPIO.LOW)
    GPIO.output(GREEN_GPIO, GPIO.LOW)
    GPIO.output(BLUE_GPIO, GPIO.LOW)

def get_random_gpio_state():
    random_boolean = bool(random.getrandbits(1))
    if random_boolean:
        return GPIO.HIGH
    return GPIO.LOW

def set_light_bar(red_state, green_state, blue_state):
    GPIO.output(RED_GPIO, red_state)
    GPIO.output(GREEN_GPIO, green_state)
    GPIO.output(BLUE_GPIO, blue_state)

def reset():
    GPIO.output(RED_GPIO, GPIO.LOW)
    GPIO.output(GREEN_GPIO, GPIO.LOW)
    GPIO.output(BLUE_GPIO, GPIO.LOW)