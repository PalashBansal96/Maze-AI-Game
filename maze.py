import pygame
import random 
from math import ceil, sqrt	
from sys import argv, exit
from time import sleep
from subprocess import Popen, PIPE, STDOUT
import maze2
from datetime import datetime
random.seed(datetime.now())

if len(argv) < 2:
	print 'Usage: ./maze [filename] [-i(nteractive)] [-f(astmode)]'
	exit(1)

block_size = 80 #pixels
board_width = 3
board_height = 3
num_points = 3
point_score = 100 
move_score = -1
walls = False
filename = argv[1]
interactive = ('-i' in argv)
fastmode = ('-f' in argv)

if board_width%2 or board_height%2:
	print "Width and height must be odd"

score = point_score

width = block_size * board_width
height = block_size * board_height

red = (0xf4, 0x43, 0x36)
white = (0xE0, 0xE0, 0xE0)
green = (0x4B, 0xa3, 0x2A)
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
	n = int(sqrt(len(maze)))
	screen.fill(white)
	for i in xrange(1, board_width):
		pygame.draw.line(screen, green, (i * block_size, 0), (i * block_size, block_size * board_height), 2)
		pygame.draw.line(screen, green, (0, i * block_size), (block_size * board_height, i * block_size), 2)
	for i in xrange(1,n+1):
		for j in xrange(1,n+1):
			c = maze[3*(i-1)+j-1]
			if c == '.':
				pass;
			elif c == 'x':
				pygame.draw.line(screen, blue, (block_size/4 + (j-1) * block_size, block_size/4 + (i-1) * block_size), (-block_size/4 + (j) * block_size, -block_size/4 + (i) * block_size), 5)
				pygame.draw.line(screen, blue, (block_size/4 + (j-1) * block_size, -block_size/4 + (i) * block_size), (-block_size/4 + (j) * block_size, block_size/4 + (i-1) * block_size), 5)
			elif c == 'o':
				pygame.draw.circle(screen, red, (block_size/2 + (j-1) * block_size, block_size/2 + (i-1) * block_size), block_size/2 - 15, 5)

def drawPlayer(position):
	pygame.draw.circle(screen, green, (position[1]*block_size + block_size/2, position[0]*block_size + block_size/2), block_size/4, 0)

def drawPoints(points):
	for position in points:
		pygame.draw.circle(screen, blue, (position[1]*block_size + block_size/2, position[0]*block_size + block_size/2), block_size/10, 0)

def getMaze():
	return "." * 9

def printMaze(maze):
	n = int(sqrt(len(maze)))
	print "-"*n
	mstr = ''
	for i in xrange(1,n+1):
		for j in xrange(1,n+1):
			mstr += maze[3*(i-1)+j-1]
		mstr += '\n'
	print mstr
	print "-"*n
	return mstr

def move(move, maze, turn):
	global score
	a = ""
	for i in xrange(len(maze)):
		if i == move-1:
			if maze[i] == '.':
				a += turn
			else:
				return False
		else:
			a += maze[i]
	return a

def getBoardCopy(b):
	a = ''
	for i in b:
		a+=i
	return a

def chooseRandomMoveFromList(board, movesList):
    possibleMoves = []
    for i in movesList:
        if board[i-1] == '.':
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None

def pcMove(board):
    computerLetter = 'o'
    playerLetter = 'x'

    # Here is our algorithm for our Tic Tac Toe AI:
    # First, check if we can win in the next move
    for i in range(1, int(sqrt(len(board)))+1):
        copy = getBoardCopy(board)
        if copy[i-1] == '.':
            copy = move(i, copy, computerLetter)
            if isWinner(copy, computerLetter):
                return i

    # Check if the player could win on their next move, and block them.
    for i in range(1, int(sqrt(len(board)))+1):
        copy = getBoardCopy(board)
        if copy[i-1] == '.':
            copy = move(i, copy, playerLetter)
            if isWinner(copy, playerLetter):
                return i

    # Try to take one of the corners, if they are free.
    mo = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if mo != None:
        return mo

    # Try to take the center, if it is free.
    if board[5-1] == '.':
        return 5

    # Move on one of the sides.
    return chooseRandomMoveFromList(board, [2, 4, 6, 8])


def isWinner(maze, le):
    return ((maze[7-1] == le and maze[8-1] == le and maze[9-1] == le) or # across the top
    (maze[4-1] == le and maze[5-1] == le and maze[6-1] == le) or # across the middle
    (maze[1-1] == le and maze[2-1] == le and maze[3-1] == le) or # across the bottom
    (maze[7-1] == le and maze[4-1] == le and maze[1-1] == le) or # down the left side
    (maze[8-1] == le and maze[5-1] == le and maze[2-1] == le) or # down the middle
    (maze[9-1] == le and maze[6-1] == le and maze[3-1] == le) or # down the right side
    (maze[7-1] == le and maze[5-1] == le and maze[3-1] == le) or # diagonal
    (maze[9-1] == le and maze[5-1] == le and maze[1-1] == le)) # diagonal

def checkWin(maze):
	if isWinner(maze, 'x'):
		return 'x'
	if isWinner(maze, 'o'):
		return 'o'
	return False

pygameInit()
maze = getMaze()

printMaze(maze)

while '.' in maze:
	print "\n-----------------------\nScore =", score
	drawMaze(maze)

	pygameUpdate()
	print "Input:"
	mstr = printMaze(maze)
	if not fastmode: sleep(1)

	mov = '0'
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
	if len(mov)>1 or mov not in "123456789":
		print "Invalid Move"
		continue
	kk = move(int(mov), maze, 'x')
	if not kk: 
		print "Wrong move"
		continue
	else:
		maze = kk
	if checkWin(maze): break
	maze = move(pcMove(maze), maze, 'o')
	if checkWin(maze): break

	
print "\n-----------------------\nGame Over\n-----------------------\n"
drawMaze(maze)
pygameUpdate()
printMaze(maze)

w = checkWin(maze)
if w == 'x':
	print 'A winner is you!'
elif w == 'o':
	print 'You lose'
else: 
	print 'Its a draw'

sleep(1)
