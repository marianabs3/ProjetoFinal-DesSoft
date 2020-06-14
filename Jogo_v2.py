# -*- coding: utf-8 -*-

#Importando as bibliotecas necessárias:
import pygame
import os
from pygame.locals import *
import random
from menu import MenuInicial, MenuInicial2, MenuInicial3
from menu import end_screen
from configs import INIT, INIT2, INIT3, GAME, END, QUIT
from Jogo_v1 import tela1


pygame.init()

WIDTH = 1100
HEIGHT = 500

tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fuga Doce")

# Estados para controle do fluxo da aplicação


TILE_SIZE = 60

BLOCK_WIDTH = 1000
BLOCK_HEIGHT = 1000

# Tamanho da tela
WIDTH = 1100
HEIGHT = 500
JUMP_SIZE = 50 #TILE_SIZE/3
SPEED = 10
GRAVITY = 2
GROUND = HEIGHT * 5 // 6

STILL = 0
JUMPING = 1
FALLING = 2

#CANDY_WIDTH = 50
#CANDY_HEIGHT = 38

VANELLOPE_WIDTH = 100
VANELLOPE_HEIGHT = 100

GUARDA_WIDTH = 180
GUARDA_HEIGHT = 180

LIVES_WIDTH = 80
LIVES_HEIGHT = 80

BRIGADEIRO_WIDTH = 100
BRIGADEIRO_HEIGHT = 100

INITIAL_BLOCKS = 1
CAKE_BLOCKS = 8

BLACK = (0, 0, 0)

# Carrega imagem de fundo
background = pygame.image.load('imagens/fundo2.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

font = pygame.font.Font('fontes/Pixeled.ttf', 20)

# Carrega imagem de blocos
block_img = pygame.image.load('imagens/brigadeiro0.png').convert_alpha()

# Carrega imagem blocos 2
cake_img = pygame.image.load('imagens/bloco_cake.png').convert_alpha()

imagem0 = pygame.image.load('imagens/penelope_frente.png').convert_alpha()
imagem0 = pygame.transform.scale(imagem0, (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))

imagem1 = pygame.image.load('imagens/penelope_move0.png').convert_alpha()
imagem1 = pygame.transform.scale(imagem1, (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))

imagem2 = pygame.image.load('imagens/penelope_move1.png').convert_alpha()
imagem2 = pygame.transform.scale(imagem2, (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))

imagem3 = pygame.image.load('imagens/penelope_move2.png').convert_alpha()
imagem3 = pygame.transform.scale(imagem3, (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))

brigadeiro = pygame.image.load('imagens/brigadeiro0.png').convert_alpha()
brigadeiro = pygame.transform.scale(brigadeiro, (BRIGADEIRO_WIDTH, BRIGADEIRO_HEIGHT))

rosquinha0 = pygame.image.load('imagens/rosquinha_move0.png').convert_alpha()
rosquinha0 = pygame.transform.scale(rosquinha0, (GUARDA_WIDTH, GUARDA_HEIGHT))
rosquinha1 = pygame.image.load('imagens/rosquinha_move1.png').convert_alpha()
rosquinha1 = pygame.transform.scale(rosquinha1, (GUARDA_WIDTH, GUARDA_HEIGHT))
rosquinha2 = pygame.image.load('imagens/rosquinha_move2.png').convert_alpha()
rosquinha2 = pygame.transform.scale(rosquinha2, (GUARDA_WIDTH, GUARDA_HEIGHT))

lives_img = pygame.image.load('imagens/vida2.png').convert_alpha()
lives_img = pygame.transform.scale(lives_img, (LIVES_WIDTH, LIVES_HEIGHT))
lives_rect = lives_img.get_rect()

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

        self.mask = pygame.mask.from_surface(self.image)


        # Posiciona o tile
        self.rect.x = x
        self.rect.y = y

        self.speedx = 0

    def update(self):
        self.rect.x += self.speedx

# Define classe da personagem principal
class Vanellope(pygame.sprite.Sprite):
    def __init__(self, all_sprites, block_sprites):
        pygame.sprite.Sprite.__init__(self)
        
        # Armazena imagens de movimento em uma lista
        self.images = [imagem1,
                    imagem2,
                    imagem3]

        self.imagem_atual = 0
        self.state = STILL
        self.speedx = 0
        self.speedy = 0
        self.real_speedx = 0
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

        self.image = imagem0
        
        # Redimensiona imagem
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = int(HEIGHT * 7 / 8)

        self.all_sprites = all_sprites
        self.block_sprites = block_sprites
        self.colidiu_block = False
        self.mask = pygame.mask.from_surface(self.image)

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
        
        if self.speedy < 0:
            collisions = pygame.sprite.spritecollide(self, self.block_sprites, False, pygame.sprite.collide_mask)
            for collision in collisions:
                #print(self.rect.y, collision.rect.bottom)
                self.colidiu_block = True

        # Se colidiu com algum bloco, volta para o ponto antes da colisão
        collisions = pygame.sprite.spritecollide(self, self.all_sprites, False, pygame.sprite.collide_mask)
        # Corrige a posição do personagem para antes da colisão
        for collision in collisions:
            # Estava indo para baixo
            if self.speedy > 0:
                if self.rect.x + self.rect.width > collision.rect.x + 30:
                    self.rect.bottom = collision.rect.top
                    # Se colidiu com algo, para de cair
                    self.speedy = 0
                    # Atualiza o estado para parado
                    self.state = STILL
            # Estava indo para cima
            elif self.speedy < 0:
                self.rect.top = collision.rect.bottom
                # Se colidiu com algo, para de cair
                self.speedy = 0
                # Atualiza o estado para parado
                self.state = STILL

        self.rect.x += self.speedx
        collisions = pygame.sprite.spritecollide(self, self.all_sprites, False, pygame.sprite.collide_mask)
        self.rect.x -= self.speedx
    
        # Corrige a posição do personagem para antes da colisão
        # for collision in collisions:
        #     # Estava indo para a direita
        #     if self.speedx > 0:
        #         self.rect.right = collision.rect.left
        #     # Estava indo para a esquerda
        #     elif self.speedx < 0:
        #         self.rect.left = collision.rect.right
        if len(collisions) > 0:
            self.real_speedx = 0
        else:
            self.real_speedx = self.speedx

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
            self.image =  imagem0

        # Atualiza imagem quando personagem está pulando
        if self.speedy != 0:
            self.image = pygame.image.load('imagens/penelope_jump.png').convert_alpha()

    
class Guard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    
        # Armazena imagens de movimento em uma lista    
        self.images = [rosquinha0,
                    rosquinha1,
                    rosquinha2]

        self.current_image = 0
        self.speedx = -2
        self.speedy = 0

        self.image = rosquinha0

        self.rect = self.image.get_rect()
        self.rect[0] = WIDTH
        self.rect[1] = 270
        self.mask = pygame.mask.from_surface(self.image)


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
    blocks = pygame.sprite.Group() #blocos

    #assets = load_assets(img_dir)
    #van_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group() #vanellope
    all_guardas = pygame.sprite.Group()
    #van_group.add(vanellope)
    all_brigadeiro = pygame.sprite.Group()
    block_sprites = pygame.sprite.Group() #bloco também
    cake_sprites = pygame.sprite.Group()
    vanellope = Vanellope(blocks, block_sprites)
    all_sprites.add(vanellope)

    rosquinha = Guard()
    all_sprites.add(rosquinha)
    all_guardas.add(rosquinha)

    position_y = [80]
    position2_y = [210]


    for i in range(INITIAL_BLOCKS):
        block_x = random.randint(WIDTH, int(WIDTH * 1.5))
        block_y = random.choice(position_y)
        block = Tile(block_img, block_x, block_y)
        brigadeiro1 = Tile(brigadeiro, block_x, block_y)
        all_brigadeiro.add(brigadeiro1)
        block_sprites.add(block)
        all_sprites.add(block)
        blocks.add(block)
        
    for i in range(CAKE_BLOCKS):
        cake_x = random.randint(800, WIDTH)
        cake_y = random.choice(position2_y)
        cake = Tile(cake_img, cake_x, cake_y)
        cake_sprites.add(cake)
        all_sprites.add(cake)
        blocks.add(cake)

        pygame.mixer.music.load('sons/Christmas synths.ogg')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    # Loop principal do jogo
    distance = 0
    create_distance = 100
    distance2 = 0
    create_distance2 = 100
    game = True
    lives = 3
    pontuacao = 0
    keys_down = {}
    while game:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game == False
                pygame.quit()
    
            if event.type == pygame.KEYDOWN:
                keys_down[event.key] = True            
            # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    vanellope.speedx -= 4
                if event.key == pygame.K_RIGHT:
                    vanellope.speedx += 4
            
            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                if event.key in keys_down and keys_down[event.key]:
                
                # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_LEFT:
                        vanellope.speedx += 4
                    if event.key == pygame.K_RIGHT:
                        vanellope.speedx -= 4
                    if event.key == pygame.K_UP:
                        vanellope.jump()

        all_sprites.update()

        for block in block_sprites:
            block.speedx = -vanellope.real_speedx

        for cake in cake_sprites:
            cake.speedx = -vanellope.real_speedx
        
        distance += vanellope.real_speedx
        distance2 += vanellope.real_speedx

        background_rect.x -= vanellope.real_speedx
            # Se o fundo saiu da janela, faz ele voltar para dentro.
            # Verifica se o fundo saiu para a esquerda
        if background_rect.right < 0:
            background_rect.x += background_rect.width
            # Verifica se o fundo saiu para a direita
        if background_rect.left >= WIDTH:
            background_rect.x -= background_rect.width

        # Verifica se algum bloco saiu da janela
        # for block in block_sprites:
        #     if block.rect.right < 0:
        if distance > create_distance:
            create_distance = distance + 1000
            # Destrói o bloco e cria um novo no final da tela
            block_x = random.randint(WIDTH, int(WIDTH * 1.5))
            block_y = random.choice(position_y)
            new_block = Tile(block_img, block_x, block_y)
            all_sprites.add(new_block)
            block_sprites.add(new_block)
            blocks.add(new_block)        

        if distance2 > create_distance2:
            create_distance2 = distance2 + 100
            cake_x = random.randint(WIDTH, int(WIDTH * 1.5))
            cake_y = random.choice(position2_y)
            new_cake = Tile(cake_img, cake_x, cake_y)
            all_sprites.add(new_cake)
            cake_sprites.add(new_cake)
            blocks.add(new_cake)

        for rosquinha in all_guardas:
            if rosquinha.rect.right < 0:
                # Destrói o bloco e cria um novo no final da tela
                rosquinha.kill()
                rosquinha_x = random.randint(WIDTH, int(WIDTH * 1.5))
                rosquinha_y = 330
                new_rosquinha = Guard()
                all_sprites.add(new_rosquinha)
                all_guardas.add(new_rosquinha)

        all_sprites.update()

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

        colisao = pygame.sprite.spritecollide(vanellope, all_guardas, False, pygame.sprite.collide_mask)
        if vanellope.colidiu_block:
            vanellope.colidiu_block = False
            #block.image = brigadeiro
            keys_down = {}
            tela1(tela)   
            block.kill()
        
        colisao = pygame.sprite.spritecollide(vanellope, all_guardas, True, pygame.sprite.collide_mask)
        if colisao:
            #keys_down = {}
            if vanellope.rect.bottom <= colisao[0].rect.top + 100:
                colisao[0].kill()
                pontuacao += 100
            else:
                #vanellope.image = imagem1
                lives -= 1
            
            r = Guard()
            all_sprites.add(r)
            all_guardas.add(r)

        if lives == 0:
            pygame.mixer.music.stop() 
            end_screen(tela)   
            
    
        for i in range(lives):
            lives_rect.bottomleft = (10 + i*(LIVES_WIDTH-20), HEIGHT - 10)
            tela.blit(lives_img, lives_rect)

        text_surface = font.render("{:08d}".format(pontuacao), True, (255, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2,  10)
        tela.blit(text_surface, text_rect)
        pygame.display.update()


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