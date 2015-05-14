import scipy.io
import scipy.misc
from scipy.misc import toimage
import numpy as np


nc_file = '../../FinalProjectData/PV_anomaly.nc'

fh = scipy.io.netcdf_file(nc_file, mode='r', mmap=True)
var = fh.variables['PV_anomaly']
var_slice = var[-1,0,...]

## save some figures
save_dir = '../../FinalProjectData/'
for i in range(500, 2000, 1):
    img = scipy.misc.toimage(var[i,0,...], high=255, low=0)
    img.save(save_dir + str(i) + '.png')

##
img = scipy.misc.toimage(var_slice, high=255, low=0)
img = np.array(img.getdata(), dtype=np.uint8)
img.shape = var_slice.shape

