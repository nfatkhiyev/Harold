import LIGHT_BAR
import time
from pygame import mixer

LIGHT_BAR.setup_light_bar_gpio()

LIGHT_BAR.reset()

pygame.mixer.init()


def main():
    pygame.mixer.music.load('duck')
    pygame.mixer.music.load.play()

    while True:
        LIGHT_BAR.set_light_bar(LIGHT_BAR.get_random_gpio_state(), LIGHT_BAR.get_random_gpio_state(), LIGHT_BAR.get_random_gpio_state())
        time.sleep(0.2)

if __name__ == '__main__':
    main()
