## prepare foregrounds train cases
import pandas as pd
posi_pd = pd.read_csv('/home/junyic/Work/Courses/4th_year/DataSci/final/PV_fullsamples.log', header=None, sep=',')

posi_eachtime = {}

for i in range(0, len(posi_pd)):
    t = int(posi_pd.iloc[i,0])
    if posi_eachtime.has_key(t):
        posi_eachtime[t].append((int(posi_pd.iloc[i, 2]),
                                 int(posi_pd.iloc[i, 3]),
                                 int(posi_pd.iloc[i, 4]),
                                 int(posi_pd.iloc[i, 5])))
    else:
        posi_eachtime[t] = [(int(posi_pd.iloc[i, 2]),
                              int(posi_pd.iloc[i, 3]),
                              int(posi_pd.iloc[i, 4]),
                              int(posi_pd.iloc[i, 5]))]
                              
##
import scipy.io
import scipy.ndimage.interpolation
import Image
import sys
sys.path.append('/home/junyic/Work/Courses/4th_year/DataSci/final/src')
import vortex_filter
from matplotlib import cm
#import vortex_filter
f = scipy.io.netcdf_file('/home/junyic/Work/Courses/4th_year/DataSci/final/PV_anomaly1.nc', mode='r', mmap=True)
PV = f.variables['PV_anomaly']

img_num = 72

for t in posi_eachtime.keys():
    PV_slice = PV[t,0,...]
    PV_imag = vortex_filter.array2imag(PV_slice, 3, vortex_filter.highlight_extremes, cm.seismic)
    for x0, y0, x1, y1 in posi_eachtime[t]:
        if x0 + 24 < x1 and y0 + 24 < y1:
            crop_imag = PV_imag.crop((x0-2, y0-2, x1-1, y1-1))
            crop_imag.save('%d.png' %img_num)
            img_num += 1