# import sqlite3
import os
import Funcs
import Location
import tsp
import pymysql 

# dbPath = 'tspDataBase.db' 
#mysql --user="s5133659" --password="FMLmxF5Y" --host="mysql.ict.griffith.edu.au" --database="s5133659db" --execute="SHOW TABLES"
connection = pymysql.connect(
	host = 'mysql.ict.griffith.edu.au',
	user = 's5133659',
	password = 'FMLmxF5Y',
	db = 's5133659db'
	) #Disgusting hardcoded values

#Query results will be returned as a dictionary
cursor = connection.cursor(pymysql.cursors.DictCursor) 

# print(
# 	cursor.execute(
# 		"""SELECT * FROM Solution"""
# ))

# except expression as identifier:
# 	pass
# else:
	# pass)

# cursor.execute("PRAGMA foreign_keys = True") #Enable foreign keys for relational databases

# qry = open('schema.sql', 'r')
# cursor.execute(qry.read())
# qry.close()

def AddProblem(problemPath : str, problemName : str):
	try:
		f = open(problemPath)

		locations = tsp.Parse(f.read())
		
		cursor.execute(
			f"""INSERT INTO Problem(Name, Comment, Size) 
			VALUES ('{problemName}', 'Yeet machine', 1337)"""
		)

		for location in locations:
			cursor.execute(
				f"""INSERT INTO Cities(Name, ID, x, y) 
				VALUES ('{problemName}', {location._id}, {location._xpos}, {location._ypos})"""
			)
		f.close()
		connection.commit()
		return 'FILE ADDED SUCCESFULLY'
	except IOError:
		return 'FILE DOES NOT EXIST'

def GetProblemInfo(problemName : str):
	# problemName = f"'{problemName}'"
	if DoesProblemExist(problemName):
		#Construct problem
		cursor.execute(f"SELECT * FROM Cities WHERE Name='{problemName}'")
		cities = cursor.fetchall()

		for city in cities:
			print(f"{city['ID']} {city['x']} {city['y']}")
	else:
		print(f"PROBLEM '{problemName}' DOES NOT EXIST")

def GetProblem(problemName : str):
	problemName = f"'{problemName}'" #Surround with '
	cursor.execute(
		f"SELECT problem FROM Problems WHERE probName={problemName}"
	)
	return Funcs.ParseEscapeChars((str(cursor.fetchone())[:-3][3:]))

def AddSolution(problemName : str, solutionText : str, length : float):
	cursor.execute(
		"INSERT INTO Solutions(solutionToID, solution, length) VALUES (?, ?, ?)", \
		(problemName, solutionText, length) \
	)
	connection.commit()

def GetSolution(problemName : str):
	#Get shortest solution stored for this path
	problemName = f"'{problemName}'" #Surround with '
	# cursor.execute(
	# 	f"SELECT problem FROM Problems WHERE probName={problemName}"
	# )
	cursor.execute(
		"SELECT a.solution " \
		"FROM Solutions a " \
		"LEFT OUTER JOIN Solutions b " \
    	"	ON a.solutionToID = b.solutionToID AND a.length < b.length " \
		"WHERE b.solutionToID IS NULL" \
	)
	return Funcs.ParseEscapeChars((str(cursor.fetchone())[2:-3]))

def DoesProblemExist(problemName : str):
	cursor.execute(
		"SELECT COUNT(1) " \
		"FROM Problem " \
		f"WHERE Name = '{problemName}'" \
	)

	result = cursor.fetchall()
	print(result[0])

	# print(cursor.fetchone().)
	return True

def DoesSolutionExist(problemName : str):
	#Disgusting boilerplate
	problemName = f"'{problemName}'"
	cursor.execute(
		"SELECT COUNT(1) " \
		"FROM Solution " \
		f"WHERE ProblemName = {problemName} " \
	)
	return int(str(cursor.fetchone())[1:-2])
