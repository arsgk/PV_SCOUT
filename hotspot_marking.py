'''
Module for finding multiple bright spots in an image
written by a.gourras, l.gergidis
'''

# import the necessary packages
from imutils import contours
from skimage import measure
import numpy as np
import argparse
from statistics import mean
import imutils
import cv2
import os
import csv
import sys
from k_means import k_means
from shapes_detect import *
from characterization import characterize
from severity_state import severity_state


def hotspots (image,directory,basename,dT_PV):

    # load the image, convert it to grayscale, and blur it
    path=os.path.split(directory)[1]
    
    
    #kanw ena mask ts arxikhs eikonas gia na ftiaksw ta roi
    original = image.copy()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    blurred = cv2.GaussianBlur(gray, (1, 1), 0)
    
    # threshold the image to reveal light regions in the
    # blurred image
    thresh = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY)[1]
    
    #input k_means algorithm 
    k_means(thresh)
    
    
    # perform a series of erosions and dilations to remove
    # any small blobs of noise from the thresholded image
    
    thresh = cv2.erode(thresh, None, iterations=0)
    thresh = cv2.dilate(thresh, None, iterations=8)
    thresh_shape=thresh
    thresh_average=np.mean(thresh_shape)

    if thresh_average >100 :
        with open('Results.csv', mode='a') as csv_file:
            fieldnames = ['Image_Name', 'Number_Of_Hotspots','X_Coordinates','Y_Coordinates', 'Radius','Issue','Severity_Stage']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'Image_Name': basename, 'Number_Of_Hotspots': '-', 'X_Coordinates': '-','Y_Coordinates': '-','Radius':'-','Issue':'No issue detected','Severity_Stage':'-'} )
        #roi number gia na apo8hkeyontai
        #ROI_number += 1		
        #cv2.imwrite('ROI_{}.png'.format(ROI_number), ROI)
    
    else:      
    #issue=characterize(shape)
    

    # perform a connected component analysis on the thresholded
    # image, then initialize a mask to store only the "large"
    # components
        labels = measure.label(thresh, connectivity=2, background=0)
        mask = np.zeros(thresh.shape, dtype="uint8")
    
        

        # loop over the unique components
        for label in np.unique(labels):
            # if this is the background label, ignore it
            if label == 0:
                continue

            # otherwise, construct the label mask and count the
            # number of pixels 
            labelMask = np.zeros(thresh.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv2.countNonZero(labelMask)

            # if the number of pixels in the component is sufficiently
            # large, then add it to our mask of "large blobs"
            if numPixels > 300:
                mask = cv2.add(mask, labelMask)

        # find the contours in the mask, then sort them from left to
        # right
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        
        if not cnts :
            with open('Results.csv', mode='a') as csv_file:
                fieldnames = ['Image_Name', 'Number_Of_Hotspots','X_Coordinates','Y_Coordinates', 'Radius','Issue','Severity_Stage']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerow({'Image_Name': basename, 'Number_Of_Hotspots': '-', 'X_Coordinates': '-','Y_Coordinates': '-','Radius':'-','Issue':'No issue detected','Severity_Stage':'-'} )
                #roi number gia na apo8hkeyontai
                #ROI_number += 1		
                #cv2.imwrite('ROI_{}.png'.format(ROI_number), ROI)
                
        else:
            cnts = contours.sort_contours(cnts)[0]
            ROI_number= 0
            cX_list=[]
            cY_list=[]
            radius_list=[]
            # loop over the contours
            for (i, c) in enumerate(cnts):
                
                # draw the bright spot on the image
                (x, y, w, h) = cv2.boundingRect(c)
                ((cX, cY), radius) = cv2.minEnclosingCircle(c)
                # print(radius)
                

            
                
                if int(radius) <30 :
                
                    #edw vriskw ta roi gia na ta apo8hkeusw
                    ROI = original[y:y+h, x:x+w]
                    d=cv2.circle(image, (int(cX), int(cY)), int(radius),
                        (0, 0, 255), 3)
                        
                    cv2.putText(image, "#{}".format(i + 1), (x, y - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                    #write(path,i,cX,cY)
                    cX_list.append(cX)
                    cY_list.append(cY)
                    radius_list.append(radius)
                    shapes_list=[]
                    issue_list=[]
                    thresh_shape=thresh
                    shape_detect(thresh_shape,shapes_list) 
                    #print(shapes_list)
                    characterize(shapes_list,issue_list)
                    #print(issue_list)
                    #Initialize the list to store the severity state of each image
                    severity_state_list=[]
                    #Call the severity state module
                    #store the output to the initialized list
                    #return the full list 
                    severity_state(severity_state_list,shapes_list,dT_PV)
                    #print(severity_state_list)
                    
                    
            
            with open('Results.csv', mode='a') as csv_file:
                fieldnames = ['Image_Name', 'Number_Of_Hotspots','X_Coordinates','Y_Coordinates', 'Radius','Issue','Severity_Stage']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerow({'Image_Name': basename, 'Number_Of_Hotspots': i+1, 'X_Coordinates': cX_list,'Y_Coordinates': cY_list,'Radius':radius_list,'Issue':issue_list,'Severity_Stage':severity_state_list} )
                #roi number gia na apo8hkeyontai
                #ROI_number += 1		
                #cv2.imwrite('ROI_{}.png'.format(ROI_number), ROI)
                