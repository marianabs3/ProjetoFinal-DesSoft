# -*- coding: utf-8 -*-

import os
import sys
import pygame
import random
#from Jogo_v2 import tela2
def main():
    """Rotina principal do jogo"""

    pygame.init() #incia rotinas do pygame

    WIDTH = 1100
    HEIGHT = 500
    surf = pygame.display.set_mode((WIDTH, HEIGHT)) #crio superficie para jogo
    pygame.display.set_caption("Fuga Doce - Eduardo, Ivan, Mariana")
    tela1(surf)

def tela1(surf):
    WIDTH = 1100
    HEIGHT = 500
    VANELLOPE_WIDTH = 100
    VANELLOPE_HEIGHT = 100
    COKE_WIDTH = 50
    COKE_HEIGHT = 50
    GUARDA_WIDTH = 200
    GUARDA_HEIGHT = 200
    CAKE_BLOCKS = 8
    TILE_SIZE = 60
    background = pygame.image.load('imagens/fundo2.png').convert_alpha()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()

    font = pygame.font.Font('fontes/Pixeled.ttf', 20)

    cake_img = pygame.image.load('imagens/bloco_cake.png').convert_alpha()

    imagem = pygame.image.load('imagens/vanellope_up.png').convert_alpha()
    imagem = pygame.transform.scale(imagem, (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))

    coke = pygame.image.load('imagens/New Piskel (3).png').convert_alpha()
    coke = pygame.transform.scale(coke, (COKE_WIDTH, COKE_HEIGHT))  
    coke_rect = coke.get_rect()

    imagem2 = pygame.image.load('imagens/penelope_frente.png').convert_alpha()
    imagem2 = pygame.transform.scale(imagem2, (VANELLOPE_WIDTH, VANELLOPE_HEIGHT)) 

    rosquinha0 = pygame.image.load('imagens/rosquinha_move0.png').convert_alpha()
    rosquinha0 = pygame.transform.scale(rosquinha0, (GUARDA_WIDTH, GUARDA_HEIGHT))
    rosquinha1 = pygame.image.load('imagens/rosquinha_move1.png').convert_alpha()
    rosquinha1 = pygame.transform.scale(rosquinha1, (GUARDA_WIDTH, GUARDA_HEIGHT))
    rosquinha2 = pygame.image.load('imagens/rosquinha_move2.png').convert_alpha()
    rosquinha2 = pygame.transform.scale(rosquinha2, (GUARDA_WIDTH, GUARDA_HEIGHT))

    tiro_imagem = pygame.image.load('imagens/tiro.png').convert_alpha()
    #Música:
    pygame.mixer.music.load('sons/fight_looped.wav')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    som_tiro = pygame.mixer.Sound('sons/tiro.ogg')
    som_colisao = pygame.mixer.Sound('sons/Record.ogg')

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


    class Carro(pygame.sprite.Sprite):
        def __init__(self, img, all_sprites, all_arcoiris, tiro_imagem, som_tiro, cake_sprites):
            pygame.sprite.Sprite.__init__(self)

            self.image = img
            self.rect = self.image.get_rect()
            #self.rect.centerx = WIDTH/2
            self.rect.centery = VANELLOPE_HEIGHT/2
            self.rect.right = VANELLOPE_WIDTH
            #self.rect.bottom = int(HEIGHT* 7/8) 
            self.rect.x = WIDTH/2
            self.rect.y = 340
            self.speedx = 0
            self.all_sprites = all_sprites
            self.all_arcoiris = all_arcoiris
            self.tiro_imagem = tiro_imagem
            self.som_tiro = som_tiro

        #def update(self):
            #self.rect.x += self.speedx
            #collisions = pygame.sprite.spritecollide(self, self.all_sprites, False, pygame.sprite.collide_mask)
            #self.rect.x -= self.speedx
            #self.rect.x +=(delta_movimento["direita"] - delta_movimento["esquerda"])*self.speedx*delta_time

        def shoot(self):
            new_tiro = Arcoiris(self.tiro_imagem, self.rect.right, self.rect.centery)
            self.all_sprites.add(new_tiro)
            self.all_arcoiris.add(new_tiro)
            self.som_tiro.play()

    class Coke(pygame.sprite.Sprite):
        def __init__(self, img):
            pygame.sprite.Sprite.__init__(self)

            self.image = img
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, WIDTH - COKE_WIDTH)
            self.rect.y = random.randint(-50, -COKE_HEIGHT)
            self.speedx = 3
            self.speedy = 4
            self.cokes_number = 3
            self.cokes_time = pygame.time.get_ticks()
            self.now = pygame.time.get_ticks()
       
        def update(self):

            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT or self.rect.right + COKE_WIDTH < 0 or self.rect.left > WIDTH:
                self.rect.x = random.randint(0, WIDTH - COKE_WIDTH)
                self.rect.y = random.randint(-50, -COKE_HEIGHT)

        def passatempo(self):

            now = pygame.time.get_ticks()
            delta_t = now - self.cokes_time

            if delta_t > 5000:
                self.cokes_time = now
                self.cokes_number -= 1

    class Guard(pygame.sprite.Sprite):
        def __init__(self, img):
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
            ##self.speedx = 0
            ##self.speedy = 0
            ##self.rect = self.image.get_rect()
            ##self.rect.x = random.randint(350, WIDTH)
            ##self.rect.y = 270


    class Arcoiris(pygame.sprite.Sprite):
        def __init__(self, img, left, centery):
            pygame.sprite.Sprite.__init__(self)

            self.image = img
            self.rect = self.image.get_rect()

            self.rect.centery = centery
            self.rect.left = left
            self.speedx = 10
        
        def update (self):
            self.rect.x += self.speedx

            if self.rect.right > WIDTH:
                self.kill()
    
    def game_screen(surf):
        game = True
        rect = imagem.get_rect()    
        delta_movimento = {"esquerda":0, "direita":0}
        velocidade = 4
        clock = pygame.time.Clock() #objeto para controle de atualização de imagem
        all_sprites = pygame.sprite.Group()
        all_cokes = pygame.sprite.Group()
        all_guardas = pygame.sprite.Group()
        all_arcoiris = pygame.sprite.Group()
        cake_sprites = pygame.sprite.Group()

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
        pontuacao = 0
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
                pontuacao += 100
                r = Guard(rosquinha0)
                all_sprites.add(r)
                all_guardas.add(r)

            colisao = pygame.sprite.spritecollide(jogador, all_guardas, True)
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

            text_surface = font.render("{:08d}".format(pontuacao), True, (255, 0, 0))
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