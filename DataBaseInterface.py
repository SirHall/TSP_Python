# import sqlite3
import os
import Funcs
import Location
import tsp
import pymysql 
import datetime
import miscGlobal
import time

# dbPath = 'tspDataBase.db' 
#mysql --user="s5133659" --password="FMLmxF5Y" --host="mysql.ict.griffith.edu.au" --database="s5133659db" --execute="SHOW TABLES"
# connection = pymysql.connect(
# 	host = 'mysql.ict.griffith.edu.au',
# 	user = 's5133659',
# 	password = 'FMLmxF5Y',
# 	db = 's5133659db'
# 	) #Disgusting hardcoded values

connection = pymysql.connect(
	host = 'localhost',
	user = 'root',
	password = '',
	db = 's5133659db'
	)

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
			VALUES ('{problemName}', '', {len(locations)})"""
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

def GetProblem(problemName : str):
	# problemName = f"'{problemName}'"
	if DoesProblemExist(problemName):
		#Construct problem
		cursor.execute(f"SELECT * FROM Cities WHERE Name='{problemName}'")
		cities = cursor.fetchall()

		strProblem = ""
		for city in cities:
			strProblem += f"{city['ID']} {city['x']} {city['y']}\n"
		return strProblem
	else:
		print(f"PROBLEM '{problemName}' DOES NOT EXIST")
	
# def GetProblem(problemName : str):
# 	problemName = f"'{problemName}'" #Surround with '
# 	cursor.execute(
# 		f"SELECT problem FROM Problems WHERE probName={problemName}"
# 	)
# 	return Funcs.ParseEscapeChars((str(cursor.fetchone())[:-3][3:]))

def AddSolution(problemName : str, solutionText : str, length : float, algorithm : str):
	# cursor.execute(
	# 	"INSERT INTO Solutions(solutionToID, solution, length) VALUES (?, ?, ?)", \
	# 	(problemName, solutionText, length) \
	# )

	cursor.execute(
		f"""INSERT INTO Solution(ProblemName, TourLength, Date, Author, Algorithm, Running Time, Tour)
		VALUES ('{problemName}', {length}, {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, 's5133659', '{algorithm}', {time.process_time()}, '{solutionText}')
		"""
	)

	connection.commit()

def GetSolution(problemName : str):
	#Get shortest solution stored for this path
	if DoesSolutionExist(problemName):
		problemName = f"'{problemName}'" #Surround with '
		cursor.execute(
			"SELECT a.Tour " \
			"FROM Solution a " \
			"LEFT OUTER JOIN Solution b " \
			"	ON a.ProblemName = b.ProblemName AND a.TourLength < b.TourLength " \
			"WHERE b.ProblemName IS NULL" \
		)
		print(cursor.fetchone())
		# return Funcs.ParseEscapeChars((str(cursor.fetchone())[2:-3]))
	else:
		print(f"SOLUTION FOR {problemName} DOES NOT EXIST")
		return ""

def DoesProblemExist(problemName : str):
	cursor.execute(
		"SELECT COUNT(1) " \
		"FROM Problem " \
		f"WHERE Name = '{problemName}'" \
	)
	result = cursor.fetchall()
	return int(str(result[0])[-2:-1]) == 1 

def DoesSolutionExist(problemName : str):
	#Disgusting boilerplate
	cursor.execute(
		"SELECT COUNT(1) " \
		"FROM Solution " \
		f"WHERE ProblemName = '{problemName}'" \
	)
	return str(cursor.fetchall()[0])[-2:-1] == 1 
