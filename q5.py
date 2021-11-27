import cv2
import keyboard
import numpy as np

camera=cv2.VideoCapture(0)
camera.set(3,640)
camera.set(4,480)
mask=np.ones((21,21))/441
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640,480))
frame_rectangle=[]
count=0
count_white,count_black=0,0

while True:
    ret,frame=camera.read()
    if ret==False:
        break

    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    x,y=gray_frame.shape
    frame_rectangle=gray_frame[(y//2)-100:(y//2),x//2:(x//2)+100]
    for i in range(len(frame_rectangle)):
        for j in range(len(frame_rectangle[i])):
            if frame_rectangle[i,j]>200:
                count_white+=1
    for i in range(len(frame_rectangle)):
        for j in range(len(frame_rectangle[i])):
            if frame_rectangle[i,j]<100:
                count_black+=1
    
   
    border = cv2.copyMakeBorder(
    frame_rectangle,
    top=2,
    bottom=2,
    left=2,
    right=2,
    borderType=cv2.BORDER_CONSTANT,
    value=(0,0,0)
)   
    
    dst=cv2.filter2D(gray_frame,-1,mask )
    dst[y//2-104:(y//2),(x//2):(x//2)+104]=border[:,:]
    if count_white>=8000:
        cv2.putText(dst,'white',(10,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1,cv2.LINE_AA)
    elif count_black>=8000:
        cv2.putText(dst,'black',(10,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1,cv2.LINE_AA)
    else:
        cv2.putText(dst,'gray',(10,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1,cv2.LINE_AA)

    count_white,count_black=0,0

    cv2.imshow('result',dst)
    cv2.waitKey(10)
    if keyboard.is_pressed('q'):
        break

camera.release()

cv2.destroyAllWindows()