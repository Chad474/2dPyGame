import pygame, os, sys, code.constants
from code.menu import Main_Menu

def main():
    pygame.init()
    pygame.display.set_caption(code.constants.TITLE)
    Main_Menu()
    pygame.quit()
main()