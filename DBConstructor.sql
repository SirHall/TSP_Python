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
	'solutionToID TEXT,' \
	'solution TEXT,' \
	'length REAL,' \
	'FOREIGN KEY(solutionToID) REFERENCES Problems(probName)'
	')')