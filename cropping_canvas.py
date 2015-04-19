try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
    
zone_codes = {}
motion_codes = {}
    
class CroppingCanvas(object):
    def __init__(self, parent=None, width=500, height=500):
        canvas = tk.Canvas(parent, width=width, height=height, bg='white')
        canvas.pack(expand=YES, fill=BOTH)
        canvas.bind('<Motion>',        self.motion_over)
        canvas.bind('<ButtonPress-1>', self.button_primary)
        canvas.bind('<B1-Motion>',     self.motion_primary)
        self.canvas = canvas
        self.crop_box_start = None #upper left corner positions
        self.crop_box_end = None #bottom right corner positions
        self.crop_box_obj = None
        
    def button_primary(self, event):
        position = (event.x, event.y)
        if self._get_zone_code(positions) == zone_codes['outside_crop']:
            self.canvas.delete(self.crop_box_obj)
            self.crop_box_start = position
            self.motion_primary_zonecode = zone_codes['outside_crop']
            return
        if self._get_zone_code(positions) == zone_codes['inside_crop']:
            self.motion_primary_zonecode = zone_codes['inside_crop']
            return
        if self._get_zone_code(positions) == zone_codes['upper_left']
            
        
        
    def motion_primary(self, event):


    def motion_over(self, event):
        
    def clear(self):
    
    def _get_zone_code(self, positions):
        """find out which zone the mouse pointer is at
        avialable names of zones are:
            outside_crop: outside of the cropping box
            inside_crop: inside of the cropping box
            upper_left: can be used to enlarge the cropping box
            upper_right:
            lower_left:
            lower_right:
        """