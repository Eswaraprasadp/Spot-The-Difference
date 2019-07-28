
# -*- coding: utf-8 -*-
"""
Author: ESWARA PRASAD P 
Domain: Signal Processing and ML
Functions: removeConcentric(), merge(), dist(), maxLength(), area(), combined(), led_on
Global variables: img, img1, img2, width_cutoff, rows, cols, diff, gray, thresh, contours, circles, limitArea, diffMatrix, answer
"""

import cv2
import numpy as np
import math
import serial
import time
img = cv2.imread("E:/Images/spot_the_difference 8.png")  #Read the image
rows = img.shape[1]  #No. of rows in image
cols = img.shape[0]   #No. of columns in image
width_cutoff = rows//2  #Centre of image width
if((rows-width_cutoff*2)==0): #Check if the no of rows os odd or even
 img1 = img[:, :width_cutoff] #ie. img1 is Left half of image
 img2 = img[:, width_cutoff:] #ie. img2 is right half of image
elif((rows-width_cutoff*2)==1):  #If the no. of rows is odd, then add 1 row extra to img1
  img1 = img[:, :width_cutoff+1]
  img2 = img[:, width_cutoff:]

rows = width_cutoff
diff = cv2.absdiff(img1, img2) 
gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 110, 220, cv2.THRESH_BINARY)  #Threshold the grayscale image for accuracy

contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #Find contours by thresh
circles = []
limitArea = 10
for c in contours:
    if(cv2.contourArea(c) >= limitArea):  #This allows only contours of area > 10 to be added to circles
        (x, y), radius = cv2.minEnclosingCircle(c)  #Gives the minimum enclosing circle of contour
        radius = int(radius)
        x = int(x)
        y = int(y)
        circles.append([x, y, radius])
#Function name: dist
#Input: Two Circles
#Output: returns distance between circles  
#Example: d = dist(circle1, circle2)      
def dist(a, b):
    return float(math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2))  #Distance between two circles: sqrt((x1-x2)**2+(y1-y2)**2)

#Function name: maxLength
#Input: Circle
#Output: returns radius of circle
#Example: r = maxLength(circle)   
def maxLength(d):  #Here maxDistance is radius
    return float(d[2])
  
#Function name: area
#Input: Circle
#Output: returns area of circle 
#Example:  a = area(circle) 
def area(g):
    return float(math.pi*(g[2]**2))

#Function name: combined
#Input: Two Circles
#Output: returns combined circle of two circles 
#Example: circle3 = combined(circle1, circle2)
def combined(c1, c2):  #Combined circle of two circles: Centre is geometrical centre of centres and radius is (sum of their radii + distance between them)/2
    return [(c1[0]+c2[0])/2, (c1[1]+c2[1])/2, (dist(c1, c2) + maxLength(c1) + maxLength(c2))/2]

#Function name: removeConcentric
#Input: Circle
#Output: Removes the smaller circle of concentric circles in a list of circles
#Example: circles = removeConcentric(circles) 
def removeConcentric(circles):  #To remove concentric circles
  circlesNew = [] 
  deleted = []
  for n in range(len(circles)):
    for m in range(n+1, len(circles)):  #To iterate through pairs of circles
        if(dist(circles[n], circles[m]) <= 1.1*maxLength(circles[n])): #If the distance between the circles relative to any of the two circles' radius less then delete the smaller one
            if(circles[m] not in deleted and area(circles[n]) >= area(circles[m])):
              deleted.append(circles[m])  #Here we store the deleted ones in list deleted
              continue
            elif(circles[n] not in deleted and area(circles[n]) < area(circles[m])):
                deleted.append(circles[n])
                continue
        elif(dist(circles[n], circles[m]) <= 1.1*maxLength(circles[m])):
            if(circles[n] not in deleted and area(circles[n]) <= area(circles[m])):
              deleted.append(circles[n])
              continue
            elif(circles[m] not in deleted and area(circles[n]) > area(circles[m])):
                deleted.append(circles[m])
                continue
        elif(dist(circles[n], circles[m]) > 1.1*max(maxLength(circles[n]), maxLength(circles[m]))):
            break       
  for c in circles:
    if c not in deleted:
        circlesNew.append(c) #We add the circles present in list circles and not in deleted
  return circlesNew

#Function name: merge
#Input: Circle
#Output: Merges two circles if they are close enough  in a list of circles
#Example: circles = merge(circles) 
def merge(circlesNew): #The merge function was not used
  circlesFinal = []
  merged = []
  deletedFinal = []

  for n in range(len(circlesNew)):
     for m in range(n+1, len(circlesNew)):
        if(dist(circlesNew[n], circlesNew[m]) <= 2.3*maxLength(circlesNew[n]) or dist(circlesNew[n], circlesNew[m]) <= 2.3*maxLength(circlesNew[m])):
            if(combined(circlesNew[m], circlesNew[n]) not in merged):
              merged.append(combined(circlesNew[m], circlesNew[n]))
              deletedFinal.append(circlesNew[n])
              deletedFinal.append(circlesNew[m])       
            
        elif(dist(circlesNew[n], circlesNew[m]) > 2.3*max(maxLength(circlesNew[n]), maxLength(circlesNew[m]))):
            if(circlesNew[n] not in merged):
                merged.append(circlesNew[n])
            if(circlesNew[m] not in circlesFinal):
                merged.append(circlesNew[m])   

  for c in merged:
    if c not in deletedFinal:
        circlesFinal.append(c)
  return circlesFinal

circles = removeConcentric(circles) #First remove concentric circles

diffMatrix = [] 

for c in circles:
    diffMatrix.append([c[0], c[1]]) #We add five points of circle to diffMatrix. These points help us to find the parts where there differences
    diffMatrix.append([c[0] - c[2], c[1]])
    diffMatrix.append([c[0] + c[2], c[1]])
    diffMatrix.append([c[0], c[1] - c[2]])
    diffMatrix.append([c[0], c[1] + c[2]])
    cv2.circle(img1, (int(c[0]), int(c[1])), int(c[2]), (0, 0, 255), 2)  #Draw the final list circles of both img1 and img2
    cv2.circle(img2, (int(c[0]), int(c[1])), int(c[2]), (0, 0, 255), 2)  #Convert to integer values since only integers are allowed in openCV circles drawing function

answer = []
for i in range(3): 
    for j in range(3):
      for x, y in diffMatrix:        #To iterate x through one-third part of thresh_opening eg. if i=1 x iterates from 1/3 to 2/3 width of thresh_opening
            if(x > i*rows//3+5 and x < (i+1)*rows//3-5 and y > j*cols//3+5 and y < (j+1)*cols//3-5):      #Check whether [x, y] is non-black ie. if there is a difference in two images in [x, y]
              if(answer[-1] != [i, j] if len(answer) else True):      #If len(arr) is positive, it checks the previous element in arr and compares with the present value of [i, j]. If len(arr) is 0 then add [i, j] 
                answer.append([i, j])     #If len(arr) is 0 or postive and [i, j] is not already present then add [i, j] to arr
                break

print(answer) #Print the list of parts where there are differences 

if((rows-width_cutoff*2)==0):
 img[:, :width_cutoff] = img1  #Rejoin the img with img1 and img2. Now the circles will be present in both sides of img
 img[:, width_cutoff:] = img2
elif((rows-width_cutoff*2)==1):
    img[:, :width_cutoff+1] = img1
    img[:, width_cutoff:] = img2

arduinoData = serial.Serial('COM3', 9600)  #Open the serial port COM3 with baud rate:9600

#Function name: led_on
#Input: int
#Output: Switches on corresponding LED
#Example: led_on(2)
def led_on(i):
    if(i==1):
        arduinoData.write('1'.encode())  #Encode the corresponding integer and send to Arduino
    elif(i==2):
        arduinoData.write('2'.encode())
    elif(i==3):
        arduinoData.write('3'.encode())
    elif(i==4):
        arduinoData.write('4'.encode())
    elif(i==5):
        arduinoData.write('5'.encode())
    elif(i==6):
        arduinoData.write('6'.encode())
    elif(i==7):
        arduinoData.write('7'.encode())
    elif(i==8):
        arduinoData.write('8'.encode())
    elif(i==9):
        arduinoData.write('9'.encode())

for a, b in answer:
    n = 3*a + b + 1    #Find the LED number n by the coordinates of answer list eg. [1, 2] corresponds to LED no. 6 ie. the right middle 
    time.sleep(5)  #Wait for some time to access the serial port to avoid conflicts with Arduino IDE
    led_on(n)  #Switch on the LEDs corresponding to ones in anser list

cv2.imwrite("Image difference.jpg", img) #Final image withthe differences circled