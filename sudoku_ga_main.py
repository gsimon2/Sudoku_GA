#!/usr/bin/env python 
#
# Sudoku GA Main
#
# This is an implementation of a GA that initializes a sudoku board and then runs a GA to attempt to find a solution to that board
#
# GAS 10-11-17

import argparse # Needed to parse arguments from command line easily

from sudoku_gui import SudokuUI # Used to display a graphic for the Sudoku Game

import threading # Used to call a thread to display the graphic while we can still do some processing in the main loop

import math # Used for doing mathematical functions



if __name__ == '__main__':
	# Set up arg parser
	parser = argparse.ArgumentParser(description='This is an implementation of a GA that initializes a sudoku board and then runs a GA to attempt to find a solution to that board')
	parser.add_argument('-s', '--size', type=int, help='The dimension size of board to use. Will create a N-by-N size board with N sub-rectangles')
	args= parser.parse_args()
	
	# Take the dimension size from the command line
	#	If none is provided default to a 9 by 9 game
	if args.size is not None:
		dimension_size = args.size
	else:
		dimension_size = 9
		
	# Initialize blank game board
	#	Note 0 is a place holder for blank
	game = [[i+1 for i in range(dimension_size)] for j in range(dimension_size)]
	
	# Display Board - This blocks processing!
	SudokuUI = SudokuUI(game = game, dimension_size=int(math.sqrt(dimension_size)))
	
	print('Exiting!')
	
		
	
	
	
