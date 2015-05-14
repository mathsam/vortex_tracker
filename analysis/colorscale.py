import scipy.io
f = scipy.io.netcdf_file('PV_anomaly1.nc', mode='r', mmap=True)
PV = f.variables['PV_anomaly']
PV = PV[501:505,0,...]

##
PV_hist = plt.hist(PV.flatten(), 300)
plt.clf()
##
bins = np.array(PV_hist[1])
centers = 0.5*(bins[:-1] + bins[1:])
freq = np.array(PV_hist[0])
##
import matplotlib
font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : 20}

matplotlib.rc('font', **font)
plt.plot(centers, np.log(freq), linewidth=2)
plt.xlabel('vorticity')
plt.ylabel('log frequency')
#plt.savefig('/home/junyic/Work/Courses/4th_year/DataSci/final/analysis/vor_hist.png')
plt.show()

##
PV_trans = PV.copy()

def highlight_extremes(cutoff, in_field):
    field = in_field.copy()
    field = np.abs(field)
    max_val = np.max(field.flatten())
    field = (field-cutoff)/(max_val-cutoff)+1.
    field[np.abs(in_field)<cutoff] = 1.0
    field = np.log(field)
    return field
##
a = highlight_extremes(50, PV_trans)
plt.imshow(a[0, ...], cmap='gray', interpolation='none')
plt.show()
##
PV_trans[0, 70:80, 60:70]
PV_trans[0, 105:120, 65:85]