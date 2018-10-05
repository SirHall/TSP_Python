from enum import Enum

class AlgorithmChoice(Enum):
	NearestNeigbour = 0
	Opt2 = 1
	SimulatedAnnealing = 2

start = 0
maxTime = 100
specialPrint = False
algorithmChoice = AlgorithmChoice.NearestNeigbour

