#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: Andrew Doto,  IU ID: adoto
#
# Based on skeleton code by R. Shah and D. Crandall, January 2021
#

import random
import sys
import time

def parse_file(filename):
    '''This function takes in a file and returns 
    three objects.
    members:      a list of members of the class
    req_teams:    a dictionary with the members of the class as keys
                  and the values are lists of the teammates they requested
    req_excludes: a dictionary with the members of the class as keys
                  and the values are lists of the teammates they requested 
                  not to work with
    '''
    # initialize the three objects
    members = []
    req_teams = {}
    req_excludes = {}
    
    # open the file
    with open(filename, "r") as f:
        for line in f.readlines():
            # isolate entry in the line
            entry = line.rstrip("\n").split(" ")
            # add member to list
            members.append(entry[0])
            # add member's requested teammates to dict
            req_teams[entry[0]] = sorted(entry[1].split('-'))
            # add member's requested exclustions to dict
            req_excludes[entry[0]] = sorted(entry[2].split(','))
        
    return members, req_teams, req_excludes

def random_start(members):
    '''This function takes in the list of members and then
    initializes random groups by breaking up into threes 
    as a starting point.'''
    
    # init list
    result = []
    
    # while list has members
    while len(members) > 0:
        # shuffle the order
        random.shuffle(members)
        # make sure list has at least 3
        if len(members) >= 3:
            # append group of three to result
            result.append(sorted(members[0:3]))
            # remove that group of three
            del members[0:3]
        else:
            # take leftover and place into group
            result.append(sorted(members[0:]))
            del members[0:]
    
    return result

def random_start2(members):
    '''This function takes in the list of members and then
    initializes random groups by putting each member into their own group 
    as a starting point.'''
    result = []
    random.shuffle(members)
    return [[member] for member in members]

def successors(s):
    '''Successor function takes in the state and returns all possible combinations
    in terms of combining groups with each other'''
    s_prime_list = []
    for group in s:
        other_groups = [x for x in s if x != group]
        for other_group in other_groups:
            remaining_groups = [y for y in other_groups if y != other_group]
            set_to_add = [group + other_group] + remaining_groups
            lengths = [len(x) for x in set_to_add]
            if max(lengths) <= 3:
                s_prime_list.append(set_to_add)
    return s_prime_list

def cost(s, reqs, excls):
    '''cost function that utilizes the requirement dictionaries
    '''
    # init diff cost categories
    group_size_cost = 0
    member_cost = 0
    exclusion_cost = 0
    
    # take the state, for every group
    for group in s:
        # for member in the group
        for member in group:
            # look at the length of the group and check if match to requested length
            if len(group) != len(reqs[member]):
                group_size_cost +=1
            
            # check if the requested teammates
            for req_teammate in reqs[member]:
                if req_teammate == 'zzz':
                    break
                if req_teammate not in group:
                    member_cost +=1

            # check if the requested exclusions were in group
            for req_exclusion in excls[member]:
                if req_exclusion in group:
                    exclusion_cost +=2

    return group_size_cost + member_cost + exclusion_cost

def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (number of complaints) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """
    # init start state and calc cost, yield quick result
    members, reqs, excls = parse_file(input_file)
    s = random_start2(members)
    best_cost = cost(s, reqs, excls)
    yield({"assigned-groups": ['-'.join(x) for x in s],
               "total-cost" : best_cost})
    
    # for n times, restart start state and yield if it's better
    for n in range(1000):
        s = random_start2(members)
        if cost(s, reqs, excls) < best_cost:
            best_cost = cost(s, reqs, excls)
            yield({"assigned-groups": ['-'.join(x) for x in s],
                   "total-cost" : best_cost})
        # inner loop, take s and get successors and their respective costs
        for k in range(1000):
            s_prime_list = successors(s)
            s_p_costs = [cost(sp, reqs, excls) for sp in s_prime_list]
            #This part helps to check with random starting states and if they get combinations which have a lower cost than the previous best cost 
            #then updates the group to this one if it has a lower cost
            if n!=0:
                if len(s_p_costs)>0:
                    min_index_1=s_p_costs.index(min(s_p_costs))
                    s=s_prime_list[min_index_1]
            # take the best cost of the s primes and compare to the recent best
            # if it's better, then replace the s and then yield that result
            if len(s_p_costs)>0:
                if min(s_p_costs) < best_cost:
                    best_cost = min(s_p_costs)
                    min_index = s_p_costs.index(min(s_p_costs))
                    s = s_prime_list[min_index]
                    yield({"assigned-groups": ['-'.join(x) for x in s],
                           "total-cost" : best_cost})
        
    # Simple example. First we yield a quick solution
    #yield({"assigned-groups": ["vibvats-djcran-zkachwal", "shah12", "vrmath"],
     #          "total-cost" : 12})

    # Then we think a while and return another solution:
    #time.sleep(10)
    #yield({"assigned-groups": ["vibvats-djcran-zkachwal", "shah12-vrmath"],
              # "total-cost" : 10})

    # This solution will never befound, but that's ok; program will be killed eventually by the
    #  test script.
   # while True:
       # pass
    
  #  yield({"assigned-groups": ["vibvats-djcran", "zkachwal-shah12-vrmath"],
      #         "total-cost" : 9})


if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
    
