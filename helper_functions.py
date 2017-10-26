#!/usr/bin/env python 
#
# Helper Functions
#
# General functions that help the operations of the sudoku GA
#
# GAS 10-12-17

import math # Used for is_square function

# Is Square
#	Determines is the provided integer is a perfect square
#	Returns True if it is - False otherwise	
def is_square(integer):
    root = math.sqrt(integer)
    if int(root + 0.5) ** 2 == integer: 
        return True
    else:
        return False


def print_ind(ind):
	print('IND ID: {} \t Fitness: {}'.format(ind.ID, ind.total_fitness))
	for row in ind.puzzle:
		print(row)
	print('\n')
