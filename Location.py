import math
from typing import List

class Location:
    
    #vars
    _id = 1
    _xpos = 0.0
    _ypos = 0.0
    
    def __init__(self, ID, xPos, yPos ):
        self._xpos = xPos
        self._ypos = yPos
        self._id = ID

    def FindDistanceTo(self, otherLocation):
        return math.sqrt((otherLocation._xpos - self._xpos)**2 + (otherLocation._ypos - self._ypos)**2)

    def Serialise(self):
        #Serialises to a CSV-compatible format
        return str(self._id) + '\t' + str(self._xpos) + '\t' + str(self._ypos) 

#Will parse a string into an instance of 'Location'

#region 'static' methods below

def ParseStringToLocation(stringToParse):
    numbers = stringToParse.strip().split()
    if len(numbers) != 3:
        return None
    return Location(int(numbers[0]), float(numbers[1]), float(numbers[2]))

def FindClosestCity(location : Location, locationsArray):
    closestLoc = None
    closestLocDist = float("inf") #Assigns the float representation of 'infinity'
    distToTest = float("inf") #Only initialize this once

    for loc in locationsArray:
        distToTest = location.FindDistanceTo(loc)
        if location.FindDistanceTo(loc) < closestLocDist:
            closestLoc = loc
            closestLocDist = distToTest
    return closestLoc

def FindTourLength(tour : List[Location]) -> None:
    length = 0.0
    index = 0
    while(index < len(tour) - 1):
        length += tour[index].FindDistanceTo(tour[index + 1])
        index += 1
    length += tour[len(tour) - 1].FindDistanceTo(tour[0]) #Distance back to start
    return length

def Swap(tour : List[Location], index1 : int, index2 : int):
    tmp = tour[index1]
    tour[index1] = tour[index2]
    tour[index2] = tmp



#
