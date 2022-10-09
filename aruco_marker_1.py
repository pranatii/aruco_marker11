import cv2
from cv2 import aruco
import numpy as np
cap=cv2.VideoCapture(0)
src_img=cv2.imread(r'AR\ar_img\wallpaper-3d-16529-17067-hd-wallpapers.jpg')
# src_img=cv2.VideoCapture(r'AR\giphy.gif')
# cv2.imshow('qweqwe',src_img)

def find_aruco(img,markersize,totalmarkers,draw=True):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    key=getattr(aruco,f'DICT_{markersize}X{markersize}_{totalmarkers}')
    arucodict=aruco.Dictionary_get(key)
    arucoparam=aruco.DetectorParameters_create()
    bbox,ids,_=aruco.detectMarkers(gray,arucodict,parameters=arucoparam)
    # print(ids)
    if draw:
        aruco.drawDetectedMarkers(img,bbox)
    
    return bbox,ids

def image_masking(srcimg,destimg,dest_points):
    destimg_h,destimg_w=destimg.shape[:2]
    srcimg=cv2.resize(srcimg,(destimg_h,destimg_w))
    srcimg_h,srcimg_w=srcimg.shape[:2]
    
    mask=np.zeros((destimg_h,destimg_w),dtype=np.uint8)
    src_points=np.array([[0,0],[0,srcimg_w],[srcimg_w,srcimg_h],[srcimg_w,0]])
    H,_=cv2.findHomography(srcPoints=src_points,dstPoints=dest_points)
    wrap_img=cv2.warpPerspective(srcimg,H,(destimg_w,destimg_h))
    
    cv2.fillConvexPoly(destimg,dest_points,(255,255,255))
    wrap_img=wrap_img+destimg
    # cv2.imshow('wrap',wrap_img)
#     return wrap_img
    # results=cv2.bitwise_and(wrap_img,wrap_img,destimg,mask=mask)
    return results
# 
while True:
    ret,frame=cap.read()
    _,src_vid=src_img.read()
    frame=cv2.resize(frame,(700,600))
    bbox,ids=find_aruco(frame,6,100)
    if bbox:
        for id,corners in zip(ids,bbox):
            corners=corners.reshape(4,2)
            corners=corners.astype(int)
            frame=image_masking(src_img,frame,corners)
  
    cv2.imshow("1st project",frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
        
