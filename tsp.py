import sys
import Location
import miscGlobal
import Funcs
import Opt2
import SimAnnealing
from typing import List
import time
import math

# print("Add -sp to input to enable 'special-print'")
# locations = [] #List of all locations
# path = [] #The generated path

# validLocationChars = "1234567890. \n"

#region Setup locations

def SolveProblem(problemText : str, problemName : str, maxTime : float):
	miscGlobal.maxTime = float(maxTime)

	path = []

	# print(Parse(problemText))
	path = Parse(problemText)
	path = NearestNeighbour(path)
	path = TwoOpt(path)
	path = SimulatedAnnealing(path)

	if miscGlobal.specialPrint == True:
		print('\nComputation time: ' + str(time.process_time() - miscGlobal.start))
		print('Total path length: ' + str(Location.FindTourLength(path)))
	else:
		Funcs.PrintData(problemName, Location.FindTourLength(path), path)
	
	return path

def Parse(lines : str):
	locations = []
	lines = lines.splitlines()
	#Parse all lines with only numbers and '.'s to instances of 'Location'
	for line in lines:
		if line.replace('\n', '', 1000).replace(' ', '', 1000) == '':
			continue
		#If all the characters in this line, are contained within 'validLocationChars'
		# if all(validLocationChars.__contains__(char) for char in line):
		if all(Funcs.Isfloat(word) for word in line.split()): #If everything on this line can be converted into a float, then it is a location
			#All characters in this line are contained within 'validLocationChars'
			#This is a location
			locations.append(Location.ParseStringToLocation(line))
		else:
			#Atleast one character in this line are not contained within 'validLocationChars'
			#This is not a location
			if miscGlobal.specialPrint == True:
				print(line.strip()) #This might be useful information
	if miscGlobal.specialPrint == True:
		print()
	return locations

def NearestNeighbour(locations : List[Location.Location]):
	path = []

	#Greedy implementation
	if miscGlobal.specialPrint == True:
		print('Greedy results:')
	locationsLeft = locations.copy()
	path.append(locationsLeft[0])
	locationsLeft.remove(locationsLeft[0])

	#Find greedy path
	closest = None #Initialize this once
	while len(locationsLeft) > 0:
		closest = Location.FindClosestCity(path[len(path) - 1], locationsLeft)
		path.append(closest)
		locationsLeft.remove(closest)
		if miscGlobal.specialPrint == True:
			Funcs.PrintProgressBar(len(path), len(locations))
		if (time.process_time() - miscGlobal.start) > miscGlobal.maxTime:
			path.extend(locationsLeft)
			locationsLeft.clear()
			if miscGlobal.specialPrint == True:
				print('\nCould not complete Nearest Neigbhour search')
		yield path
	if miscGlobal.specialPrint == True:
		print()
		Funcs.PrintTour(path)
	return path

def TwoOpt(path : List[Location.Location]):
	#2Opt
	if miscGlobal.specialPrint == True:
		print('Opt2 Results:')
	pathLenDiff = 10
	pathLenDiffThreshold = 0.001
	lastLength = Location.FindTourLength(path)
	 #If the path_delta < 1, it's not worth calculating anymore
	while pathLenDiff >= pathLenDiffThreshold and (time.process_time() - miscGlobal.start) < miscGlobal.maxTime:
		path = Opt2.Opt2(path)
		newLength = Location.FindTourLength(path)
		pathLenDiff = lastLength - newLength #Calculate this once
		if miscGlobal.specialPrint == True:
			print('Made path shorter by: ' + str(lastLength - newLength))
		lastLength = newLength

	if miscGlobal.specialPrint == True:
		Funcs.PrintTour(path)
	return path

def SimulatedAnnealing(path : List[Location.Location]):
	# Simulated annealing
	if (time.process_time() - miscGlobal.start) < miscGlobal.maxTime:
		if miscGlobal.specialPrint == True:
			print('Simulated annealing results:')
		iterations = 1000000
		initTemp = 1000000
		targetTemp = 0.000000001
		coolingRate = SimAnnealing.FindCoolingVal(iterations, initTemp, targetTemp)
		path = SimAnnealing.SimulatedAnneal(path, temp = initTemp, targetTmp = targetTemp, maxIts = iterations, coolRate = coolingRate)
		if miscGlobal.specialPrint == True:
			Funcs.PrintTour(path)
	return path

def Pr(message : str):
	print(str, end = '')
