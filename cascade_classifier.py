import cv2
import os


vortex_cascade = cv2.CascadeClassifier(os.getenv('HOME')+'/Dropbox/COS424_FinalProject/HAR_cascade.xml')

fourcc = cv2.VideoWriter_fourcc('P','I','M','1')
video = cv2.VideoWriter('./HAR_vortex_track.avi', fourcc, 20, (800, 600))

#vortex_cascade = cv2.CascadeClassifier('/usr/lib/opencv/opencv/data/haarcascades/haarcascade_eye.xml')

eval_center = lambda x: (x[0] + x[2]/2, x[1] + x[3]/2)
vor_centers = []
valid_vor_centers = []

line_num = 0
for indx, i in enumerate(range(501, 1301)):
    img = cv2.imread(os.getenv('HOME') + '/Dropbox/COS424_FinalProject/movie1/%d.png' %i)
    print i
    #gray = img
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    vortices = vortex_cascade.detectMultiScale(gray, 1.01, 2, maxSize=(40,40))
    centers = map(eval_center, vortices)
    vor_centers.append(centers)
    for (x,y,w,h) in vortices:
        if 255 in gray[y:y+9,x:x+9]:
            continue
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    
    cv2.imshow('vortex', img)
    #plt.imshow(img, cmap='gray')
    #plt.show()
    video.write(img)
    
    valid_vor_centers.append([])
    f = open("vor.%d" %indx, mode='w')
    for (cx, cy) in centers:
        if 255 in gray[cy-4:cy+5,cx-4:cx+5]:
            continue
        valid_vor_centers[indx].append((cx, cy))
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
f = open("InDataFile", mode='w')
for i in valid_vor_centers:
    f.write(str(len(i)) + '\n')
f.close()
## save vor_centers as json file
import json
f = open('vor_centers.dat', mode='w')
json.dump(vor_centers, f)
