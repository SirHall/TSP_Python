import wx
import wx.lib.agw.aui
import wx.lib.mixins.inspection

import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg

import plotter

def AddFigure(figure : matplotlib.figure.Figure):
	# figure = matplotlib.figure.Figure(dpi = None, figsize = (2, 2))
	canvas = FigureCanvasWxAgg(panel, -1, figure)
	toolbar = NavigationToolbar2WxAgg(canvas)

	toolbar.Realize() #Damn, I just realised!

	sizer = wx.BoxSizer(wx.VERTICAL)
	sizer.Add(canvas, 1, wx.EXPAND)
	sizer.Add(toolbar, 0, wx.LEFT | wx.EXPAND)
	panel.SetSizer(sizer)

def ShowWindow():
	frame.Show()
	app.MainLoop()

def ShowPlot():
	plotter.ApplyPlot()
	AddFigure(plotter.GetFigure())

#Setup basic window
app = wx.lib.mixins.inspection.InspectableApp()
frame = wx.Frame(None, 0, 'TSP Solver v3000™', \
	style = wx.MAXIMIZE_BOX | wx.SYSTEM_MENU | wx.RESIZE_BORDER | wx.CLOSE_BOX | wx.CAPTION | wx.MINIMIZE_BOX)
panel = wx.Panel(frame, id = 0)

#Try basic plot
plotter.PlotXY(1, 2)
plotter.PlotXY(2, 3)
plotter.PlotXY(3, 4)

ShowPlot()
ShowWindow()

# ApplyPlot().plot([1, 2, 3], [2, 3, 4], 'b-')





# wx.Panel.__init__(self, parent, id=id)
# panel.nb = aui.AuiNotebook(self)

# self.SetSizer(sizer)