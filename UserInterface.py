from Tkinter import *
from tkFileDialog import *
from scipy.io import netcdf
from matplotlib import cm
import PIL
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import ttk
import cropping_canvas

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
        self.canvas = cropping_canvas.CroppingCanvas(self)
        self.canvas.pack(side='bottom')
    #self.master.iconname('tkpython')
    
    def createWidgets(self):          # get all widgets
        self.makeMenuBar()
        #self.addExplanation()
        #self.makeCanvas()
        self.saveData()
    
    def makeMenuBar(self):            # get menubar
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
        self.fileMenu()
    
    def addExplanation(self):
        self.text = Text(self)
        self.text.insert(END, 'Please load your netcdf files or pictures')
        self.text.pack()
    
    def makeCanvas(self):             # get canvans
        self.canvas = cropping_canvas.Canvas(self)
        self.canvas.pack(side='bottom')
    
    
    
    def fileMenu(self):               # define the action of file menu
        pulldown = Menu(self.menubar)
        pulldown.add_command(label='Load',command=self.loadFiles)
        self.menubar.add_cascade(label='File', menu=pulldown)
    
    def loadFiles(self):              # load files and transfer from netCDF to picture
        self.filename = askopenfilename(filetypes=(('NetCDF file','*.nc'),
                                                   ('Picture file','*.png')))
        if os.path.splitext(self.filename)[1] == '.nc':
            self.filetype = 0
            self.getNetCdfData()
            #self.makeCanvas()
        elif os.path.splitext(self.filename)[1] == '.jpg' or '.jpeg' or '.png':
            self.filetype = 1
            self.getImgData()
            #self.makeCanvas()
        else:
            print 'error'

#f = netcdf.netcdf_file(filename,'r')
#self.dataMatr = f.variables['PV_anomaly']

    def getNetCdfData(self):
        f = netcdf.netcdf_file(self.filename,'r')
        keywords = f.variables.keys()
        self.keySelected = keywords[0]
        self.combobox = ttk.Combobox(self, textvariable=StringVar())
        self.combobox['values'] = keywords
        self.combobox.current(0)
        self.combobox.bind('<<ComboboxSelected>>',self.combobox_do)
        self.combobox.pack()
        self.dataMatr = f.variables[self.keySelected];
        self.time_spinbox = Spinbox(self, from_=0, to=self.dataMatr.shape[0])
        self.layer_spinbox = Spinbox(self, from_=0, to=self.dataMatr.shape[1])
        #button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
        self.layer_spinbox.pack()
        self.time_spinbox.pack()
        Button(self, text='draw', command=self.drawNetCDF).pack()
    
    def combobox_do(self,event):
        self.keySelected = self.combobox.get()

    def drawNetCDF(self):                # draw the diagram on canvas
        layer = self.layer_spinbox.get()
        time = self.time_spinbox.get()
        self.imgMatr = self.dataMatr[time, layer]
        mapper = cm.ScalarMappable(cmap=cm.hsv)
        image_array = np.uint8(255*mapper.to_rgba(self.imgMatr))
        image_to_disp = PIL.Image.fromarray(image_array)
        image_name = "time=%s, layer=%s" %(time, layer)
        self.canvas.update_image(image_to_disp, image_name)
            
    def getImgData(self):
        self.imgMatr = mpimg.imread(self.filename)
        numbins = np.amax(self.imgMatr)
        nondimen_imgMatr = self.imgMatr/numbins
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
