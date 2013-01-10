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

# Matrix of possible cell values
possible = []
# All default to True, where True denotes that a value is possible, and False == Impossible
for i in range(0,9):
	possrow = []
	for j in range(0,9):
		posscell = []
		for k in range(0,9):
			posscell.append(True)
		possrow.append(posscell)
	possible.append(possrow)

# Show dat pretty table
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
		
# Clear the table by resetting all values to zero
def cleartable():
	for row in range(0, 9):
		for col in range(0, 9):
			table[row][col] = 0

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

# Load a table from a set
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

# Read each cell in the table and determine the remaining possibilities
def eliminate(table,possible):
	for i in range(0,9):	# Row
		for j in range(0,9):	# Column
			if table[i][j] != 0:	# If the cell is nonzero it must be an integer between 1 and 9, since we have an input validation
				for k in range(0,9):
					possible[i][j][k] = False				# All possibilities get set to false, the actual value gets reset to True below
					possible[i][k][table[i][j] - 1] = False			# Set all cells in the respective row to false for the value
					possible[k][j][table[i][j] - 1] = False			# Set all cells in the respective column to false for the value
					for l in range(0 + 3 * (i / 3),3 + 3 * (i / 3)):	# Set all cells in the respective box to false for the value
						for m in range(0 + 3 * (j / 3),3 + 3 * (j / 3)):
							possible[l][m][table[i][j] - 1] = False
				possible[i][j][table[i][j] - 1] = True				# Reset the cell to True for the actual value
	return table, possible

# Use boolean values from the possiblities table to solve each cell
def solve(table,possible):
	for i in range(0,9):
		for j in range(0,9):
			if table[i][j] == 0:	# Solve from explicitly eliminated possibilities. Sum how many are eliminated, if there are 8, then solve it.
				if possible[i][j].count(False) == 8:
					table[i][j] = possible[i][j].index(True) + 1
			# Implicit solve each row	
			# Implicit solve each column
			# Implicit solve each box
	return table, possible

# Main Menu
def mainmenu():
	print "\nMain Menu\n","1 - Enter a Value\n","2 - Load a Table\n","3 - Show Current Table\n","4 - Attempt to Solve\n","5 - Clear Table\n","6 - Exit"
	menu = raw_input("Enter your selection: ")
	if int(menu) == 1:
		r = promptandvalidate('Enter Row Number (1-9): ',1,9)		# Row input
		c = promptandvalidate('Enter Column Number (1-9): ',1,9)	# Column input
		n = promptandvalidate('Enter Cell Value (1-9): ',1,9)		# Cell value input
		table[r-1][c-1] = n
		print '\n---'
		mainmenu()
	elif int(menu) == 2:		# Load a table
		loadtable()
		print '\n---'
		mainmenu()
	elif int(menu) == 3:
		showprettytable()	# Display the table
		print '\n---'
		mainmenu()
	elif int(menu) == 4:
		# Attempt to solve the table
		for i in range(0,10):   # HARDCODED ITERATION COUNT IS TEMPORARY
			eliminate(table,possible)
			solve(table,possible)
		print '\n---'
		mainmenu()
	elif int(menu) == 5:
		print 'Are you sure? (y/n)'
		sure = raw_input('> ')
		if sure == 'y' or sure == 'Y':
			cleartable()	# Clear table by resetting all values to zero
		mainmenu()
	elif int(menu) == 6:
		sys.exit(0)
	else:
		print 'Invalid input. Try again.'
		mainmenu()

mainmenu()