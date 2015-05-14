import cv2
import os


vortex_cascade = cv2.CascadeClassifier('/home/junyic/Work/Courses/4th_year/DataSci/final/newtrain/LBP1/cascade.xml')

cap = cv2.VideoCapture('/home/junyic/Work/Courses/4th_year/DataSci/final/JupiterApproach_high.mp4')

fourcc = cv2.VideoWriter_fourcc('P','I','M','1')
video = cv2.VideoWriter('./jupiter_vortex_track.avi', fourcc, 20, (1200, 1080)) # (width, height)


#vortex_cascade = cv2.CascadeClassifier('/usr/lib/opencv/opencv/data/haarcascades/haarcascade_eye.xml')
i = 0
while(1):
    img = cap.read()[1]
    img = cv2.resize(img[:,200:800,:], (0,0), fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    print i
    i += 1
    #gray = img
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    
    vortices = vortex_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=1, maxSize=(200,200))
    for (x,y,w,h) in vortices:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    
    cv2.imshow('vortex', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    #plt.imshow(img, cmap='gray')
    #plt.show()
    video.write(img)
    
video.release()
#cv2.destroyAllWindows()
