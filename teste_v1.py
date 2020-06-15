# -*- coding: utf-8 -*-

import pygame
import os
from pygame.locals import *
import random
from menu import pontinhos
from configs import *
from Jogo_v1 import tela1
from sprites import *
from assets import *

def tela1(surf):
    def game_screen(surf):
        game = True
        assets = load_assets()
        rect = assets['carro'].get_rect()    
        delta_movimento = {"esquerda":0, "direita":0}
        velocidade = 4
        
        clock = pygame.time.Clock() #objeto para controle de atualização de imagem
        
        all_sprites = pygame.sprite.Group()
        all_cokes = pygame.sprite.Group()
        all_guardas = pygame.sprite.Group()
        all_arcoiris = pygame.sprite.Group()
        cake_sprites = pygame.sprite.Group()

        groups = {}
        groups['all_sprites'] = all_sprites
        groups['all_guardas'] = all_guardas
        groups['all_cokes'] = all_cokes
        groups['all_arcoiris'] = all_arcoiris
        groups['cake_sprites'] = cake_sprites

        jogador = Carro(imagem, all_sprites, all_arcoiris, tiro_imagem, som_tiro, cake_sprites)
        all_sprites.add(jogador)
        rosquinha = Guard(rosquinha0)
        all_sprites.add(rosquinha)
        all_guardas.add(rosquinha)

        #for j in range(1):
            #guarda1 = Guard(rosquinha0)
            #all_sprites.add(guarda1)
            #all_guardas.add(guarda1)
        
        for i in range(3):
            coke1 = Coke(coke)
            all_sprites.add(coke1)
            all_cokes.add(coke1)

        position2_y = [210]

        for i in range(CAKE_BLOCKS):
            cake_x = random.randint(800, WIDTH)
            cake_y = random.choice(position2_y)
            cake = Tile(cake_img, cake_x, cake_y)
            cake_sprites.add(cake)
            all_sprites.add(cake)
        
        distance2 = 0
        create_distance2 = 100
        pontos1 = 0
        keys_down1 = {}
      
        while game:
            delta_time = clock.tick(60) #garantes um FPS máximo de 60 Hz
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                    pygame.quit() #terminado a aplicação do pygame
                    sys.exit() #sair pela rotina do sistema 
                if evento.type == pygame.KEYDOWN:
                    keys_down1[evento.key] = True
                    if evento.key == pygame.K_LEFT:
                        jogador.speedx -= 8
                    if evento.key == pygame.K_RIGHT:
                        jogador.speedx += 8
                    if evento.key == pygame.K_SPACE:
                        jogador.shoot()
                if evento.type == pygame.KEYUP:
                    if evento.key in keys_down1 and keys_down1[evento.key]:
                        if evento.key == pygame.K_LEFT:
                            jogador.speedx += 8
                        if evento.key == pygame.K_RIGHT:
                            jogador.speedx -= 8
                            

            for rosquinha in all_guardas:
                if rosquinha.rect.right < 0:
                    # Destrói o bloco e cria um novo no final da tela
                    rosquinha.kill()
                    rosquinha_x = random.randint(WIDTH, int(WIDTH * 1.5))
                    rosquinha_y = 330
                    new_rosquinha = Guard(rosquinha0)
                    all_sprites.add(new_rosquinha)
                    all_guardas.add(new_rosquinha)

            
            all_sprites.update()

            for cake in cake_sprites:
                cake.speedx = -jogador.speedx
            
            distance2 += jogador.speedx

            background_rect.x -= jogador.speedx
            if background_rect.right < 0:
                background_rect.x += background_rect.width
            if background_rect.left >= WIDTH:
                background_rect.x -= background_rect.width

            if distance2 > create_distance2:
                create_distance2 = distance2 + 100
                cake_x = random.randint(WIDTH, int(WIDTH * 1.5))
                cake_y = random.choice(position2_y)
                new_cake = Tile(cake_img, cake_x, cake_y)
                all_sprites.add(new_cake)
                cake_sprites.add(new_cake)

            surf.fill([255, 255, 255])

            surf.blit(background, background_rect)
            background_rect2 = background_rect.copy()
            if background_rect.left > 0:
                background_rect2.x -= background_rect2.width
            else:
                background_rect2.x += background_rect2.width
            surf.blit(background, background_rect2)

            all_sprites.draw(surf)

            pygame.display.flip()


            colisao = pygame.sprite.groupcollide(all_arcoiris, all_guardas, True, True)
            if colisao:
                pontos1 += 200
                r = Guard(rosquinha0)
                all_sprites.add(r)
                all_guardas.add(r)

            colisao = pygame.sprite.spritecollide(jogador, all_guardas, True, pygame.sprite.collide_mask)
            if colisao:
                keys_down1 = {}
                return

            colisao = pygame.sprite.spritecollide(jogador, all_cokes, True)
            if colisao:
                coke1.cokes_number += 1
                som_colisao.play()
                jogador.speedx += 0.05
            
            for i in range(len(colisao)):
                c = Coke(coke)
                all_sprites.add(c)
                all_cokes.add(c)
                c.passatempo()


            coke1.passatempo()

            for i in range(coke1.cokes_number):
                coke_rect.bottomleft = (10 + i*(COKE_WIDTH-20), HEIGHT - 450)
                surf.blit(coke, coke_rect)

            if coke1.cokes_number == 0:
                return

            text_surface = font.render("{:08d}".format(pontinhos(pontos1)), True, (255, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.midtop = (WIDTH / 2,  10)
            surf.blit(text_surface, text_rect)
            
            pygame.display.flip()

            
#     surf = pygame.display.set_mode((WIDTH, HEIGHT))


#     pygame.display.flip() #faz atualização da tela

#     try:
    game_screen(surf)
#     finally:
#         pygame.quit()
 #if __name__ == "__main__":
#     main()
