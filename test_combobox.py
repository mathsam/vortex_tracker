from Tkinter import *
import ttk
from scipy.io import netcdf

class App:
    
    value_of_combo = 'X'
    
    
    def __init__(self, parent):
        self.parent = parent
        self.combo()
    
    def combobox_do(self,event):
    #print self.box.get()
        print self.combobox.get()
    def combo(self):
        filename = 'obs_lowreso.nc'
        f = netcdf.netcdf_file(filename,'r')
        keywords = f.variables.keys()
        self.combobox = ttk.Combobox(self.parent, textvariable=StringVar())
        self.combobox['values'] = keywords
        self.combobox.current(0)
        self.combobox.bind('<<ComboboxSelected>>',self.combobox_do)
        
        self.combobox.pack()
if __name__ == '__main__':
    root = Tk()
    app = App(root)
    root.mainloop()

def selectDataParameter(self):    # set layer No. and time and then draw the picture
    if self.filetype == 0:
        self.Combox(self, textvariable)
            self.layer_spinbox = Spinbox(self, from_=0, to=1)
            self.time_spinbox = Spinbox(self, from_=0, to=1999)
            #button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
            self.layer_spinbox.pack()
            self.time_spinbox.pack()
            Button(self, text='draw', command=self.drawPic).pack()

if self.filetype == 0:
    self.getNetCdfData()
        elif self.filetype == 1:
            print 'in development'
        else:
        print 'error'


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
        numbins = np.amax(self.imgMatr)
        nondimen_imgMatr = self.imgMatr/numbins
        plt.imshow(nondimen_imgMatr)
        plt.show()
#self.canvas.create_image(0,0,image=nondimen_imgMatr)