import cv2
import os


vortex_cascade = cv2.CascadeClassifier(os.getenv('HOME')+'/Dropbox/COS424_FinalProject/HAR_cascade.xml')

fourcc = cv2.VideoWriter_fourcc('P','I','M','1')
video = cv2.VideoWriter('./HAR_vortex_track.avi', fourcc, 20, (800, 600))

#vortex_cascade = cv2.CascadeClassifier('/usr/lib/opencv/opencv/data/haarcascades/haarcascade_eye.xml')

for i in range(501, 1300):
    img = cv2.imread(os.getenv('HOME') + '/Dropbox/COS424_FinalProject/movie1/%d.png' %i)
    print i
    #gray = img
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    vortices = vortex_cascade.detectMultiScale(gray, 1.003, 1, maxSize=(40,40))
    for (x,y,w,h) in vortices:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    
    cv2.imshow('vortex', img)
    #plt.imshow(img, cmap='gray')
    #plt.show()
    video.write(img)
    
video.release()
#cv2.destroyAllWindows()
