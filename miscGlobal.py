from enum import Enum
from typing import List
import Location


class AlgorithmChoice(Enum):
	NearestNeigbour = 0
	Opt2 = 1
	SimulatedAnnealing = 2

start = 0
maxTime = 100
specialPrint = False
algorithmChoice = AlgorithmChoice.NearestNeigbour
tour = List[Location.Location]
name = ""
