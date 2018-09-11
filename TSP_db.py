import DataBaseInterface
import sys
import tsp
import Funcs
import Location
import glob

glob.specialPrint = sys.argv.__contains__('-sp')
if glob.specialPrint:
	sys.argv.remove('-sp')

if sys.argv[2] == 'ADD': #> python3 TSP_db.py problemName ADD problemDir.tsp 
	DataBaseInterface.AddProblem(sys.argv[3], sys.argv[1])
elif sys.argv[2] == 'SOLVE': #> python TSP_db.py problemName SOLVE maxSolveTime
	solution = tsp.SolveProblem(
		DataBaseInterface.GetProblem(sys.argv[1]), \
		sys.argv[1],
		sys.argv[3]
		)
	DataBaseInterface.AddSolution(
		sys.argv[1], \
		Funcs.TourToText(solution), \
		Location.FindTourLength(solution) \
	)
	# print(DataBaseInterface.RetrieveProblemInfo(sys.argv[1]))
elif sys.argv[2] == 'FETCH': #> python TSP_db.py problemName FETCH
	print(DataBaseInterface.GetSolution(sys.argv[1]))
else:
	print(f"INVALID ARGUMENT : {sys.argv[2]}") #Invalid argument
