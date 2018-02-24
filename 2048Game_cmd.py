import random
import termios, sys
import tabulate
import time

def init():
	matrix = [[0] * 4 for _ in range(4)]
	pos = random.sample(range(16), 2)
	row0, col0 = pos[0] // 4, pos[0] % 4
	row1, col1 = pos[1] // 4, pos[1] % 4
	matrix[row0][col0] = 2
	matrix[row1][col1] = 2

	return matrix

def move(matrix, dirn):
	flag = 0
	if dirn == 'up' or dirn == 'down':
		for j in range(4):
			col = []
			for i in range(4):
				col.append(matrix[i][j])
			col = _update(col, dirn == 'up')
			for i in range(4):
				if matrix[i][j] != col[i]:
					flag = 1
					matrix[i][j] = col[i]
				
	elif dirn == 'left' or dirn == 'right':
		for i in range(4):
			row = []
			for j in range(4):
				row.append(matrix[i][j])
			row = _update(row, dirn == 'left')
			for j in range(4):
				if matrix[i][j] != row[j]:
					flag = 1
					matrix[i][j] = row[j]
	return flag

def _update(rowCol, dirn = True):
	if not dirn:
		rowCol.reverse()
	
	raw = []
	while rowCol:
		tmp = rowCol.pop(0)
		if tmp == 0:
			continue
		raw.append(tmp)

	new = [0] * 4
	j = 0
	while raw:
		tmp = raw.pop(0)
		if not raw or tmp != raw[0]:
			new[j] = tmp
		else:
			raw.pop(0)
			new[j] = tmp * 2
		j += 1

	if not dirn:
		new.reverse()

	return new

def insert(matrix, flag):
	if flag:
		tmp = []
		for i in range(4):
			for j in range(4):
				if matrix[i][j] == 0:
					tmp.append((i, j))
		choice = random.choice(tmp)
		i, j = choice
		# matrix[i][j] = random.choice([2, 4])
		matrix[i][j] = 2

def getChar(prompt = 'Continue to play\n'):
	
	fd = sys.stdin.fileno()
	old = termios.tcgetattr(fd)
	new = termios.tcgetattr(fd)
	new[3] = new[3] & ~termios.ICANON
	try:
		termios.tcsetattr(fd, termios.TCSADRAIN, new)
		sys.stderr.write(prompt)
		# sys.stderr.flush()
		ch = sys.stdin.read(3)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old)
	print
	return ch

def gameOver(matrix):
	# check if matrix is empty
	for i in range(4):
		for j in range(4):
			if matrix[i][j] == 0:
				return False
	# check if there exists identical adjacent numbers
	for i in range(3):
		for j in range(4):
			if matrix[i][j] == matrix[i + 1][j]:
				return False
	for j in range(3):
		for i in range(4):
			if matrix[i][j] == matrix[i][j + 1]:
				return False
	return True

def output(matrix):
	tmp = [[''] * 4 for _ in range(4)]
	for i in range(4):
		for j in range(4):
			if matrix[i][j] != 0:
				tmp[i][j] = matrix[i][j]
	print tabulate.tabulate(tmp, tablefmt = 'grid')

def main():
	matrix = init()
	moves = 0
	while True:
		output(matrix)
		time.sleep(0.01)
		if gameOver(matrix):
			print moves, 'moves'
			print 'Game over!'
			break
		moves += 1

		dirnMap = {'\x1b[A': 'up', '\x1b[B': 'down', '\x1b[C': 'right', '\x1b[D': 'left'}
		ch = getChar()
		# ch = random.choice(dirnMap.keys())
		dirn = dirnMap[ch]
		print dirn
		flag = move(matrix, dirn)
		insert(matrix, flag)

if __name__ == '__main__':
	main()