import pygame
import sys
from random import randint,choice

pygame.init()
pygame.display.set_caption("Snake")

WIDTH = 480
HEIGHT = 480
TILESIZE = 24
GRID_WIDTH = WIDTH//TILESIZE
GRID_HEIGHT = HEIGHT//TILESIZE

FPS = 6

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

direction = choice(["left","right","up","down"])
head = (randint(2,GRID_WIDTH-3),randint(2,GRID_HEIGHT-3))
body = []
length = 10
food = None

def draw():
	global head,body,food
	pygame.draw.rect(screen,"green",((head[0] * TILESIZE,head[1] * TILESIZE),(TILESIZE,TILESIZE)))
	for segment in body:
		pygame.draw.rect(screen,"green",((segment[0] * TILESIZE,segment[1] * TILESIZE),(TILESIZE,TILESIZE)))

	if food:
		pygame.draw.rect(screen,"red",((food[0] * TILESIZE,food[1] * TILESIZE),(TILESIZE,TILESIZE)))

def spawn_food():
	global food,head,body
	pos = None
	while pos in [head,*body,food,None]:
		pos = (randint(0,GRID_WIDTH-1),randint(0,GRID_HEIGHT-1))
	return pos

def move():
	global head,body,length
	body.append(head)
	if len(body) >= length:
		body.pop(0)
	if direction == "left":
		head = (head[0]-1,head[1])
	elif direction == "right":
		head = (head[0]+1,head[1])
	elif direction == "up":
		head = (head[0],head[1]-1)
	elif direction == "down":
		head = (head[0],head[1]+1)

def collide():
	global head,body,food
	if head == food:
		eat()
	if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
		return True
	if head in body:
		return True
	return False

def eat():
	global head,food,length
	food = None
	length += 1

run = True
lose = False
while run:
	if not lose:
		screen.fill("black")
	else:
		screen.fill("dark red")
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			break
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT and direction != "right":
				direction = "left"
			elif event.key == pygame.K_RIGHT and direction != "left":
				direction = "right"
			elif event.key == pygame.K_DOWN and direction != "up":
				direction = "down"
			elif event.key == pygame.K_UP and direction != "down":
				direction = "up"
			elif event.key == pygame.K_r:
				direction = choice(["left","right","up","down"])
				head = (randint(2,GRID_WIDTH-3),randint(2,GRID_HEIGHT-3))
				body = []
				length = 10
				food = None
				lose = False
	
	if not lose:
		if not food:
			food = spawn_food()
		move()
		lose = collide()
	draw()

	pygame.display.update()
	clock.tick(FPS)

pygame.quit()
sys.exit()
