#Problem 1: Navigation

Find the shortest path between agent and you. <br />

 Abstraction of problem: <br />
 1) Set of states:<br />
 Here, states are the vaild co-ordinates for movement by agent.<br />
 
 2) Initial State:<br />
 Initial state is the location (co-ordinate) of the agent 'p' in the input map.<br />
 If the current value of given co-ordinate in the house map equals to 'p', the co-ordinate is the current state.<br />
 
 3) Successor function:<br />
 Successor function gives the co-ordinates that are valid for move. For example: if the value of co-ordinate currently is 'X', that co-ordinate is not a valid move that agent can take. In the program, <br />
 ```
 moves() {
     checks whether it can move left, right, up and down by checking the value of current coordiate
    
    returns valid moves
 }
 ```
 
 gives the successor states.<br />
 
 4) Goal state:<br />
 The goal state is the location of '@'. <br />
 
 5) Cost function:<br />
 Here, every move costs same. <br />
 
 Search abstraction: (It uses BFS)<br />
 ```
initial state <- co-ordinate with value 'p' 
path <- initial state 
distance <- 0 
visited <- empty list 
fringe <- a FIFO queue with path, depth 
loop do 
    path, distance <- pop(fringe) //First element of queue 
    visited <- insert initial state
    for valid_move in moves:
       if valid_move equals '@': 
          string_path <- get string representation of path
           return distance, string_path 
            
       if valid_move is in visited: 
          continue
          
       visisted <- append(valid_move)
       new_path <- copy of path
       append valid_move to new_path 
       fringe <- append (new_path, distance + 1)
```        

Part 2: Hide-and-seek <br />

Abstraction of problem: <br />
 1) Set of states: <br />
 Here, states are the vaild co-ordinates where 'p' can be placed. <br />
 
 2) Initial State: <br />
 Initial state is the map of the house. <br />
 
 3) Successor function: <br />
 Successor function gives the new house map with 'p' added to the valid co-ordinates where 'p' can not see other 'p' in row and column. <br />
 
 4) Goal state: <br />
 The goal state is the map of house with number of 'p' equal to k, if k = 0, it gives the map with maximum 'p' placed in map. <br />
 
 5) Cost function: <br />
 Here, every move costs same. <br />
 
 Search abstraction: <br />
 I tried BFS and DFS both. There was no difference in the time to get solution. But when k is greater than maximum number of 'p' that can be placed in map, it takes alot of time to get 'None' both for BFS and DFS. <br />
However, I submitted the DFS one. <br />
```
fringe <- [] (LIFO) 
fringe <- insert intial board map 
loop do: 
    state <- pop first element of fringe 
    
    for new_map in successor(state): 
      if number of 'p' in new_map == k: 
        return new_map 
        
       fringe <- insert new_map in first position (first index)

if k == 0:
  return state 
return empty, no solution
```

Successor function abstraction: <br />
```
new_map_states <- empty list 
for every row in rows: 
    for every column in columns:
      if current_co-ordinate value == '.' and validation(row, column) == true:
         new_map_states <- append(map with one 'p' added to  current_coordinate) 
 
return new_map_states

```
```
validation(current_row, current_column):

 step1: for each row below current_row keeping  current_column constant:
          if (row, current_column) value in ['X', '@', '.']: 
               return True 
          return Fasle

 step 2: repeat step 1 process for row above the current_row values
 step 3: repeat step 1 process for columns below current_columns keeping row constant 
 step 4: repeat step 1 for columns above current_columns keeping row constant 
 step 5: if k == 0:
          for same value of row and column below and above current_row repeat step 2 
```
  
