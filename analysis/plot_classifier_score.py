## save classification scores
np.save('FP', FP)
np.save('TP', TP)
np.save('PRECISION', PRECISION)
np.save('RECALL', RECALL)


##

import matplotlib
font = {'size'   : 18}
matplotlib.rc('font', **font)


plt.plot(FP, TP, '--o')
plt.xlabel('False positive')
plt.ylabel('True positive')
plt.show()

##
plt.plot(RECALL, PRECISION, '--o')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.show()

## ROC
data_dir = '/home/junyic/Work/Courses/4th_year/DataSci/final/detection_evaluation/'
which_data = 'DataII'

FP_gray = np.load(data_dir + 'gray_scale/' + which_data + '/FP.npy')
TP_gray = np.load(data_dir + 'gray_scale/' + which_data + '/TP.npy')
FP_sesi = np.load(data_dir + 'sesmic_scale/' + which_data + '/FP.npy')
TP_sesi = np.load(data_dir + 'sesmic_scale/' + which_data + '/TP.npy')

import matplotlib
font = {'size'   : 18}
matplotlib.rc('font', **font)


plt.plot(FP_gray, TP_gray, '--o', label='linear colormap')
plt.plot(FP_sesi, TP_sesi, '--o', label='nonlinear colormap')
plt.xlabel('False positive')
plt.ylabel('True positive')
plt.legend(loc='best')
plt.xlim([-1, 30])
plt.ylim([0, 1])
plt.show()

## precision recall
data_dir = '/home/junyic/Work/Courses/4th_year/DataSci/final/detection_evaluation/'
which_data = 'DataI'

PRECISION_gray = np.load(data_dir + 'gray_scale/' + which_data + '/PRECISION.npy')
RECALL_gray = np.load(data_dir + 'gray_scale/' + which_data + '/RECALL.npy')
PRECISION_sesi = np.load(data_dir + 'sesmic_scale/' + which_data + '/PRECISION.npy')
RECALL_sesi = np.load(data_dir + 'sesmic_scale/' + which_data + '/RECALL.npy')

import matplotlib
font = {'size'   : 18}
matplotlib.rc('font', **font)


plt.plot(RECALL_gray, PRECISION_gray, '--o', label='linear colormap')
plt.plot(RECALL_sesi, PRECISION_sesi, '--o', label='nonlinear colormap')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.legend(loc='best')
#plt.xlim([-1, 30])
plt.ylim([0, 1.1])
plt.show()
