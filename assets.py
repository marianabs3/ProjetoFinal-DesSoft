import pygame
import os
from configs import *


BACKGROUND = 'background'
FONT = 'font'
BLOCK_IMG = 'block_img'
CAKE_IMG = 'cake_img'
BRIGADEIRO = 'brigadeiro0'
IMAGEM0 = 'imagem0'
IMAGEM1 = 'imagem1'
IMAGEM2 = 'imagem2'
IMAGEM3 = 'imagem3'
IMAGEM4 = 'imagem4'
ROSQUINHA0 = 'rosquinha0'
ROSQUINHA1 = 'rosquinha1'
ROSQUINHA2 = 'rosquinha2'
LIVES_IMG = 'lives_img'
COKE = 'coke'
TIRO = 'tiro'
CARRO = 'carro'


def load_assets():
    assets = {}
    assets[BACKGROUND] = pygame.image.load(os.path.join(IMAGENS_DIR, 'fundo2.png')).convert()
    assets[BACKGROUND] = pygame.transform.scale(assets['background'], (WIDTH, HEIGHT))
    assets[BRIGADEIRO] = pygame.image.load(os.path.join(IMAGENS_DIR, 'brigadeiro0.png')).convert_alpha()
    assets[BRIGADEIRO] = pygame.transform.scale(assets['brigadeiro0'], (BRIGADEIRO_WIDTH, BRIGADEIRO_HEIGHT))
    assets[BLOCK_IMG] = pygame.image.load(os.path.join(IMAGENS_DIR, 'bloco.png')).convert_alpha()
    assets[BLOCK_IMG] = pygame.transform.scale(assets['block_img'], (TILE_SIZE, TILE_SIZE))
    assets[CAKE_IMG] = pygame.image.load(os.path.join(IMAGENS_DIR, 'bloco_cake.png')).convert_alpha()
    assets[CAKE_IMG] = pygame.transform.scale(assets['cake_img'], (TILE_SIZE, TILE_SIZE))
    assets[IMAGEM0] = pygame.image.load(os.path.join(IMAGENS_DIR, 'penelope_frente.png')).convert_alpha()
    assets[IMAGEM0] = pygame.transform.scale(assets['imagem0'], (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))
    assets[IMAGEM1] = pygame.image.load(os.path.join(IMAGENS_DIR, 'penelope_move0.png')).convert_alpha()
    assets[IMAGEM1] = pygame.transform.scale(assets['imagem1'], (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))
    assets[IMAGEM2] = pygame.image.load(os.path.join(IMAGENS_DIR, 'penelope_move1.png')).convert_alpha()
    assets[IMAGEM2] = pygame.transform.scale(assets['imagem2'], (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))
    assets[IMAGEM3] = pygame.image.load(os.path.join(IMAGENS_DIR, 'penelope_move2.png')).convert_alpha()
    assets[IMAGEM3] = pygame.transform.scale(assets['imagem3'], (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))
    assets[IMAGEM4] = pygame.image.load(os.path.join(IMAGENS_DIR, 'penelope_jump.png')).convert_alpha()
    assets[IMAGEM4] = pygame.transform.scale(assets['imagem4'], (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))
    assets[ROSQUINHA0] = pygame.image.load(os.path.join(IMAGENS_DIR, 'rosquinha_move0.png')).convert_alpha()
    assets[ROSQUINHA0] = pygame.transform.scale(assets['rosquinha0'], (GUARDA_WIDTH, GUARDA_HEIGHT))
    assets[ROSQUINHA1] = pygame.image.load(os.path.join(IMAGENS_DIR, 'rosquinha_move1.png')).convert_alpha()
    assets[ROSQUINHA1] = pygame.transform.scale(assets['rosquinha1'], (GUARDA_WIDTH, GUARDA_HEIGHT))
    assets[ROSQUINHA2] = pygame.image.load(os.path.join(IMAGENS_DIR, 'rosquinha_move2.png')).convert_alpha()
    assets[ROSQUINHA2] = pygame.transform.scale(assets['rosquinha2'], (GUARDA_WIDTH, GUARDA_HEIGHT))
    assets[LIVES_IMG] = pygame.image.load(os.path.join(IMAGENS_DIR, 'vida2.png')).convert_alpha()
    assets[LIVES_IMG] = pygame.transform.scale(assets['lives_img'], (LIVES_WIDTH, LIVES_HEIGHT))
    assets[COKE] = pygame.image.load(os.path.join(IMAGENS_DIR, 'New Piskel (3).png')).convert_alpha()
    assets[COKE] = pygame.transform.scale(assets['coke'], (COKE_WIDTH, COKE_HEIGHT))
    assets[TIRO] = pygame.image.load(os.path.join(IMAGENS_DIR, 'tiro.png')).convert_alpha()
    assets[TIRO] = pygame.transform.scale(assets['tiro'], (TIRO_WIDTH, TIRO_HEIGHT))
    assets[CARRO] = pygame.image.load(os.path.join(IMAGENS_DIR, 'vanellope_up.png')).convert_alpha()
    assets[CARRO] = pygame.transform.scale(assets['carro'], (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))
    assets[FONT] = pygame.font.Font('fontes/Pixeled.ttf', 20)

    # Carrega os sons do jogo
    pygame.mixer.music.load(os.path.join(SONS_DIR, 'Christmas synths.ogg'))
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.load('sons/fight_looped.wav')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    som_tiro = pygame.mixer.Sound('sons/tiro.ogg')
    som_colisao = pygame.mixer.Sound('sons/Record.ogg')
    return assets
    
    
    
