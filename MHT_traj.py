colors_np = np.random.randint(0,255,(len(traj.keys()),3))
colors = {}
for i, id in enumerate(traj.keys()):
    colors[id] = colors_np[i]

##
import cv2
import os

fourcc = cv2.VideoWriter_fourcc('P','I','M','1')
video = cv2.VideoWriter('./HAR_vortex_track.avi', fourcc, 20, (800, 600))

for indx, i in enumerate(range(501, 1001)):
    img = cv2.imread(os.getenv('HOME') + '/Dropbox/COS424_FinalProject/movie1/%d.png' %i)
    print i
    #gray = img
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for id in traj:
        for positions in traj[id]:
            if positions[0] > indx:
                continue
            if len(traj[id])< 20:
                continue
            x = int(positions[1])
            y = int(positions[2])
            cv2.circle(img, (x,y), 5, colors[id].tolist(), -1)

    #cv2.imshow('vortex', img)
    #plt.imshow(img, cmap='gray')
    #plt.show()
    video.write(img)


video.release()