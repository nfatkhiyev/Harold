import LIGHT_BAR
import time

LIGHT_BAR.setup_light_bar_gpio()

LIGHT_BAR.reset()

def main():
    while True:
        LIGHT_BAR.set_light_bar(LIGHT_BAR.get_random_gpio_state(), LIGHT_BAR.get_random_gpio_state(), LIGHT_BAR.get_random_gpio_state())
        time.sleep(0.2)

if __name__ == '__main__':
    main()
