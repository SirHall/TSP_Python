import Location
import time
import Funcs
import miscGlobal
from typing import List


#Based off of: https://en.wikipedia.org/wiki/2-opt


def Opt2(tour : List[Location.Location]):
    
    oldTour = tour.copy()
    newTour = tour.copy()
    shortestDist = Location.FindTourLength(tour)

    i = 0
    j = 0
    ij = len(tour)**2
    while(i < len(tour)):
        j = i + 1
        if miscGlobal.specialPrint == True:
            Funcs.PrintProgressBar(i * j, ij)
        while(j < len(tour)):
            if time.process_time() > miscGlobal.maxTime: #A little bit spaghetti 
                if miscGlobal.specialPrint == True:
                    print()
                return oldTour
            newTour = oldTour.copy()
            TwoOptSwap(i, j, oldTour, newTour)
            # print('Elements: ' + str(len(newTour)))
            newDist = Location.FindTourLength(newTour)
            # print('CurDist: ' + str(newDist))
            if(newDist < shortestDist):
                oldTour = newTour
                shortestDist = newDist
                # print("\tNew shorter dist: " + str(shortestDist))
            j += 1
        i += 1
    if miscGlobal.specialPrint == True:
        Funcs.PrintProgressBar(100, 100)
        print()
    return oldTour

def TwoOptSwap(i : int, j : int, oldTour : List[Location.Location], newTour : List[Location.Location]):
    #1. take route[0] to route[i-1] and add them in order to new_route
    index = 0
    while(index < i):
        newTour[index] = oldTour[index]
        index += 1

    # 2. take route[i] to route[k] and add them in reverse order to new_route
    index = i
    decrement = 0
    while(index <= j):
        newTour[index] = oldTour[j - decrement]
        index += 1
        decrement += 1

    # 3. take route[k+1] to end and add them in order to new_route
    index = j + 1
    while (index < len(oldTour)):
        newTour[index] = oldTour[index]
        index += 1