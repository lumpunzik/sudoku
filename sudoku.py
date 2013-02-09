import sys

default = 0	# Default empty cell value

# Matrix of Sudoku Table
table = []
# Populate initially with default values
for i in range(0,9):
	row = []
	for j in range(0,9):
		row.append(default)
	table.append(row)

# Matrix of possible cell values
possible = []
# Fills each cell with integers 1-9 as possibilities
for i in range(0,9):
	possrow = []
	for j in range(0,9):
		posscell = []
		for k in range(1,10):
			posscell.append(k)
		possrow.append(posscell)
	possible.append(possrow)

# Show dat pretty table
def showprettytable():
	print '\nCurrent Table (dash denotes empty cell)\n'
	for i in range(0,9):
		if i % 3 == 0:
			print '\n'
		for j in range(0,9):
			if j % 3 == 0:
				print '\t',
			if table[i][j] == default:
				print '-',
			else:
				print str(table[i][j]),
		print '\n'

# Clear the table by resetting all values to zero
def cleartable():
	for row in range(0,9):
		for col in range(0,9):
			table[row][col] = 0
			possible[row][col] = []
			for depth in range(1,10):
				possible[row][col].append(depth)

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
				for k in range(1,10):
					if possible[i][j].count(k) == 0:
						pass
					else:
						possible[i][j].remove(k)
					if possible[i][k - 1].count(table[i][j]) == 0:  	# Remove cell value as possibility for the row
						pass
					else:
						possible[i][k - 1].remove(table[i][j])
					if possible[k - 1][j].count(table[i][j]) == 0:  	# Remove cell value as possibility for the column
						pass
					else:
						possible[k - 1][j].remove(table[i][j])
				for l in range(3 * (i / 3), 3 + 3 * (i / 3)):			# Remove cell value as possibility for the box
					for m in range(3 * (j / 3), 3 + 3 * (j / 3)):
						if possible[l][m].count(table[i][j]) == 0:
							pass
						else:
							possible[l][m].remove(table[i][j])
				possible[i][j].append(table[i][j])             			# Reset cell's value as its sole possibility
	return table, possible

# Debugging function that prints a matrix of all the remaining possibilities in the table
def printposs(possible):    
	for i in range(0,9):
		for j in range(0,9):
			print possible[i][j]
		print'\n'

# Solve individual cells if possible
def solve(table,possible):
	for i in range(0,9):
		for j in range(0,9):
			if table[i][j] == 0:
				listcount = 0
				for k in range(1,10):
					listcount = listcount + possible[i][j].count(k)
				if listcount == 1:								# Solve if only one possibility remains for the cell
					table[i][j] = possible[i][j].pop()
					print 'solving cell %sx%s (explicit)' % (i, j)	# For debugging
					possible[i][j].append(table[i][j])
					eliminate(table,possible)					# Run the elimination routine whenever a cell is solved
	for i in range(0,3):										# Solve boxes by counting the number of cells where a value is possible; if there is only one such cell, then the cell must be that value
		for j in range(0,3):
			for k in range(1,10):
				boxcount = 0
				for l in range(i * 3, 3 + (i * 3)):
					for m in range(j * 3, 3 + (j * 3)):
						if possible[l][m].count(k) == 0:
							pass
						else:
							boxcount += 1
				if boxcount == 1:
					for l in range(i * 3, 3 + (i * 3)):
						for m in range(j * 3, 3 + (j * 3)):
							if possible[l][m].count(k) == 1 and table[l][m] == 0:
								print 'solving cell %sx%s (implicit box)' % (l, m)	# For debugging
								table[l][m] = possible[l][m].pop(possible[l][m].index(k))
								possible[l][m].append(table[l][m])
								eliminate(table,possible)
	for i in range(0,9):										# Solve rows the same way as the box solver above
		for j in range(1,10):
			rowcount = 0
			for k in range(0,9):
				if possible[i][k].count(j) == 0:
					pass
				else:
					rowcount += 1
			if rowcount == 1:
				for k in range(0,9):
					if possible[i][k].count(j) == 1 and table[i][k] == 0:
						print 'solving cell %sx%s (implicit row)' % (i, k)	# For debugging
						table[i][k] = possible[i][k].pop(possible[i][k].index(j))
						possible[i][k].append(table[i][k])
						eliminate(table,possible)
	for i in range(0,9):										# Solve columns the same way as the row solver above
		for j in range(1,10):
			colcount = 0
			for k in range(0,9):
				if possible[k][i].count(j) == 0:
					pass
				else:
					colcount += 1
			if colcount == 1:
				for k in range(0,9):
					if possible[k][i].count(j) == 1 and table[k][i] == 0:
						print 'solving cell %sx%s (implicit column)' % (i, k)	# For debugging
						table[k][i] = possible[k][i].pop(possible[k][i].index(j))
						possible[k][i].append(table[k][i])
						eliminate(table,possible)
	return table, possible

# If the solver runs through without changing a value, just in case it might be needed
def guess(table,possible):
	pass

# Attempts to solve the table by iterating the eliminate, solve functions
def attempt(table,possible):
	count = 0
	for i in range(0,9):
		for j in range(0,9):
			if table[i][j] == 0:
				count += 1
	if count > 0:
		for iterations in range(1,30):		# Run 30 iterations
			eliminate(table,possible)
			solve(table,possible)
			print iterations
	else:
		print 'The table is filled completely.'

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
		cleartable()			# Clears table first, so that the 'possible' matrix is reset
		loadtable()
		print '\n---'
		mainmenu()
	elif int(menu) == 3:
		showprettytable()		# Display the table
		print '\n---'
		mainmenu()
	elif int(menu) == 4:
		attempt(table,possible)
		#printposs(possible)
		print '\n---'
		mainmenu()
	elif int(menu) == 5:
		print 'Are you sure? (y/n)'
		sure = raw_input('> ')
		if sure == 'y' or sure == 'Y':
			cleartable()		# Clear table by resetting all values to zero
		mainmenu()
	elif int(menu) == 6:
		sys.exit(0)
	elif int(menu) == 7:
		printposs(possible)
		mainmenu()
	else:
		print 'Invalid input. Try again.'
		mainmenu()

mainmenu()