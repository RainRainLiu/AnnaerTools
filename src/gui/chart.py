from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from pylab import Figure, np


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

    def update_figure(self, labels, fracs, title, text):
        self.axes.clear()
        self.axes.set_title(title)
        self.axes.pie( x=fracs, labels=labels,autopct=lambda pct: self.func(pct, fracs), textprops=dict(color="#000000")
                       ,startangle=90)
        #print(self.sizeHint().h)
        self.axes.text(-(self.fig.get_size_inches()[0]/3), (self.fig.get_size_inches()[1])/5, text,
                      horizontalalignment='left',color='green', fontsize=12)
        self.draw()
    def updateLine(self, scale, dataList):
        self.axes.clear()
        for line in dataList:
            self.axes.plot(scale, line[1], label=line[0], marker='.')
        self.axes.set( xlabel='Data', ylabel='Value',
                title='最近30日' )
        self.axes.grid(linestyle='--', linewidth=1)
        self.axes.legend()
        self.draw()