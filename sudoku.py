import sys

z = 0	# Default empty cell value

# Matrix of Sudoku Table
table = []
# Populate initially with default values
for i in range(0,9):
	row = []
	for j in range(0,9):
		row.append(z)
	table.append(row)

def showprettytable():
	print '\nCurrent Table (dash denotes empty cell)\n'
	for i in range(0, 9):
		if i % 3 == 0:
			print '\n'
		for j in range(0, 9):
			if j % 3 == 0:
				print '\t',
			if table[i][j] == z:
				print '-',
			else:
				print str(table[i][j]),
		print '\n'

# Show Table
def showtable():
	print '\nCurrent Table (0 denotes empty cell)\n'
	print table[0], '\n', table[1], '\n', table[2], '\n', table[3], '\n', table[4], '\n', table[5], '\n', table[6], '\n', table[7], '\n', table[8], '\n', # Print each row on a new line

def promptandvalidate(prompt,low,high):
	result = raw_input(prompt)
	if result.isdigit():
		num = int(result)
		if low <= num <= high:
			return num
		else:
			print 'Invalid input.  Try again.'
			return promptandvalidate(prompt,low,high)
	else:
		print 'Invalid input.  Try again.'
		return promptandvalidate(prompt,low,high)

def loadtable():
	line = promptandvalidate('Enter a Puzzle Number (1-1011): ',1,1011)
	puzzle = ''
	with open('puzzles.txt', 'r') as f:
		for num in range(0,line):
			puzzle = f.readline()
		f.close()
	# puzzle string now stores our desired table
	for i in range(0,81):
		table[i/9][i%9] = int(puzzle[i])
	# math sure is awesome
	print 'Puzzle number ' + str(line) + ' now loaded.'

# Comparison routine for values in the same box
def box(number,r1,r2,c1,c2):
	for rowx in range(r1,r2):
		for colx in range(c1,c2):
			for num in range(1,10):
				if table[rowx][colx] == num:
					number[num-1] = True
	return number

# Solve
def solve():
	skipped = 0						# Number of cells initially at 0 that could not be solved in this iteration
	blank = 0						# Number of cells initially at 0 before running the solving routine
	for row in range(0,9):			# For every row...
		for col in range(0,9):		# ...And for every cell in each row (reads the table from left-to-right, top-to-bottom):
			number = [False,False,False,False,False,False,False,False,False];	# For values 1-9, True indicates that the current cell cannot be that number. Defaults to False for all when moving to a new cell.
			if table[row][col] == 0:			# If the current cell is blank, run the solving routine, otherwise skip to the next cell.
				blank += 1
				for rowx in range(0,9):			# Compare values from same row
					for num in range(1,10):
						if table[row][rowx] == num:
							number[num-1] = True
				for colx in range(0,9):			# Compare values from same column
					for num in range(1,10):
						if table[colx][col] == num:
							number[num-1] = True
				if row <= 2:					# Compare values from same box
					if col <= 2:
						box(number,0,3,0,3)
					elif col <= 5:
						box(number,0,3,3,6)
					elif col <= 8:
						box(number,0,3,6,9)
				elif row <= 5:
					if col <= 2:
						box(number,3,6,0,3)
					elif col <= 5:
						box(number,3,6,3,6)
					elif col <= 8:
						box(number,3,6,6,9)
				elif row <= 8:
					if col <= 2:
						box(number,6,9,0,3)
					elif col <= 5:
						box(number,6,9,3,6)
					elif col <= 8:
						box(number,6,9,6,9)
				solvable = 0
				for num in range(0,9):					# Is this cell solvable?
					if not number[num]:			# Count the number of possible values for the cell
						solvable += 1
				if solvable == 1:						# If there is only one possible value remaining, solve it.
					print '\nCell %sx%s is solvable!\nSolved.' % (row,col)	 # FINALLY actually solve here lolololol
					for num in range(0,9):
						if not number[num]:
							table[row][col] = num + 1
				else:									# Otherwise, skip this cell
					skipped += 1                        # ...And add it to the skip count for this iteration
	if blank > skipped:		# If at least one initially blank cell becomes filled, this iterates the solver until table is completely solved or requires more cells to be filled manually. 
		solve()
	else:					# If no cells were filled, blank == skipped, so there's no use in iteration.
		print '\nThe current table is as solved as possible.'

# Main Menu
def mainmenu():
	print "\nMain Menu\n","1 - Enter a Value\n","2 - Load a Table\n","3 - Show Current Table\n","4 - Attempt to Solve\n","5 - Clear Table\n","6 - Exit"
	menu = raw_input("Enter your selection: ")
	if int(menu) == 1:
		r = promptandvalidate('Enter Row Number (1-9): ',1,9)		# Row input
		c = promptandvalidate('Enter Column Number (1-9): ',1,9)	# Column input
		n = promptandvalidate('Enter Cell Value (1-9): ',1,9)	    # Cell value input
		table[r-1][c-1] = n
		print '\n---'
		mainmenu()
	elif int(menu) == 2:	# Load a table
		loadtable()
		print '\n---'
		mainmenu()
	elif int(menu) == 3:
		showprettytable()			# Display the table
		print '\n---'
		mainmenu()
	elif int(menu) == 4:
		solve()
		print '\n---'
		mainmenu()
	elif int(menu) == 5:
		print 'Are you sure? (y/n)'
		sure = raw_input('> ')
		if sure == 'y':		# Clears the table by resetting all values to zero
			for row in range(0,9):
				for col in range(0,9):
					table[row][col] = 0
			print 'Table cleared.'		
		print '\n---'
		mainmenu()
	elif int(menu) == 6:
		sys.exit(0)
	else:
		print 'Invalid input. Try again.'
		mainmenu()

mainmenu()
