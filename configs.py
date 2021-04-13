# -*- coding: utf-8 -*-
"""
Fuga Doce - Sweet Escape
Constantes e definições importantes
"""
from os import path

pontuacao = 0
# Tamanho da tela
WIDTH = 1100
HEIGHT = 500

# Tamanho do pulo e bloco
JUMP_SIZE = 50 
TILE_SIZE = 60

# Tamanho do bloco brigadeiro
BLOCK_WIDTH = 1000
BLOCK_HEIGHT = 1000

# Parâmetros importantes
SPEED = 10
GRAVITY = 2
GROUND = HEIGHT * 5 // 6

# Estados movimentação Vanellope
STILL = 0
JUMPING = 1
FALLING = 2

# Dimensões Vanellope
VANELLOPE_WIDTH = 100
VANELLOPE_HEIGHT = 100

# Dimensões do Guarda
GUARDA_WIDTH = 180
GUARDA_HEIGHT = 180

# Dimensões do coração 
LIVES_WIDTH = 80
LIVES_HEIGHT = 80

# Dimensões do brigadeiro
BRIGADEIRO_WIDTH = 100
BRIGADEIRO_HEIGHT = 100

# Número de blocos
INITIAL_BLOCKS = 1
CAKE_BLOCKS = 8

FPS = 120

BLACK = (0, 0, 0)

# Estados do menu
INIT = 3
INIT2 = 4
INIT3 = 5
GAME = 6
END = 7
QUIT = 8

COKE_WIDTH = 50
COKE_HEIGHT = 50

TIRO_WIDTH = 57
TIRO_HEIGHT = 14

#Distância padrão
standard_distance = 100