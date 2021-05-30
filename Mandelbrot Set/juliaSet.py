import pygame
import time

pygame.init()

pygame.display.set_caption('Julia Set')

WIDTH = 1225
HEIGHT = 700
win = pygame.display.set_mode((WIDTH,HEIGHT))

win.fill((0,31,121))

exit = False
maxNoOfIteration = 100

JC = -0.70176 - 0.3842j

'''
−0.70176 − 0.3842j
−0.8i
−0.835 − 0.2321i
−0.7269 + 0.1889i (0.3 instead of 0.4 line 44 and maxiteration = 1000)
'''
screen = [[maxNoOfIteration for i in range(WIDTH)] for j in range(HEIGHT)]

for y in range(HEIGHT):
	for x in range(WIDTH):
		f = (x/WIDTH * 3.5 - 1.8) + (y/HEIGHT * 2.2 - 1) * 1j
		belongs = True
		for i in range(maxNoOfIteration):
			f = f**2 + JC
			if abs(f) > 2:
				belongs = False
				screen[y][x] = i
				break

for i in range(WIDTH):
	for j in range(HEIGHT):
		if screen[j][i] == maxNoOfIteration:
			win.set_at((i,j),(0,0,0))
		else:
			win.set_at((i,j),(0,31 * ((0.3 + screen[j][i]/maxNoOfIteration)**2), 131 * ((0.3 + screen[j][i]/maxNoOfIteration)**2)))

exit = False

while True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit = True
			break

	if exit:
		break

	pygame.display.update()