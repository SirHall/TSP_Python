from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
import wx.lib.mixins.inspection
import DataBaseInterface
from typing import List
import wx.lib.agw.aui
import matplotlib
import miscGlobal
import Location
import plotter
import random
import Funcs
import time
import tsp
import wx

def SetupFrameUI():
	menuBar = wx.MenuBar()

	#MenuBar: File [Exit, AddToDB, LoadFromDB]
	fileButton = wx.Menu()
	exitItem = fileButton.Append(wx.ID_EXIT, 'Exit', 'Close program')
	addToDBItem = fileButton.Append(wx.ID_ANY, 'Add to database', 'Adding to database')
	loadProblemItem = fileButton.Append(wx.ID_ANY, 'Load problem', 'Loading problem')

	menuBar.Append(fileButton, 'File')
	
	#MenuBar: Solve [Show Problems, Show Solutions]
	solveButton = wx.Menu()
	showProblemsItem = solveButton.Append(wx.ID_ANY, 'Show problems in DB', 'Getting problems')
	showSolutionsItem = solveButton.Append(wx.ID_ANY, 'Show solutions in DB', 'Getting solution')
	solveLoadedItem = solveButton.Append(wx.ID_ANY, 'Solve loaded tour', 'Solving tour')

	menuBar.Append(solveButton, 'Solve')
	
	#MenuBar: Choose Algorithm [NearestNeighbour, Opt2, Simulated Annealing]
	chooseButton = wx.Menu()
	nearestNeigbourItem = chooseButton.Append(wx.ID_ANY, 'Nearest Neighbour')
	opt2Item = chooseButton.Append(wx.ID_ANY, '2-Opt')
	simulatedAnnealingItem = chooseButton.Append(wx.ID_ANY, 'Simulated Annealing')
	
	menuBar.Append(chooseButton, 'Choose Algorithm')

	frame.SetMenuBar(menuBar)
	frame.Bind(wx.EVT_MENU, frame.Close, exitItem)
	frame.Bind(wx.EVT_MENU, AddToDB, addToDBItem)
	frame.Bind(wx.EVT_MENU, ShowAllProbsFromDB, showProblemsItem)
	frame.Bind(wx.EVT_MENU, ShowAllSolsFromDB, showSolutionsItem)
	frame.Bind(wx.EVT_MENU, ChooseNearestNeighbour, nearestNeigbourItem)
	frame.Bind(wx.EVT_MENU, ChooseOpt2, opt2Item)
	frame.Bind(wx.EVT_MENU, ChooseSimulatedAnnealing, simulatedAnnealingItem)
	frame.Bind(wx.EVT_MENU, LoadProblem, loadProblemItem)
	frame.Bind(wx.EVT_MENU, SolveLoadedPath, solveLoadedItem)

def GetStrInput(message : str, title : str = ''):
	dialog = wx.TextEntryDialog(frame, message, title)
	if dialog.ShowModal() == wx.ID_OK:
		val = dialog.GetValue()
		dialog.Destroy()
		return val
	dialog.Destroy()
	return None

def GetFileInput():
	dialog = wx.FileDialog(frame, "Open", "", "", "Python files (*.tsp)|*.tsp", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
	dialog.ShowModal()
	path = dialog.GetPath()
	dialog.Destroy()
	return path

def MessageBox(message: str, title : str = ''):
	wx.MessageBox(message, title, wx.OK)

def ErrorBox(message: str, title : str = ''):
	wx.MessageBox(message, title, wx.OK | wx.ICON_ERROR)

def AddToDB(any):
	DataBaseInterface.AddProblem(GetFileInput(), GetStrInput("Problem name: "), comment = GetStrInput("Comment: "))

def ShowAllProbsFromDB(any):
	problems = DataBaseInterface.GetAllProblems()
	probStr = ""
	for problem in problems:
		probStr += f"{problem['Name']}\n"
	MessageBox("Problems:\n\n" + probStr)

def ShowAllSolsFromDB(any):
	solutions = DataBaseInterface.GetAllSolutions()
	solsStr = ""
	for solution in solutions:
		solsStr += f"{solution['SolutionID']}    {solution['ProblemName']}\n"
	MessageBox("Solutions:\n\nID    Name\n" + solsStr)

def ChooseNearestNeighbour(any):
	SetAlgorithm(miscGlobal.AlgorithmChoice.NearestNeigbour)

def ChooseOpt2(any):
	SetAlgorithm(miscGlobal.AlgorithmChoice.Opt2)

def ChooseSimulatedAnnealing(any):
	SetAlgorithm(miscGlobal.AlgorithmChoice.SimulatedAnnealing)

def SolveLoadedPath(self):
	timeStr =  'Something that won\'t format'
	while not Funcs.Isfloat(timeStr):
		timeStr = GetStrInput("Max computation time: ")
	miscGlobal.start = time.process_time()
	miscGlobal.maxTime = float(timeStr)
	
	if miscGlobal.algorithmChoice == miscGlobal.AlgorithmChoice.NearestNeigbour:
		for stepPath in tsp.NearestNeighbour(miscGlobal.tour):
			miscGlobal.tour = stepPath
			PlotTour()

#Loads a problem from the database and sets it as the current tour
def LoadProblem(self):
	miscGlobal.tour = DataBaseInterface.GetProblem(GetStrInput("Problem name: "))
	PlotTour()

def SetAlgorithm(choice : miscGlobal.AlgorithmChoice):
	miscGlobal.algorithmChoice = choice

def AddFigure(figure : matplotlib.figure.Figure):
	frame.canvas = FigureCanvasWxAgg(panel, -1, figure)
	frame.toolbar = NavigationToolbar2WxAgg(frame.canvas)

	frame.toolbar.Realize() #Damn, I just realised!

	frame.sizer = wx.BoxSizer(wx.VERTICAL)
	frame.sizedCanvas = frame.sizer.Add(frame.canvas, 1, wx.EXPAND)
	frame.sizer.Add(frame.toolbar, 0, wx.LEFT | wx.EXPAND)
	panel.SetSizer(frame.sizer)

def Update():
	panel.Refresh()
	panel.Update()

	winSize = frame.GetSize();
	winSize.DecBy(1)
	frame.SetSize(winSize)
	winSize.IncBy(1)
	frame.SetSize(winSize)
	# frame.SendSizeEvent()
	pass
	# frame.Update()
	# frame.sizedCanvas
	
	# frame.sizer.Update()


def UpdateFigure(figure : matplotlib.figure.Figure):
	# frame.canvas = None
	# frame.toolbar = None
	# frame.sizer = None
	# # panel.SetSizer(None)
	# panel.Sizer.Clear(True)

	# frame.canvas = FigureCanvasWxAgg(panel, -1, figure)
	# frame.toolbar = NavigationToolbar2WxAgg(frame.canvas)

	# frame.toolbar.Realize() #Damn, I just realised!

	# frame.sizedCanvas = frame.sizer.Add(frame.canvas, 1, wx.EXPAND)
	# frame.sizer.Add(frame.toolbar, 0, wx.LEFT | wx.EXPAND)
	# panel.SetSizer(frame.sizer)

	# AddFigure(figure)
	# panel.GetSizer().GetChildren().Remove(frame.sizedCanvas)
	# panel.
	pass

def ShowWindow():
	frame.Show()
	app.MainLoop()
	

def ShowPlot():
	AddFigure(plotter.GetFigure())

def PlotTour():
	plotter.ClearPlot()
	for location in miscGlobal.tour:
		plotter.PlotXY(location._xpos, location._ypos)
	plotter.ApplyPlot()
	Update()
	# UpdateFigure(plotter.GetFigure())



#Setup basic window
app = wx.lib.mixins.inspection.InspectableApp()
frame = wx.Frame(None, -1, 'TSP Solver v3000™', \
	style = wx.MAXIMIZE_BOX | wx.SYSTEM_MENU | wx.RESIZE_BORDER | wx.CLOSE_BOX | wx.CAPTION | wx.MINIMIZE_BOX)
panel = wx.Panel(frame, id = -1)
frame.CenterOnScreen()
frame.canvas = FigureCanvasWxAgg(panel, -1, plotter.GetFigure())
SetupFrameUI()

for k in range(0, 1):
	plotter.ClearPlot()
	for i in range(0, 10):
		plotter.PlotXY(i, random.randint(0, 10))
	plotter.ApplyPlot()

	#Show window
ShowPlot()
ShowWindow()