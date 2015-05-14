import os.path

def log_positions(imag_info, positions):
    """
    posotions is a tuple (start_x, start_y, end_x, end_y)
    """
    filename = imag_info["field_name"] + ".log"
    time = str(imag_info["time"])
    layer = str(imag_info["layer"])
    f = open(filename, 'a')
    f.write("%s, %s, %f, %f, %f, %f\n" %((time, layer) + positions))
