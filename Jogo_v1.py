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
    background = pygame.image.load('imagens/cenario3.jpg').convert_alpha()
    background = pygame.transform.scale(background, (WIDHT, HEIGHT))
    imagem = pygame.image.load('imagens/vanellope_up.png').convert_alpha()
    imagem = pygame.transform.scale(imagem, (IMAGEM_WIDHT, IMAGEM_HEIGHT))
    coke = pygame.image.load('imagens/New Piskel (3).png').convert_alpha()
    coke = pygame.transform.scale(coke, (COKE_WIDHT, COKE_HEIGHT))  

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
    
    game = True
    rect = imagem.get_rect()    
    delta_movimento = {"esquerda":0, "direita":0}
    velocidade = 0.3
    clock = pygame.time.Clock() #objeto para controle de atualização de imagem
    coke1 = Coke(coke)
    coke2 = Coke(coke)    
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
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT:
                    delta_movimento["esquerda"] = 0
                if evento.key == pygame.K_RIGHT:
                    delta_movimento ["direita"]= 0
        
        rect.x += (delta_movimento["direita"] - delta_movimento["esquerda"])*velocidade*delta_time
        coke1.update()
        coke2.update()
        surf.fill([255, 255, 255])
        surf.blit(background, (0, 0))
        surf.blit(imagem, [rect.x, 350])
        surf.blit(coke1.image, coke1.rect)
        surf.blit(coke2.image, coke2.rect)

        pygame.display.flip() #faz atualização da tela

if __name__ == "__main__":
    main()