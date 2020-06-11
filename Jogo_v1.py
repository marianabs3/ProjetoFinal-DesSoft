import os
import sys
import pygame
import random

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
    background = pygame.image.load('imagens/fundo2.png').convert_alpha()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()

    font = pygame.font.SysFont(None, 20)
    text = font.render('COMBUSTÍVEL', True, (0, 0, 0))

    imagem = pygame.image.load('imagens/vanellope_up.png').convert_alpha()
    imagem = pygame.transform.scale(imagem, (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))

    coke = pygame.image.load('imagens/New Piskel (3).png').convert_alpha()
    coke = pygame.transform.scale(coke, (COKE_WIDTH, COKE_HEIGHT))  

    imagem2 = pygame.image.load('imagens/penelope_frente.png').convert_alpha()
    imagem2 = pygame.transform.scale(imagem2, (VANELLOPE_WIDTH, VANELLOPE_HEIGHT)) 

    rosquinha0 = pygame.image.load('imagens/rosquinha_move0.png').convert_alpha()
    rosquinha0 = pygame.transform.scale(rosquinha0, (GUARDA_WIDTH, GUARDA_HEIGHT))
    rosquinha1 = pygame.image.load('imagens/rosquinha_move1.png').convert_alpha()
    rosquinha1 = pygame.transform.scale(rosquinha1, (GUARDA_WIDTH, GUARDA_HEIGHT))
    rosquinha2 = pygame.image.load('imagens/rosquinha_move2.png').convert_alpha()
    rosquinha2 = pygame.transform.scale(rosquinha2, (GUARDA_WIDTH, GUARDA_HEIGHT))

    tiro_imagem = pygame.image.load('imagens/tiro.png').convert_alpha()

    class Carro(pygame.sprite.Sprite):
        def __init__(self, img, all_sprites, all_arcoiris, tiro_imagem):
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

        def update(self):
            self.rect.x += self.speedx
            #collisions = pygame.sprite.spritecollide(self, self.all_sprites, False, pygame.sprite.collide_mask)
            #self.rect.x -= self.speedx
            #self.rect.x +=(delta_movimento["direita"] - delta_movimento["esquerda"])*self.speedx*delta_time

        def shoot(self):
            new_tiro = Arcoiris(self.tiro_imagem, self.rect.right, self.rect.centery)
            self.all_sprites.add(new_tiro)
            self.all_arcoiris.add(new_tiro)

    class Coke(pygame.sprite.Sprite):
        def __init__(self, img):
            pygame.sprite.Sprite.__init__(self)

            self.image = img
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, WIDTH - COKE_WIDTH)
            self.rect.y = random.randint(-50, -COKE_HEIGHT)
            self.speedx = 3
            self.speedy = 4
       
        def update(self):
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT or self.rect.right + COKE_WIDTH < 0 or self.rect.left > WIDTH:
                self.rect.x = random.randint(0, WIDTH - COKE_WIDTH)
                self.rect.y = random.randint(-50, -COKE_HEIGHT)

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

        jogador = Carro(imagem, all_sprites, all_arcoiris, tiro_imagem)
        all_sprites.add(jogador)
        rosquinha = Guard(rosquinha0)
        all_sprites.add(rosquinha)
        all_guardas.add(rosquinha)

        #for j in range(1):
            #guarda1 = Guard(rosquinha0)
            #all_sprites.add(guarda1)
            #all_guardas.add(guarda1)
        
        for i in range(1):
            coke1 = Coke(coke)
            all_sprites.add(coke1)
            all_cokes.add(coke1)

        while game:
            delta_time = clock.tick(60) #garantes um FPS máximo de 60 Hz
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                    pygame.quit() #terminado a aplicação do pygame
                    sys.exit() #sair pela rotina do sistema 
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_LEFT:
                        jogador.speedx -= 4
                    if evento.key == pygame.K_RIGHT:
                        jogador.speedx += 4
                    if evento.key == pygame.K_SPACE:
                        jogador.shoot()
                if evento.type == pygame.KEYUP:
                    if evento.key == pygame.K_LEFT:
                        jogador.speedx += 4
                    if evento.key == pygame.K_RIGHT:
                        jogador.speedx -= 4
                        

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

            background_rect.x -= jogador.speedx
            if background_rect.right < 0:
                background_rect.x += background_rect.width
            if background_rect.left >= WIDTH:
                background_rect.x -= background_rect.width

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
                r = Guard(rosquinha0)
                all_sprites.add(r)
                all_guardas.add(r)

            colisao = pygame.sprite.spritecollide(jogador, all_guardas, True)
            if colisao:
                jogador.image = imagem2
                

            colisao = pygame.sprite.spritecollide(jogador, all_cokes, True)
            if colisao:
                jogador.speedx += 0.05
            
            for coke1 in colisao:
                c = Coke(coke)
                all_sprites.add(c)
                all_cokes.add(c)
            
    surf = pygame.display.set_mode((WIDTH, HEIGHT))


    pygame.display.flip() #faz atualização da tela

    try:
        game_screen(surf)
    finally:
        pygame.quit()
if __name__ == "__main__":
    main()