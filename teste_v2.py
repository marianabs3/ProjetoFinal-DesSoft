# -*- coding: utf-8 -*-
import pygame
import os
from pygame.locals import *
import random
from menu import MenuInicial, MenuInicial2, MenuInicial3, end_screen, pontinhos
from configs import *
from Jogo_v1 import tela1
from sprites import *
from assets import *


def game_screen(tela):
    # Função de tempo de animação   
    clock = pygame.time.Clock()

    assets = load_assets()
    background_rect = assets['background'].get_rect()
    lives_rect = assets['lives_img'].get_rect()

    # Cria grupo de sprites da personagem principal
    blocks = pygame.sprite.Group() #blocos
    #assets = load_assets(img_dir)
    van_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group() #vanellope
    all_guardas = pygame.sprite.Group()
    #van_group.add(vanellope)
    all_brigadeiro = pygame.sprite.Group()
    block_sprites = pygame.sprite.Group() #bloco também
    cake_sprites = pygame.sprite.Group()

    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_guards'] = all_guardas
    groups['all_brigadeiro'] = all_brigadeiro
    groups['block_sprites'] = block_sprites
    groups['cake_sprites'] = cake_sprites
    groups['blocks'] = blocks

    vanellope = Vanellope(all_sprites, van_group, assets['imagem0'])
    #all_sprites.add(vanellope)
    rosquinha = Guard()
    #all_sprites.add(rosquinha)
    #all_guardas.add(rosquinha)

    position_y = [80]
    position2_y = [210]


    for i in range(INITIAL_BLOCKS):
        block_x = random.randint(WIDTH, int(WIDTH * 1.5))
        block_y = random.choice(position_y)
        block = Tile(assets['block_img'], block_x, block_y)
        brigadeiro1 = Tile(assets['brigadeiro0'], block_x, block_y)
        all_brigadeiro.add(brigadeiro1)
        block_sprites.add(block)
        all_sprites.add(block)
        blocks.add(block)
        
    for i in range(CAKE_BLOCKS):
        cake_x = random.randint(800, WIDTH)
        cake_y = random.choice(position2_y)
        cake = Tile(assets['cake_img'], cake_x, cake_y)
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
    pontos = 0
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
            new_block = Tile(assets['block_img'], block_x, block_y)
            all_sprites.add(new_block)
            block_sprites.add(new_block)
            blocks.add(new_block)        

        if distance2 > create_distance2:
            create_distance2 = distance2 + 100
            cake_x = random.randint(WIDTH, int(WIDTH * 1.5))
            cake_y = random.choice(position2_y)
            new_cake = Tile(assets['cake_img'], cake_x, cake_y)
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
        
        tela.blit(assets['background'], background_rect)
        background_rect2 = background_rect.copy()
        
        if background_rect.left > 0:
                # Precisamos desenhar o fundo à esquerda
            background_rect2.x -= background_rect2.width
        else:
                # Precisamos desenhar o fundo à direita
            background_rect2.x += background_rect2.width
        tela.blit(assets['background'], background_rect2)

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
                pontos += 100
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
            tela.blit(assets['lives_img'], lives_rect)

        text_surface = assets['font'].render("{:08d}".format(pontinhos(pontos)), True, (255, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2,  10)
        tela.blit(text_surface, text_rect)
        pygame.display.update()

