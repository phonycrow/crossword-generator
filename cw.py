import copy
from pathlib import Path
from random import random
import time

letters = "ESIARNTOLCDUGPMHBYFVKWZXJQ"
consonants = "SRNTLCDGPMHBYFVKWZXJQ"
vowels = "EIAOU"
dictionary_file = Path(__file__).parent / "dictionary.txt"
possibilities_file = Path(__file__).parent / "possibilities.txt"

# Sample boards

board1 = [	"_|A|_|_|_",
			"B|_|_|_|_",
			"_|_|_|_|_",
			"_|_|_|_|_",
			"_|_|_|_|_",]

board2 = [	"_|A|_|_|#",
			"B|_|_|_|_",
			"_|_|_|_|_",
			"_|_|_|_|_",
			"#|_|_|_|_",]

board3 = [	"_|A|_|#|_|_|_",
			"E|_|_|#|_|_|_",
			"_|_|_|_|_|_|_",
			"#|#|_|_|_|#|#",
			"_|_|_|_|_|_|_",
			"_|_|_|#|_|_|E",
			"_|_|_|#|_|S|_",]


board4 = [  "_|_|_|_|#|_|_|_|#|_|_|_|_",
			"_|_|_|_|_|_|_|_|#|_|_|_|_",
			"_|_|_|_|_|_|_|_|#|_|_|_|_",
			"#|#|#|_|_|_|_|_|_|_|#|#|#",
			"_|_|_|_|#|_|_|_|_|_|_|_|_",
			"_|_|_|_|#|_|_|_|_|#|_|_|_",
			"_|_|_|_|#|#|#|#|#|_|_|_|_",
			"_|_|_|#|_|_|_|_|#|_|_|_|_",
			"_|_|_|_|_|_|_|_|#|_|_|_|_",
			"#|#|#|_|_|_|_|_|_|_|#|#|#",
			"_|_|_|_|#|_|_|_|_|_|_|_|_",
			"_|_|_|_|#|_|_|_|_|_|_|_|_",
			"_|_|_|_|#|_|_|_|#|_|_|_|_",]

board5= [   "_|_|_|_|#|_|_|_|_|_|#|_|_|_|_",
			"_|_|_|_|#|_|_|_|_|_|#|_|_|_|_",
			"_|_|_|_|_|_|_|_|_|_|#|_|_|_|_",
			"_|_|_|_|_|_|_|#|_|_|_|_|_|_|_",
			"#|#|#|_|_|_|_|_|_|_|_|_|_|#|#",
			"_|_|_|_|_|#|_|L|_|#|_|_|_|_|_",
			"_|_|_|_|_|_|#|_|_|_|_|_|_|_|_",
			"_|_|_|#|_|_|_|#|_|_|_|#|_|_|_",
			"_|_|_|_|_|_|_|_|#|_|_|_|_|_|_",
			"_|_|_|_|_|#|_|_|_|#|_|_|_|_|_",
			"#|#|_|_|_|_|_|_|_|_|_|_|#|#|#",
			"_|_|_|_|_|_|_|#|_|_|_|_|_|_|_",
			"_|_|_|_|#|_|_|_|_|_|_|_|_|_|_",
			"_|_|_|_|#|_|_|_|_|_|#|_|_|_|_",
			"_|_|_|_|#|_|_|_|_|_|#|_|_|_|_",]

board6 = [  "_|_|_|#|_|_|_|_|#|_|_|_|_|_|_",
			"_|_|_|#|_|_|_|_|#|_|_|_|_|_|_",
			"_|_|_|_|_|_|_|_|#|_|_|_|_|_|_",
			"_|_|_|_|_|_|_|_|#|_|_|_|#|#|#",
			"#|#|#|_|_|_|#|_|_|E|_|_|_|_|_",
			"_|_|_|_|_|#|_|_|_|_|_|_|_|_|_",
			"_|_|_|_|#|_|_|_|_|_|_|#|_|_|_",
			"_|_|_|#|_|_|_|#|_|_|_|#|_|_|_",
			"_|_|_|#|_|_|_|_|_|_|#|_|_|_|_",
			"_|_|_|_|_|_|_|_|_|#|_|_|_|_|_",
			"_|_|_|_|_|_|_|_|#|_|_|_|#|#|#",
			"#|#|#|_|_|_|#|_|_|_|_|_|_|_|_",
			"_|_|_|_|_|_|#|_|_|_|_|_|_|_|_",
			"_|_|_|_|_|_|#|_|_|_|_|#|_|_|_",
			"_|_|_|_|_|_|#|_|_|_|_|#|_|_|_",]

OLD_DICT = False
STARTUP = 1

class Space:
	def __init__(self, letter, row, column):
		self.letter = letter
		self.possible_letters = dict((l,[1000000,1000000]) for l in letters)
		self.row = row
		self.column = column

	def __eq__(self, other):
		return self.letter == other.letter and self.possible_letters.keys() == other.possible_letters.keys()

	def is_empty(self):
		return self.letter == '_'

	def is_black(self):
		return self.letter == '#'

	def __repr__(self):
		return f"space{self.row},{self.column}:{self.letter}"

	def __str__(self):
		return f"space{self.row},{self.column}:{self.letter}"

class Board:
	def __init__(self, text_board):
		self.board = []
		# Fill board object with inputted text board
		for i, r in enumerate(text_board):
			row = []
			for j, s in enumerate(r.split('|')):
				row.append(Space(s, i, j))
			self.board.append(row)

	def __eq__(self, other):
		for r, row in enumerate(self.board):
			for c, space in enumerate(row):
				if space != other.board[r][c]:
					return False

	def get_space(self, r, c):
		return self.board[r][c]

	def get_space(self, space):
		return self.board[space.row][space.column]

	def find_impossible(self):
		for r, row in enumerate(self.board):
			for c, space in enumerate(row):
				if len(space.possible_letters) == 0:
					return True, r, c
		return False, None, None

	def clear_counts(self):
		for row in self.board:
			for space in row:
				for l in space.possible_letters.keys():
					space.possible_letters[l] = 0

	# add possibilities for one set of spaces (one word)
	def add_possibilities(self, spaces, idx):
		length = len(spaces)
		words = []
		# find words that work in the given spaces
		for word in dictionary:
			if len(word) != length:
				continue

			bad = False
			for i, space in enumerate(spaces):
				if not space.is_empty():
					if word[i] != space.letter:
						# space is not empty and letter does not match word
						bad = True
						break
				else:
					if word[i] not in space.possible_letters.keys():
						# word is not possible based on perpendicular possible words
						bad = True
						break
			if bad:
				continue
			words.append(word)

		# update possible letters based on possible words
		for i, space in enumerate(spaces):
			if space.is_empty():
				possible_letters = dict()
				# sum possiblities for each letter
				for word in words:
					if word[i] in possible_letters:
						possible_letters[word[i]] += 1
					else:
						possible_letters[word[i]] = 1
				to_remove = []
				for l in space.possible_letters.keys():
					if l in possible_letters:
						# use the most constricting constraint (row or column)
						space.possible_letters[l][idx] = min(space.possible_letters[l][idx], possible_letters[l])
					else:
						to_remove.append(l)
				for l in to_remove:
					space.possible_letters.pop(l)

	# find the possibilities for each space on the board
	def possibilities(self, dictionary):
		prev_board = copy.deepcopy(self.board)

		for row in self.board:
			spaces = []
			for space in row:
				if space.is_black():
					if spaces:
						# black space found, add possibilities for word
						self.add_possibilities(spaces, 0)
					spaces = []
				else:
					spaces.append(space)
			if spaces:
				# edge of board found, add possibilites for word
				self.add_possibilities(spaces, 0)

		for i in range(len(self.board[0])):
			column = []
			# get column as list
			for row in self.board:
				column.append(row[i])

			spaces = []
			for space in column:
				if space.is_black():
					if spaces:
						# black space found, add possibilities for word
						self.add_possibilities(spaces, 1)
					spaces = []
				else:
					spaces.append(space)
			if spaces:
				# edge of board found, add possibilites for word
				self.add_possibilities(spaces, 1)

		# repeat until no more updates
		if self.board != prev_board:
			self.possibilities(dictionary)

		return True

	def str_possibilities(self):
		s = ""
		for r, row in enumerate(self.board):
			for c, space in enumerate(row):
				if space.is_empty():
					possibilities = dict(sorted(space.possible_letters.items(), key=lambda item: -min(item[1][0],item[1][1])))
					s += f"{r}, {c}: {possibilities}" + '\n'
				else:
					s += f"{r}, {c}: {space}" + '\n'
		return s

	# get the first empty space left->right top->bottom
	def get_first_empty(self):
		prev_is_vowel = None
		for row in self.board:
			for space in row:
				if space.is_empty():
					return space, prev_is_vowel
				elif space.is_black():
					prev_is_vowel = None
				elif space.letter in vowels:
					prev_is_vowel = True
				else:
					prev_is_vowel = False
		return None, None

	# get the most difficult space to fill based on a hueristic
	def get_worst_empty(self):
		worst_n = 1000000000
		worst_space = None
		for row in self.board:
			for space in row:
				if space.is_empty():
					if len(space.possible_letters) <= 1:
						return space
					n = max(map(lambda v: v[0]*v[1], space.possible_letters.values()))
					if n < worst_n:
						worst_n = n
						worst_space = space
		return worst_space

	def worst_spaces_ranked(self):
		ranked = []
		for row in self.board:
			for space in row:
				if space.is_empty():
					n = max(map(lambda v: v[0]*v[1], space.possible_letters.values()))
					ranked.append((n, space))
		return sorted(ranked, key=lambda item: item[0])

	def __str__(self):
		s = "  "
		for i in range(len(self.board[0])):
			s += f'{i}'
			if i < 10:
				s += ' '
		s += '\n0 '

		for r, row in enumerate(self.board):
			for space in row:
				s += space.letter + '|'
			if r != len(self.board[0])-1:
				s += f'\n{r+1}'
				if r+1 < 10:
					s += ' '
		return s

dictionary = []
# load the dictionary
with open(dictionary_file, 'r') as f:
	for row in f:
		if row[0] != "#":
			dictionary.append(row[:-1])

def fill_board(board):
	if not board.possibilities(dictionary):
		# current letters are impossible
		return False

	space = board.get_worst_empty()
	if space:
		# there is still an empty space
		if len(space.possible_letters) == 0:
			# space is impossible, go back
			return False
		print(board)
		# sort possibilities by a hueristic, start searching with best possibility
		possibilities = dict(sorted(space.possible_letters.items(), key=lambda item: -min(item[1][0],item[1][1])+letters.index(item[0])))
		for p in possibilities.keys():
			space.letter = p
			if fill_board(copy.deepcopy(board)):
				return True
		# all possibilities are impossible
		return False
	print(board)
	# no more empty spaces, success!
	return True

start = time.time()
b = Board(board6)
b.possibilities(dictionary)
with open(possibilities_file, 'w') as f:
	# save possibilities, used to manually fill in a space if it is taking too long
	f.write(b.str_possibilities())

print(fill_board(b))
print(f"It took {time.time()-start:.2f} seconds")
