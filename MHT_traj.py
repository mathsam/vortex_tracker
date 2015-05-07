import pandas as pd

traj_pd = pd.read_csv('traj.csv', sep=' ', header=None)
traj = {}

for i in range(0, len(traj_pd)):
    id = int(traj_pd.iloc[i, 1])
    num_frame = int(traj_pd.iloc[i, 0])
    if traj.has_key(id):
        traj[id].append([num_frame, traj_pd.iloc[i, 2], traj_pd.iloc[i, 3]])
    else:
        traj[id] = [[num_frame, traj_pd.iloc[i, 2], traj_pd.iloc[i, 3]]]

colors_np = np.random.randint(0,255,(len(traj.keys()),3))
colors = {}
for i, id in enumerate(traj.keys()):
    colors[id] = colors_np[i]

##
import cv2
import os

f = scipy.io.netcdf_file('/home/junyic/Work/Courses/4th_year/DataSci/final/PV_anomaly1.nc', mode='r', mmap=True)
PV = f.variables['PV_anomaly']

ZOOM_FACTOR = 3
image_width = PV.shape[3]*ZOOM_FACTOR
image_height = PV.shape[2]*ZOOM_FACTOR


fourcc = cv2.VideoWriter_fourcc('P','I','M','1')
video = cv2.VideoWriter('./HAR_vortex_traj.avi', fourcc, 20, (image_width, image_height))


for indx, i in enumerate(range(400, 2000)):
    print i
    PV_slice = PV[i,0,...]
    PV_hires = scipy.ndimage.interpolation.zoom(PV_slice, 3, mode='wrap')
    
    mapper = cm.ScalarMappable(cmap=cm.Paired)
    img = mapper.to_rgba(PV_hires, alpha=None, bytes=True)

    for id in traj:
        for positions in traj[id]:
            if positions[0] > indx:
                continue
            if positions[0] < indx - 100:
                continue
            if len(traj[id])< 20:
                continue
            x = int(positions[1])
            y = int(positions[2])
            cv2.circle(img, (x,y), 4, colors[id].tolist(), -1)

    video.write(img[...,:3])


video.release()