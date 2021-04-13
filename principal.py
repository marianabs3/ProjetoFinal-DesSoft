# -*- coding: utf-8 -*-
"""
 Projeto final de DesSoft 2020.1
 Equipe: Eduardo Papandrea Santana, Ivan de Alcantara Barbosa Barros e Mariana Barbosa Sousa
 Fuga Doce - Sweet Escape
"""

#Importando as bibliotecas necessárias:
import pygame
import os
from pygame.locals import *
import random
from menu import *
from configs import *
from modo_race import tela1

# Inicia programa
pygame.init()

# Carrega tela
tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fuga Doce")

# Carrega imagem de fundo
background = pygame.image.load('imagens/fundo2.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

# Carrega fonte
font = pygame.font.Font('fontes/Pixeled.ttf', 20)

# Carrega imagem de blocos
block_img = pygame.image.load('imagens/brigadeiro0.png').convert_alpha()

# Carrega imagem blocos 2
cake_img = pygame.image.load('imagens/bloco_cake.png').convert_alpha()

# Carrega imagens de movimentação da Vanellope
imagem0 = pygame.image.load('imagens/penelope_frente.png').convert_alpha()
imagem0 = pygame.transform.scale(imagem0, (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))

imagem1 = pygame.image.load('imagens/penelope_move0.png').convert_alpha()
imagem1 = pygame.transform.scale(imagem1, (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))

imagem2 = pygame.image.load('imagens/penelope_move1.png').convert_alpha()
imagem2 = pygame.transform.scale(imagem2, (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))

imagem3 = pygame.image.load('imagens/penelope_move2.png').convert_alpha()
imagem3 = pygame.transform.scale(imagem3, (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))

# Carrega imagem do brigadeiro
brigadeiro = pygame.image.load('imagens/brigadeiro0.png').convert_alpha()
brigadeiro = pygame.transform.scale(brigadeiro, (BRIGADEIRO_WIDTH, BRIGADEIRO_HEIGHT))

# Carrega imagens da movimentação da rosquinha
rosquinha0 = pygame.image.load('imagens/rosquinha_move0.png').convert_alpha()
rosquinha0 = pygame.transform.scale(rosquinha0, (GUARDA_WIDTH, GUARDA_HEIGHT))

rosquinha1 = pygame.image.load('imagens/rosquinha_move1.png').convert_alpha()
rosquinha1 = pygame.transform.scale(rosquinha1, (GUARDA_WIDTH, GUARDA_HEIGHT))

rosquinha2 = pygame.image.load('imagens/rosquinha_move2.png').convert_alpha()
rosquinha2 = pygame.transform.scale(rosquinha2, (GUARDA_WIDTH, GUARDA_HEIGHT))

# Carrega imagens das vidas
lives_img = pygame.image.load('imagens/vida2.png').convert_alpha()
lives_img = pygame.transform.scale(lives_img, (LIVES_WIDTH, LIVES_HEIGHT))
lives_rect = lives_img.get_rect()

# Sons utilizados nas dinâmicas
rosquinha_morrendo = pygame.mixer.Sound('sons/rosquinha morrendo.ogg')
vanellope_perdendo = pygame.mixer.Sound('sons/vanellope perdendo vida.ogg')
vanellope_morte = pygame.mixer.Sound('sons/vanelope morte.ogg')

class Tile(pygame.sprite.Sprite):
    """
    Classe de todos os blocos 
    """
    def __init__(self, tile_img, x, y):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Aumenta o tamanho do tile.
        tile_img = pygame.transform.scale(tile_img, (TILE_SIZE, TILE_SIZE))

        # Define a imagem do tile.
        self.image = tile_img
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Mascára de colisão
        self.mask = pygame.mask.from_surface(self.image)

        # Posiciona o tile
        self.rect.x = x
        self.rect.y = y

        self.speedx = 0

    def update(self):
        self.rect.x += self.speedx

class Vanellope(pygame.sprite.Sprite):
    """
    Classe da personagem principal
    """
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

        self.image = imagem0
        
        # Redimensiona imagem
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = int(HEIGHT * 7 / 8)

        # Declara parâmetros necessários na função
        self.all_sprites = all_sprites
        self.block_sprites = block_sprites
        self.colidiu_block = False
        
        # Mascára de colisão
        self.mask = pygame.mask.from_surface(self.image)

    # Define o movimento de pular 
    def jump(self):
        if self.state == STILL:
            self.speedy -= JUMP_SIZE
            self.state = JUMPING

    def morrendo(self):        
            pygame.mixer.music.stop() 
            vanellope_morte.play()
            pygame.time.delay(2000)

    # Carrega as informações
    def update(self):
        
        self.speedy += GRAVITY
        
        if self.speedy > 0:
            self.state = FALLING
        
        self.rect.y += self.speedy
        
        # Verifica colisão com algum bloco
        if self.speedy < 0:
            collisions = pygame.sprite.spritecollide(self, self.block_sprites, False, pygame.sprite.collide_mask)
            for collision in collisions:
                self.colidiu_block = True

        # Se colidiu com algum bloco, volta para o ponto antes da colisão
        collisions = pygame.sprite.spritecollide(self, self.all_sprites, False, pygame.sprite.collide_mask)
        
        # Corrige a posição do personagem para antes da colisão
        for collision in collisions:
            # Estava indo para baixo
            if self.speedy > 0:
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

        # Atualiza posições após colisão
        self.rect.x += self.speedx
        collisions = pygame.sprite.spritecollide(self, self.all_sprites, False, pygame.sprite.collide_mask)
        self.rect.x -= self.speedx
    
        # Atualiza velocidades após colisão
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
        
        # Mascára de colisão
        self.mask = pygame.mask.from_surface(self.image)

class Guard(pygame.sprite.Sprite):
    """
    Classe dos guardas rosquinhas
    """
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

        # Redimensiona imagem
        self.rect = self.image.get_rect()
        self.rect[0] = WIDTH
        self.rect[1] = 270
        
        # Mascára de colisão
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
    
        # Atualiza posição
        self.rect.x += self.speedx
        
        #Percorre lista das imagens e cria animação
        self.current_image = (self.current_image + 1) % 3  # Volta para imagem 0 da lista
        self.image = self.images[ self.current_image ]


def game_screen(tela, pontuacao):
    """
    Função da tela principal que rodará o jogo
    """
    # Função de tempo de animação   
    clock = pygame.time.Clock()

    # Grupo para os blocos
    blocks = pygame.sprite.Group() 

    # Grupo para todas as sprites
    all_sprites = pygame.sprite.Group()

    # Grupo para os guardas
    all_guardas = pygame.sprite.Group()
    
    # Grupo para os brigadeiros
    all_brigadeiro = pygame.sprite.Group()

    # Grupo 2 para os blocos
    block_sprites = pygame.sprite.Group() 

    # Grupo para os blocos de bolo
    cake_sprites = pygame.sprite.Group()

    # Cria personagem
    vanellope = Vanellope(blocks, block_sprites)
    all_sprites.add(vanellope)

    # Score inicial
    pontuacao = 0

    # Cria guarda rosquinha
    rosquinha = Guard()
    all_sprites.add(rosquinha)
    all_guardas.add(rosquinha)

    # Posição dos blocos de bolo
    position_y = [80]
    position2_y = [210]

    # Cria blocos e brigadeiro
    for i in range(INITIAL_BLOCKS):
        block_x = random.randint(WIDTH, int(WIDTH * 1.5))
        block_y = random.choice(position_y)
        block = Tile(block_img, block_x, block_y)
        brigadeiro1 = Tile(brigadeiro, block_x, block_y)
        all_brigadeiro.add(brigadeiro1)
        block_sprites.add(block)
        all_sprites.add(block)
        blocks.add(block)
        
    # Cria blocos de bolo
    for i in range(CAKE_BLOCKS):
        cake_x = random.randint(800, WIDTH)
        cake_y = random.choice(position2_y)
        cake = Tile(cake_img, cake_x, cake_y)
        cake_sprites.add(cake)
        all_sprites.add(cake)
        blocks.add(cake)

    # Carrega som principal do jogo
    pygame.mixer.music.load('sons/Christmas synths.ogg')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    # Parâmetros importantes 
    distance = 0
    create_distance = standard_distance
    distance2 = 0
    create_distance2 = standard_distance
    game = True
    lives = 3
    keys_down = {}

    # Loop principal do jogo
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

        # Define velocidade dos blocos
        for block in block_sprites:
            block.speedx = -vanellope.real_speedx

        # Define velocidade dos blocos de bolo
        for cake in cake_sprites:
            cake.speedx = -vanellope.real_speedx
        
        # Atualiza posição dos blocos
        distance += vanellope.real_speedx
        distance2 += vanellope.real_speedx

        background_rect.x -= vanellope.real_speedx
            
        # Verifica se o fundo saiu para a direita
        if background_rect.right < 0:
            background_rect.x += background_rect.width
            
        # Verifica se o fundo saiu para a esquerda
        if background_rect.left >= WIDTH:
            background_rect.x -= background_rect.width

        # Verifica se algum bloco saiu da janela
        if distance > create_distance:
            create_distance = distance + standard_distance
            # Destrói o bloco e cria um novo no final da tela
            block_x = random.randint(WIDTH, int(WIDTH * 1.5))
            block_y = random.choice(position_y)
            new_block = Tile(block_img, block_x, block_y)
            all_sprites.add(new_block)
            block_sprites.add(new_block)
            blocks.add(new_block)        

        # Verifica se algum bloco de bolo saiu da janela
        if distance2 > create_distance2:
            create_distance2 = distance2 + standard_distance
            # Destrói o bloco e cria um novo no final da tela
            cake_x = random.randint(WIDTH, int(WIDTH * 1.5))
            cake_y = random.choice(position2_y)
            new_cake = Tile(cake_img, cake_x, cake_y)
            all_sprites.add(new_cake)
            cake_sprites.add(new_cake)
            blocks.add(new_cake)

        # Verifica se algum guarda saiu da janela
        for rosquinha in all_guardas:
            if rosquinha.rect.right < 0:
                # Destrói guarda e cria um novo 
                rosquinha.kill()
                rosquinha_x = random.randint(WIDTH, int(WIDTH * 1.5))
                rosquinha_y = 330
                new_rosquinha = Guard()
                all_sprites.add(new_rosquinha)
                all_guardas.add(new_rosquinha)

        all_sprites.update()

        tela.fill(BLACK) 
        
        # Desenha e posiciona fundo
        tela.blit(background, background_rect)
        background_rect2 = background_rect.copy()
        
        # Desenha fundo a direita e esquerda
        if background_rect.left > 0:
            background_rect2.x -= background_rect2.width
        else:
            background_rect2.x += background_rect2.width
        tela.blit(background, background_rect2)

        # Dsenha todas sprites
        all_sprites.draw(tela)

        pygame.display.flip()

        all_sprites.update()       

        # Declara colisão da personagem principal com os guardas
        colisao = pygame.sprite.spritecollide(vanellope, all_guardas, False, pygame.sprite.collide_mask)
        
        # Verifica se personagem principal colidiu com bloco brigadeiro
        if vanellope.colidiu_block:
            vanellope.colidiu_block = False
            keys_down = {}
            
            # É direcionada a fase do carrinho
            pontuacao = tela1(tela, pontuacao)
            
            # Carrega música principal quando volta
            pygame.mixer.music.load('sons/Christmas synths.ogg')
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)   
            
            block.kill()
        
        # Declara colisão dos guardas com a personagem principal
        colisao = pygame.sprite.spritecollide(vanellope, all_guardas, True, pygame.sprite.collide_mask)
        
        if colisao:
            
            # Verifica se rosquinha foi atingida por cima
            if vanellope.rect.bottom <= colisao[0].rect.top + standard_distance:
                
                # Toca som da rosquinha morrendo
                rosquinha_morrendo.play()
                
                # Mata rosquinha e atualiza placar
                colisao[0].kill()
                pontuacao += 100
           
            else: 
                # Toca som quando perde e atualiza vidas
                vanellope_perdendo.play()
                lives -= 1
            
            # Cria novo guarda
            r = Guard()
            all_sprites.add(r)
            all_guardas.add(r)

        # Se não tiver vidas, entra tela de game over
        if lives == 0:
            vanellope.morrendo() 
            end_screen(tela, pontuacao)  
            
        # Desenha vidas
        for i in range(lives):
            lives_rect.bottomleft = (10 + i*(LIVES_WIDTH-20), HEIGHT - 10)
            tela.blit(lives_img, lives_rect)

        # Desenha fonte do placar
        text_surface = font.render("{:08d}".format(pontuacao), True, (255, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2,  10)
        tela.blit(text_surface, text_rect)
        pygame.display.update()

# Declara estados do menu
state = INIT
while state != QUIT:
    if state == INIT:
        state = MenuInicial(tela)
    elif state == INIT2:
        state = MenuInicial2(tela)
    elif state == INIT3:
        state = MenuInicial3(tela)
    elif state == GAME:
        state = game_screen(tela, pontuacao)
    elif state == END:
        state = end_screen(tela, pontuacao)
    else:
        state = QUIT