# -*- coding: utf-8 -*-
"""
Fuga Doce - Sweet Escape
Funçoes das telas de menu
"""
import pygame
import os
from pygame.locals import *
from configs import *

# Carregando imagens do Menu
menu_img = pygame.image.load('imagens/Inicio1.png')
menu_img1 = pygame.image.load('imagens/Inicio2.png')
menu_img2 = pygame.image.load('imagens/Inicio3.png')
eng_img = pygame.image.load('imagens/GameOver.png')


def MenuInicial(window):
    """
    Define tela de menu inicial
    """
    marcador = True

    # ===== Loop principal =====
    while marcador:
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
    """
    Define tela de menu de contexto da historia
    """
    marcador1 = True

    # ===== Loop principal =====
    while marcador1:
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

        # ----- Atualiza estado do jogo
        pygame.display.update()  # Mostra o novo frame para o jogador

def MenuInicial3(window):
    """
    Define tela de menu de instruções
    """
    marcador2 = True
    # ===== Loop principal =====
    while marcador2:
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

        # ----- Atualiza estado do jogo
        pygame.display.update()  # Mostra o novo frame para o jogador

def end_screen(window, pontuacao):
    """
    Define tela do game over
    """
    marcador3 = True
    # ===== Loop principal =====
    while marcador3:
        # ----- Trata eventos
        clock = pygame.time.Clock()
        window.blit(eng_img, (0,0))
        font = pygame.font.Font('fontes/Stabillo Medium.ttf', 30)
        text_window = font.render("Sua pontuação foi: {:08d}".format(pontuacao), True, (255, 0, 0))
        text_rect = text_window.get_rect()
        text_rect.midtop = (WIDTH / 2,  10)
        window.blit(text_window, text_rect)
        
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
            
            # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_DOWN:
                    dado = False
                    return QUIT
            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                
                if event.key == pygame.K_DOWN:
                    dado = False
                    return QUIT

        # ----- Atualiza estado do jogo
        pygame.display.update()  # Mostra o novo frame para o jogador
