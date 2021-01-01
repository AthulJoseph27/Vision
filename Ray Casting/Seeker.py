import pygame
import math
import time
import random

def radians(theta):
	return theta * math.pi/180

class Vector:
	def __init__(self,x,y,theta,magnitude):
		self.x = x
		self.y = y
		self.theta = radians(theta)
		self.magnitude = magnitude

class Ray:
	def __init__(self,vector):
		self.vector = vector

	def intersection(self,wall):

		wall_slope = math.tan(wall.vector.theta)
		ray_slope = math.tan(self.vector.theta)

		if wall_slope * wall.vector.x == ray_slope * self.vector.x:
			if wall_slope == ray_slope:
				return (None,None)

			if self.vector.x > wall.vector.x or self.vector.y > wall.vector.y:
				return (None,None)
			else:
				return (wall.vector.x,wall.vector.y)

			if wall_slope + ray_slope == 0:

				if self.vector.x > wall.vector.x or self.vector.y > wall.vector.y:
					return (wall.vector.x,wall.vector.y)
				else:
					return (None,None)

		if wall_slope == ray_slope:
			return (None,None)

		X = ((wall.vector.y - self.vector.y) + (ray_slope * self.vector.x - wall_slope * wall.vector.x)) / (ray_slope - wall_slope)
		Y = ((ray_slope * wall.vector.y - wall_slope * self.vector.y) + wall_slope * ray_slope * (self.vector.x - wall.vector.x)) / (ray_slope - wall_slope)

		wall_end = (round(wall.vector.x + wall.vector.magnitude * math.cos(wall.vector.theta)) , round(wall.vector.y + wall.vector.magnitude * math.sin(wall.vector.theta)))

		if round(X) < min(wall.vector.x,wall_end[0]) or round(X) > max(wall.vector.x,wall_end[0]) or round(Y) < min(wall.vector.y,wall_end[1]) or round(Y) > max(wall.vector.y,wall_end[1]):
			return (None,None)

		v1 = (math.cos(self.vector.theta),math.sin(self.vector.theta))
		if (((X - self.vector.x)**2 + (Y - self.vector.y)**2)**0.5) == 0:
			return (X,Y)
		v2 = ((X - self.vector.x)/(((X - self.vector.x)**2 + (Y - self.vector.y)**2)**0.5),(Y - self.vector.y)/(((X - self.vector.x)**2 + (Y - self.vector.y)**2)**0.5))
		
		# print(v1[0] * v2[0] + v1[1] * v2[1])
		# print(v1)
		# print(v2)
		# print()
		# print()

		if round(v1[0] * v2[0] + v1[1] * v2[1]) == -1:
			return (None,None)

		if (((X - self.vector.x)**2 + (Y - self.vector.y)**2)**0.5) > self.vector.magnitude:
			return (None,None)

		return (X,Y)


	def draw(self,win,walls):
		ix = [None,None]
		dist = HEIGHT**2
		for w in walls:
			temp = self.intersection(w)
			if temp[0] == None:
				continue
			if ix[0] != None :
				if ((self.vector.x - temp[0])**2+(self.vector.y-temp[1])**2) < dist:
					dist = ((self.vector.x - temp[0])**2+(self.vector.y-temp[1])**2)
					ix[0] = temp[0]
					ix[1] = temp[1] 
			else:
				ix[0] = temp[0]
				ix[1] = temp[1] 
				
				dist = ((self.vector.x - temp[0])**2+(self.vector.y-temp[1])**2)
				
		end = None
		if ix[0] == None:
			end = (round(self.vector.x + self.vector.magnitude * math.cos(self.vector.theta)) , round(self.vector.y + self.vector.magnitude * math.sin(self.vector.theta)))
		else:
			end = ix
			pygame.draw.line(win,(255,255,255),ix,ix,8)
		start = (self.vector.x,self.vector.y)
		pygame.draw.line(win,(255,255,0),start,end,2)


class Wall:
	def __init__(self,vector):
		self.vector = vector

	def draw(self,win,color=(0,0,0)):
		start = (self.vector.x,self.vector.y)
		end = (round(self.vector.x + self.vector.magnitude * math.cos(self.vector.theta)), round(self.vector.y + self.vector.magnitude * math.sin(self.vector.theta)))
		pygame.draw.line(win,color,start,end,8)

pygame.init()
clock = pygame.time.Clock()

WIDTH = 700
HEIGHT = 700
pygame.display.set_caption('Seeker')
win = pygame.display.set_mode((WIDTH,HEIGHT))
win.fill((0,0,0))

exit = False

walls = []
for i in range(20):
	walls.append(Wall(Vector(random.randint(0,750),random.randint(0,750),random.randint(0,360),random.randint(100,200))))
	walls[-1].draw(win)

# walls.append(Wall(Vector(100,100,0,200)))
# walls[-1].draw(win)

for a in range(0,361):
	ray = Ray(Vector(350,350,a,100))
	ray.draw(win,walls)

isDragging = False


while True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit = True
			break
		elif event.type == pygame.MOUSEBUTTONDOWN:
			isDragging = True
		elif event.type == pygame.MOUSEBUTTONUP:
			isDragging = False
		elif event.type == pygame.MOUSEMOTION:
			if isDragging:
				win.fill((0,0,0))
				for i in range(len(walls)):
					walls[i].draw(win)
				mx,my = pygame.mouse.get_pos()
				for a in range(0,361):
					ray = Ray(Vector(mx,my,a,100))
					ray.draw(win,walls)
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				for i in range(len(walls)):
						walls[i].draw(win,(0,200,0))
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				for i in range(len(walls)):
						walls[i].draw(win)

	if exit:
		break

	pygame.display.update()


