from Tkinter import *
from tkFileDialog import *
from scipy.io import netcdf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class Vortex(Frame):                  # class of the interface
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(expand=True, fill='both')
        self.createWidgets()
        self.x_initial = 0
        self.y_initial = 0
        self.x_end = 0.1
        self.y_end = 0.1
        self.master.title("Vortex Automatic Tracking System")
        #self.master.iconname('tkpython')

    def createWidgets(self):          # get all widgets
        self.makeMenuBar()
        self.makeCanvas()
        self.selectDataParameter()
        self.saveData()

    def makeMenuBar(self):            # get menubar
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
        self.fileMenu()

    def makeCanvas(self):             # get canvans
        canvas = Canvas(width=525, height=300, bg='white')
        canvas.pack(side='bottom')
        

    def selectDataParameter(self):    # set layer No. and time and then draw the picture
        self.layer_spinbox = Spinbox(self, from_=0, to=1)
        self.time_spinbox = Spinbox(self, from_=0, to=1999)
        #button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
        self.layer_spinbox.pack()
        self.time_spinbox.pack()
        Button(self, text='draw', command=self.drawPic).pack()

    def fileMenu(self):               # define the action of file menu
        pulldown = Menu(self.menubar)
        pulldown.add_command(label='Load',command=self.loadFiles)
        self.menubar.add_cascade(label='File', menu=pulldown)

    def loadFiles(self):              # load files and transfer from netCDF to picture
        filename = askopenfilename()
        f = netcdf.netcdf_file(filename,'r')
        self.dataMatr = f.variables['PV_anomaly']
        
    def drawPic(self):                # draw the diagram on canvas
        layer = self.layer_spinbox.get()
        time = self.time_spinbox.get()
        imgMatr = self.dataMatr[time, layer]
        numbins = np.amax(imgMatr)
        nondimen_imgMatr = imgMatr/numbins
        plt.imshow(nondimen_imgMatr)
        plt.show()

    def saveData(self):
        self.x_initial = 0
        self.y_initial = 0
        self.x_end = 0.1
        self.y_end = 0.1


if __name__ == '__main__':
    root = Vortex()
    root.mainloop()
