# -*- coding: utf-8 -*-
import pygame
import os
from pygame.locals import *
import random

pygame.init()

TILE_SIZE = 120

BLOCK_WIDTH = 1000
BLOCK_HEIGHT = 1000

# Tamanho da tela
WIDTH = 1100
HEIGHT = 500
JUMP_SIZE = TILE_SIZE/3
SPEED = 10
GRAVITY = 2
GROUND = HEIGHT * 5 // 6

STILL = 0
JUMPING = 1
FALLING = 2

#CANDY_WIDTH = 50
#CANDY_HEIGHT = 38

INITIAL_BLOCKS = 2
CAKE_BLOCKS = 8

BLACK = (0, 0, 0)

# Cria a tela
tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Vanellope")

# Carrega imagem de fundo
background = pygame.image.load('fundo2.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

# Carrega imagem de blocos
block_img = pygame.image.load('bloco.png').convert_alpha()

# Carrega imagem blocos 2
cake_img = pygame.image.load('bloco_cake.png').convert_alpha()

class Tile(pygame.sprite.Sprite):

    # Construtor da classe.
    def __init__(self, tile_img, x, y):
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Aumenta o tamanho do tile.
        tile_img = pygame.transform.scale(tile_img, (TILE_SIZE, TILE_SIZE))

        # Define a imagem do tile.
        self.image = tile_img
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Posiciona o tile
        self.rect.x = x
        self.rect.y = y

        self.speedx = 0

    def update(self):
        self.rect.x += self.speedx

# Define classe da personagem principal
class Vanellope(pygame.sprite.Sprite):
    def __init__(self, blocks):
        pygame.sprite.Sprite.__init__(self)
        
        # Armazena imagens de movimento em uma lista
        self.images = [pygame.image.load('penelope_move0.png').convert_alpha(),
                       pygame.image.load('penelope_move1.png').convert_alpha(),
                       pygame.image.load('penelope_move2.png').convert_alpha()]

        self.imagem_atual = 0
        self.state = STILL
        self.speedx = 0
        self.speedy = 0

        self.image = pygame.image.load('penelope_frente.png').convert_alpha()
        
        # Redimensiona imagem
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = int(HEIGHT * 7 / 8)

        self.blocks = blocks

    # Define o movimento de pular 
    def jump(self):
        if self.state == STILL:
            self.speedy -= JUMP_SIZE
            self.state = JUMPING
        
    # Carrega as informações
    def update(self):
        
        self.speedy += GRAVITY
        
        if self.speedy > 0:
            self.state = FALLING
        self.rect.y += self.speedy

        if self.rect.bottom > GROUND:
            self.rect.bottom = GROUND
            self.speedy = 0
            self.state = STILL

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH -1
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

       
class Guard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    
        # Armazena imagens de movimento em uma lista    
        self.images = [pygame.image.load('rosquinha_move0.png').convert_alpha(),
                       pygame.image.load('rosquinha_move1.png').convert_alpha(),
                       pygame.image.load('rosquinha_move2.png').convert_alpha()]

        self.current_image = 0
        self.speedx = -2
        self.speedy = 0

        self.image = pygame.image.load('rosquinha_move0.png').convert_alpha()

        self.rect = self.image.get_rect()
        self.rect[0] = WIDTH
        self.rect[1] = 330


    def update(self):
    
        self.rect.x += self.speedx
        #if self.rect.right > WIDTH:
         #   self.rect.right = WIDTH
          #  self.speedx = -2
        #if self.rect.left < 0:   
         #   self.rect.left = 0
          #  self.speedx = 2
        
        #Percorre lista das imagens e cria animação
        self.current_image = (self.current_image + 1) % 3  # Volta para imagem 0 da lista
        self.image = self.images[ self.current_image ]

        

# all_candies = pygame.sprite.Group()
# for i in range(5):
#     candy = Candy(candy_img)
#     all_candies.add(candy)

# position_x = [WIDTH, 1200, 1300]

# Carrega todos os assets de uma vez.
"""
def load_assets(img_dir):
    assets = {}
    assets[PLAYER_IMG] = pygame.image.load(path.join(img_dir, 'penelope_frente.png')).convert_alpha()
    assets[PLAYER2_IMG] = pygame.image.load(path.join(img_dir, 'penelope_jump.png')).convert_alpha()
    assets[PLAYER3_IMG] = pygame.image.load(path.join(img_dir, 'penelope_move0.png')).convert_alpha()
    assets[PLAYER4_IMG] = pygame.image.load(path.join(img_dir, 'penelope_move1.png')).convert_alpha()
    assets[PLAYER5_IMG] = pygame.image.load(path.join(img_dir, 'penelope_move2.png')).convert_alpha()
    assets[BLOCK] = pygame.image.load(path.join(img_dir, 'bloco.png')).convert()
    assets[CAKE] = pygame.image.load(path.join(img_dir, 'bloco_cake.png')).convert()
    assets[GUARDA] = pygame.image.load(path.join(img_dir, 'rosquinha_move0.png')).convert()
    assets[GUARDA1] = pygame.image.load(path.join(img_dir, 'rosquinha_move1.png')).convert()
    assets[GUARDA2] = pygame.image.load(path.join(img_dir, 'rosquinha_move2.png')).convert()
    return assets

"""

def game_screen(tela):
    # Função de tempo de animação   
    clock = pygame.time.Clock()

    # Cria grupo de sprites da personagem principal
    blocks = pygame.sprite.Group()

    #assets = load_assets(img_dir)

    van_group = pygame.sprite.Group()
    vanellope = Vanellope(blocks)
    van_group.add(vanellope)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(vanellope)

    rosquinha = Guard()
    van_group.add(rosquinha)
    all_sprites.add(rosquinha)

    position_y = [210, 80]

    world_sprites = pygame.sprite.Group()
    for i in range(INITIAL_BLOCKS):
        block_x = random.randint(WIDTH, int(WIDTH * 1.5))
        block_y = random.choice(position_y)
        block = Tile(block_img, block_x, block_y)
        world_sprites.add(block)
        all_sprites.add(block)
        blocks.add(block)

    cake_sprites = pygame.sprite.Group()
    for i in range(CAKE_BLOCKS):
        cake_x = random.randint(800, WIDTH)
        cake_y = random.choice(position_y)
        cake = Tile(cake_img, cake_x, cake_y)
        cake_sprites.add(cake)
        all_sprites.add(cake)
        blocks.add(cake)

    # Loop principal do jogo
    game = True
    while game:
        clock.tick(120)
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

        for block in world_sprites:
            block.speedx = -vanellope.speedx

        for cake in cake_sprites:
            cake.speedx = -vanellope.speedx
            
        all_sprites.update()

        background_rect.x -= vanellope.speedx
            # Se o fundo saiu da janela, faz ele voltar para dentro.
            # Verifica se o fundo saiu para a esquerda
        if background_rect.right < 0:
            background_rect.x += background_rect.width
            # Verifica se o fundo saiu para a direita
        if background_rect.left >= WIDTH:
            background_rect.x -= background_rect.width

        # Verifica se algum bloco saiu da janela
        for block in world_sprites:
            if block.rect.right < 0:
                # Destrói o bloco e cria um novo no final da tela
                block.kill()
                block_x = random.randint(WIDTH, int(WIDTH * 1.5))
                block_y = random.choice(position_y)
                new_block = Tile(block_img, block_x, block_y)
                all_sprites.add(new_block)
                world_sprites.add(new_block)
                blocks.add(new_block)

        all_sprites.update()
        
        for cake in cake_sprites:
            if cake.rect.right < 0:
                # Destrói o bloco e cria um novo no final da tela
                cake.kill()
                cake_x = random.randint(WIDTH, int(WIDTH * 1.5))
                cake_y = random.choice(position_y)
                new_cake = Tile(cake_img, cake_x, cake_y)
                all_sprites.add(new_cake)
                cake_sprites.add(new_cake)
                blocks.add(new_cake)

        for rosquinha in van_group:
            if rosquinha.rect.right < 0:
                # Destrói o bloco e cria um novo no final da tela
                rosquinha.kill()
                rosquinha_x = random.randint(WIDTH, int(WIDTH * 1.5))
                rosquinha_y = 330
                new_rosquinha = Guard()
                all_sprites.add(new_rosquinha)
                van_group.add(new_rosquinha)

        tela.fill(BLACK) 
        
        tela.blit(background, background_rect)
        background_rect2 = background_rect.copy()
        
        if background_rect.left > 0:
                # Precisamos desenhar o fundo à esquerda
            background_rect2.x -= background_rect2.width
        else:
                # Precisamos desenhar o fundo à direita
            background_rect2.x += background_rect2.width
        tela.blit(background, background_rect2)

        all_sprites.draw(tela)

        pygame.display.flip()

        # Desenha personagem
        # van_group.update()
        # van_group.draw(tela)

        # all_candies.update()
        # all_candies.draw(tela)

        all_sprites.update()

        pygame.display.update()

try:
    game_screen(tela)
finally:
    pygame.quit()