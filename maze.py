import pygame
import random 
from math import ceil
from sys import argv, exit
from time import sleep
from subprocess import Popen, PIPE, STDOUT
import maze2
from datetime import datetime
random.seed(datetime.now())

if len(argv) < 3:
	print 'Usage: ./maze <level> [filename] [-i(nteractive)] [-f(astmode)]'
	exit(1)

block_size = 80 #pixels
board_width = 7
board_height = 9
num_points = 3
point_score = 100 
move_score = -1
walls = False
filename = argv[2]
interactive = ('-i' in argv)
fastmode = ('-f' in argv)
level = int(argv[1])

if level == 1: 
	num_points = 1
	board_width = 3
	board_height = 3
	walls = False
elif level == 2: 
	block_size = 60
	num_points = 1
	board_width = 5
	board_height = 5
	walls = False
elif level == 3: 
	block_size = 60
	num_points = 3
	board_width = 5
	board_height = 5
	walls = False
elif level == 4: 
	block_size = 50
	num_points = 5
	board_width = 7
	board_height = 9
	walls = False
elif level == 5: 
	block_size = 60
	num_points = 1
	board_width = 5
	board_height = 5
	walls = True
elif level == 6: 
	block_size = 50
	num_points = 3
	board_width = 7
	board_height = 9
	walls = True
elif level == 7: 
	block_size = 40
	num_points = 10
	board_width = 15
	board_height = 15
	walls = True
elif level == 8: 
	block_size = 20
	num_points = 45
	board_width = 61
	board_height = 41
	walls = True
else:
	print "Invalid level"
	exit(1)

if board_width%2 or board_height%2:
	print "Width and height must be odd"

score = point_score

width = block_size * board_width
height = block_size * board_height


red = (0xf4, 0x43, 0x36)
white = (0xE0, 0xE0, 0xE0)
green = (0x8B, 0xC3, 0x4A)
blue = (0x1E, 0x88, 0xE5)

screen = pygame.display.set_mode((width, height))

def pygameInit():
	# pygame.init()
	screen.fill(white)

def drawRect(position, wall, color = (0,0,0)):
	pygame.draw.rect(screen, color, (block_size*position[0], block_size*position[1], block_size, block_size), 0 if wall else 1)

def pygameUpdate():
	pygame.display.update()

def drawMaze(maze):
	global walls
	screen.fill(white)
	for i in xrange(len(maze)):
		for j in xrange(len(maze[i])):
			if maze[i][j]=='W' and walls: 
				drawRect((j,i), True, red)
			elif not walls:
				drawRect((j,i), False, green) 

def drawPlayer(position):
	pygame.draw.circle(screen, green, (position[1]*block_size + block_size/2, position[0]*block_size + block_size/2), block_size/6, 0)

def drawPoints(points):
	for position in points:
		pygame.draw.circle(screen, blue, (position[1]*block_size + block_size/2, position[0]*block_size + block_size/2), block_size/10, 0)

def getMaze(walls = True):
	if walls: 
		return maze2.Maze.generate(int(ceil((width//block_size-1)/2.0)), int(ceil((height//block_size-1)/2.0)))._to_str_matrix()
	m = []
	for i in xrange(height/block_size):
		q = []
		for j in xrange(width/block_size):
			q.append(".")
		m.append(q)
	return m

def initPlayer():
	player = (0,0)
	while maze[player[0]][player[1]]=='W':
		player = (random.randint(1,len(maze)-1), random.randint(1,len(maze[0])-1))
	return player

def initPoints():
	points = []
	for i in xrange(num_points):
		k = (0,0)
		while maze[k[0]][k[1]]=='W' or k == player or k in points:
			k = (random.randint(0,len(maze)-1), random.randint(0,len(maze[0])-1))
		points.append(k)
	return points

def printMaze(maze, player, points):
	print "-"*len(maze[0])
	mstr = ""
	mstr += str(len(maze)) + " " + str(len(maze[0])) + "\n"
	m = []
	for i in maze:
		m.append(list(i))
	m[player[0]][player[1]] = 'P'
	for i in points: 
		m[i[0]][i[1]] = 'o'
	for i in m: 
		mstr+=''.join(i) + "\n"
	print mstr,
	print "-"*len(maze[0])
	return mstr

def eatPoint(position, points, maze):
	if position not in points: return
	points.remove(position)
	global score
	score += point_score

def move(player, move, points, maze):
	global score
	n = player
	if move == 'up':
		n = (player[0]-1, player[1])
	elif move == 'down':
		n = (player[0]+1, player[1])
	elif move == 'left':
		n = (player[0], player[1]-1)
	elif move == 'right':
		n = (player[0], player[1]+1)
	else: 
		print "Error: Invalid Input"
	score += move_score
	try:
		if n[0]<0 or n[1]<0 or maze[n[0]][n[1]]=='W':
			print "Wrong move"
			return player
	except: 
		print "Wrong move"
		return player
	if n in points:
		eatPoint(n, points, maze)
	return n


pygameInit()
maze = getMaze(walls)
player = initPlayer()
points = initPoints()

printMaze(maze, player, points)

while len(points)>0 and score>0:
	print "\n-----------------------\nScore =", score
	drawMaze(maze)
	drawPlayer(player)
	drawPoints(points)
	pygameUpdate()
	print "Input:"
	mstr = printMaze(maze, player, points)
	if not fastmode: sleep(0.5)

	mov = 'left'
	if not interactive:
		p = Popen([filename], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
		stdout_data = p.communicate(input=mstr + '\n')
		if len(stdout_data[1])>1:
			print "Output: ", stdout_data[0]
			print "Error: ", stdout_data[1]
			exit(2)
		mov = stdout_data[0]
	else: 
		mov = raw_input()
	print "Your move:", mov
	if len(mov)==0:
		print "Empty Move"
		continue
	if mov[-1]=='\n': mov = mov[:-1]
	player = move(player, mov, points, maze)
	
print "\n-----------------------\nGame Over\n-----------------------\n"
print "Score =", score
drawMaze(maze)
drawPlayer(player)
drawPoints(points)
pygameUpdate()
printMaze(maze, player, points)

if score<=0 or len(points)>0: 
	print "You Lost"
else:
	print "You Win"

sleep(2)
