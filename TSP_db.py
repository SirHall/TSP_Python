import DataBaseInterface
import sys
import tsp

if sys.argv[2] == 'ADD':
	DataBaseInterface.AddProblem(sys.argv[3], sys.argv[1])
elif sys.argv[2] == 'SOLVE':
	tsp.SolveProblem(
		DataBaseInterface.RetrieveProblemInfo(sys.argv[1]), \
		sys.argv[1],
		sys.argv[3]
		)
	# print(DataBaseInterface.RetrieveProblemInfo(sys.argv[1]))
elif sys.argv[2] == 'FETCH':
	pass
else:
	print(f"INVALID ARGUMENT : {sys.argv[2]}")
