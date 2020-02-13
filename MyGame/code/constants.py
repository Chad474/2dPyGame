import pygame

TITLE = 'Gravity'

BLOCK_SIZE = 32
SCREEN_WIDTH = 1024 # 32 * 32
SCREEN_HEIGHT = 576 # 32* 18
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

COLOR_KEY = (200,0,200)

MAX_FPS = 60

def split(frame, x, y, w, h):
    img = pygame.Surface([w, h])
    img.blit(frame, (0,0), (x, y, w, h))
    return img

