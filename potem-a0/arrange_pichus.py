#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : [PUT YOUR NAME AND USERNAME HERE]
#
# Based on skeleton code in CSCI B551, Spring 2021
#

import sys
import math

# Parse the map from a given filename
def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().rstrip("\n").split("\n")]

# Count total # of pichus on board
def count_pichus(board):
    return sum([ row.count('p') for row in board ] )

# Return a string with the board rendered in a human-pichuly format
def printable_board(board):
    return "\n".join([ "".join(row) for row in board])

# Add a pichu to the board at the given position, and return a new board (doesn't change original)
def add_pichu(board, row, col):
    return board[0:row] + [board[row][0:col] + ['p',] + board[row][col+1:]] + board[row+1:]
        
    
def test_valid_state(board, row, col, k):
    total_col = len(board[0])
    
    for c in range(col - 1, -1, -1):
        if board[row][c] == 'X':
            break
        if board[row][c] == '@':
            break
        if board[row][c] == 'p':
            return False
        
    for c in range(col + 1, total_col):
        if board[row][c] == 'X':
            break
        if board[row][c] == '@':
            break
        if board[row][c] == 'p':
            return False
        
    for r in range(row - 1, -1, -1):
        if board[r][col] == 'X':
            break
        if board[r][col] == '@':
            break
        if board[r][col] == 'p':
            return False
        
    for r in range(row + 1, len(board)):
        if board[r][col] == 'X':
            break
        if board[r][col] == '@':
            break
        if board[r][col] == 'p':
            return False
        
    if k != 0:
        return True
    
    for r in range(row + 1, len(board)):
        if board[r][r] == 'X':
            break
        if board[r][r] == '@':
            break
        if board[r][r] == 'p':
            return False

    for r in range(row - 1, -1, -1):
        if board[r][r] == 'X':
            break
        if board[r][r] == '@':
            break
        if board[r][r] == 'p':
            return False
        
    return True
    
# Get list of successors of given board state
def successors(board, k):
    pichus = []
    
    for r in range(0, len(board)):
        for c in range(0, len(board[0])):
            if board[r][c] == '.' and test_valid_state(board, r, c, k):
                    pichus.append(add_pichu(board, r, c))

    return pichus

# check if board is a goal state
def is_goal(board, k):
    return count_pichus(board) == k 

# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_map, success), where:
# - new_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_board, k):
    fringe = [initial_board]
    
    while len(fringe) > 0:
        state = fringe.pop(0)
        
        for s in successors(state, k):
            if is_goal(s, k):
                return(s,True)
            
            fringe.insert(0, s)
            
    if k == 0:
        return (state, True)
    
    return ([],False)

# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    
    # This is K, the number of agents
    k = int(sys.argv[2])
    
    print ("Starting from initial board:\n" + printable_board(house_map) + "\n\nLooking for solution...\n")
    (newboard, success) = solve(house_map, k)
    print ("Here's what we found:")
    print (printable_board(newboard) if success else "None")