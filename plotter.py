import matplotlib.pyplot as plt

# _plotter = Plotter()

xArray = []
yArray = []

def PlotXY(x : float, y : float):
	xArray.append(x)
	yArray.append(y)

def ApplyPlot():
	plt.plot(xArray, yArray, 'b-')
	plt.plot(xArray, yArray, 'go')
	# plt.show()

def ClearPlot():
	plt.clf() 

def GetFigure():
	return plt.gcf()