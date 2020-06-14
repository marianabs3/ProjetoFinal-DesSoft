import pygame
import os
from configs import *



BACKGROUND = 'background'
FONT = 'font'
BLOCK_IMG = 'block_img'
IMAGEM0 = 'imagem0'
IMAGEM1 = 'imagem1'
IMAGEM2 = 'imagem2'
IMAGEM3 = 'imagem3'
IMAGEM4 = 'imagem4'
ROSQUINHA0 = 'rosquinha0'
ROSQUINHA1 = 'rosquinha1'
ROSQUINHA2 = 'rosquinha2'
LIVES_IMG ='lives_img'

def load_assets():
    assets = {}
    assets[BACKGROUND] = pygame.image.load(os.path.join(IMAGENS_DIR, 'fundo2.png')).convert()
    assets[BLOCK_IMG] = pygame.image.load(os.path.join(IMAGENS_DIR, 'brigadeiro0.png')).convert()
    assets[BLOCK_img] = pygame.transform.scale(assets['block_img'], (TILE_SIZE, TILE_SIZE))
    assets[IMAGEM0] = pygame.image.load(os.path.join(IMAGENS_DIR, 'penelope_frente.png')).convert()
    assets[IMAGEM0] = pygame.transform.scale(assets['imagem0'], (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))
    assets[IMAGEM1] = pygame.image.load(os.path.join(IMAGENS_DIR, 'penelope_move0.png')).convert()
    assets[IMAGEM1] = pygame.transform.scale(assets['imagem1'], (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))
    assets[IMAGEM2] = pygame.image.load(os.path.join(IMAGENS_DIR, 'penelope_move1.png')).convert()
    assets[IMAGEM2] = pygame.transform.scale(assets['imagem2'], (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))
    assets[IMAGEM3] = pygame.image.load(os.path.join(IMAGENS_DIR, 'penelope_move2.png')).convert()
    assets[IMAGEM3] = pygame.transform.scale(assets['imagem3'], (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))
    assets[IMAGEM4] = pygame.image.load(os.path.join(IMAGENS_DIR, 'penelope_jump.png')).convert()
    assets[IMAGEM4] = pygame.transform.scale(assets['imagem4'], (VANELLOPE_WIDTH, VANELLOPE_HEIGHT))
    assets[ROSQUINHA0] = pygame.image.load(os.path.join(IMAGENS_DIR, 'rosquinha_move0.png')).convert()
    assets[ROSQUINHA0] = pygame.transform.scale(assets['rosquinha0'], (GUARDA_WIDTH, GUARDA_HEIGHT))
    assets[ROSQUINHA1] = pygame.image.load(os.path.join(IMAGENS_DIR, 'rosquinha_move1.png')).convert()
    assets[ROSQUINHA1] = pygame.transform.scale(assets['rosquinha1'], (GUARDA_WIDTH, GUARDA_HEIGHT))
    assets[ROSQUINHA2] = pygame.image.load(os.path.join(IMAGENS_DIR, 'rosquinha_move2.png')).convert()
    assets[ROSQUINHA2] = pygame.transform.scale(assets['rosquinha2'], (GUARDA_WIDTH, GUARDA_HEIGHT))
    assets[LIVES_IMG] = pygame.image.load(os.path.join(IMAGENS_DIR, 'vida2.png')).convert()
    assets[ROSQUINHA2] = pygame.transform.scale(assets['lives_img'], (LIVES_WIDTH, LIVES_HEIGHT))

    # Carrega os sons do jogo
    pygame.mixer.music.load(os.path.join(SONS_DIR, 'Christmas synths.ogg'))
    pygame.mixer.music.set_volume(0.3)
    return assets
    
    
    
