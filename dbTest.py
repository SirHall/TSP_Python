import DataBaseInterface

DataBaseInterface.cursor.execute("""SHOW TABLES;""")

print(DataBaseInterface.cursor.fetchall())

# result = DataBaseInterface.cursor.execute("""SELECT * FROM Problem""")
# print(result)
