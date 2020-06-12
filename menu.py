import pygame
def MenuInicial(window):

    casa = True

    # ===== Loop principal =====
    while casa:
        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                pygame.quit()

        # ----- Gera saídas
        window.fill((0, 0, 255))  # Preenche com a cor branca

        # ----- Atualiza estado do jogo
        pygame.display.update()  # Mostra o novo frame para o jogador