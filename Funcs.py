import Location
import sys
import os
from typing import List

# Written by Ovidiu(Ovi) Opris
# s5133659

def PrintTour(tour : List[Location.Location]):
	# print('Length: ' + str(Location.FindTourLength(tour)))
	for n in tour :
		print(str(n._id) + ', ', end = "", flush = True)
	print('-1\n')

def TourToText(tour : List[Location.Location]):
	text = 'Length: ' + str(Location.FindTourLength(tour)) + '\n'
	for n in tour :
		text += f"{n._id}\t{n._xpos}\t{n._ypos}\n"
	text += f"-1\t{tour[0]._xpos}\t{tour[0]._ypos}\n" #Add first 
	return text

def Isfloat(value):
	try:
		float(value)
		return True
	except ValueError:
		return False

def PrintProgressBar(current : float, fin : float, totalLength = 40):
	progress = current / fin
	line = '█' * int(round(progress * totalLength))
	blankSpace = ' ' * (totalLength - len(line))

	print('\r\t╣' + line + blankSpace +  '╠ ' + str(int(round(progress * 100))) + '%', end = '', flush = True)

def PrintData(fileName : str, tourLength : float, path : List[Location.Location]):
	#Prints in a CSV-compatible file format
	print('FileDir:\t' + fileName)
	print('Length:\t' + str(tourLength))
	print('Tour: ')
	for loc in path:
		print(loc.Serialise())
	#Finalise it with the starting location
	print(path[0].Serialise())

def ParseEscapeChars(input : str):
	input = input.replace("\\n", "\n")
	input = input.replace("\\t", "\t")
	return input