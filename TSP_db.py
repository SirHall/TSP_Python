import DataBaseInterface
import sys
import tsp
import Funcs
import Location
import glob

glob.specialPrint = sys.argv.__contains__('-sp')
if glob.specialPrint:
	sys.argv.remove('-sp')

problemName = sys.argv[1]

if sys.argv[2] == 'ADD': #> python3 TSP_db.py problemName ADD problemDir.tsp
	if not DataBaseInterface.DoesProblemExist(problemName): 
		print(DataBaseInterface.AddProblem(sys.argv[3], problemName))
	else:
		print("PROBLEM ALREADY EXISTS")
elif sys.argv[2] == 'SOLVE': #> python TSP_db.py problemName SOLVE maxSolveTime
	if DataBaseInterface.DoesProblemExist(problemName):
		solution = tsp.SolveProblem(
			DataBaseInterface.GetProblem(problemName), \
			problemName,
			sys.argv[3]
			)
		DataBaseInterface.AddSolution(
			problemName, \
			Funcs.TourToText(solution), \
			Location.FindTourLength(solution) \
		)
	else:
		print(f"Problem '{problemName}' does not exist")
	# print(DataBaseInterface.RetrieveProblemInfo(sys.argv[1]))
elif sys.argv[2] == 'FETCH': #> python TSP_db.py problemName FETCH
	if DataBaseInterface.DoesSolutionExist(problemName):
		print(DataBaseInterface.GetSolution(problemName))
	else:
		print(f"Solution for problem '{problemName}' does not yet exist")
elif sys.argv[2] == 'PROBLEMEXISTS':
	print('TRUE' if DataBaseInterface.DoesProblemExist(problemName) else 'FALSE')	
elif sys.argv[2] == 'SOLEXISTS':
	print(f"{DataBaseInterface.DoesSolutionExist(problemName)} Solutions")
else:
	print(f"INVALID ARGUMENT : {sys.argv[2]}") #Invalid argument
