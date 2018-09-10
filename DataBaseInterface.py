import sqlite3
import os
import Funcs

dbPath = 'tspDataBase.db' #Disgusting hardcoded values
connection = sqlite3.connect(dbPath)
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = True") #Enable foreign keys for relational databases

#Yes, I know it's bad practise to use 'AUTOINCREMENT', it just makes implementation simpler for such a simple project
cursor.execute(
	'CREATE TABLE IF NOT EXISTS ' \
	'Problems(' \
	'probName TEXT PRIMARY KEY,' \
	'problem TEXT' \
	')')

cursor.execute(
	'CREATE TABLE IF NOT EXISTS ' \
	'Solutions(' \
	'solutionID INTEGER PRIMARY KEY AUTOINCREMENT,' \
	'solutionToID TEXT' \
	'solution TEXT,' \
	'length REAL,' \
	'FOREIGN KEY(solutionToID) REFERENCES Problems(probName)'
	')')


# CreateTable(
# 	'Problems', 
# 	'probID', 'int'
# 	'problem', 'file',

# 	)

def AddProblem(problemPath : str, problemName : str):
	f = open(problemPath)
	cursor.execute(
		"INSERT INTO Problems(probName, problem) VALUES (?, ?)", \
		(problemName, f.read()) \
	)
	f.close()
	connection.commit()

def RetrieveProblemInfo(problemName : str):
	problemName = f"'{problemName}'" #Surround with '
	cursor.execute(
		f"SELECT problem FROM Problems WHERE probName={problemName}"
	)
	return Funcs.ParseEscapeChars((str(cursor.fetchone())[:-3][3:]))

def SetSolution(problemName : str, solutionText : str, length : float):
	#Get shortest solution for this problemName. If this is shorter, replace it
	cursor.execute(
		"INSERT INTO Solutions(solutionToID, solution) VALUES (?, ?)", \
		(problemName, solutionText) \
	)

def GetSolution(problemName : str):
	#Get solution stored for this path
	pass

#Old
def CreateTable(tableName : str, *parameters : str):
	# cursor.execute('CREATE TABLE IF NOT EXISTS {tableName}({parameters})')
	#Create a new table with the parameters passed
	input = ''
	isParName = True #Are we looking at the parameter type, or name?
	for word in parameters:
		input += word if isParName else ParseType(word) #Add the word to 'input'
		input += ' ' if isParName else ', ' #If we are on a type, add a comma 
		isParName = not isParName #Flip between parameter names, and types
	input = input[:-2]
	print(f'CREATE TABLE IF NOT EXISTS {tableName}({input})')
	cursor.execute(f'CREATE TABLE IF NOT EXISTS {tableName}({input})')

def InsertData(tableName : str, *values : str):
	inputNames = '' #Stores all parameter names
	inputValues = '' #Stores all values given each parameter name
	isColName = True #Are we looking at the column name, or value?
	for word in values:
		if isColName:
			inputNames += word + ', '
		else:
			inputValues += word + ', '
		isColName = not isColName
	
	#Remove trailing ', '
	inputNames = inputNames[:-2]
	inputValues = inputValues[:-2]

	print(f'INSERT INTO {tableName}({inputNames}) VALUES ({inputValues})')
	cursor.execute(f'INSERT INTO {tableName}({inputNames}) VALUES ({inputValues})') #Prone to SQL injection attacks
	connection.commit()

def CloseDataBase():
	cursor.close()
	connection.close()

def ParseType(valType : str):
	#Python doesn't have a switch-case statement...
	if valType.lower() == 'str': return 'TEXT'
	if valType.lower() == 'string': return 'TEXT'
	if valType.lower() == 'float': return 'REAL'
	if valType.lower() == 'int': return 'INT'
	if valType.lower() == 'bool': return 'BOOLEAN'
	if valType.lower() == 'file': return 'BLOB'
	return valType
