import random
import pygame
from configs import *
from assets import *

class Tile(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, assets, x, y):
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Define a imagem do tile.
        self.assets = assets
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
    def __init__(self, groups, assets):
        pygame.sprite.Sprite.__init__(self)
        
        # Armazena imagens de movimento em uma lista
        self.images = [assets[IMAGEM1],
                    assets[IMAGEM2],
                    assets[IMAGEM3]]

        self.imagem_atual = 0
        self.state = STILL
        self.speedx = 0
        self.speedy = 0
        self.real_speedx = 0
        self.groups = groups
        self.assets = assets

        self.image = assets[IMAGEM0]
        
        # Redimensiona imagem
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = int(HEIGHT * 7 / 8)
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
            collisions = pygame.sprite.spritecollide(self, self.groups['block_sprites'], False, pygame.sprite.collide_mask)
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
        collisions = pygame.sprite.spritecollide(self, self.groups['all_sprites'], False, pygame.sprite.collide_mask)
        self.rect.x -= self.speedx
    
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
            self.image =  assets[IMAGEM0]

        # Atualiza imagem quando personagem está pulando
        if self.speedy != 0:
            self.image = assets[IMAGEM4]

    
class Guard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    
        # Armazena imagens de movimento em uma lista    
        self.images = [assets[ROSQUINHA0],
                    assets[ROSQUINHA1],
                    assets[ROSQUINHA2]]

        self.current_image = 0
        self.speedx = -2
        self.speedy = 0
        self.assets = assets

        self.image = assets[ROSQUINHA0]

        self.rect = self.image.get_rect()
        self.rect[0] = WIDTH
        self.rect[1] = 270
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
    
        self.rect.x += self.speedx       
        #Percorre lista das imagens e cria animação
        self.current_image = (self.current_image + 1) % 3  # Volta para imagem 0 da lista
        self.image = self.images[ self.current_image ]