import pygame
import time

pygame.init()

pygame.display.set_caption('Mandelbrot Set')

WIDTH = 800
HEIGHT = 800
win = pygame.display.set_mode((WIDTH,HEIGHT))

win.fill((0,31,121))

exit = False
maxNoOfIteration = 100


# X lies between -2.5 to 1
# Y lies between -1 to 1

'''
f(z) = z^2 + c

f(0) = 1
f(1) = 1 + 1 = 2
f(2) = 5


z = 0
c = x + iy
f(0) = x + iy
f(f(0)) = (x + iy)^2 + (x + iy)
f(f(0)) = (x^2 - y^2 + i 2xy) + (x + iy) 
'''
screen = [[maxNoOfIteration for i in range(WIDTH)] for j in range(HEIGHT)]

for y in range(HEIGHT):
	for x in range(WIDTH):
		cn = (x/WIDTH * 2.7 - 2.1) + (y/HEIGHT * 2.7 - 1.5) * 1j
		f = 0
		belongs = True
		for i in range(maxNoOfIteration):
			f = f**2 + cn
			if abs(f) > 2:
				belongs = False
				screen[y][x] = i
				break

for i in range(WIDTH):
	for j in range(HEIGHT):
		if screen[j][i] == maxNoOfIteration:
			win.set_at((i,j),(0,0,0))
		else:
			win.set_at((i,j),(0,31 * ((0.4 + screen[j][i]/maxNoOfIteration)**2), 131 * ((0.4 + screen[j][i]/maxNoOfIteration)**2)))

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