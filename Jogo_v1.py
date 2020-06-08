import os
import sys
import pygame
import random

def main():
    """Rotina principal do jogo"""

    pygame.init() #incia rotinas do pygame

    WIDHT = 700
    HEIGHT = 500
    surf = pygame.display.set_mode((WIDHT, HEIGHT)) #crio superficie para jogo
    pygame.display.set_caption("Jogo")
    IMAGEM_WIDHT = 100
    IMAGEM_HEIGHT = 100
    COKE_WIDHT = 50
    COKE_HEIGHT = 50
    GUARDA_WIDTH = 200
    GUARDA_HEIGHT = 200
    background = pygame.image.load('imagens/cenario3.jpg').convert_alpha()
    background = pygame.transform.scale(background, (WIDHT, HEIGHT))
    font = pygame.font.SysFont(None, 20)
    text = font.render('COMBUSTÍVEL', True, (0, 0, 0))
    imagem = pygame.image.load('imagens/vanellope_up.png').convert_alpha()
    imagem = pygame.transform.scale(imagem, (IMAGEM_WIDHT, IMAGEM_HEIGHT))
    coke = pygame.image.load('imagens/New Piskel (3).png').convert_alpha()
    coke = pygame.transform.scale(coke, (COKE_WIDHT, COKE_HEIGHT))  
    imagem2 = pygame.image.load('imagens/penelope_frente.png').convert_alpha()
    imagem2 = pygame.transform.scale(imagem2, (IMAGEM_WIDHT, IMAGEM_HEIGHT)) 

    rosquinha0 = pygame.image.load('imagens/rosquinha_move0.png').convert_alpha()
    rosquinha0 = pygame.transform.scale(rosquinha0, (GUARDA_WIDTH, GUARDA_HEIGHT))

    tiro_imagem = pygame.image.load('imagens/tiro.png').convert_alpha()

    class Carro(pygame.sprite.Sprite):
        def __init__(self, img, all_sprites, all_arcoiris, tiro_imagem):
            pygame.sprite.Sprite.__init__(self)

            self.image = img
            self.rect = self.image.get_rect()
            self.rect.centery = IMAGEM_HEIGHT/2
            self.rect.right = IMAGEM_WIDHT
            self.rect.bottom = IMAGEM_HEIGHT 
            self.rect.x = 0
            self.rect.y = 340
            self.speedx = 0.3
            self.all_sprites = all_sprites
            self.all_arcoiris = all_arcoiris
            self.tiro_imagem = tiro_imagem

        def update(self):
            self.rect.x +=(delta_movimento["direita"] - delta_movimento["esquerda"])*self.speedx*delta_time

        def shoot(self):
            new_tiro = Arcoiris(self.tiro_imagem, self.rect.right, self.rect.centery)
            self.all_sprites.add(new_tiro)
            self.all_arcoiris.add(new_tiro)

    class Coke(pygame.sprite.Sprite):
        def __init__(self, img):
            pygame.sprite.Sprite.__init__(self)

            self.image = img
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, WIDHT - COKE_WIDHT)
            self.rect.y = random.randint(-50, -COKE_HEIGHT)
            self.speedx = 3
            self.speedy = 4
       
        def update(self):
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT or self.rect.right + COKE_WIDHT < 0 or self.rect.left > WIDHT:
                self.rect.x = random.randint(0, WIDHT - COKE_WIDHT)
                self.rect.y = random.randint(-50, -COKE_HEIGHT)

    class Guard(pygame.sprite.Sprite):
        def __init__(self, img):
            pygame.sprite.Sprite.__init__(self)
    
        # Armazena imagens de movimento em uma lista    
            self.image = img
            self.speedx = 0
            self.speedy = 0
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(350, WIDHT)
            self.rect.y = 270


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

            if self.rect.right > WIDHT:
                self.kill()
    
    game = True
    rect = imagem.get_rect()    
    delta_movimento = {"esquerda":0, "direita":0}
    velocidade = 0.3
    clock = pygame.time.Clock() #objeto para controle de atualização de imagem
    all_sprites = pygame.sprite.Group()
    all_cokes = pygame.sprite.Group()
    all_guardas = pygame.sprite.Group()
    all_arcoiris = pygame.sprite.Group()

    jogador = Carro(imagem, all_sprites, all_arcoiris, tiro_imagem)
    all_sprites.add(jogador)

    for j in range(1):
        guarda1 = Guard(rosquinha0)
        all_sprites.add(guarda1)
        all_guardas.add(guarda1)
    
    for i in range(3):
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
                    delta_movimento["esquerda"] = 1
                if evento.key == pygame.K_RIGHT:
                    delta_movimento["direita"] = 1
                if evento.key == pygame.K_SPACE:
                    jogador.shoot()
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT:
                    delta_movimento["esquerda"] = 0
                if evento.key == pygame.K_RIGHT:
                    delta_movimento ["direita"]= 0
        
        all_sprites.update()

        colisao = pygame.sprite.groupcollide(all_arcoiris, all_guardas, True, True)

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
        surf.fill([255, 255, 255])
        surf.blit(background, (0, 0))
        surf.blit(text, (10, 10))
        all_sprites.draw(surf)

        pygame.display.flip() #faz atualização da tela

if __name__ == "__main__":
    main()