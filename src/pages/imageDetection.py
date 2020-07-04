# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cv2
import numpy as np
import dlib
import math
import sys
import random as rand

def getPt(n1,n2,perc):
    diff = n2 - n1;
    return n1 + ( diff * perc )    

def drawLine(p1,p2,p3,frame):
    for i in np.linspace(0,1,30):
        xa = getPt( p1[0] , p2[0] , i )
        ya = getPt( p1[1] , p2[1] , i )
        xb = getPt( p2[0] , p3[0] , i )
        yb = getPt( p2[1] , p3[1] , i )
        x = int(getPt( xa , xb , i ))
        y = int(getPt( ya , yb , i ))
        cv2.circle(frame, (x,y), 1, (255,255,255), -1)

def calculateK(p1,p2):
    C = [0,0]
    lenAB = math.sqrt(math.pow(p1[0] - p2[0], 2.0) + math.pow(p1[1] - p2[1], 2.0))
    if lenAB > 0: 
        C[0] = int(p2[0] + (p2[0] - p1[0]) / lenAB * 70)
        C[1] = int(p2[1] + (p2[1] - p1[1]) / lenAB * 70)
        return tuple(C)
    else:
        return p2
    
def getIntersection(line1, line2):
    s1 = np.array(line1[0])
    e1 = np.array(line1[1])

    s2 = np.array(line2[0])
    e2 = np.array(line2[1])

    a1 = (s1[1] - e1[1]) / (s1[0] - e1[0])
    b1 = s1[1] - (a1 * s1[0])

    a2 = (s2[1] - e2[1]) / (s2[0] - e2[0])
    b2 = s2[1] - (a2 * s2[0])

    if abs(a1 - a2) < sys.float_info.epsilon:
        return False

    x = (b2 - b1) / (a1 - a2)
    y = a1 * x + b1
    return (int(x), int(y))

def main():
        
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    img = cv2.imread(sys.argv[1]) #'/home/arseni/.config/spyder-py3/braziltest.jpg'
    
    resize = 1
    width = int(img.shape[1] * resize)
    height = int(img.shape[0] * resize)
    dim = (width, height)
    # resize image
    frame = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 
    #mouthleft = 48
    #mouthright = 54
    #noseleft = 31
    #noseright = 35
    #lefteyeOuter = 36
    #lefteyeInner = 39
    #leftiris = 37
    #righteyeOuter = 45
    #righteyeInner = 42
    #rightiris = 42
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    
    for face in faces:
        landmarks = predictor(gray, face)
        
    dist = (landmarks.part(22).x - landmarks.part(21).x) #Distance between brows
    offSet = int(dist * 0.26315) #Value used in scaling brows
    
    topY = 0 # Decides top point of both brows
    if (landmarks.part(24).y-offSet/2) < (landmarks.part(19).y-offSet/2):
        topY = int(landmarks.part(24).y-offSet/2)
    else:
        topY = int(landmarks.part(19).y-offSet/2)
        
    topInnerY = 0 #Decides top point of both brows inner part
    if (landmarks.part(21).y) < (landmarks.part(22).y):
        topInnerY = int(landmarks.part(21).y)
    else:
        topInnerY = int(landmarks.part(22).y)
    
    leftTopPoint = getIntersection(((landmarks.part(32).x,landmarks.part(32).y), calculateK((landmarks.part(32).x,landmarks.part(32).y), (int((landmarks.part(37).x + landmarks.part(38).x)/2),int((landmarks.part(37).y + landmarks.part(38).y)/2)))),((landmarks.part(18).x,topY),(landmarks.part(20).x,topY)))
    rightTopPoint = getIntersection(((landmarks.part(34).x,landmarks.part(34).y), calculateK((landmarks.part(34).x,landmarks.part(34).y), (int((landmarks.part(44).x + landmarks.part(43).x)/2),int((landmarks.part(44).y + landmarks.part(43).y)/2)))),((landmarks.part(23).x,topY),(landmarks.part(25).x,topY)))
    rightBelowTop = (rightTopPoint[0],rightTopPoint[1]+int(1.5*offSet))
    leftBelowTop = (leftTopPoint[0],leftTopPoint[1]+int(1.5*offSet))
    
    farLeftPoint = getIntersection(((landmarks.part(31).x,landmarks.part(31).y), calculateK((landmarks.part(31).x,landmarks.part(31).y), (landmarks.part(36).x,landmarks.part(36).y))),((landmarks.part(17).x,landmarks.part(17).y),(landmarks.part(18).x,landmarks.part(18).y)))
    farRightPoint = getIntersection(((landmarks.part(34).x,landmarks.part(34).y), calculateK((landmarks.part(34).x,landmarks.part(34).y), (landmarks.part(45).x,landmarks.part(45).y))),((landmarks.part(25).x,landmarks.part(25).y),(landmarks.part(26).x,landmarks.part(26).y)))
    
    leftMiddlePoint = getIntersection(((landmarks.part(48).x,landmarks.part(48).y), calculateK((landmarks.part(48).x,landmarks.part(48).y), (landmarks.part(39).x + offSet,landmarks.part(39).y))),((landmarks.part(22).x,topInnerY),(landmarks.part(21).x,topInnerY)))
    rightMiddlePoint = getIntersection(((landmarks.part(54).x,landmarks.part(54).y), calculateK((landmarks.part(54).x,landmarks.part(54).y), (landmarks.part(42).x - offSet,landmarks.part(42).y))),((landmarks.part(22).x,topInnerY),(landmarks.part(21).x,topInnerY)))
    helperR = (rightMiddlePoint[0],rightMiddlePoint[1]+int(1.5*offSet)) #helper point for rightBelowMid, vertical offSet created point used for intersection
    rightBelowMid = getIntersection(((landmarks.part(54).x,landmarks.part(54).y), calculateK((landmarks.part(54).x,landmarks.part(54).y), (landmarks.part(42).x - offSet,landmarks.part(42).y))),(helperR, rightBelowTop))
    helperL = (leftMiddlePoint[0],leftMiddlePoint[1]+int(1.5*offSet)) #helper point for leftBelowMid, vertical offSet created point used for intersection
    leftBelowMid = getIntersection(((landmarks.part(48).x,landmarks.part(48).y), calculateK((landmarks.part(48).x,landmarks.part(48).y), (landmarks.part(39).x + offSet,landmarks.part(39).y))),(helperL, leftBelowTop))
    
    drawLine(rightMiddlePoint, (rightTopPoint[0]+int(1.5*offSet), rightTopPoint[1]-int(1.3*offSet)), (farRightPoint[0]-int(0.4*offSet), farRightPoint[1]+int(0.4*offSet)), frame)
    drawLine(rightBelowMid, (rightBelowTop[0]+int(1.5*offSet), rightBelowTop[1]-int(1.3*offSet)), (farRightPoint[0]-int(0.4*offSet), farRightPoint[1]+int(0.4*offSet)), frame)
    
    drawLine(leftMiddlePoint, (leftTopPoint[0]-int(1.5*offSet), leftTopPoint[1]-int(1.3*offSet)), (farLeftPoint[0]+int(0.4*offSet), farLeftPoint[1]+int(0.4*offSet)), frame)
    drawLine(leftBelowMid, (leftBelowTop[0]-int(1.5*offSet), leftBelowTop[1]-int(1.3*offSet)), (farLeftPoint[0]+int(0.4*offSet), farLeftPoint[1]+int(0.4*offSet)),frame)
    
    oH,oW = frame.shape[:2]
    image = np.dstack([frame, np.ones((oH,oW), dtype="uint8") * 255])
    lgo_img = cv2.imread('logo.png',cv2.IMREAD_UNCHANGED)
    sclW = 0.5
    sclH = 0.058
    w = int(oW * sclW)
    h = int(oH * sclH)
    dim = (w,h)
    lgo = cv2.resize(lgo_img, dim, interpolation = cv2.INTER_AREA)
    lH,lW = lgo.shape[:2]
    ovr = np.zeros((oH,oW,4), dtype="uint8")
    ovr[oH - lH - 10:oH - 10, oW - lW - 10:oW - 10] = lgo
    final = image.copy()
    final = cv2.addWeighted(ovr,0.5,final,1.0,0,final)
    suffix = str(rand.randint(1,100000000000))
    cv2.imwrite('savedData' + suffix + '.jpg', img)
    cv2.imwrite('output.jpg', final)
   # cv2.imshow("Combine Image",final) #Remove this and below when done with program
if __name__ == "__main__":
    main()