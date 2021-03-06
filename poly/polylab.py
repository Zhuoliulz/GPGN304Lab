import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
from PolygonInteracter import PolygonInteractor

class DraggablePoint:
    lock = None #only one can be animated at a time
    def __init__(self, point):
        self.point = point
        self.press = None
        self.background = None

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.point.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.point.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.point.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.point.axes: return
        if DraggablePoint.lock is not None: return
        contains, attrd = self.point.contains(event)
        if not contains: return
        self.press = (self.point.center), event.xdata, event.ydata
        DraggablePoint.lock = self

        # draw everything but the selected rectangle and store the pixel buffer
        canvas = self.point.figure.canvas
        axes = self.point.axes
        self.point.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.point.axes.bbox)

        # now redraw just the rectangle
        axes.draw_artist(self.point)

        # and blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_motion(self, event):
        if DraggablePoint.lock is not self:
            return
        if event.inaxes != self.point.axes: return
        self.point.center, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.point.center = (self.point.center[0]+dx, self.point.center[1]+dy)

        canvas = self.point.figure.canvas
        axes = self.point.axes
        # restore the background region
        canvas.restore_region(self.background)

        # redraw just the current rectangle
        axes.draw_artist(self.point)

        # blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_release(self, event):
        'on release we reset the press data'
        if DraggablePoint.lock is not self:
            return

        self.press = None
        DraggablePoint.lock = None

        # turn off the rect animation property and reset the background
        self.point.set_animated(False)
        self.background = None

        # redraw the full figure
        self.point.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.point.figure.canvas.mpl_disconnect(self.cidpress)
        self.point.figure.canvas.mpl_disconnect(self.cidrelease)
        self.point.figure.canvas.mpl_disconnect(self.cidmotion)

fig = plt.figure()
dataSubplot = fig.add_subplot(2,2,1)
modelSubplot = fig.add_subplot(2,2,3)

'''
drs = []
circles = [patches.Circle((0.3, 0.4), 0.03, fc='r', alpha=0.5),
               patches.Circle((0.5,0.2), 0.03, fc='g', alpha=0.5),
               patches.Circle((0.2,0.1), 0.03, fc='b', alpha=0.5),
               patches.Circle((0.6,0.4), 0.03, fc='y', alpha=0.5),]

for circ in circles:
    modelSubplot.add_patch(circ)
    dr = DraggablePoint(circ)
    dr.connect()
    drs.append(dr)
'''
    
theta = np.arange(0, 2*np.pi, 2.0)
r = 0.2

xs = r*np.cos(theta)+0.25
ys = r*np.sin(theta)+0.25
poly = patches.Polygon(list(zip(xs, ys)), animated=True)
modelSubplot.add_patch(poly)
p = PolygonInteractor(modelSubplot, poly)

# buttons
# load data
def loadData(self):
    5
ax0=plt.axes([.55,.85,.175,.1])
loadDataButton=Button(ax0,'Load Data')
loadDataButton.on_clicked(loadData)
# load model
def loadModel(self):
    5
ax1=plt.axes([.775,.85,.175,.1])
loadModelButton=Button(ax1,'Load Model')
loadModelButton.on_clicked(loadModel)
# new model
def newPoly(self):
    5
ax2=plt.axes([.55,.7,.175,.1])
clearModelButton=Button(ax2,'Clear Model')
clearModelButton.on_clicked(newPoly)
# save model
def saveModel(self):
    5
ax3=plt.axes([.775,.7,.175,.1])
saveModelButton=Button(ax3,'Save Model')
saveModelButton.on_clicked(saveModel)
# add vertex

plt.show()
