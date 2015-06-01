import numpy as np
from PIL import Image, ImageTk, ImageDraw
import sys
import position_logger

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
OFFSET = 25 
ZOOM_FACTOR = 1.25
MAX_ZOOM_IN = 4.
MIN_ZOOM_OUT = 1.25
    
class CroppingCanvas(tk.Canvas):
    def __init__(self, parent=None, width=768, height=768):
        tk.Canvas.__init__(self, parent, width=width, height=height, bg='white')
        self.x = self.y = 0
        self.pack(side="top", fill="both", expand=True)
        self.config(scrollregion=self.bbox("all"))
        self.bind('<Motion>',        self.motion_over)
        self.bind('<ButtonPress-1>', self.button_primary)
        self.bind('<B1-Motion>',     self.motion_primary)

	'''
        if 'linux' in sys.platform:
            self.bind("<Button-4>", self.zoom_in)
            self.bind("<Button-5>", self.zoom_out)
	'''

        self.bind("<Button-4>", self.zoom_in)
        self.bind("<Button-5>", self.zoom_out)
        self.bind("<Double-Button-1>", self.log_cropbox_positions)

        self.crop_box_obj = None
        self.crop_box_start_x = None	# upper left corner x
        self.crop_box_start_y = None	# upper left corner y
        self.crop_box_end_x = None	# bottom right corner x
        self.crop_box_end_y = None	# bottom right corner y
        
        # Add the scrollbar
        self.scroll = tk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.config(yscrollcommand=self.scroll.set)

        self.scale = 1.0
        self.zoom_log = 0 # scale = ZOOM_FACTOR**zoom_log if no numerical error
        self.orig_im = Image.open('./Images/welcome.png').resize((width, height))
        self.im = None  
        self.im_id = None

        #current displayed imag is part of the original imag
        #and the corrsponding locations is stored in self.im_locs,
        #which is (upper_left_x, upper_left_y, lower_right_x, lower_right_y)
        #orig_im.size is (width, height)
        self.im_locs = (0, 0) + self.orig_im.size
        self.redraw()

    def update_image(self, imag_to_disp, imag_info):
        """update the image drawn on canvas
        Args:
                imag_to_disp: PIL Image object
                imag_info: a dict describing the image
                           desired format is {'field_name': 'PV_anomaly.nc.PV',
                                              'layer': 0,
                                              'time', 501}
        """
        self.orig_im = imag_to_disp.resize((self.winfo_width(), self.winfo_height()))
        self.imag_info = imag_info
        self.scale = 1.0
        self.zoom_log = 0 # scale = ZOOM_FACTOR**zoom_log if no numerical error
        self.im = None
        self.im_id = None
        self.im_locs = (0, 0) + self.orig_im.size
        self._clear_cropbox()
        self.redraw()

    def _clear_cropbox(self):
        self.delete('cropbox')
        self.crop_box_obj = None
        self.crop_box_start_x = None	# upper left corner x
        self.crop_box_start_y = None	# upper left corner y
        self.crop_box_end_x = None	# bottom right corner x
        self.crop_box_end_y = None	# bottom right corner y
       

    def log_cropbox_positions(self, event):
        """log the cropping box positions in the original (un-zoomed) image"""
        if self.crop_box_obj:
            upper_left = self._positions_in_origimg((self.crop_box_start_x, self.crop_box_start_y))
            lower_right = self._positions_in_origimg((self.crop_box_end_x, self.crop_box_end_y))
            position_logger.log_positions(self.imag_info, upper_left + lower_right) 
            draw_box = ImageDraw.Draw(self.orig_im)
            draw_box.rectangle([upper_left, lower_right], outline=None)
            self._clear_cropbox()
            self.redraw()

    def _locs_trans(self, s, mouse_positions, obj_positions):
        new_x = mouse_positions[0]*(1-s) + obj_positions[0]*s
        new_y = mouse_positions[1]*(1-s) + obj_positions[1]*s
        return new_x, new_y

    def zoom_in(self, event):
        if self.scale >= MAX_ZOOM_IN:
            return
        self.scale *= ZOOM_FACTOR
        self.zoom_log += 1

        s = 1./ZOOM_FACTOR
        if self.zoom_log == 0:
            # use the evaluated coordinate after zoom in as a correction
            # due to the rounding error. Use it below in crop_box
            self.crop_box_start_x, self.crop_box_start_y = self._positions_in_origimg((self.crop_box_start_x, self.crop_box_start_y))
            self.crop_box_end_x, self.crop_box_end_y = self._positions_in_origimg((self.crop_box_end_x, self.crop_box_end_y))
            self.im_locs = (0, 0) + self.orig_im.size
        else:
            # in current image, the zoom in area will be
            ch = self.im.height()
            cw = self.im.width()
            ulx, uly = self._locs_trans(s, (event.x, event.y), (0, 0))
            lrx, lry = self._locs_trans(s, (event.x, event.y), (cw, ch))
            self.im_locs = self._positions_in_origimg((ulx, uly)) + \
                       self._positions_in_origimg((lrx, lry))

        self.redraw()

        if self.crop_box_obj: 
            if self.zoom_log != 0:
                self.crop_box_start_x, self.crop_box_start_y = self._locs_trans(1/s, (event.x, event.y), (self.crop_box_start_x, self.crop_box_start_y))
                self.crop_box_end_x, self.crop_box_end_y = self._locs_trans(1/s, (event.x, event.y), (self.crop_box_end_x, self.crop_box_end_y))

            self.coords(self.crop_box_obj, self.crop_box_start_x, self.crop_box_start_y, self.crop_box_end_x, self.crop_box_end_y)
            self.tag_raise(self.crop_box_obj)
        return
        
    def zoom_out(self, event):
        orig_w, orig_h = self.orig_im.size
        # put the zoomed out image together with the original image, how big is the 
        # zoomed out canvas
        canvas_width = self.im_locs[2] - self.im_locs[0]
        canvas_height = self.im_locs[3] - self.im_locs[1]
        if canvas_width >= orig_w*MIN_ZOOM_OUT or canvas_height >= orig_h*MIN_ZOOM_OUT:
            return
        self.scale /= ZOOM_FACTOR
        self.zoom_log -= 1

        s = ZOOM_FACTOR
        if self.zoom_log == 0:
            self.crop_box_start_x, self.crop_box_start_y = self._positions_in_origimg((self.crop_box_start_x, self.crop_box_start_y))
            self.crop_box_end_x, self.crop_box_end_y = self._positions_in_origimg((self.crop_box_end_x, self.crop_box_end_y))
            self.im_locs = (0, 0) + self.orig_im.size  
        else:
            ch = self.im.height()
            cw = self.im.width()
            # in current image, the zoom in area will be
            ulx, uly = self._locs_trans(s, (event.x, event.y), (0, 0))
            lrx, lry = self._locs_trans(s, (event.x, event.y), (cw, ch))
            self.im_locs = self._positions_in_origimg((ulx, uly)) + \
                       self._positions_in_origimg((lrx, lry))

        self.redraw()

        if self.crop_box_obj: 
            if self.zoom_log != 0:
                self.crop_box_start_x, self.crop_box_start_y = self._locs_trans(1/s, (event.x, event.y), (self.crop_box_start_x, self.crop_box_start_y))
                self.crop_box_end_x, self.crop_box_end_y = self._locs_trans(1/s, (event.x, event.y), (self.crop_box_end_x, self.crop_box_end_y))

            self.coords(self.crop_box_obj, self.crop_box_start_x, self.crop_box_start_y, self.crop_box_end_x, self.crop_box_end_y)
            self.tag_raise(self.crop_box_obj)
        return


    def _positions_in_origimg(self, positions):
        if None in positions:
            return (None, None)
        x = float(positions[0])
        y = float(positions[1])
        cw, ch = self.orig_im.size
        cw_in_origimg = self.im_locs[2] - self.im_locs[0]
        ch_in_origimg = self.im_locs[3] - self.im_locs[1]
        px_in_orig = self.im_locs[0] + x/cw*cw_in_origimg
        py_in_orig = self.im_locs[1] + y/ch*ch_in_origimg
        return px_in_orig, py_in_orig


    def redraw(self):
        if self.im_id: self.delete(self.im_id)
        tmp = self.orig_im.crop(map(int, self.im_locs))
        # draw
        self.im = ImageTk.PhotoImage(tmp.resize(self.orig_im.size))
        self.im_id = self.create_image(0, 0, anchor=tk.NW, image=self.im)

    def button_primary(self, event):
        positions = (event.x, event.y)
        positions = (self.canvasx(event.x), self.canvasy(event.y))
        
        # create rectangle if not yet exist
        if self.crop_box_obj is None:
            self.crop_box_start_x = self.canvasx(event.x)
            self.crop_box_start_y = self.canvasy(event.y)
            self.crop_box_obj = self.create_rectangle(self.x, self.y, 1, 1, fill="", 
                                                      width=3.0, outline='black',
                                                      tags='cropbox')
            self.motion_primary_zonecode = zone_codes['outside']
            self.event_positions = positions
            return 

        self.motion_primary_zonecode = self._get_zone_code(positions)
        #self.motion_primary_zonecode = 3
        self.event_positions = positions
        self.tag_raise(self.crop_box_obj)
        return
        
    def motion_primary(self, event):
        dX = self.canvasx(event.x) - self.event_positions[0]
        dY = self.canvasy(event.y) - self.event_positions[1]

        if self.motion_primary_zonecode == zone_codes['outside']:
            curX, curY = (event.x, event.y)
            curX, curY = (self.canvasx(event.x), self.canvasy(event.y))
            self.crop_box_start_x = self.event_positions[0]
            self.crop_box_start_y = self.event_positions[1]
	    
            # expand rectangle as you drag the mouse
            self.coords(self.crop_box_obj, self.crop_box_start_x, self.crop_box_start_y, curX, curY)
            self.crop_box_end_x = curX
            self.crop_box_end_y = curY
            return

        if self.motion_primary_zonecode == zone_codes['inside']:
            self.crop_box_start_x += dX
            self.crop_box_start_y += dY
            self.crop_box_end_x += dX
            self.crop_box_end_y += dY
            self.coords(self.crop_box_obj, self.crop_box_start_x, self.crop_box_start_y,
                                                  self.crop_box_end_x, self.crop_box_end_y)
            self.event_positions = (event.x, event.y)
            return

        if self.motion_primary_zonecode == zone_codes['upper_left']:
            self.crop_box_start_x += dX
            self.crop_box_start_y += dY
            self.coords(self.crop_box_obj, self.crop_box_start_x, self.crop_box_start_y,
                                                  self.crop_box_end_x, self.crop_box_end_y)
            self.event_positions = (event.x, event.y)
            return

        if self.motion_primary_zonecode == zone_codes['upper_right']:
            self.crop_box_start_y += dY
            self.crop_box_end_x += dX
            self.coords(self.crop_box_obj, self.crop_box_start_x, self.crop_box_start_y,
                                                  self.crop_box_end_x, self.crop_box_end_y)
            self.event_positions = (event.x, event.y)
            return

        if self.motion_primary_zonecode == zone_codes['lower_left']:
            self.crop_box_start_x += dX
            self.crop_box_end_y += dY
            self.coords(self.crop_box_obj, self.crop_box_start_x, self.crop_box_start_y,
                                                  self.crop_box_end_x, self.crop_box_end_y)
            self.event_positions = (event.x, event.y)
            return

        if self.motion_primary_zonecode == zone_codes['lower_right']:
            self.crop_box_end_x += dX
            self.crop_box_end_y += dY
            self.coords(self.crop_box_obj, self.crop_box_start_x, self.crop_box_start_y,
                                                  self.crop_box_end_x, self.crop_box_end_y)
            self.event_positions = (event.x, event.y)
            return

    def motion_over(self, event):
        positions = (self.canvasx(event.x), self.canvasy(event.y))
        cur_zone = self._get_zone_code(positions)

        if cur_zone == zone_codes['outside']:
            self.config(cursor='left_ptr')

        if cur_zone == zone_codes['inside']:
            self.config(cursor='fleur')

        if cur_zone == zone_codes['upper_left']:
            self.config(cursor='top_left_corner')

        if cur_zone == zone_codes['upper_right']:
            self.config(cursor='top_right_corner')

        if cur_zone == zone_codes['lower_left']:
            self.config(cursor='bottom_left_corner')

        if cur_zone == zone_codes['lower_right']:
            self.config(cursor='bottom_right_corner')

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

        if ux > upper_left_x+OFFSET and ux < lower_right_x-OFFSET and uy > upper_left_y+OFFSET and uy < lower_right_y-OFFSET:
            return zone_codes["inside"]

        if ux > upper_left_x and ux < upper_left_x+OFFSET and uy > upper_left_y and uy < upper_left_y+OFFSET:
            return zone_codes["upper_left"]

        if ux > lower_right_x-OFFSET and ux < lower_right_x and uy > upper_left_y and uy < upper_left_y+OFFSET:
            return zone_codes["upper_right"]

        if ux > upper_left_x and ux < upper_left_x+OFFSET and uy > lower_right_y-OFFSET and uy < lower_right_y:
            return zone_codes["lower_left"]

        if ux > lower_right_x-OFFSET and ux < lower_right_x and uy > lower_right_y-OFFSET and uy < lower_right_y:
            return zone_codes["lower_right"]
       
    def on_button_release(self, event):
        pass

    def save_button(self, event):
        pass

if __name__ == "__main__":
    master = tk.Tk()
    app = CroppingCanvas(master)
    master.title('PyVortex: Python Program to find and track vortex')
    tk.mainloop()
