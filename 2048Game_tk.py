from Tkinter import *
import random # randomly generate numbers
from datetime import datetime # to record start and end time
from tabulate import tabulate # to print matrix in grids and save to a .txt file

# create number colour dictionary
# rgb code from http://www.w3schools.com/colors/colors_picker.asp

# red
# colours = {0: '#ffe6e6', 2: '#ffcccc', 4: '#ffb3b3', 8: '#ff9999', 16: '#ff8080', 32: '#ff6666', 64: '#ff4d4d', 128: '#ff3333', 256: '#ff1a1a', 512: '#ff0000', 1024: '#e60000', 2048: '#cc0000', 4096: '#b30000'}

# rainbow
colours = {0: '#ffe6e6', 2: '#ff4000', 4: '#ff8000', 8: '#ffbf00', 16: '#ffff00', 32: '#80ff00', 64: '#40ff00', 128: '#00ff00', 256: '#00ff40', 512: '#00ff80', 1024: '#00ffbf', 2048: '#00ffff', 4096: '#00bfff'}



class Game(Frame):
	def __init__(self):
		'''
		initialisation function
		'''
		Frame.__init__(self)
		self.grid()
		# add title
		self.master.title('2048')
		# key bind to allow arrow key input
		self.master.bind('<Up>', self.callback_up)
		self.master.bind('<Down>', self.callback_down)
		self.master.bind('<Left>', self.callback_left)
		self.master.bind('<Right>', self.callback_right)

		# game state
		self.isOver = False

		# initialise matrix
		self.init()

		# initialise total number of moves to 0
		self.moves = 0

		# define canvas size
		self.canvas = Canvas(self, width = 620, height = 620)
		self.canvas.pack()

		# record gameStart time spot 
		self.tStart = datetime.now()
		
		# update grid to show initialised matrix
		self.canvasDraw()

		self.mainloop()

	def canvasDraw(self):
		'''
		draw to canvas
		'''
		self.canvas.delete('all')

		# 4 x 4 rectangles with width = height = 150px

		# draw 5 horizontal lines
		self.canvas.create_line(10, 10, 610, 10)
		self.canvas.create_line(10, 160, 610, 160)
		self.canvas.create_line(10, 310, 610, 310)
		self.canvas.create_line(10, 460, 610, 460)
		self.canvas.create_line(10, 610, 610, 610)

		# draw 5 vertical lines
		self.canvas.create_line(10, 10, 10, 610)
		self.canvas.create_line(160, 10, 160, 610)
		self.canvas.create_line(310, 10, 310, 610)
		self.canvas.create_line(460, 10, 460, 610)
		self.canvas.create_line(610, 10, 610, 610)

		# display matrix content
		for i in range(4):
			for j in range(4):
				num = self.matrix[i][j]
				# location of num on canvas
				x, y = 85 + 150 * j, 85 + 150 * i
				# draw rectangle for the background colour of each number
				self.canvas.create_rectangle(10 + 150 * j, 10 + 150 * i, 160 + 150 * j, 160 + 150 * i, fill = colours[num])
				# if matrix[i][j] is zero, do not show matrix[i][j] on canvas (leave rectangle empty)
				if self.matrix[i][j] != 0:
					self.canvas.create_text(x, y, text = str(num), font = ('Serif', 60 - len(str(num)) * 5, 'bold')) # reduce font size when the number of digits increases

	def thumbnailDraw(self):
		'''
		show summary information of a finished game
		'''

		# use rectangle to cover original canvas
		self.canvas.create_rectangle(10, 10, 610, 610, fill = 'grey')

		# display a shrinked view of matrix, width and height of each rectangle reduce to 80px

		# draw horizontal lines
		self.canvas.create_line(150, 50, 470, 50)
		self.canvas.create_line(150, 130, 470, 130)
		self.canvas.create_line(150, 210, 470, 210)
		self.canvas.create_line(150, 290, 470, 290)
		self.canvas.create_line(150, 370, 470, 370)

		# draw vertical lines
		self.canvas.create_line(150, 50, 150, 370)
		self.canvas.create_line(230, 50, 230, 370)
		self.canvas.create_line(310, 50, 310, 370)
		self.canvas.create_line(390, 50, 390, 370)
		self.canvas.create_line(470, 50, 470, 370)
		
		# display matrix content
		for i in range(4):
			for j in range(4):
				num = self.matrix[i][j]
				x, y = 190 + 80 * j, 90 + 80 * i
				self.canvas.create_rectangle(150 + 80 * j, 50 + 80 * i, 230 + 80 * j, 130 + 80 * i, fill = colours[num])
				if self.matrix[i][j] != 0:
					self.canvas.create_text(x, y, text = str(num), font = ('Serif', 40 - len(str(num)) * 5, 'bold'))

		# display 'Game over!' message
		self.canvas.create_text(310, 420, text = 'Game over!', fill = 'red', font = ('Serif', 50, 'bold'))

		# display summary information
		self.canvas.create_text(310, 520, text = '\n'.join(self.summary), font = ('Serif', 24, 'bold'))

	def init(self):
		'''
		create a 4 x 4 matrix to store numbers (empty grids are denoted by 0) and initialise matrix with two numbers (2 or 4) at random locations
		'''
		self.matrix = [[0] * 4 for _ in range(4)]
		indices = [i for i in range(16)]
		random.shuffle(indices)
		# get first two indices to initialise two numbers at corresponding locations
		pos = indices[:2]
		# location 1
		row0, col0 = pos[0] // 4, pos[0] % 4
		# location 2
		row1, col1 = pos[1] // 4, pos[1] % 4
		# number can be 2 or 4
		self.matrix[row0][col0] = random.choice([2, 4])
		self.matrix[row1][col1] = random.choice([2, 4])

	def move(self, dirn):
		'''
		update matrix and determine whether move is in effect
		'''
		# use flag to denote matrix has been updated (i.e., whether the move is effective) with move in direction dirn (up, down, left, right)
		flag = 0
		# 'up' or 'down' direction, update each column of matrix
		if dirn == 'up' or dirn == 'down':
			for j in range(4):
				col = [] # get each column
				for i in range(4):
					col.append(self.matrix[i][j])
				col = self._update(col, dirn == 'up') # update column
				# assign value to matrix and determine whether move is in effect by comparing updated column with the original
				for i in range(4):
					if self.matrix[i][j] != col[i]:
						flag = 1
						self.matrix[i][j] = col[i]
		# 'left' or 'right' direction, update each row of matrix
		elif dirn == 'left' or dirn == 'right':
			for i in range(4):
				row = [] # get each row
				for j in range(4):
					row.append(self.matrix[i][j])
				row = self._update(row, dirn == 'left') # update row
				for j in range(4):
					if self.matrix[i][j] != row[j]:
						flag = 1
						self.matrix[i][j] = row[j]
		# return whether move is in effect
		return flag

	def _update(self, rowCol, dirn = True):
		'''
		update each row or column
		'''
		# define 'up' and 'left' as True dirn
		# reverse rowCol for 'down' and 'right'
		# requiring new array to be reversed at the end
		if not dirn:
			rowCol.reverse()
		
		# use queue to store non-zero numbers in rowCol
		queue = []
		while rowCol:
			tmp = rowCol.pop(0)
			if tmp == 0:
				continue
			queue.append(tmp)

		# initialise new array to be returned
		new = [0] * 4
		# initialise the index of new to j
		j = 0
		# pop each number in queue
		# case 1: queue is empty or current number is not equal to the next number in queue, update new[j] with current number
		# case 2: otherwise, pop the next number and update new[j] with their sum
		while queue:
			# pop from queue
			tmp = queue.pop(0)
			# case 1
			if not queue or tmp != queue[0]:
				new[j] = tmp
			# case 2
			else:
				queue.pop(0)
				new[j] = tmp * 2
			# update index of new
			j += 1

		# reverse new array
		if not dirn:
			new.reverse()

		return new

	def insert(self):
		'''
		insert a random number (2 or 4) to a random location in matrix
		'''
		# use tmp to store locations with number 0 (empty grids)
		tmp = []
		for i in range(4):
			for j in range(4):
				if self.matrix[i][j] == 0:
					tmp.append((i, j))
		# randomly choose a location from tmp
		choice = random.choice(tmp)
		i, j = choice
		# assign 2 or 4 to selected location
		self.matrix[i][j] = random.choice([2, 4])

	def gameOver(self):
		'''
		determine whether game is over
		'''
		# check if matrix has zero (empty grids), moves allowed
		for i in range(4):
			for j in range(4):
				# empty grid found, game can continue
				if self.matrix[i][j] == 0:
					return False
		
		# check if there exists identical adjacent numbers (in adjacent rows or columns), they can be combined to allow moves

		# check rows
		for i in range(3):
			for j in range(4):
				if self.matrix[i][j] == self.matrix[i + 1][j]:
					return False
		# check columns
		for j in range(3):
			for i in range(4):
				if self.matrix[i][j] == self.matrix[i][j + 1]:
					return False
		return True

	# 4 callback functions for four arrow keys
	def callback_up(self, event):
		self.getDirn('up')

	def callback_down(self, event):
		self.getDirn('down')

	def callback_left(self, event):
		self.getDirn('left')

	def callback_right(self, event):
		self.getDirn('right')

	def getDirn(self, dirn):
		'''
		get direction and update game state
		'''
		# only allow input before game is over
		if not self.isOver:
			# check whether game is over
			if not self.gameOver():
				# move grids using dirn and determine whether move is in effect
				flag = self.move(dirn)
				# use flag to decide whether to insert a new random number at a random location
				if flag:
					# update total number of moves
					self.moves += 1
					# insert 2 or 4 to a random location in the matrix
					self.insert()
				# show grids
				self.canvasDraw()
			else:
				# update game state isOver
				self.isOver = True
				# record gameOver time spot
				self.tEnd = datetime.now()
				# calculate how long one game lasts
				self.tDiff = self.tEnd - self.tStart
				
				# time formats and convert time difference into seconds
				tStart = self.tStart.strftime('%m/%d/%Y %H:%M:%S')
				tEnd = self.tEnd.strftime('%m/%d/%Y %H:%M:%S')
				tDiff = self.tDiff.seconds

				# create a .txt file to store summary information
				# use game end time as file name to avoid potential clash
				filename = self.tEnd.strftime('%Y-%m-%d %H-%M-%S') + '.txt'

				f = open(filename, 'w+')

				self.summary = []
				
				# summary information includes:
				# - game start time
				# - game end time
				# - game last time
				# - total moves
				self.summary.append('Game started at:\t' + tStart)
				self.summary.append('Game ended at:\t' + tEnd)
				self.summary.append('Game lasted:\t' + str(tDiff) + ' second(s)')
				self.summary.append('Total move(s):\t' + str(self.moves))

				# write to .txt file
				f.write('\n'.join(self.summary))
				f.write('\n')
				f.write(tabulate(self.matrix, tablefmt = 'grid'))
				
				f.close()

				# update canvas to show summary information
				self.thumbnailDraw()

# start game
if __name__ == '__main__':
	game = Game()


# sound from http://soundbible.com/tags-mac.html
# successful merge: http://soundbible.com/1672-Button-Press.html
# move not effective: http://soundbible.com/1540-Computer-Error-Alert.html