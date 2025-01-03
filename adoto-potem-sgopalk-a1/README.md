# B551 Assignment 1: Searching

 
## Part 1: The 2021 Puzzle 

In this problem we have a 4*5 board with 4 rows and 5 columns, it has 20 tiles. The rows and columns can wrap around to the other side of the board and have restricted movement. 
From the given state we have to reach the goal state which is a board with each number arranged in a sorted order in the 4*5 board.
States: A board in any configuration with numbers from 1 to 20 on a 4*5 board.
Initial state: A state which has numbers from 1 to 20 on a 4 * 5 board.

Successor function: <br />
This function generates the legal states after the rows or columns in the board moves in one of the four directions (left, right, down, up). The 1st and the 3rd rows can move only in the left direction and the 2nd and 4th rows can move in the right direction. 
Similarly the 1st, 3rd and the 5th columns can move only in the Upward direction and  2nd and 4th rows can move in the downward direction.

Goal state: <br />
This is the state when the board has all the numbers from 1 to 20 arranged in a sorted manner in the 4 * 5 board.

Path Cost: <br />
Each move of a row or a column in the board costs 1, the path cost is the total number of steps/moves the agent takes in the path.

Strategy: <br />
The strategy used here is the A* search algorithm. We compute the cost till the current state from the initial state -g(s)- and the cost from the current state to the goal state as a heuristic h(s). The total cost g(s)+h(s) is the cost function.
The g(s) is incremented by 1 each time we make a move on the board. The directions in which the rows or columns are moved are also stored.
In this case we have chosen the number of misplaced tiles to be the heuristic function. Just so that the number of misplaced tiles does not overestimate the cost to the goal we have divided the count by the number of elements in the row or column depending on which is moved.
The heuristic function is admissible because after checking for many values on the real cost and the heuristic values from a state it never overestimates. In some cases, only the number of misplaced tiles for a heuristic were overestimating the real cost hence we divided that number by the row or column count and now that does not overestimate either.
We have used a priority queue in the form of a heap queue which helps us to sort the successors based on their heuristic and then pop the one with the least count of the number of misplaced tiles.

How the Search Algorithm works :- <br/>
The Fringe holds the cost function, the cost to the current state, the current state and the path to that state. With each move of the board we add a cost of 1 to the cost function and add the state to the visited array.
Starting off from the initial node we find the possible successors from that board configuration. We calculate the heuristic for each of the successors and store the values in a heap queue. 
Then we pop the elements based on the lower cost and repeat this until we reach the goal state.

Assumptions as given: <br />
It is a 4*5 board, with 4 Rows and 5 Columns.

Problems faced:- <br />
Trying to make the columns move up and down was kind of tricky and tried a few methods before landing on the one where I find the Transpose and work on it in the same way as the rows.
Realised the misplaced count of tiles does overestimate at times and for that reason divided the count by the number of elements in the row or the column and it solved the issue.

Other methods tried: <br />
Tried the Manhattan distance for a heuristic but it overestimated the cost for certain configurations. 
The main reason being, the rows and columns can wrap around and this causes the Manhattan distance to overestimate as it gives the shortest distance only if the moves are in right angles.


## Part 2
1. Problem Statement:<br />
Given the start and end city, find the shortest driving route/good driving direction between the start and end city based on the different cost criteria.
<br /><br />
cost criteria can be following: <br />
  - segments tries to find a route with the fewest number of road segments (i.e. edges of the graph). <br />
  - distance tries to find a route with the shortest total distance. <br />
  - time finds the fastest route, assuming one drives the speed limit. <br />
  - safe tries to find the safest route | the one that minimizes the probability of having an accident.<br /> <br />
  
We assume that the rate of accidents is 1 per million miles driven for the U.S. Interstate Highway
System, and 2 per million miles drives for all other roads. We can identify an Interstate Highway
because it will have an I in the name. Assume that the probability of having an accident
on any given route is thus one-millionth times the number of Interstate miles plus two-millionth
times the number of non-Interstate miles. <br />

We are provided with the dataset of major highway segment of US. <br />
Highway Dataset Description: <br />
  - start city
  - end city
  - highway name <br />
  - distance<br />
  - speed limit <br />

City gps dataset: Contains list of cities and their latitue, longitute coordinates <br />
  -city name <br />
  -latitude <br />
  -longitude <br />
<br />
2. Problem Abstraction: <br /> <br />
  i. state_space: All possible cities <br />
  ii. start_state: start_city <br />
  iii. goall_state: end_city <br />
  iv. cost_choice: cost to use to find the shortest path (segments, time, safe, distance) <br />
  v. heuristic function: calculates the cost from current city to end city <br />
  vi. successors: all the cities you can go from and to current_city <br />

3. Solution: <br />
The proposed solution to find the good driving direction between start and end city is by implementing A* star search on graph using a priority queue. We first get all the neighbouring cities that can be visited from and to the start city. These cities will be our successors. We iterate through the neighbouring cities to visit, calculate the total cost of visiting that city and store the city name, the total cost, distance in miles, accident count, time taken and path taken from start to that city in priority queue. Here, the total cost will the sum of cost of taking path from start city to current city (given by cost function) and cost of going from current city to goal city via direct path (given by heuristic function). We maintain a visited list to keep track of visited cities so that we won't be looping over same citites. Everytime we visit a city, we keep that city name in visited list. We iteratively pop the first element of the priority queue and check whether it is goal city. If not we check whether it is in visited list. If not, we get its successors and store in queue. We repeat it until we get to goal city. <br /><br />

Cost function<br/>
In this problem, we calculate the cost based on cost criteria or cost choice. If it is segments, we get the total paths to be taken from starting city to current city. <br/>
If choice is distance, we calculate the sum of total miles to be taken to go from start city to current city based on the distance we get from highway dataset.
If choice is time, we calculate the sum of time taken to go from start city to current city based on distance and speed limit. <br/>
  time = (speed limit) / distance
<br />
If choice is safe, we get the sum of accidents in each path. <br />
If highway is interstate then <br />
  accidents = length / 1000000 <br />
else <br />
  accidents = 2 * length / 1000000 <br/>
  
<br />

Heuristic function: <br />
Huristic function also depends on cost choice. <br />
For different choice it returns different value: <br />
  - segment: returns 1
  - distance: we calculate the distance between current city and goal city based on latitude and longitude data using a Harvesine Formula if lattitude and longitude data is available else assign distance as 0. <br />
  - time: we get all the neighbouring cities from current city and get least time of neighbouring city. <br />
  - safe: we get all the neighbouring cities from current city and get least accident route of neighbouring city <br />


## Part 3: Choosing Teams

Problem Statement: <br />
Given a set of people and their preferences for a team, try to satisfy as many people as possible with the least number of complaints. </br>

Cost criteria can be following: </br>
  - If the requested group size for a person is not met, a cost of 1 is added
  - If a requested member for a person is not assigned, a cost of 1 is added
  - If a person is specified as not work with but is assigned to them, a cost of 2 is added
<br />
Assumptions: <br />
We assume that the group size can be a maximum of 3. <br />

Problem Abstraction: <br />
  i. State_space: All possible combinations or groups of persons with a maximum limit of 3 in a group <br />
  ii. Start_state: all members in their own group <br />
  iv. Cost_choice: minimize the cost we get for the set of groups <br />
  vi. Successors: Being a local search we choose the option with the least cost assigned to the group.<br />
<br />
Approach :- <br />

For part 3, the goal of part 3 was to create a program to take in a file that contains the entries of class members that describes their preferences for working on a group project. 
To begin solving this part of the assignment, I began by conceptualizing this problem as a local search problem. 
Mainly, this is due to the fact that the problem doesn't require or necessitate the recording the path taken to reach the goal, but rather finding the state that meets or gets close to the goal state. 
In this problem, the state space is all possible combinations of all members of the class in groups of at most three. The heuristic function for this part of the assignment was built-in to the challenge, in that the heuristic function was the amount of "complaint" emails, or the "total cost" reported in the program.
<br />
My main inspiration for the approach in solving this problem was the lecture on local search and steepest descent in particular. I found this approach to be very useful for this rather interesting and challening part of the assignment. 
<br />
The first element of the program that I tackled was creating a function to parse the file. The key goal of interest was to find a way to store the member's preferences in a way that would be easily referenced in the cost function. 
Next was the function to create the initial state. This was interesting because I actually wrote two functions for this. The first was to take the list of class members and then shuffle them, and then to break them up into groups of three. <br />
This worked, but after discussing this strategy with my team, we decided to go with, in my view, a better solution which was to start all members in their own group.
<br />
Once we made that decision, that informed the development of the successor function. This function returned all possible combinations of all the groups; essentially what happens is that it incrementally "builds" the groups as the solver function iterates. 
<br />
So all in all, our search solution starts with all members in their own group, then checks all successors with the cost function (which is the heuristic) and then replaces the current state with the successor state with the best value for the cost. 
We repeat this process and return results as it improves. Overall, it was an interesting challenge but a fun one as well!


