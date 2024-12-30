#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: Sumanth Gopalkrishna 2000753899
#
# Based on skeleton code by D. Crandall, January 2021
#

import sys
import heapq
import copy

ROWS=4
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

#Converts the given board from a 1 D array to a 2 D array
def one_d_to_2_d(one_d_board):
    j=0 
    s=[]
    for row in range(ROWS):
        inner_list=[]
        for col in range(COLS):
            inner_list.append(one_d_board[j])
            j+=1
        s.append(inner_list)
    return(s)

#moves the numbers in the rows to the left by one 
def leftshift(state,n):
    left_state=copy.deepcopy(state)
    left_state[n]=left_state[n][1:]+left_state[n][:1]
    return left_state

#moves the numbers in the rows to the right by one 
def rightshift(state,n):
    right_state=copy.deepcopy(state)
    right_state[n]=right_state[n][-1:]+right_state[n][:-1]
    return right_state

#returns the Transpose of the board
def transpose_board(board):
  return [list(col) for col in zip(*board)]


# return a list of possible successor states
def successors(state):
    
    moves=[]  #holds the possible successor states
    
    #row movement
    for i in range(0,ROWS):
        if i%2==0:
            row=(leftshift(state,i),"L"+str(i+1)) #the 1st and 3rd rows move LEFT 
        else:
            row=(rightshift(state,i),"R"+str(i+1)) #the 2nd and 4th rows move RIGHT 
        moves.append(row)
        
    #column movement
    for n in range(0,COLS):        
        if n%2==0:
            #getting the transpose of the board and then shifting the rows left and performing a transpose again on this board does the same thing as a column moving up
            up=leftshift(transpose_board(state),n) #the 1st, 3rd and 5th columns move UP
            change_state=transpose_board(up)
            direction="U"+str(n+1)
        else:
            #getting the transpose of the board and then shifting the rows right and performing a transpose again on this board does the same thing as a column moving down
            down=rightshift(transpose_board(state),n) #the 2nd and 4th columns move DOWN
            change_state=transpose_board(down)            
            direction="D"+str(n+1)
        moves.append((change_state,direction)) #appends a tuple which contains the state of the board and the directions the board has moved
    return moves

def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")]

#The heuristic function- Returns the count of the number of misplaced tiles and divids the count by 5 or 4 depending on whether it is a row or a column. 
def heuristic(count_state):
    direction=count_state[1]
    board=count_state[0]
    num_count=0
    count=0
    for i in range(ROWS):
        for j in range(COLS):
            num_count+=1
            if board[i][j]!=num_count:
                count+=1     #holds the number of misplaced tiles
                
    #if row,  divide by 5 because 5 elements are there
    if "R" in direction or "L" in direction:
        count=count/COLS
    #if column, divide by 4 because 4 elements are there        
    elif "U" in direction or "D" in direction:
        count=count/ROWS                    

    return(count)

    
# To check if we have reached the goal state 
def is_goal(state):
    goal=[[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20]]
    if state==goal:
        return True
    return False

def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    board_2_d=one_d_to_2_d(initial_board)
    fringe=[]
    fringe+=[(0,0,board_2_d,[]),]
    visited_nodes=[]    # holds all the nodes visited so it does not get revisited
    
    while len(fringe)>0:
        heapq.heapify(fringe)  #creating a Heapq so we can pop the elements based on the priority of the Heuristic function which is the number of misplaced tiles 
        (h,cost,curr_state,path)=heapq.heappop(fringe)
        
        if is_goal(curr_state):
            return (path)
      
        for s in successors(curr_state):
             if s[0] not in visited_nodes:    
                 fringe.append([heuristic(s)+cost,cost+1,s[0],path+[s[1]]]) #the fringe holds the h(s)+cost till that state (g(s)) as the cost function, s[0] is the board state , s[1] is the direction in which the board has moved, path is a list which holds all the directions from the initial state to this current state
                 visited_nodes.append(s[0])
    
    return []


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
