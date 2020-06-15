import pygame
import random
from configs import WIDTH, HEIGHT, INIT, GAME, QUIT
from teste_v2 import game_screen
from teste_v1 import tela1
from menu import *

pygame.init()

tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fuga Doce")

state = INIT
while state != QUIT:
    if state == INIT:
        state = MenuInicial(tela)
    elif state == INIT2:
        state = MenuInicial2(tela)
    elif state == INIT3:
        state = MenuInicial3(tela)
    elif state == GAME:
        state = game_screen(tela)
    elif state == END:
        state = end_screen(tela)
    else:
        state = QUIT