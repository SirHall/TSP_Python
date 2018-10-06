# import sqlite3
import os
import Funcs
import Location
import tsp
import pymysql 
import datetime
import miscGlobal
import time
from typing import List

# dbPath = 'tspDataBase.db' 
#mysql --user="s5133659" --password="FMLmxF5Y" --host="mysql.ict.griffith.edu.au" --database="s5133659db" --execute="SHOW TABLES"
connection = pymysql.connect(
	host = 'mysql.ict.griffith.edu.au',
	user = 's5133659',
	password = 'FMLmxF5Y',
	db = 's5133659db'
	) #Disgusting hardcoded values

# connection = pymysql.connect(
# 	host = 'localhost',
# 	user = 'root',
# 	password = '',
# 	db = 's5133659db'
# 	)tion = pymysql.connect(
# 	host = 'localhost',
# 	user = 'root',
# 	password = '',
# 	db = 's5133659db'
# 	)

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

def AddProblem(problemPath : str, problemName : str, comment : str = ''):
	try:
		f = open(problemPath)

		locations = tsp.Parse(f.read())
		
		cursor.execute(
			f"""INSERT INTO Problem(Name, Comment, Size) 
			VALUES ('{problemName}', '{comment}', {len(locations)})"""
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
		locations = []
		for city in cities:
			locations.append(Location.Location(city['ID'], city['x'], city['y']))
		return locations
	else:
		print(f"PROBLEM '{problemName}' DOES NOT EXIST")

def GetAllProblems():
	cursor.execute("SELECT * FROM Problem WHERE 1")
	return cursor.fetchall()
	

def AddSolution(problemName : str, solutionText : str, length : float, algorithm : str):
	cursor.execute(
		f"""INSERT INTO Solution(ProblemName, TourLength, Date, Author, Algorithm, RunningTime, Tour)
		VALUES ('{problemName}', {length}, STR_TO_DATE('{datetime.datetime.now().strftime("%Y-%m-%d")}', '%Y-%m-%d'), 
		's5133659', '{algorithm}', {int(miscGlobal.start + time.process_time())}, '{solutionText}')"""
	)

	connection.commit()

def GetSolution(problemName : str):
	#Get shortest solution stored for this path
	print(problemName)
	if DoesSolutionExist(problemName):
		cursor.execute(
			"SELECT a.Tour " \
			"FROM Solution a " \
			"LEFT OUTER JOIN Solution b " \
			"ON a.ProblemName = b.ProblemName AND a.TourLength < b.TourLength " \
			f"WHERE a.ProblemName = '{problemName}'" \
		)
		shortestSolution = cursor.fetchone()['Tour'].replace(",", "").replace("-1", "").split()
		print('Shortest path')
		print(shortestSolution)

		#Get all the cities that match up to this tour
		cursor.execute(
			f"""SELECT * FROM Cities WHERE Name = '{problemName}'"""
		)

		cities = cursor.fetchall()
		
		#Construct the path
		path = []
		for ID in shortestSolution:
			for city in cities:
				if int(city['ID']) == int(ID):
					path.append(Location.Location(city['ID'], city['x'], city['y']))
		return path

	else:
		print(f"SOLUTION FOR {problemName} DOES NOT EXIST")
		return ""

def GetAllSolutions():
	cursor.execute("SELECT * FROM Solution WHERE 1")
	return cursor.fetchall()

def DoesProblemExist(problemName : str):
	cursor.execute(
		"SELECT COUNT(1) " \
		"FROM Problem " \
		f"WHERE Name = '{problemName}'" \
	)
	result = cursor.fetchall()
	return int(str(result[0])[-2:-1]) >= 1 

def DoesSolutionExist(problemName : str):
	#Disgusting boilerplate
	cursor.execute(
		"SELECT COUNT(1) " \
		"FROM Solution " \
		f"WHERE ProblemName = '{problemName}'" \
	)
	result = cursor.fetchall()
	# print(result)
	return int(str(result[0])[-2:-1]) >= 1 
