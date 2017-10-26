#!/usr/bin/env python 
#
# Sudoku GA Main
#
# This is an implementation of a GA that initializes a sudoku board and then runs a GA to attempt to find a solution to that board
#
# GAS 10-11-17

import argparse # Needed to parse arguments from command line easily
from sudoku_gui import SudokuUI # Used to display a graphic for the Sudoku Game
import math # Used for doing mathematical functions
import random # Used for providing random number generation
import datetime # Used to get system time and date
from class_sudoku_individual import PuzzleIndividual # Individuals that will be evolved to solve the puzzle
from helper_functions import is_square # Function that determines if the input is a perfect square or not
from helper_functions import print_ind # Function that neatly prints the individual ID, Fitness, and puzzle
import copy # Allows deep copying of individuals
import atexit # Allows to run a function before exit. Used to pull up GUI for last elite individual


POP_SIZE = 400
GEN_COUNT = 2000
MUTATION_PROB = 0.15
TOURNAMENT_SIZE = 2
CURRENT_GEN = 0

class GA:
	def __init__(self, initial_pop):
		self.id_counter = POP_SIZE
		self.population = initial_pop
		self.parent_pool = []
		self.children_pool = []
		self.canidate_pool = []
		self.elite_ind = self.population[0]
	
	
	# Preps the next generation
	#	Tournament selection to decide the parent pool
	#	Cross over from the parents to create the children pool
	#	Children pool and last generation population are added together to create the canidate pool
	#	Mutation occurs in the canidate pool
	#	Canidate pool individuals fitnesses are accessed
	#	Tournament selection for next generation
	def next_generation(self):
		global CURRENT_GEN
		# Perform tournament selection for parent pool
		self.parent_pool = []
		for i in range(len(self.population)):
			tourn = random.sample(self.population,TOURNAMENT_SIZE)
			fitness_list = []
			
			for ind in tourn:
				fitness_list.append(ind.total_fitness)
			
			winner_index = fitness_list.index(max(fitness_list))			
			self.parent_pool.append(copy.deepcopy(tourn[winner_index]))
		
		# Perform cross over on the parent pool to create the children pool
		self.cross_over()
		
		# Add the population and children pool together to make the canidate pool
		self.canidate_pool = self.population + self.children_pool
		
		# Perfrom cross over on the canidate pool
		self.mutation()
		
		# Perform tournament selection for next generation with elitism
		self.population = []
		self.population.append(copy.deepcopy(self.elite_ind))
		self.update_canidate_pool_fitness()
		for i in range(POP_SIZE-1):
			tourn = random.sample(self.canidate_pool,TOURNAMENT_SIZE)
			fitness_list = []
			
			for ind in tourn:
				fitness_list.append(ind.total_fitness)
			
			winner_index = fitness_list.index(max(fitness_list))			
			self.population.append(copy.deepcopy(tourn[winner_index]))
			
		# Increment the generation counter
		CURRENT_GEN += 1
		
		# Update fitness
		self.update_population_fitness()
		

	# Cross over
	#	Breeds parents to create a children_pool
	# 	Changes random blocks between the parents to create the children
	def cross_over(self):
		self.children_pool = []
		
		for i in range(int(len(self.parent_pool)/2)):
			# Grab 2 parents from the parent pool
			parents = random.sample(self.parent_pool,2)
		
			# Initially the children are identical to their single parent
			child1 = copy.deepcopy(parents[0])
			child2 = copy.deepcopy(parents[1])
			
			# Update the Children's IDs
			child1.ID = self.id_counter
			self.id_counter += 1
			child2.ID = self.id_counter
			self.id_counter += 1
			
			# Pick a split point for where we should break up the parents blocks
			split_point = random.randint(1,dimension_size-1)
			
			#print('Split_point: {}'.format(split_point))
			
			# Cross over
			parent1_flat_blocks = self.convert_2D_to_1D(copy.deepcopy(parents[0].blocks))
			parent2_flat_blocks = self.convert_2D_to_1D(copy.deepcopy(parents[1].blocks))
			
			child1_flat_blocks = parent1_flat_blocks[0:split_point] + parent2_flat_blocks[-1 * (dimension_size - split_point):]
			child2_flat_blocks = parent2_flat_blocks[0:split_point] + parent1_flat_blocks[-1 * (dimension_size - split_point):]
			
			child1.blocks = copy.deepcopy(self.convert_1D_to_2D(child1_flat_blocks))
			child2.blocks = copy.deepcopy(self.convert_1D_to_2D(child2_flat_blocks))
			
			# Update the childrens puzzle, fitness map, and total_fitness
			child1.update_fitness_map()
			child2.update_fitness_map()
			
			# Add the children to the pool
			self.children_pool.append(child1)
			self.children_pool.append(child2)
			
			# Printing for debugging Cross over
			"""
			print('----------------')
			print(len(parents[0].blocks))
			print(len(child1.blocks))
			print_ind(parents[0])
			print_ind(parents[1])
			print_ind(child1)
			print_ind(child2)
			print('----------------')
			"""
			
		
	# Shuffles the numbers in a random block of mutated individuals
	def mutation(self):
		
		# Everyone in the canidate pool has as chance to be mutated
		for ind in self.canidate_pool:
			if random.random() <= MUTATION_PROB:
				
				# Find mutation block location
				mutation_spot = random.randint(0,dimension_size-1)
				
				"""
				print('\n--------------')
				print('Mutation spot: {}'.format(mutation_spot))
				print('Original:')
				print_ind(ind)
				"""
				
				# Shuffle the values in that block
				flat_blocks = self.convert_2D_to_1D(ind.blocks)
				values = [h for h in range(1,dimension_size+1)]
				random.shuffle(values)
				flat_blocks[mutation_spot] = copy.deepcopy(([[values.pop() for i in range(block_dimension)] for j in range(block_dimension)]))
				ind.blocks = self.convert_1D_to_2D(flat_blocks)
				ind.update_fitness_map()
				
				"""
				print('\nMutated')
				print_ind(ind)
				"""
				
	# Takes the 2 dimensional list of blocks and converts it to a flat list
	def convert_2D_to_1D(self, blocks_2D):
		blocks_1D = []
		for sublist in blocks_2D:
			for item in sublist:
				blocks_1D.append(copy.deepcopy(item))
		return blocks_1D
	
	# Takes a flat list of blocks and converts them to a 2D list
	def convert_1D_to_2D(self, blocks_1D):
		blocks_2D = ([[0 for i in range(block_dimension)] for j in range(block_dimension)])
		i = 0
		for row in range(block_dimension):
			for column in range(block_dimension):
				blocks_2D[row][column] = copy.deepcopy(blocks_1D[i])
				i += 1
		return blocks_2D
	
	# Updates the puzzle, fitness map, and total fitness of each individual of the population
	def update_population_fitness(self):
		max_fit = 0
		for ind in self.population:
			ind.update_fitness_map()
			
			if ind.total_fitness > max_fit:
				max_fit = ind.total_fitness
				self.elite_ind = copy.deepcopy(ind)
			
	# Updates the puzzle, fitness map, and total fitness of each individual in the canidate pool
	def update_canidate_pool_fitness(self):
		for ind in self.canidate_pool:
			ind.update_fitness_map()
	
	# Write the current population to the log file
	def ga_log(self):
		with open('logs/{}'.format(LOG_FILE_NAME), 'a') as file:
			for ind in self.population:
				file.write('{},{},{}\n'.format(CURRENT_GEN, ind.ID, ind.total_fitness))

@atexit.register
def exit_code():
	ui = SudokuUI(game = ga.elite_ind, dimension_size = block_dimension)
	
if __name__ == '__main__':
	global dimension_size
	global block_dimension
	global MAX_FITNESS
	global MUTATION_PROB
	
	# Set up arg parser
	parser = argparse.ArgumentParser(description='This is an implementation of a GA that initializes a sudoku board and then runs a GA to attempt to find a solution to that board')
	parser.add_argument('-s', '--size', type=int, help='The dimension size of board to use. Will create a N-by-N size board with N sub-rectangles')
	parser.add_argument('-l', '--log', type=str, help='The log file name')
	args= parser.parse_args()
	
	# Take the dimension size from the command line
	#	If none is provided default to a 9 by 9 game
	if args.size is not None:
		if is_square(args.size) is False:
			print('Please input a perfect square')
			exit()
		else:
			dimension_size = args.size
			block_dimension = int(math.sqrt(dimension_size))
	else:
		dimension_size = 9
		block_dimension = 3
	
	MAX_FITNESS = (dimension_size * dimension_size) * 3
	
	if args.log is not None:
		LOG_FILE_NAME = args.log
	else:
		LOG_FILE_NAME = "log.dat"
	
	# Provide the number generator with a seed based off of the current time
	seed = datetime.datetime.now()
	random.seed(seed)

	# Write the header of the log
	with open('logs/{}'.format(LOG_FILE_NAME), 'w') as file:
		file.write('Generation,ID,Fitness\n')
    
	# Create a list of individuals
	intitial_pop = []
	for i in range(POP_SIZE):
		new_ind = PuzzleIndividual(dimension_size, block_dimension)
		new_ind.ID = i
		intitial_pop.append(new_ind)
	
	# Start the GA
	ga = GA(intitial_pop)
	ga.update_population_fitness()
	ga.ga_log()
	
	
	stagnate_counter = 10
	last_gen_elite_fitness = ga.elite_ind.total_fitness
	
	# Enter generation loop
	while CURRENT_GEN < GEN_COUNT:
		ga.next_generation()
		ga.ga_log()
		#print('Population size: {} \t Parent size: {} \t Children pool: {} \t Canidate pool: {}'.format(len(ga.population), len(ga.parent_pool), len(ga.children_pool), len(ga.canidate_pool)))
		print('Generation: {} \n\t Elite Ind: {}, fitness: {}\n'.format(CURRENT_GEN,ga.elite_ind.ID, ga.elite_ind.total_fitness))
		
		# Check for a solution to the puzzle
		if ga.elite_ind.total_fitness == MAX_FITNESS:
			break
			
		# Check if progress is stagnate
		if last_gen_elite_fitness == ga.elite_ind.total_fitness:
			stagnate_counter -= 1
		else:
			# Improvement in top fitness, longer stagnate counter and less mutation to allow best to spread in pop
			last_gen_elite_fitness = ga.elite_ind.total_fitness
			stagnate_counter = 20
			MUTATION_PROB /= 2
		
		# if progress has been stagnate too long, increase the mutation prob
		if stagnate_counter <= 0:
			if MUTATION_PROB <= 0.85:
				MUTATION_PROB += 0.05
			stagnate_counter = 10
			print('Increase in mutation rate! New rate: {}\n\n'.format(MUTATION_PROB))
	
		
	
	#ui = SudokuUI(game = ind, dimension_size = block_dimension)
	
	
	print('Exiting!')
	
		
	
	
	
