import pygame
import librosa
import math
import time
from pygame import mixer

pygame.init()
mixer.init()

song_name = input("Enter Song File Name:\n")

y, sr = librosa.load(song_name)
mixer.music.load(song_name)
y_harmonic, y_percussive = librosa.effects.hpss(y)

hog_len = 750
Radius1 = 100
Radius2 = 45
R1 = 45
R2 = 100
center = [200, 350]

A = []
B = []

for i in range(len(y_percussive)):
    ang = i/hog_len*math.pi*2
    radius = R1+Radius1*y_harmonic[i]
    A.append([int(center[0]+(radius*math.cos(ang))),
             int(center[1]+(radius*math.sin(ang)))])
    radius = R2+Radius2*y_percussive[i]
    B.append([int(center[0]+(radius*math.cos(ang))),
             int(center[1]+(radius*math.sin(ang)))])


clock = pygame.time.Clock()

win = pygame.display.set_mode((400, 700))
win.fill((20, 20, 20))

p = 0

exit = False

neon_green = (57, 255, 20)
dark_green = (16, 98, 0)

mixer.music.play()

while not exit:

    clock.tick(29.68)  # 1000/(750/512*23) = 29.68 ~= 30
    win.fill((20, 20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit = True

    if exit:
        break

    if p+hog_len <= len(y_harmonic):
        H = A[p:p+hog_len]
        P = B[p:p+hog_len]
        p += hog_len
    else:
        H = A[p:]
        P = B[p:]

    for i in range(len(H)):
        pygame.draw.circle(win, neon_green, H[i], 2)
        pygame.draw.circle(win, dark_green, P[i], 2)

    pygame.display.update()
