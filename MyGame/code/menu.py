import pygame, game
from constants import MAX_FPS, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN, COLOR_KEY

class Main_Menu():
    def __init__(self):
        QUIT = False
        while not QUIT:
            QUIT = start_menu()
def help_menu():
    help_img = pygame.image.load('images/menu/help_menu.png').convert()
    help_img.set_colorkey(COLOR_KEY)
    help_rect = help_img.get_rect()
    help_pos = (0,0)    
    clock = pygame.time.Clock()
    EXIT = False
    
    while not EXIT:
        SCREEN.blit(help_img, help_pos)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return False
        clock.tick(MAX_FPS)

def start_game():
    clock = pygame.time.Clock()
    QUIT = False
    HELP = False
    MAIN = False
    level = 0
        
    while not QUIT:
        QUIT, HELP, MAIN, level = game.Play(level)
        if QUIT:
            return True
        elif MAIN:
            return False
        elif HELP:
            HELP = help_menu()
        clock.tick(MAX_FPS)
        
def pause_menu(paused_screen):
    pause_img = pygame.image.load('images/menu/pause_menu.png').convert()
    pause_img.set_colorkey(COLOR_KEY)    
    pause_rect = pause_img.get_rect()
    pause_pos = (SCREEN_WIDTH/2 - pause_rect.w/2 , SCREEN_HEIGHT/2 - pause_rect.h/2)
    
    menu_list = [(282,108), (282,216), (282,330)]
    
    select_button = pygame.image.load('images/menu/startMenu_btnSelect.png').convert()
    select_button.set_colorkey(COLOR_KEY)
    
    select_state = 0
    
    clock = pygame.time.Clock()
    PAUSE = True
    
    while PAUSE:
        SCREEN.blit(paused_screen, (0,0))
        SCREEN.blit(pause_img, pause_pos)
        SCREEN.blit(select_button, menu_list[select_state])
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if select_state == 0:
                        return 'Continue'
                    elif select_state == 1:
                        return help_menu()
                    elif select_state == 2:
                        return 'Main'
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if select_state == 0:
                        select_state = 1
                    elif select_state == 1:
                        select_state = 2
                    elif select_state == 2:
                        select_state = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if select_state == 0:
                        select_state = 2
                    elif select_state == 1:
                        select_state = 0
                    elif select_state == 2:
                        select_state = 1
        clock.tick(MAX_FPS) 

def start_menu():
    background = pygame.image.load('images/background/sky1.png').convert()
    startMenu_img = pygame.image.load('images/menu/start_menu.png').convert()
    startMenu_img.set_colorkey(COLOR_KEY)
    startMenu_rect = startMenu_img.get_rect()
    startMenu_pos = (SCREEN_WIDTH/2 - startMenu_rect.w/2 , SCREEN_HEIGHT/2 - startMenu_rect.h/2)
    
    menu_list = [(282,108), (282,216), (282,330)]
    
    select_button = pygame.image.load('images/menu/startMenu_btnSelect.png').convert()
    select_button.set_colorkey(COLOR_KEY)
    
    select_state = 0
    
    clock = pygame.time.Clock()
    	
    QUIT = False
     
    while not QUIT:
        SCREEN.blit(background, (0,0))
        SCREEN.blit(startMenu_img, startMenu_pos)
        SCREEN.blit(select_button, menu_list[select_state])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    QUIT = True
                elif event.type == pygame.QUIT:
                    QUIT = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if select_state == 0:
                            QUIT = start_game()
                        elif select_state == 1:
                            QUIT = help_menu()
                        elif select_state == 2:
                            QUIT = True
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if select_state == 0:
                            select_state = 1
                        elif select_state == 1:
                            select_state = 2
                        elif select_state == 2:
                            select_state = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        if select_state == 0:
                            select_state = 2
                        elif select_state == 1:
                            select_state = 0
                        elif select_state == 2:
                            select_state = 1
        clock.tick(MAX_FPS)
    return True