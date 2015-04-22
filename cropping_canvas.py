import numpy as np
from PIL import Image, ImageTk
import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
    
zone_codes = {}
zone_codes["inside"] = 0
zone_codes["outside"] = 1
zone_codes["upper_left"] = 2
zone_codes["upper_right"] = 3
zone_codes["lower_left"] = 4
zone_codes["lower_right"] = 5
offset = 25 
    
class CroppingCanvas(tk.Tk):
    def __init__(self, parent=None, width=500, height=500):
	tk.Tk.__init__(self)
        self.x = self.y = 0

        self.canvas = tk.Canvas(parent, width=width, height=height, bg='white')
        self.canvas.pack(side="top", fill="both", expand=True)
	self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.bind('<Motion>',        self.motion_over)
        self.canvas.bind('<ButtonPress-1>', self.button_primary)
        self.canvas.bind('<B1-Motion>',     self.motion_primary)
	'''
        if 'linux' in sys.platform:
            self.canvas.bind("<Button-4>", self.zoom_in)
            self.canvas.bind("<Button-5>", self.zoom_out)
	'''
	self.canvas.bind("<Button-4>", self.zoom1)
	self.canvas.bind("<Button-5>", self.zoom2)

        self.crop_box_obj = None
        self.crop_box_start_x = None	# upper left corner x
        self.crop_box_start_y = None	# upper left corner y
	self.crop_box_end_x = None	# bottom right corner x
        self.crop_box_end_y = None	# bottom right corner y

	self.scale = 1.0
        self.orig_im = Image.open('./Images/test1_src.png')
	self.im = None
	self.im_id = None
	#self._draw_image()
	self.redraw()

    '''
    def _draw_image(self):
        self.im = Image.open('./Images/test1_src.png')
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_im)
    '''

    def _draw_image(self):
        self.im = Image.open('./Images/test1_src.png')
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_im)

    def zoom_in(self, event):
        size = (event.width, event.height)
        resized = self.im.resize(size, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized)
        self.canvas.delete("IMG")
        self.canvas.create_image(0, 0, image=self.image, anchor=NW, tags="IMG")

    '''
    def zoom_in(self, event):
        self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
    '''

    def zoom_out(self, event):
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def zoom1(self,event):
        self.scale *= 2
        self.redraw(event.x, event.y)

    def zoom2(self,event):
        self.scale *= 0.5
        self.redraw(event.x, event.y)

    def on_wheel(self, event):
        d = event.delta
        print d
        if d < 0:
            amt=0.9
        else:
            amt=1.1
        self.canvas.scale("all", event.x, event.y, amt, amt)

    def redraw(self, x=0, y=0):
        if self.im_id: self.canvas.delete(self.im_id)
        iw, ih = self.orig_im.size
        # calculate crop rect
        cw, ch = iw / self.scale, ih / self.scale
        if cw > iw or ch > ih:
            cw = iw
            ch = ih
        # crop it
        _x = int(iw/2 - cw/2)
        _y = int(ih/2 - ch/2)
        tmp = self.orig_im.crop((_x, _y, _x + int(cw), _y + int(ch)))
        size = int(cw * self.scale), int(ch * self.scale)
        # draw
        self.im = ImageTk.PhotoImage(tmp.resize(size))
        self.im_id = self.canvas.create_image(x, y, image=self.im)
        #gc.collect()

    def button_primary(self, event):
        positions = (event.x, event.y)
        positions = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        
        # create rectangle if not yet exist
        if self.crop_box_obj is None:
            self.crop_box_start_x = event.x
	    self.crop_box_start_y = event.y
            self.crop_box_obj = self.canvas.create_rectangle(self.x, self.y, 1, 1, fill="black")
	    self.motion_primary_zonecode = zone_codes['outside']
	    self.event_positions = positions
            return 

        self.motion_primary_zonecode = self._get_zone_code(positions)
        #self.motion_primary_zonecode = 3
	self.event_positions = positions
	self.canvas.tag_raise(self.crop_box_obj)
        return
        
    def motion_primary(self, event):
        dX = event.x - self.event_positions[0]
        dY = event.y - self.event_positions[1]
        dX = self.canvas.canvasx(event.x) - self.event_positions[0]
        dY = self.canvas.canvasy(event.y) - self.event_positions[1]

        if self.motion_primary_zonecode == zone_codes['outside']:
            curX, curY = (event.x, event.y)
            curX, curY = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
	    self.crop_box_start_x = self.event_positions[0]
	    self.crop_box_start_y = self.event_positions[1]
	    
            # expand rectangle as you drag the mouse
            self.canvas.coords(self.crop_box_obj, self.crop_box_start_x, self.crop_box_start_y, curX, curY)
	    self.crop_box_end_x = curX
	    self.crop_box_end_y = curY
	    return

        if self.motion_primary_zonecode == zone_codes['inside']:
            self.crop_box_start_x += dX
            self.crop_box_start_y += dY
            self.crop_box_end_x += dX
            self.crop_box_end_y += dY
            self.canvas.coords(self.crop_box_obj, self.crop_box_start_x, self.crop_box_start_y,
                                                  self.crop_box_end_x, self.crop_box_end_y)
            self.event_positions = (event.x, event.y)
	    return

        if self.motion_primary_zonecode == zone_codes['upper_left']:
            #dX = event.x - self.event_positions[0]
            #dY = event.y - self.event_positions[1]
            self.crop_box_start_x += dX
            self.crop_box_start_y += dY
            self.canvas.coords(self.crop_box_obj, self.crop_box_start_x, self.crop_box_start_y,
                                                  self.crop_box_end_x, self.crop_box_end_y)
            self.event_positions = (event.x, event.y)
            return

        if self.motion_primary_zonecode == zone_codes['upper_right']:
            #dX = event.x - self.event_positions[0]
            #dY = event.y - self.event_positions[1]
            self.crop_box_start_y += dY
            self.crop_box_end_x += dX
            self.canvas.coords(self.crop_box_obj, self.crop_box_start_x, self.crop_box_start_y,
                                                  self.crop_box_end_x, self.crop_box_end_y)
            self.event_positions = (event.x, event.y)
            return

        if self.motion_primary_zonecode == zone_codes['lower_left']:
            #dX = event.x - self.event_positions[0]
            #dY = event.y - self.event_positions[1]
            self.crop_box_start_x += dX
            self.crop_box_end_y += dY
            self.canvas.coords(self.crop_box_obj, self.crop_box_start_x, self.crop_box_start_y,
                                                  self.crop_box_end_x, self.crop_box_end_y)
            self.event_positions = (event.x, event.y)
            return

        if self.motion_primary_zonecode == zone_codes['lower_right']:
            #dX = event.x - self.event_positions[0]
            #dY = event.y - self.event_positions[1]
            self.crop_box_end_x += dX
            self.crop_box_end_y += dY
            self.canvas.coords(self.crop_box_obj, self.crop_box_start_x, self.crop_box_start_y,
                                                  self.crop_box_end_x, self.crop_box_end_y)
            self.event_positions = (event.x, event.y)
            return

    def motion_over(self, event):
        positions = (event.x, event.y)
        positions = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        cur_zone = self._get_zone_code(positions)

        if cur_zone == zone_codes['outside']:
            self.canvas.config(cursor='left_ptr')

        if cur_zone == zone_codes['inside']:
            self.canvas.config(cursor='fleur')

        if cur_zone == zone_codes['upper_left']:
            self.canvas.config(cursor='top_left_corner')

        if cur_zone == zone_codes['upper_right']:
            self.canvas.config(cursor='top_right_corner')

        if cur_zone == zone_codes['lower_left']:
            self.canvas.config(cursor='bottom_left_corner')

        if cur_zone == zone_codes['lower_right']:
            self.canvas.config(cursor='bottom_right_corner')

    def clear(self):
        return

    def _get_zone_code(self, positions):
        """
	find out which zone the mouse pointer is at
        avialable names of zones are:
            inside: inside of the cropping box
            outside: outside of the cropping box
            upper_left: 
            upper_right:
            lower_left:
            lower_right:
        """

        ux = positions[0]
        uy = positions[1]
	upper_left_x = np.minimum(self.crop_box_start_x, self.crop_box_end_x)
	upper_left_y = np.minimum(self.crop_box_start_y, self.crop_box_end_y)
	lower_right_x = np.maximum(self.crop_box_start_x, self.crop_box_end_x)
	lower_right_y = np.maximum(self.crop_box_start_y, self.crop_box_end_y)
	self.crop_box_start_x = upper_left_x
	self.crop_box_start_y = upper_left_y
	self.crop_box_end_x = lower_right_x
	self.crop_box_end_y = lower_right_y

        if ux < upper_left_x or ux > lower_right_x or uy < upper_left_y or uy > lower_right_y:
            return zone_codes["outside"]

        if ux > upper_left_x+offset and ux < lower_right_x-offset and uy > upper_left_y+offset and uy < lower_right_y-offset:
            return zone_codes["inside"]

        if ux > upper_left_x and ux < upper_left_x+offset and uy > upper_left_y and uy < upper_left_y+offset:
            return zone_codes["upper_left"]

        if ux > lower_right_x-offset and ux < lower_right_x and uy > upper_left_y and uy < upper_left_y+offset:
            return zone_codes["upper_right"]

        if ux > upper_left_x and ux < upper_left_x+offset and uy > lower_right_y-offset and uy < lower_right_y:
            return zone_codes["lower_left"]

        if ux > lower_right_x-offset and ux < lower_right_x and uy > lower_right_y-offset and uy < lower_right_y:
            return zone_codes["lower_right"]
       
    def on_button_release(self, event):
        pass

    def save_button(self, event):
        pass

if __name__ == "__main__":
    app = CroppingCanvas()
    app.title('PyVortex: Python Program to find and track vortex')
    app.mainloop()
