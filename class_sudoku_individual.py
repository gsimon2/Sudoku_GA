#!/usr/bin/env python 
#
# Sudoku Puzzle Individual Class
#
# A class that can update its puzzle 2D map and fitness 2D map easily after block munipulations performed by the GA
# Fitness functons draw heavily from the example at: http://newcoder.io/gui/part-2/
#
# GAS 10-12-17

import numpy as np # Used to combine matrix blocks to make the game board
import random # Used for providing random number generation
import datetime # Used to get system time and date

class PuzzleIndividual:
	def __init__(self, dimension_size, block_dimension):
		
		# Provide the number generator with a seed based off of the current time
		seed = datetime.datetime.now()
		random.seed(seed)
	
		# Create a matrix of blocks 
		#   Blocks are the smaller sections of the sudoku board
		#	Each block will start with a correct set of numbers 1-dimension size	
		blocks = ([[0 for i in range(block_dimension)] for j in range(block_dimension)])
		for row in range(block_dimension):
			for column in range(block_dimension):
				values = [h for h in range(1,dimension_size+1)]
				random.shuffle(values)
				blocks[row][column] = ([[values.pop() for i in range(block_dimension)] for j in range(block_dimension)])
				
		self.generation = 0 # Generation that this individual is a part of
		self.ID = 0 # ID of the individual
		self.blocks = blocks
		self.puzzle = '' # Current sudoku board values
		self.dimension_size = dimension_size
		self.block_dimension = block_dimension
		self.fitness_map = [[0 for i in range(dimension_size)] for j in range(dimension_size)] # map of how good each element is
		self.total_fitness = 0 # Current Fitness of this individual
		
		
		# Updates
		self.update_puzzle() # Updates the board values based on the block values
		self.update_fitness_map() # Update the fitness map for the initial puzzle values
		#self.testing_update_puzzle()
		self.update_total_fitness()
		
	
	# Debugging initialization function
	def testing_update_puzzle(self):
		puzzle = ([[0 for i in range(self.dimension_size)] for j in range(self.dimension_size)])
		
		# Populate 9 - 1 going top to bot
		for column in range(self.dimension_size):
			values = [h for h in range(1,self.dimension_size+1)]
			for row in range(self.dimension_size):
				#random.shuffle(values)
				puzzle[row][column] = values.pop()	
		
		# Populate 9 -1 going left to right
		for row in range(self.dimension_size):
			values = [h for h in range(1,self.dimension_size+1)]
			for column in range(self.dimension_size):
				#random.shuffle(values)
				puzzle[row][column] = values.pop()
				
		self.puzzle = puzzle
		
		
	# Create a game board based off of the blocks
	#	np.bmat() puts together the block matris into one big one
	#	tolist() converst the matrix type to a list of list - what is the type expected by the GUI		
	def update_puzzle(self):
		self.puzzle = np.bmat(self.blocks).tolist()
	
	
	# Calculates the total fitness of the individual based off of the sum of the fitness map
	def update_total_fitness(self):
		current_sum = 0
		for g in range(self.dimension_size):
			for f in range(self.dimension_size):
				current_sum += self.fitness_map[g][f]
		self.total_fitness = current_sum
	
	
	# Updates the fitness map by giving one point to each elements (single space) for every rule (row,column,block) that it obeys
	def update_fitness_map(self):
		
		self.update_puzzle()
		
		# Clear current fitness map
		self.fitness_map = [[0 for i in range(self.dimension_size)] for j in range(self.dimension_size)]
		
		# Give points for elements that have their row in order
		for row in xrange(self.dimension_size):
			if self.check_row(row):
				for i in xrange(self.dimension_size):
					self.fitness_map[row][i] += 1
		
		# Give points for elements that have their column in order		
		for column in xrange(self.dimension_size):
			if self.check_column(column):
				for i in xrange(self.dimension_size):
					self.fitness_map[i][column] += 1
		
		# Give points for elements that have their block in order
		for row in xrange(self.block_dimension):
			for column in xrange(self.block_dimension):
				if self.check_square(row,column):
					for r in xrange(row * self.block_dimension, (row + 1) * self.block_dimension):
						for c in xrange(column * self.block_dimension, (column + 1) * self.block_dimension):
							self.fitness_map[r][c] += 1
		
		# Recalc the total now that the fitness map is updated				
		self.update_total_fitness()
			
	# Takes a self.dimension_size list and makes sure its a proper list of [1,dimension_size]
	def check_block(self,block):
		return set(block) == set(range(1, self.dimension_size + 1))
	
	# Checks if the row is a complete set
	def check_row(self, row):
		return self.check_block(self.puzzle[row])
		
	# Checks if the column is a complete set
	def check_column(self, column):
		return self.check_block([self.puzzle[row][column] for row in xrange(self.dimension_size)])
	
	# Checks if the block (square) is a complete set
	def check_square(self, row, column):
		return self.check_block(
		[
				self.puzzle[r][c]
				for r in xrange(row * self.block_dimension, (row + 1) * self.block_dimension)
				for c in xrange(column * self.block_dimension, (column + 1) * self.block_dimension)
		]
	)
	
