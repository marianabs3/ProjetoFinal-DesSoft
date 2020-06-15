# -*- coding: utf-8 -*-

# Importa bibliotecas necessárias
import os
import sys
import pygame
import random
from configs import *

# Função que reperesenta a fase do carrinho
def tela1(surf, pontuacao):

    # Carrega e dimensiona imagem de fundo
    background = pygame.image.load('imagens/fundo2.png').convert_alpha()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()

    # Carrega fonte
    font = pygame.font.Font('fontes/Pixeled.ttf', 20)

    # Carrega imagem do bolo
    cake_img = pygame.image.load('imagens/bloco_cake.png').convert_alpha()

    # Carrega e dimensiona imagem do carro da personagem principal
    imagem = pygame.image.load('imagens/vanellope_up.png').convert_alpha()
    imagem = pygame.transform.scale(imagem, (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))

    # Carrega e dimensiona imagem da coca
    coke = pygame.image.load('imagens/New Piskel (3).png').convert_alpha()
    coke = pygame.transform.scale(coke, (COKE_WIDTH, COKE_HEIGHT))  
    coke_rect = coke.get_rect()

    # Carrega e dimensiona imagem da personagem principal de frente
    imagem2 = pygame.image.load('imagens/penelope_frente.png').convert_alpha()
    imagem2 = pygame.transform.scale(imagem2, (VANELLOPE_WIDTH, VANELLOPE_HEIGHT)) 

    # Carrega e dimensiona imagens de animação da rosquinha
    rosquinha0 = pygame.image.load('imagens/rosquinha_move0.png').convert_alpha()
    rosquinha0 = pygame.transform.scale(rosquinha0, (GUARDA_WIDTH, GUARDA_HEIGHT))
    rosquinha1 = pygame.image.load('imagens/rosquinha_move1.png').convert_alpha()
    rosquinha1 = pygame.transform.scale(rosquinha1, (GUARDA_WIDTH, GUARDA_HEIGHT))
    rosquinha2 = pygame.image.load('imagens/rosquinha_move2.png').convert_alpha()
    rosquinha2 = pygame.transform.scale(rosquinha2, (GUARDA_WIDTH, GUARDA_HEIGHT))

    # Carrega e dimensiona imagem do tiro
    tiro_imagem = pygame.image.load('imagens/tiro.png').convert_alpha()
    tiro_imagem = pygame.transform.scale(tiro_imagem, (TIRO_WIDTH, TIRO_HEIGHT))

    # Carrega música de fundo
    pygame.mixer.music.load('sons/fight_looped.wav')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    # Carrega som do tiro
    som_tiro = pygame.mixer.Sound('sons/tiro.ogg')

    # Carrega som da colisão
    som_colisao = pygame.mixer.Sound('sons/Record.ogg')

    # Carrega som da rosquinha morrendo
    rosquinha_morrendo = pygame.mixer.Sound('sons/rosquinha morrendo.ogg')

    # Carrega som da Vanellope perdendo vida
    vanellope_perdendo = pygame.mixer.Sound('sons/vanellope perdendo vida.ogg')

    # Classe que define os blocos
    class Tile(pygame.sprite.Sprite):
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

        def update(self, cake_sprites, all_sprites, all_cokes):
            self.rect.x += self.speedx

    # Classe que define a personagem no carro
    class Carro(pygame.sprite.Sprite):
        def __init__(self, img, all_sprites, all_arcoiris, tiro_imagem, som_tiro, cake_sprites):
            pygame.sprite.Sprite.__init__(self)

            self.image = img
            self.rect = self.image.get_rect()
            
            # Redimensiona personagem
            self.rect.centery = VANELLOPE_HEIGHT/2
            self.rect.right = VANELLOPE_WIDTH

            self.rect.x = WIDTH/2
            self.rect.y = 340
            self.speedx = 0
            self.all_sprites = all_sprites
            
            # Declara grupos e sons que serão utilizados na classe
            self.all_arcoiris = all_arcoiris
            self.tiro_imagem = tiro_imagem
            self.som_tiro = som_tiro

        # Função para o tiro
        def shoot(self):
            new_tiro = Arcoiris(self.tiro_imagem, self.rect.right, self.rect.centery)
            self.all_sprites.add(new_tiro)
            self.all_arcoiris.add(new_tiro)
            self.som_tiro.play()

    # Classe que representa as cocas
    class Coke(pygame.sprite.Sprite):
        def __init__(self, cake_sprites, img):
            pygame.sprite.Sprite.__init__(self)

            self.image = img
            self.rect = self.image.get_rect()

            # Redimensiona coca
            self.rect.x = random.randint(0, WIDTH - COKE_WIDTH)
            self.rect.y = random.randint(-50, -COKE_HEIGHT)
            
            # Velocidades
            self.speedx = 3
            self.speedy = 4
            
            # Declara número de cocas e tempo
            self.cokes_number = 3
            self.cake_sprites = cake_sprites
            self.cokes_time = pygame.time.get_ticks()
       
        def update(self, cake_sprites, all_sprites, all_cokes):
            
            # Declara parâmetros
            self.cake_sprites = cake_sprites
            self.all_sprites = all_sprites
            self.all_cokes = all_cokes
            
            # Atualiza posições
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            
            # Verifica se coca saiu da tela e cria novas
            if self.rect.top > HEIGHT or self.rect.right + COKE_WIDTH < 0 or self.rect.left > WIDTH:
                self.rect.x = random.randint(0, WIDTH - COKE_WIDTH)
                self.rect.y = random.randint(-50, -COKE_HEIGHT)

            colisao = pygame.sprite.spritecollide(self, self.cake_sprites, False, pygame.sprite.collide_mask)
            
            # Se colidiu com o bloco, mata a coca e cria uma nova
            if colisao:
                self.kill()
                new_coke = Coke(cake_sprites, coke)
                all_sprites.add(new_coke)
                all_cokes.add(new_coke)
                
        # Função para o tempo da fase
        def passatempo(self):

            now = pygame.time.get_ticks()
            delta_t = now - self.cokes_time

            # Se passar 5 segundos, perde uma coca
            if delta_t > 5000:
                self.cokes_time = now
                self.cokes_number -= 1

    # Classe que representa os guardas rosquinhas
    class Guard(pygame.sprite.Sprite):
        def __init__(self, img):
            pygame.sprite.Sprite.__init__(self)
    
            # Armazena imagens de movimento em uma lista    
            self.images = [rosquinha0,
                           rosquinha1,
                           rosquinha2]
            
            self.current_image = 0
            
            # Velocidades
            self.speedx = -8
            self.speedy = 0

            self.image = rosquinha0

            self.rect = self.image.get_rect()
            self.rect[0] = WIDTH
            self.rect[1] = 270
            
            # Mascára de colisão
            self.mask = pygame.mask.from_surface(self.image)

        def update(self, cake_sprites, all_sprites, all_cokes):
    
            # Atualiza posição
            self.rect.x += self.speedx
        
            #Percorre lista das imagens e cria animação
            self.current_image = (self.current_image + 1) % 3  # Volta para imagem 0 da lista
            self.image = self.images[ self.current_image ]

    # Classe que representa o tiro
    class Arcoiris(pygame.sprite.Sprite):
        def __init__(self, img, left, centery):
            pygame.sprite.Sprite.__init__(self)

            self.image = img
            self.rect = self.image.get_rect()

            # Redimensiona tiro
            self.rect.centery = centery
            self.rect.left = left
            
            # Velocidade
            self.speedx = 10
        
        def update (self, cake_sprites, all_sprites, all_cokes):
            
            # Atualiza posição
            self.rect.x += self.speedx

            # Se saiu a direita da tela, "mata" aquele tiro
            if self.rect.right > WIDTH:
                self.kill()
    
    # Função da tela principal que rodará o jogo
    def game2_screen(surf, pontuacao):
        
        # Parâmetros que serão utilizados
        game = True
        rect = imagem.get_rect()    
        delta_movimento = {"esquerda":0, "direita":0}
        velocidade = 4
       
        clock = pygame.time.Clock() #objeto para controle de atualização de imagem
        
        # Cria grupo para todas as sprites
        all_sprites = pygame.sprite.Group()

        # Cria grupo para as cocas
        all_cokes = pygame.sprite.Group()

        # Cria grupo para os guardas
        all_guardas = pygame.sprite.Group()

        # Cria grupo para os tiros
        all_arcoiris = pygame.sprite.Group()

        # Cria grupo para os bolos
        cake_sprites = pygame.sprite.Group()

        # Cria o player
        jogador = Carro(imagem, all_sprites, all_arcoiris, tiro_imagem, som_tiro, cake_sprites)
        all_sprites.add(jogador)
        
        # Cria o guarda
        rosquinha = Guard(rosquinha0)
        all_sprites.add(rosquinha)
        all_guardas.add(rosquinha)
        
        # Cria as 3 cocas iniciais
        for i in range(3):
            coke1 = Coke(cake_sprites, coke)
            all_sprites.add(coke1)
            all_cokes.add(coke1)

        # Posiciona os blocos
        position2_y = [210]

        # Cria os blocos de bolo
        for i in range(CAKE_BLOCKS):
            cake_x = random.randint(800, WIDTH)
            cake_y = random.choice(position2_y)
            cake = Tile(cake_img, cake_x, cake_y)
            cake_sprites.add(cake)
            all_sprites.add(cake)
        
        # Parâmetros
        distance2 = 0
        create_distance2 = 100
        keys_down1 = {}
      
        # Loop principal
        while game:
            delta_time = clock.tick(60) #garantes um FPS máximo de 60 Hz
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                    pygame.quit() #terminado a aplicação do pygame
                    sys.exit() #sair pela rotina do sistema 
                
                if evento.type == pygame.KEYDOWN:
                    keys_down1[evento.key] = True
                    # Dependendo da tecla, altera a velocidade.
                    if evento.key == pygame.K_LEFT:
                        jogador.speedx -= 8
                    if evento.key == pygame.K_RIGHT:
                        jogador.speedx += 8
                    
                    # Atira
                    if evento.key == pygame.K_SPACE:
                        jogador.shoot()
               
                if evento.type == pygame.KEYUP:
                    if evento.key in keys_down1 and keys_down1[evento.key]:
                        # Dependendo da tecla, altera a velocidade.
                        if evento.key == pygame.K_LEFT:
                            jogador.speedx += 8
                        if evento.key == pygame.K_RIGHT:
                            jogador.speedx -= 8
                            
            # Verifica se algum guarda saiu da janela
            for rosquinha in all_guardas:
                if rosquinha.rect.right < 0:
                    # Destrói o guarda e cria um novo
                    rosquinha.kill()
                    rosquinha_x = random.randint(WIDTH, int(WIDTH * 1.5))
                    rosquinha_y = 330
                    new_rosquinha = Guard(rosquinha0)
                    all_sprites.add(new_rosquinha)
                    all_guardas.add(new_rosquinha)

            
            # Define velocidade dos blocos
            for cake in cake_sprites:
                cake.speedx = -jogador.speedx
            
            all_sprites.update(cake_sprites, all_sprites, all_cokes)
            
            # Atualiza posição do bloco
            distance2 += jogador.speedx


            background_rect.x -= jogador.speedx
            
             # Verifica se o fundo saiu para a direita
            if background_rect.right < 0:
                background_rect.x += background_rect.width
            
            # Verifica se o fundo saiu para a esquerda
            if background_rect.left >= WIDTH:
                background_rect.x -= background_rect.width

            # Verifica se algum bloco saiu da janela
            if distance2 > create_distance2:
                create_distance2 = distance2 + 100
                # Destrói o bloco e cria um novo no final da tela
                cake_x = random.randint(WIDTH, int(WIDTH * 1.5))
                cake_y = random.choice(position2_y)
                new_cake = Tile(cake_img, cake_x, cake_y)
                all_sprites.add(new_cake)
                cake_sprites.add(new_cake)

            # Desenha e dimensiona fundo
            surf.fill([255, 255, 255])
            surf.blit(background, background_rect)
            background_rect2 = background_rect.copy()
            
            # Desenha fundo a direita e esquerda
            if background_rect.left > 0:
                background_rect2.x -= background_rect2.width
            else:
                background_rect2.x += background_rect2.width
            surf.blit(background, background_rect2)

            all_sprites.draw(surf)

            pygame.display.flip()

            # Declara colisão do tiro com os guardas
            colisao = pygame.sprite.groupcollide(all_arcoiris, all_guardas, True, True)
            
            # Se houve colisão, atualiza pontos e mata rosquinha
            if colisao:
                rosquinha_morrendo.play()
                pontuacao += 200
                
                # Cria novo guarda
                r = Guard(rosquinha0)
                all_sprites.add(r)
                all_guardas.add(r)

            # Declara colisão do player com o guarda
            colisao = pygame.sprite.spritecollide(jogador, all_guardas, True, pygame.sprite.collide_mask)
           
            # Se houve colisão, volta para outra fase
            if colisao:
                keys_down1 = {}
                vanellope_perdendo.play()
                return pontuacao
                
                # Carrega novamente som principal da fase
                pygame.mixer.music.load('sons/fight_looped.wav')
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)

            # Declara colisão do player com as cocas
            colisao = pygame.sprite.spritecollide(jogador, all_cokes, True)
            
            # Se houver colisão, aumenta número de cocas do jogador
            if colisao:
                coke1.cokes_number += 1
                som_colisao.play()
            
            # Cria novas cocas conforme a colisão
            for i in range(len(colisao)):
                c = Coke(cake_sprites, coke)
                all_sprites.add(c)
                all_cokes.add(c)
                c.passatempo()

            # Verifica o tempo desde última colisão com a coca
            coke1.passatempo()

            # Desenha as cocas
            for i in range(coke1.cokes_number):
                coke_rect.bottomleft = (10 + i*(COKE_WIDTH-20), HEIGHT - 450)
                surf.blit(coke, coke_rect)

            # Se não possui mais cocas, jogador volta a outra fase
            if coke1.cokes_number == 0:
                keys_down1 = {}
                return pontuacao
                
                # Carrega novamente som principal do jogo
                pygame.mixer.music.load('sons/fight_looped.wav')
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
            
            # Carrega fonte do placar
            text_surface = font.render("{:08d}".format(pontuacao), True, (255, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.midtop = (WIDTH / 2,  10)
            surf.blit(text_surface, text_rect)
            
            pygame.display.flip()

    return game2_screen(surf, pontuacao)

