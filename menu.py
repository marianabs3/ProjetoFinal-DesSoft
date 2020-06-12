import pygame

def MenuInicial():
	black=(0,0,0)
	white=(255,255,255)
	red=(255,0,0)

    WIDTH = 1100
    HEIGHT = 500

    tela = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fuga Doce")

	clock = pygame.time.Clock()
	crashed = False

	menu_img1=pygame.image.load('tela_1.png')
	menu_img2=pygame.image.load('tela_2.png')
	menu_img3=pygame.image.load('tela 3.png')


    def Menu(img):
        gameDisplay.blit(menu_img1,(0,0))

	imagemAtual=Menu(menu_img1)

	while not crashed:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				crashed=True
			if event.type==pygame.KEYDOWN:

				if event.key==pygame.K_RETURN:
					imagemAtual=Menu(menu_img2)

                    if event.type==pygame.QUIT:
				        crashed=True
			        if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_RETURN:
					        imagemAtual=Menu(menu_img3)
                        elif event.type==pygame.QUIT:
					        crashed=True

		pygame.display.update()
		clock.tick(60)

	pygame.quit()
	quit()
Menu()
