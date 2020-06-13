import pygame
import os
from pygame.locals import *

menu_img = pygame.image.load('imagens/tela_1.jpeg')
menu_img1 = pygame.image.load('imagens/tela_2.jpeg')
menu_img2 = pygame.image.load('imagens/tela_3.jpeg')
eng_img = pygame.image.load('imagens/Fuga Doce (4).png')

INIT = 3
INIT2 = 4
INIT3 = 5
GAME = 6
END = 7
QUIT = 8


def MenuInicial(window):

    casa = True

    # ===== Loop principal =====
    while casa:
        # ----- Trata eventos
        clock = pygame.time.Clock()
        window.blit(menu_img, (0,0))

        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
            
            # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_RETURN:
                    casa = False
                    return INIT2

            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                
                if event.key == pygame.K_RETURN:
                    casa = False
                    return INIT2

        # ----- Gera saídas
        #window.fill((0, 0, 255))  # Preenche com a cor branca

        # ----- Atualiza estado do jogo
        pygame.display.update()  # Mostra o novo frame para o jogador

def MenuInicial2(window):

    bola = True

    # ===== Loop principal =====
    while bola:
        # ----- Trata eventos
        clock = pygame.time.Clock()
        window.blit(menu_img1, (0,0))

        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
            
            # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_SPACE:
                    bola = False
                    return INIT3

            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                
                if event.key == pygame.K_SPACE:
                    bola = False
                    return INIT3
        # ----- Gera saídas
        #window.fill((0, 0, 255))  # Preenche com a cor branca

        # ----- Atualiza estado do jogo
        pygame.display.update()  # Mostra o novo frame para o jogador

def MenuInicial3(window):

    amor = True
    # ===== Loop principal =====
    while amor:
        # ----- Trata eventos
        clock = pygame.time.Clock()
        window.blit(menu_img2, (0,0))

        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
            
            # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_RIGHT:
                    amor = False
                    return GAME
            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                
                if event.key == pygame.K_RIGHT:
                    amor = False
                    return GAME
        

        # ----- Gera saídas
        #window.fill((0, 0, 255))  # Preenche com a cor branca

        # ----- Atualiza estado do jogo
        pygame.display.update()  # Mostra o novo frame para o jogador

def end_screen(window):

    dado = True
    # ===== Loop principal =====
    while dado:
        # ----- Trata eventos
        clock = pygame.time.Clock()
        window.blit(eng_img, (0,0))

        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
            
            # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_p:
                    dado = False
                    return QUIT
            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                
                if event.key == pygame.K_p:
                    dado = False
                    return QUIT
        

        # ----- Gera saídas
        #window.fill((0, 0, 255))  # Preenche com a cor branca

        # ----- Atualiza estado do jogo
        pygame.display.update()  # Mostra o novo frame para o jogador

	