import Tkinter as tk
from PIL import Image, ImageTk

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
    
class CroppingCanvas(tk.Tk):
    def __init__(self, parent=None, width=500, height=500):
	tk.Tk.__init__(self)
        self.x = self.y = 0
        self.canvas = tk.Canvas(parent, width=width, height=height, bg='white')
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind('<Motion>',        self.motion_over)
        self.canvas.bind('<ButtonPress-1>', self.button_primary)
        self.canvas.bind('<B1-Motion>',     self.motion_primary)

        self.crop_box_obj = None

        self.crop_box_start_x = None #upper left corner x
        self.crop_box_start_y = None #upper left corner y
	self.crop_box_end_x = None #bottom right corner x
        self.crop_box_end_y = None #bottom right corner y

	self._draw_image()

    def _draw_image(self):
        self.im = Image.open('./Images/test1_src.png')
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_im)

    def button_primary(self, event):
        positions = (event.x, event.y)
        
        # create rectangle if not yet exist
        if self.crop_box_obj is None:
            self.crop_box_start_x = event.x
	    self.crop_box_start_y = event.y
            self.crop_box_obj = self.canvas.create_rectangle(self.x, self.y, 1, 1, fill="black")
	    self.motion_primary_zonecode = zone_codes['outside']
	    self.event_positions = positions
            return 

        #self.motion_primary_zonecode = self._get_zone_code(positions)
        self.motion_primary_zonecode = 0
	self.event_positions = positions
        return
        
    def motion_primary(self, event):
        if self.motion_primary_zonecode == zone_codes['outside']:
            curX, curY = (event.x, event.y)
	    self.crop_box_start_x = self.event_positions[0]
	    self.crop_box_start_y = self.event_positions[1]
	    
            # expand rectangle as you drag the mouse
            self.canvas.coords(self.crop_box_obj, self.crop_box_start_x, self.crop_box_start_y, curX, curY)
	    self.crop_box_end_x = curX
	    self.crop_box_end_y = curY
	    return

        if self.motion_primary_zonecode == zone_codes['inside']:
	    dX = event.x - self.event_positions[0]
	    dY = event.y - self.event_positions[1]
	    self.canvas.coords(self.crop_box_obj, self.crop_box_start_x + dX, self.crop_box_start_y + dY,
			                          self.crop_box_end_x + dX, self.crop_box_end_y + dY)
	    '''self.crop_box_start_x += dX
	    self.crop_box_start_y += dY
	    self.crop_box_end_x += dX
	    self.crop_box_end_y += dY'''
	    return

        if self.motion_primary_zonecode == zone_codes['upper_left']:
            return

    def motion_over(self, event):
        if event.x < 50 or event.x > 150 or event.y < 20 or event.y > 80:
            self.canvas.config(cursor='left_ptr')
        if event.x > 60 and event.x < 140 and event.y > 30 and event.y < 70:
            self.canvas.config(cursor='fleur')
        if event.x >= 50 and event.x <= 60 and event.y >=20 and event.y <=30:
            self.canvas.config(cursor='top_left_corner')

    def clear(self):
        return

    def _get_zone_code(self, positions):
        """find out which zone the mouse pointer is at
        avialable names of zones are:
            inside: inside of the cropping box
            outside: outside of the cropping box
            upper_left: can be used to enlarge the cropping box
            upper_right:
            lower_left:
            lower_right:
        """

        ux = positions[0]
        uy = positions[1]

        if uy > border_top-10 and uy < border_top+10:
            if ux > border_left-10 and ux < border_left+10: return 1
            if ux > border_left+10 and ux < border_right-10: return 2
            if ux > border_right-10 and ux < border_right+10: return 3
            if ux > border_right+10 and ux < border_right+30: return 10

        if uy > border_top+10 and uy < border_bottom-10:
            if ux > border_left-10 and ux < border_left+10: return 4
            if ux > border_left+10 and ux < border_right-10: return 5
            if ux > border_right-10 and ux < border_right+10: return 6

        if uy > border_bottom-10 and uy < border_bottom+10:
           if ux > border_left-10 and ux < border_left+10: return 7
           if ux > border_left+10 and ux < border_right-10: return 8
           if ux > border_right-10 and ux < border_right+10: return 9
       
    def on_button_release(self, event):
        pass

    def save_button(self, event):
        pass

if __name__ == "__main__":
    app = CroppingCanvas()
    app.mainloop()
