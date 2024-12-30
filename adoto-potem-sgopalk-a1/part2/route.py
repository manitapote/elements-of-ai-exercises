#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: name IU ID
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
import sys
import pandas as pd
import heapq
from math import radians, cos, sin, asin, sqrt

#Gets the route to destination
#start: start city
#end: end/destination city
#cost: cost of choice (segments, distance, time, safe)
def get_route(start, end, cost):
	df = pd.read_csv("road-segments.txt",
				header = None,
				delimiter = ' ')
	df.columns = ['start_city', 'end_city', 'length', 'speed_limit', 'name_of_highway']
	city_lat_long = pd.read_csv('city-gps.txt', header=None, delimiter=' ')
	
	city_lat_long.columns = ['city', 'lat', 'long']

	#First element is cost of  choice, second is current city, third is miles, 
	#Fourth is hours, fifth is accidents and sixth holds path of route.
	#Fringe to store necessary data
	fringe = [(0.0, start, 0.0, 0.0, 0.0, [])]

	#Maintains the list of visited cities
	visited = []

	while len(fringe) > 0:
		#rearrange the data in fringe based on cost (priority queue)
		heapq.heapify(fringe)

		(cost_amount, state, miles, hours, accidents, path) = heapq.heappop(fringe)

		if state in visited:
			continue

		for index, city in successors(state, df).iterrows():
			#swaps the start and end city if the end city is current city
			if city['end_city'] == state:
				temp = city['start_city']
				city['start_city'] = state
				city['end_city'] = temp

			if is_goal(state, end):
				return {"total-segments" : len(path), 
					"total-miles" : miles, 
					"total-hours" : hours, 
					"total-expected-accidents" : accidents/1000000, 
					"route-taken" : path}

			new_cost = cost_(city, 
					cost_amount, 
					cost, 
					miles,
					hours,
					accidents,
					path)

			total_cost =  new_cost[0] + \
			heuristic(city['end_city'], end, city_lat_long, df, cost)

			fringe.append((total_cost, 
						city['end_city'], 
						new_cost[1],
						new_cost[2],
						new_cost[3],
						new_cost[4]))
		visited.append(state)

	return {"total-segments" : len(path), 
		"total-miles" : miles, 
		"total-hours" : hours, 
		"total-expected-accidents" : accidents/1000000, 
		"route-taken" : path}

#Checks whether the state is the goal/end state
#returns boolean
def is_goal(state, end_state):
	return state == end_state

#Gets all cities that can be visited from and to current_city
def successors(current_city, df):
	return df.loc[(df['start_city'] == current_city) | (df['end_city'] == current_city)]

#Calculates the cost of visiting next node from starting node
#returns cost: cost of visiting next node based on cost choice,
#miles: total miles from starting node to next node
#hours: total time in visiting next node
#accidents: total accidents in visitng next node
#new_path: path upto next node
def cost_(next_state, cost_amount, cost_choice, miles, hours, accidents, path):
	cost = 0
	new_path = path.copy()
	highway_info = next_state['name_of_highway'] + ' for ' + str(next_state['length']) + ' miles'
	
	new_path.append((next_state['end_city'] , highway_info))
	
	miles += next_state['length']
	hours += next_state['length'] / next_state['speed_limit']
  
	if next_state['name_of_highway'].startswith('I'):
		accidents += next_state['length']
	else:
		accidents += next_state['length'] * 2

	if cost_choice == 'segments':
		cost = cost_amount + 1
	if cost_choice == 'distance':
		cost = miles
	if cost_choice == 'time':
		cost = hours
	if cost_choice == 'safe':
		cost = accidents

	return (cost, miles, hours, accidents, new_path)

#Calculates heuritic based on cost choice
def heuristic(start, end, gps_df, df, choice):
	if choice == 'distance':
		origin = gps_df.loc[gps_df['city'] == start]
		destination = gps_df.loc[gps_df['city'] == end]
		
		if len(origin) == 0 or len(destination) == 0:
			return 0
		
		return calculate_distance_between_lat_long(origin['lat'],
				origin['long'],
				destination['lat'],
				destination['long'])

	if choice == 'time':
		return min(df[(df['start_city'] == start) | (df['end_city'] == start)].apply(
			lambda x: x['length'] / x['speed_limit'], 
			axis = 1))
	
	if choice == 'segments':
		return 0
	
	condition = (df['start_city'] == start) | (df['end_city'] == start)
	interstate_condition = df['name_of_highway'].str.get(0).isin(['I'])

	interstate_highway = df[condition & interstate_condition]['length']
	
	non_interstate = df[condition & (~interstate_condition)]['length']
	
	if not len(non_interstate):
		return min(interstate_highway)
	if not len(interstate_highway):
		return min(non_interstate) * 2
	
	return min(min(non_interstate) * 2, min(interstate_highway))

################## Code taken from other source starts here ###################################

#This code was taken from the following site:
#https://www.geeksforgeeks.org/program-distance-two-points-earth/

#Calculates the distance between two lattitue and longtitute points based on Haversine Formula
def calculate_distance_between_lat_long(lat1, long1, lat2, long2):
	long1 = radians(long1) 
	long2 = radians(long2) 
	lat1 = radians(lat1) 
	lat2 = radians(lat2) 

	# Haversine formula  
	dlon = long2 - long1  
	dlat = lat2 - lat1 
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

	c = 2 * asin(sqrt(a))  

	# Radius of earth in miles 
	r = 3956

	# calculate the result in miles
	return(c * r)


################## Code taken from other source ends here ###################################

# Please don't modify anything below this line
if __name__ == "__main__":
	if len(sys.argv) != 4:
		raise(Exception("Error: expected 3 arguments"))

	(_, start_city, end_city, cost_function) = sys.argv
	if cost_function not in ("segments", "distance", "time", "safe"):
		raise(Exception("Error: invalid cost function"))

	result = get_route(start_city, end_city, cost_function)
	
	# Pretty print the route
	print("Start in %s" % start_city)
	for step in result["route-taken"]:
		print("   Then go to %s via %s" % step)

	print("\n Total segments: %6d" % result["total-segments"])
	print("    Total miles: %10.3f" % result["total-miles"])
	print("    Total hours: %10.3f" % result["total-hours"])
	print("Total accidents: %15.8f" % result["total-expected-accidents"])


