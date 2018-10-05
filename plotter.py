import matplotlib.pyplot as plt

# _plotter = Plotter()



def PlotXY(x : float, y : float):
	xArray.append(x)
	yArray.append(y)

def ApplyPlot():
	plt.plot(xArray, yArray, 'b-')
	plt.plot(xArray, yArray, 'go')
	xArray.clear()
	yArray.clear()
	# plt.show()

def ClearPlot():
	xArray.clear()
	yArray.clear()
	# plt.cla()
	plt.clf() 

def GetFigure():
	return plt.gcf()

xArray = []
yArray = []