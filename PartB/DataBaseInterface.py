import sqlite3

dbPath = 'testDataBase.db'
connection = sqlite3.connect(dbPath)
cursor = connection.cursor()

def CreateTable(tableName : str, *parameters : str):
	# cursor.execute('CREATE TABLE IF NOT EXISTS {tableName}({parameters})')
	#Create a new table with the parameters passed
	input = ''
	isParName = True #Are we looking at the parameter type, or name?
	for word in parameters:
		input += word #Add the word to 'input'
		input += ' ' if isParName else ', ' #If we are on a type, add a comma 
		isParName = not isParName #Flip between parameter names, and types
	input = input[:-2]
	print(f'CREATE TABLE IF NOT EXISTS {tableName}({input})')
	cursor.execute(f'CREATE TABLE IF NOT EXISTS {tableName}({input})')

def InsertData(tableName : str, *values : str):
	inputNames = '' #Stores all parameter names
	inputValues = ''#Stores all values given each parameter name
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
	cursor.execute(f'INSERT INTO {tableName}({inputNames}) VALUES ({inputValues})')
	# cursor.execute(f'INSERT INTO {tableName} VALUES ({inputValues})')
	connection.commit()

def CloseDataBase():
	cursor.close()
	connection.close()
