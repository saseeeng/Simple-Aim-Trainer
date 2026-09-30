import pygame

from game import Game


def main():
    pygame.init()
    try:
        Game().run()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()