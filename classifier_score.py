## get test cases
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

## test detection
import cv2
import os
import scipy.io
import scipy.ndimage.interpolation
from matplotlib import cm
import sys
sys.path.append('/home/junyic/Work/Courses/4th_year/DataSci/final/src')
import vortex_filter
import PIL.Image
import time

t1 = time.time()

thresholds = np.array([1.001, 1.002, 1.003, 1.005, 1.01, 1.02, 1.03, 1.05, 1.1, 1.2, 1.3])
#thresholds = np.array([1.001])
FP = np.zeros(len(thresholds))
TP = np.zeros(len(thresholds))
PRECISION = np.zeros(len(thresholds))
RECALL = np.zeros(len(thresholds))


f = scipy.io.netcdf_file('/home/junyic/Work/Courses/4th_year/DataSci/final/PV_anomaly.nc', mode='r', mmap=True)
PV = f.variables['PV_anomaly']
CUTOFF = 400.
ZOOM_FACTOR = 3
image_width = PV.shape[3]*ZOOM_FACTOR
image_height = PV.shape[2]*ZOOM_FACTOR


def score_classification(results, truth):
    score = []
    for i, i_positions in enumerate(results):
        true_or_false = False
        center_x = i_positions[0] + 0.5*i_positions[2]
        center_y = i_positions[1] + 0.5*i_positions[3]
        for i_truth in truth:
            if i_truth[0] <= center_x <= i_truth[2] and i_truth[1] <= center_y <= i_truth[3]:
                score.append(True)
                true_or_false = True
                continue
        if true_or_false == False:
            score.append(False)
    return score


for run_i, thre in enumerate(thresholds):
    vor_centers = []
    valid_vor_centers = []
    classi_results = []
    total_vortex_num = 0
    for indx, i in enumerate(posi_eachtime.keys()):
        print i
        PV_slice = PV[i,0,...]
        PV_hires = scipy.ndimage.interpolation.zoom(PV_slice, ZOOM_FACTOR, mode='wrap')
        gray = vortex_filter.highlight_extremes(PV_hires)
        #gray = 255 - gray
    
        mapper = cm.ScalarMappable(cmap=cm.Paired)
        PV_color = mapper.to_rgba(PV_hires, alpha=None, bytes=True)
    
        mapper = cm.ScalarMappable(cmap=cm.seismic)
        gray = mapper.to_rgba(gray, alpha=None, bytes=True)
        gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
        gray[gray==23] = 255
        
        vortex_cascade = cv2.CascadeClassifier('/home/junyic/Work/Courses/4th_year/DataSci/final/train_seismic/HAR_smallbg/cascade.xml')
        vortices = vortex_cascade.detectMultiScale(gray, thre, 3, minSize=(15,15), maxSize=(120, 120))
        centers = map(eval_center, vortices)
        vor_centers.append(centers)
        
        classi_results += score_classification(vortices, posi_eachtime[i])
        total_vortex_num += len(posi_eachtime[i])
    classi_results = np.array(classi_results)

    TP[run_i] = np.sum(classi_results)/float(total_vortex_num)
    FP[run_i] = np.sum(~classi_results)/float(total_vortex_num)
    RECALL[run_i] = np.sum(classi_results)/float(total_vortex_num)
    PRECISION[run_i] = np.sum(classi_results)/float(len(classi_results))
    
print "run time is %f" %(time.time()-t1)