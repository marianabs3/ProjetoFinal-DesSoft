# -*- coding: utf-8 -*-
import pygame
import os
from pygame.locals import *

pygame.init()

# Tamanho da tela
WIDTH = 1100
HEIGHT = 500
JUMP_SIZE = 30
SPEED = 10
GRAVITY = 2
GROUND = HEIGHT * 5 // 6

STILL = 0
JUMPING = 1
FALLING = 2

# Define classe da personagem principal
class Vanellope(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        # Armazena imagens de movimento em uma lista
        self.images = [pygame.image.load('penelope_move0.png').convert_alpha(),
                       pygame.image.load('penelope_move1.png').convert_alpha(),
                       pygame.image.load('penelope_move2.png').convert_alpha()]

        self.imagem_atual = 0
        self.state = STILL
        self.speed = SPEED
        self.speedx = 0
        self.speedy = 0

        self.image = pygame.image.load('penelope_frente.png').convert_alpha()
        
        # Redimensiona imagem
        self.rect = self.image.get_rect()
        self.rect[0] = 100
        self.rect[1] = 284
    
    # Define o movimento de pular 
    def jump(self):
        if self.state == STILL:
            self.speedy -= JUMP_SIZE
            self.state = JUMPING
        
    # Carrega as informações
    def update(self):
        
        self.rect.x += self.speedx
        self.speedy += GRAVITY
        
        if self.speedy > 0:
            self.state = FALLING
        self.rect.y += self.speedy

        if self.rect.bottom > GROUND:
            self.rect.bottom = GROUND
            self.speedy = 0
            self.state = STILL

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:   
            self.rect.left = 0

        # Percorre lista das imagens e cria animação
        self.imagem_atual = (self.imagem_atual + 1) % 2  # Volta para imagem 0 da lista
        self.image = self.images[ self.imagem_atual ]

        # Atualiza a imagem quando personagem está parado
        if self.speedx == 0:
            self.image =  pygame.image.load('penelope_frente.png').convert_alpha()

        # Atualiza imagem quando personagem está pulando
        if self.speedy != 0:
            self.image = pygame.image.load('penelope_jump.png').convert_alpha()

# Cria a tela
tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Vanellope")

# Carrega imagem de fundo
background = pygame.image.load('fundo2.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Cria grupo de sprites da personagem principal
van_group = pygame.sprite.Group()
vanellope = Vanellope()
van_group.add(vanellope)

# Função de tempo de animação   
clock = pygame.time.Clock()

# Loop principal do jogo
game = True

while game:
    clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game == False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
           
           # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                vanellope.speedx -= 4
            if event.key == pygame.K_RIGHT:
                vanellope.speedx += 4
        
        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                vanellope.speedx += 4
            if event.key == pygame.K_RIGHT:
                vanellope.speedx -= 4
            if event.key == pygame.K_UP:
                vanellope.jump()

    tela.blit(background, (0,0))

    # Desenha personagem
    van_group.update()
    van_group.draw(tela)
    
    pygame.display.update()

pygame.quit()