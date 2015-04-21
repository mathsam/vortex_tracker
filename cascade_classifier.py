import cv2

vortex_cascade = cv2.CascadeClassifier('./cascade.xml')

img = cv2.imread('/home/junyic/Work/Courses/4th_year/DataSci/final/movie/500.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

vortices = vortex_cascade.detectMultiScale(gray, 1.3, 5)

for (x,y,w,h) in vortices:
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    
cv2.imshow('vortex', img)