import cv2
import numpy as np

ball = []
cap = cv2.VideoCapture("C:/Users/rishi/humanoid/archery.mp4")   
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))               
out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('m','p','4','v'),30,(frame_width,frame_height))
while cap.isOpened():
  ret, frame = cap.read()
  if ret is False:
    break
  #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  blurred = cv2.GaussianBlur(frame, (5, 5), 0)
  hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
  upper_blue = np.array([139,255,255])
  lower_blue = np.array([98,50,50])
  upper_yellow = np.array([42,255,255])
  lower_yellow = np.array([30,187,206])
  upper_red = np.array([178,255,255])
  lower_red  = np.array([168,100,100])
  mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
  mask_yellow = cv2.inRange(hsv,lower_yellow,upper_yellow)
  mask_red = cv2.inRange(hsv,lower_red,upper_red)

  #mask = cv2.bitwise_or(mask_blue,mask_yellow,mask_red)  
  mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
  mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
  mask_red = cv2.inRange(hsv, lower_red, upper_red)
  mask = cv2.bitwise_or(mask_blue, mask_yellow, mask_red)
  mask = cv2.erode(mask, None, iterations=16)
  mask = cv2.dilate(mask, None, iterations=16)
  edges = cv2.Canny(mask, 150, 450)
  
  (contours,_)=cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

  center = None

  if len(contours)>0:
    c = max(contours, key=cv2.contourArea)
    ((x,y),radius) = cv2.minEnclosingCircle(c)
    try:
      cv2.circle(frame, (int(x), int(y)),10, (255,0,0),-1)
      ball.append((int(x), int(y)))
    except:
      pass
    if len(ball)>2:
      for i in range(1,len(ball)):
        cv2.line(frame, ball[i-1], ball[i],(0,0,255),5)
    cv2.imshow('',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # wait for 1 ms and break if 'q' is pressed
      break
    out.write(frame)

out.release()