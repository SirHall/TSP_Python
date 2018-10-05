import DataBaseInterface
import sys
import tsp
import Funcs
import Location
import miscGlobal
import plotter

miscGlobal.specialPrint = sys.argv.__contains__('-sp')
if miscGlobal.specialPrint:
	sys.argv.remove('-sp')

problemName = sys.argv[1]

if len(sys.argv) >= 4 and sys.argv[2] == 'ADD': #> python3 TSP_db.py problemName ADD problemDir.tsp
	if not DataBaseInterface.DoesProblemExist(problemName): 
		print(DataBaseInterface.AddProblem(sys.argv[3], problemName))
	else:
		print("PROBLEM ALREADY EXISTS")
elif len(sys.argv) >= 4 and sys.argv[2] == 'SOLVE': #> python TSP_db.py problemName SOLVE maxSolveTime
	if DataBaseInterface.DoesProblemExist(problemName):
		solution = tsp.SolveProblem(
			DataBaseInterface.GetProblem(problemName), \
			problemName,
			sys.argv[3]
			)
		DataBaseInterface.AddSolution(
			problemName, \
			Funcs.TourToIDText(solution), \
			Location.FindTourLength(solution), \
			"Test algorithm" \
		)
	else:
		print(f"Problem '{problemName}' does not exist")
	# print(DataBaseInterface.RetrieveProblemInfo(sys.argv[1]))
elif len(sys.argv) >= 3 and sys.argv[2] == 'FETCH': #> python TSP_db.py problemName FETCH
	if DataBaseInterface.DoesSolutionExist(problemName):
		print(DataBaseInterface.GetSolution(problemName))
	else:
		print(f"Solution for problem '{problemName}' does not yet exist")
elif len(sys.argv) >= 3 and sys.argv[2] == 'PROBLEMEXISTS':
	print('TRUE' if DataBaseInterface.DoesProblemExist(problemName) else 'FALSE')	
elif len(sys.argv) >= 3 and sys.argv[2] == 'SOLEXISTS':
	print(f"{DataBaseInterface.DoesSolutionExist(problemName)} Solutions")
elif len(sys.argv) >= 3 and sys.argv[2] == 'PLOTPROB':
	if DataBaseInterface.DoesProblemExist(problemName):
		locations = tsp.Parse(DataBaseInterface.GetProblem(problemName))
		for location in locations:
			plotter.PlotXY(location._xpos, location._ypos)
		plotter.ShowPlot()
	else:
		print(f"PROBLEM {problemName} DOES NOT EXIST")
elif len(sys.argv) >= 3:
	print(f"INVALID ARGUMENT : {sys.argv[2]}") #Invalid argument



DataBaseInterface.cursor.close();
DataBaseInterface.connection.close();