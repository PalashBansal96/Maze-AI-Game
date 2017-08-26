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
	print 'Usage: ./maze <size_level> [4 filenames] [-i(nteractive)] [-f(astmode)]'
	exit(1)

block_size = 80 #pixels
board_width = 5
board_height = 5
num_points = 3
point_score = 100 
move_score = -1
walls = False
interactive = ('-i' in argv)
filename = [argv[2], argv[3], argv[4], argv[5]] if not interactive else []

fastmode = ('-f' in argv)
level = int(argv[1])

if level == 1: 
	num_points = 1
	board_width = 5
	board_height = 5
	walls = False
elif level == 2: 
	block_size = 60
	num_points = 1
	board_width = 10
	board_height = 10
	walls = False
elif level == 3: 
	block_size = 40
	num_points = 3
	board_width = 15
	board_height = 15
	walls = False
elif level == 4: 
	block_size = 30
	num_points = 5
	board_width = 20
	board_height = 20
	walls = False
else:
	print "Invalid level"
	exit(1)

if board_width%2 or board_height%2:
	print "Width and height must be odd"

score = point_score

width = block_size * board_width
height = block_size * board_height


red = (0xf4, 0x03, 0x16)
red2 = (0xe5, 0x73, 0x73)
white = (0xE0, 0xE0, 0xE0)
green = (0x4B, 0xa3, 0x2A)
blue = (0x0E, 0x48, 0xE5)
blue2 = (0x4f, 0xc3, 0xf7)

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
			if maze[i][j]=='W': 
				drawRect((j,i), True, green)
			elif not walls:
				drawRect((j,i), False, green) 

def drawPlayer(position,color):
	pygame.draw.circle(screen, color, (position[1]*block_size + block_size/2, position[0]*block_size + block_size/2), block_size/4, 0)


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

def printMaze():
	print "-"*len(maze[0]) + "----"
	mstr = ""
	mstr += str(len(maze)) + " " + str(len(maze[0])) + "\n"
	mstr += chars[currentPlayer] + "\n"
	m = []
	for i in maze:
		m.append(list(i))
	if king1_char not in dead_players: m[king1[0]][king1[1]] = king1_char
	if king2_char not in dead_players: m[king2[0]][king2[1]] = king2_char
	if ninja1_char not in dead_players: m[ninja1[0]][ninja1[1]] = ninja1_char
	if ninja2_char not in dead_players: m[ninja2[0]][ninja2[1]] = ninja2_char
	for i in m: 
		mstr+=''.join(i) + "\n"
	print mstr,
	print "-"*len(maze[0]) + "----"
	return mstr

def eatPoint(position, points, maze):
	if position not in points: return
	points.remove(position)
	global score
	score += point_score

def move(player, move, maze):
	global score1
	global score2
	n = player
	delt  = 0
	if chars[currentPlayer] in '1A':
		delt = 1
	elif chars[currentPlayer] in '2B':
		delt = 2
	if move == 'up':
		n = (player[0]-delt, player[1])
	elif move == 'down':
		n = (player[0]+delt, player[1])
	elif move == 'left':
		n = (player[0], player[1]-delt)
	elif move == 'right':
		n = (player[0], player[1]+delt)
	if move == 'upleft':
		n = (player[0]-delt, player[1]-delt)
	elif move == 'upright':
		n = (player[0]-delt, player[1]+delt)
	elif move == 'downleft':
		n = (player[0]+delt, player[1]-delt)
	elif move == 'downright':
		n = (player[0]+delt, player[1]+delt)
	else: 
		print "Error: Invalid Input"
	try:
		if n[0]<0 or n[1]<0 or maze[n[0]][n[1]]=='W':
			print "Wrong move"
			n = player
	except: 
		print "Wrong move"
		n = player
	if n == king1:
		print "King1 Died"
		dead_players.append(king1_char)
		score2 += 1000
	elif n == king2:
		print "King2 Died"
		dead_players.append(king2_char)
		score1 += 1000
	if n == ninja1:
		print "Ninja1 Died"
		dead_players.append(ninja1_char)
		score2 += 100
	elif n == ninja2:
		print "Ninja2 Died"
		dead_players.append(ninja2_char)
		score1 += 100
	if n == player:
		print "You died"
	else: 
		if currentPlayer<2:
			score1 +=1
		else:
			score2 +=1
	maze[player[0]][player[1]] = 'W' 
	return n

score1 = 0
score2 = 0
currentPlayer = 0
king1_char = '1'
king2_char = 'A'
ninja1_char = '2'
ninja2_char = 'B'
chars = '12AB'
dead_players = []
pygameInit()
maze = getMaze(walls)
king1 = (0,0)
ninja1 = (board_width-1, 0)
ninja2 = (0, board_height-1)
king2 = (board_width-1, board_height-1)
printMaze()

while king1_char not in dead_players and king2_char not in dead_players:
	print "\n-----------------------\nScore T1 =", score1, "T2 =", score2
	drawMaze(maze)
	if king1_char not in dead_players: drawPlayer(king1, red)
	if king2_char not in dead_players: drawPlayer(king2, red2)
	if ninja1_char not in dead_players: drawPlayer(ninja1, blue)
	if ninja2_char not in dead_players: drawPlayer(ninja2, blue2)
	pygameUpdate()
	print "Input:"
	mstr = printMaze()
	if not fastmode: sleep(0.5)
	if chars[currentPlayer] in dead_players:
		print "Player", chars[currentPlayer], "is dead, so skipping"
		currentPlayer = (currentPlayer+1)%4
		continue
	mov = 'left'
	if not interactive:
		p = Popen([filename[currentPlayer]], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
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
	if currentPlayer==0:
		king1 = move(king1, mov, maze)
	if currentPlayer==2:
		king2 = move(king2, mov, maze)
	if currentPlayer==1:
		ninja1 = move(ninja1, mov, maze)
	if currentPlayer==3:
		ninja2 = move(ninja2, mov, maze)
	currentPlayer = (currentPlayer+1)%4

print "\n-----------------------\nGame Over\n-----------------------\n"
print "\n-----------------------\nScore T1 =", score1, "T2 =", score2
drawMaze(maze)
if king1_char not in dead_players: drawPlayer(king1, red)
if king2_char not in dead_players: drawPlayer(king2, red2)
if ninja1_char not in dead_players: drawPlayer(ninja1, blue)
if ninja2_char not in dead_players: drawPlayer(ninja2, blue2)
pygameUpdate()
printMaze()

if score1>score2:
	print "Team 1 wins by", score1 - score2
elif score2>score1:
	print "Team 2 wins by", score2 - score1
else:
	print "Its a draw"

sleep(2)
