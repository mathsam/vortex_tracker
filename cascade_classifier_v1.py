import cv2
import os
import scipy.io
import scipy.ndimage.interpolation
from matplotlib import cm
import sys
sys.path.append('/home/junyic/Work/Courses/4th_year/DataSci/final/src')
import vortex_filter


f = scipy.io.netcdf_file('/home/junyic/Work/Courses/4th_year/DataSci/final/PV_anomaly.nc', mode='r', mmap=True)
PV = f.variables['PV_anomaly']

CUTOFF = 400.
ZOOM_FACTOR = 3
image_width = PV.shape[3]*ZOOM_FACTOR
image_height = PV.shape[2]*ZOOM_FACTOR

def highlight_extremes(cutoff, in_field, bytes):
    field = in_field.copy()
    field = np.abs(field)
    max_val = np.max(field.flatten())
    field = (field-cutoff)/(max_val-cutoff)
    field[np.abs(in_field)<cutoff] = 0.5
    if bytes:
        field = np.uint8(field*255)
    return field

def highlight_local_extremes(in_field, cutoff_ratio, size=40):
    import scipy.ndimage.filters
    out_field = abs(in_field - np.mean(in_field.flatten()))
    out_field2 = out_field**2
    out_field2 = scipy.ndimage.filters.uniform_filter(out_field2, size=size, mode='wrap')
    out_field_std = np.sqrt(out_field2)
    out_field[out_field < cutoff_ratio*out_field_std] = cutoff_ratio*out_field_std[out_field < cutoff_ratio*out_field_std]
    return out_field
    

fourcc = cv2.VideoWriter_fourcc('P','I','M','1')
video = cv2.VideoWriter('./HAR_vortex_track.avi', fourcc, 20, (image_width, image_height))


eval_center = lambda x: (x[0] + x[2]/2, x[1] + x[3]/2)
vor_centers = []
valid_vor_centers = []

line_num = 0
for indx, i in enumerate(range(0, 1)):
    print i
    PV_slice = PV[i,0,...]
    PV_hires = scipy.ndimage.interpolation.zoom(PV_slice, ZOOM_FACTOR, mode='wrap')
    gray = vortex_filter.highlight_extremes(PV_hires, 400)
    #gray = 255 - gray
    #gray = PV_hires.copy()

    mapper = cm.ScalarMappable(cmap=cm.gray)
    PV_color = mapper.to_rgba(np.abs(PV_hires), alpha=None, bytes=True)

    mapper = cm.ScalarMappable(cmap=cm.gray)
    gray = mapper.to_rgba(gray, alpha=None, bytes=True)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    gray[gray==23] = 255
    
    vortex_cascade = cv2.CascadeClassifier('/home/junyic/Work/Courses/4th_year/DataSci/final/train_data/classifier1/cascade.xml')
    vortices = vortex_cascade.detectMultiScale(gray, 1.2, 3, minSize=(20,20), maxSize=(200, 200))
    centers = map(eval_center, vortices)
    vor_centers.append(centers)
    for (x,y,w,h) in vortices:
        img = cv2.rectangle(PV_color,(x,y),(x+w,y+h),(256,256,256),2)
    
    video.write(img[...,:3])
    
    f = open("vor.%d" %indx, mode='w')
    for (cx, cy) in centers:
        f.write(str(cx) + ' ' + str(cy))
        """
        for off_setx in range(-2, 3):
            for off_sety in range(-2, 3):
                f.write(' ' + str(gray[cy+off_sety, cx+off_setx]))
        f.write(' ' + str(line_num))
        line_num += 1
        """
        f.write('\n')
    f.close()

video.release()
#cv2.destroyAllWindows()

##
a = PIL.Image.fromarray(img)
a = a.convert('RGB')
a.show()
##
a.save('demo_dataII_gray.png')