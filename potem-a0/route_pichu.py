#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : [Manita Pote, potem]
#
# Based on skeleton code provided in CSCI B551, Spring 2021.


import sys
import json

# Parse the map from a given filename
def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().rstrip("\n").split("\n")]

# Return a string with the board rendered in a human/pichu-readable format
def printable_board(board):
    return "\n".join([ "".join(row) for row in board])
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
    return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
    moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

    # Return only moves that are within the board and legal (i.e. go through open space ".")
    return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]


# Perform search on the map
#
# Takes a single parameter as input -- the house map --
# Returns a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)
def search(house_map):
    # Find pichu start position
    for row_i in range(len(house_map)):
        for col_i in range(len(house_map[0])):
            if house_map[row_i][col_i] == 'p':
                pichu_loc = (row_i, col_i)
                
    #Fringe to store path from start position to sucessive states 
    fringe=[([pichu_loc],0)] 
    
    #Stores visited nodes
    visited = []
    
    while fringe:
        [curr_move, curr_dist]=fringe.pop(0)
        
        #Keeps track of visited nodes
        visited.append(curr_move[-1]) 
        
        for move in moves(house_map, curr_move[-1][0], curr_move[-1][1]):
            if move in visited:
                continue
            
            new_path = curr_move.copy()

            new_path.append(move)

            if house_map[move[0]][move[1]] == "@":
                return (curr_dist + 1, get_direction(new_path))
            
            #Fringe stores the whole path from start node to current node
            fringe.append((new_path, curr_dist + 1))
                
    if not fringe:
        return(-1, '')

#Gets the direction strings for the path
def get_direction(paths):
    direction = ''
    
    for i in range(1, len(paths)):
        if paths[i - 1][0] > paths[i][0]:
            direction += 'U'
        elif paths[i - 1][0] < paths[i][0]:
            direction += 'D'
        if paths[i - 1][1] > paths[i][1]: 
            direction += 'L'
        elif paths[i - 1][1] < paths[i][1]:
            direction += 'R'
            
    return direction

# Main Function
if __name__ == "__main__":
    house_map = parse_map(sys.argv[1])
    
    print("Routing in this board:\n" + printable_board(house_map) + "\n")
    print("Shhhh... quiet while I navigate!")
    
    (distance, paths) = search(house_map)
    
    print("Here's the solution I found:")
    print(str(distance) + " " + paths)

