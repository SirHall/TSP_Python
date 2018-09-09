import sys
import Location
import glob
import Funcs
import Opt2
import SimAnnealing
from typing import List
import time
import math

# print("Add -sp to input to enable 'special-print'")

glob.specialPrint = sys.argv.__contains__('-sp')
if glob.specialPrint:
	sys.argv.remove('-sp')

locations = []

# validLocationChars = "1234567890. \n"

glob.maxTime = float(sys.argv[2])

#region Setup locations
tspFile = open(sys.argv[1])
lines = tspFile.readlines()

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
		if glob.specialPrint == True:
			print(line.strip()) #This might be useful information
if glob.specialPrint == True:
	print()

path = [] #The generated path

#Greedy implementation
if glob.specialPrint == True:
	print('Greedy results:')
locationsLeft = locations.copy()
path.append(locationsLeft[0])
locationsLeft.remove(locationsLeft[0])

# #Find greedy path
closest = None #Initialize this once
while len(locationsLeft) > 0:
	closest = Location.FindClosestCity(path[len(path) - 1], locationsLeft)
	path.append(closest)
	locationsLeft.remove(closest)
	if glob.specialPrint == True:
		Funcs.PrintProgressBar(len(path), len(locations))
	if time.process_time() > glob.maxTime:
		path.extend(locationsLeft)
		locationsLeft.clear()
		if glob.specialPrint == True:
			print('\nCould not complete Nearest Neigbhour search')
if glob.specialPrint == True:
	print()
	Funcs.PrintTour(path)

#2Opt
if glob.specialPrint == True:
	print('Opt2 Results:')
pathLenDiff = 10
pathLenDiffThreshold = 0.001
lastLength = Location.FindTourLength(path)
 #If the path_delta < 1, it's not worth calculating anymore
while pathLenDiff >= pathLenDiffThreshold and time.process_time() < glob.maxTime:
	path = Opt2.Opt2(path)
	newLength = Location.FindTourLength(path)
	pathLenDiff = lastLength - newLength #Calculate this once
	if glob.specialPrint == True:
		print('Made path shorter by: ' + str(lastLength - newLength))
	lastLength = newLength

if glob.specialPrint == True:
	Funcs.PrintTour(path)

# Simulated annealing
if time.process_time() < glob.maxTime:
	if glob.specialPrint == True:
		print('Simulated annealing results:')
	iterations = 1000000
	initTemp = 1000000
	targetTemp = 0.000000001
	coolingRate = SimAnnealing.FindCoolingVal(iterations, initTemp, targetTemp)
	path = SimAnnealing.SimulatedAnneal(path, temp = initTemp, targetTmp = targetTemp, maxIts = iterations, coolRate = coolingRate)
	if glob.specialPrint == True:
		Funcs.PrintTour(path)

if glob.specialPrint == True:
	print('\nComputation time: ' + str(time.process_time()))
	print('Total path length: ' + str(Location.FindTourLength(path)))
else:
	Funcs.PrintData(tspFile.name, Location.FindTourLength(path), path)

tspFile.close()
#

def Pr(message : str):
	print(str, end = '')