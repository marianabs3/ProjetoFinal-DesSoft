import random
import pygame
from configs import *
from assets import *



class Tile(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, assets, x, y):
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        assets = load_assets()
        # Define a imagem do tile.
        self.assets = assets
        self.images = [assets['block_img'],
                    assets['cake_img'],
                    assets['brigadeiro0']]

        self.image = assets['cake_img']


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
        assets = load_assets()
        # Armazena imagens de movimento em uma lista
        self.images = [assets['imagem1'],
                    assets['imagem2'],
                    assets['imagem3']]

        self.imagem_atual = 0
        self.state = STILL
        self.speedx = 0
        self.speedy = 0
        self.real_speedx = 0
        self.groups['all_sprites'] = all_sprites
        self.assets = assets
        #self.all_sprites = all_sprites


        self.image = assets['imagem0']
        self.mask = pygame.mask.from_surface(self.image)

        
        # Redimensiona imagem
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = int(HEIGHT * 7 / 8)
        self.colidiu_block = False

    # Define o movimento de pular 
    def jump(self):
        if self.state == STILL:
            self.speedy -= JUMP_SIZE
            self.state = JUMPING

    # Carrega as informações
    def update(self):
        assets = load_assets()

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
        collisions = pygame.sprite.spritecollide(self, self.all_sprites, False, pygame.sprite.collide_mask)
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
            self.image = assets['imagem0']

        # Atualiza imagem quando personagem está pulando
        if self.speedy != 0:
            self.image = assets['imagem4']

    
class Guard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        assets = load_assets()
        self.assets = assets

        # Armazena imagens de movimento em uma lista    
        self.images = [assets['rosquinha0'],
                    assets['rosquinha1'],
                    assets['rosquinha2']]

        self.current_image = 0
        self.speedx = -2
        self.speedy = 0

        self.image = assets['rosquinha0']
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = WIDTH
        self.rect[1] = 270


    def update(self):
    
        self.rect.x += self.speedx       
        #Percorre lista das imagens e cria animação
        self.current_image = (self.current_image + 1) % 3  # Volta para imagem 0 da lista
        self.image = self.images[ self.current_image ]

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

assets = load_assets()
# Cria grupo de sprites da personagem principal
blocks = pygame.sprite.Group() #blocos
#assets = load_assets(img_dir)
van_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group() #vanellope
all_guardas = pygame.sprite.Group()
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
groups['van group'] = van_group

vanellope = Vanellope(van_group, assets['imagem0'])
all_sprites.add(vanellope)
van_group.add(vanellope)
rosquinha = Guard()
all_sprites.add(rosquinha)
all_guardas.add(rosquinha)