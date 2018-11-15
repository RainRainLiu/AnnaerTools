from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from pylab import *


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        print(width, height)
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.parent = parent
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)


    def func(self, pct, allvals):
        absolute = float( pct / 100. * np.sum( allvals ) )
        return "{:.1f}%\n{:.2f} ".format( pct, absolute )

    def update_figure(self, labels, fracs, title):
        self.axes.clear()
        self.axes.set_title(title)
        self.axes.pie( x=fracs, labels=labels,autopct=lambda pct: self.func(pct, fracs), textprops=dict(color="#000000")
                       ,startangle=90)
        self.draw()
    def updateLine(self, scale, dataList):
        self.axes.clear()
        for line in dataList:
            self.axes.plot(scale, line[1], label=line[0], marker='.')
            for a, b in zip(scale, line[1]):
                self.axes.text(a, b, b, ha='center', va='bottom', fontsize=10)
        self.axes.legend()
        self.draw()