import Location
import math
import random
import time
import miscGlobal
import Funcs
from typing import List

def SimulatedAnneal(tour : List[Location.Location], temp : float = 1000000.0, coolRate : float = 0.0003, targetTmp : float = 0.001, maxIts : int = 10000000):
	bestTour = tour
	bestDist = Location.FindTourLength(tour)

	currentTour = bestTour
	currentDist = bestDist

	#Initialise these once
	tourIndex1 = 0
	tourIndex2 = 0

	totalIts = 0

	while temp > targetTmp and totalIts < maxIts:
		if (100 / maxIts * totalIts) % 1 == 0 and miscGlobal.specialPrint == True: #Only write to console when needed
			Funcs.PrintProgressBar(totalIts, maxIts)
			
		if time.process_time() > miscGlobal.maxTime: #A little bit spaghetti 
			if miscGlobal.specialPrint == True:
				print()
			return bestTour
		totalIts += 1
		newTour = currentTour.copy()

		while tourIndex1 == tourIndex2: #Make sure that these aren't the same
			tourIndex1 = random.randint(0, len(newTour) - 1)
			tourIndex2 = random.randint(0, len(newTour) - 1)

		#Swap the locations
		Location.Swap(newTour, tourIndex1, tourIndex2)
		
		newDist = Location.FindTourLength(newTour)

		if AcceptProbs(currentDist, newDist, temp) : #Should we accept this new tour
			currentTour = newTour
			currentDist = newDist
			# print('New tour dist: ' + str(currentDist))

		if newDist < bestDist:
			bestTour = newTour
			bestDist = newDist

		tourIndex1 = tourIndex2 #Makes them both equal so they will be recalculated
		
		temp *= 1 - coolRate
		# print(temp)
	
	if miscGlobal.specialPrint == True:
		Funcs.PrintProgressBar(100, 100)
		print()
	return bestTour

def AcceptProbs(currDist : float, newDist : float, temp : float):
	if(newDist < currDist):
		return True
	return math.exp((currDist - newDist) / temp) > random.random()

#Can see my proog for this here: https://www.desmos.com/calculator/cwzfjjl8z2
def FindCoolingVal(iterations : int, initTemp : float, targetTemp : float ):
	#Find cooling value, to reach a given target temperature, given a maximum number of iterations
	return -((targetTemp/initTemp)**(1.0/iterations)) + 1