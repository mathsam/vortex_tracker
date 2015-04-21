from Tkinter import *

from tkFileDialog import *

class Vortex(Frame):                  # class of the interface
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(expand=True, fill='both')
        self.createWidgets()
        self.master.title("Vortex Automatic Tracking System")
        self.layer = 1
        self.time = 0
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
        self.x_initial = 0
        self.y_initial = 0
        self.x_end = 0.1
        self.y_end = 0.1

    def selectDataParameter(self):    # set layer No. and time and then draw the picture
        Spinbox(self, from_=0, to=10, textvariable=self.layer).pack()
        Spinbox(self, from_=0, to=10, textvariable=self.time).pack()
        button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
        Button(self, text='draw', command=self.drawPic).pack(**button_opt)

    def fileMenu(self):               # define the action of file menu
        pulldown = Menu(self.menubar)
        pulldown.add_command(label='Load',command=self.loadFiles)
        self.menubar.add_cascade(label='File', underline=0, menu=pulldown)

    def loadFiles(self):              # load files and transfer from netCDF to picture
        self.filename = askopenfilename(**self.file_opt)
        


if __name__ == '__main__':
    root = Vortex()
    root.mainloop()
