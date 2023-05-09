#######################################################################################
#              THIS MODULE READS THERMAL IMAGES AND SCALES THEM 		              #
#       >  READ .TIFF IMAGES 			                                              #
#       >  SCALES IMAGES FOR POST PROCESSING                                          #
#       >  MAKES THES VISIBLE 	 	                                                  #
#           				                                                          #
#           >  WRITTEN BY A.GKOURAS, L.GERGIDIS					                      # 
#           						                                                  #
#	          *****************IMPORTANT*********************		                  #
#        IF IT FAILS TO RUN, CHECK DIRECTORIES AND IMPORT MODULES PROPERLY            #	
#######################################################################################
#######################################################################################
#										      #                                       #
#                                    CODE FOR PV_AUTO SCOUT	                          #
#										      #		                                  #                      
#                                     Flow chart                                      #
#       Reads multiple images from the correct path using the glob module             #
#                                                                                     #
#                                                                                     #
#               python .\image_processor.py --directory "*.*" --altitude 15           #
#                                                                                     #                             
#                                                                                     #
#                                                                                     #
#                                                                                     #
#######################################################################################


#import the necessery packages check README.TXT for further instructions
import numpy as np
import cv2 
import os
import os.path
import tifffile as tiff
import matplotlib.pyplot as plt 
import glob
import argparse
import time
from colormap import *
from hotspot_marking import hotspots
from temperature_conversion import temp_conversion


#Empy the previous Results.csv from the last inspection

file_path= "../Results.csv"
if os.path.exists(file_path):
    f = open("Results.csv", "w")
    f.truncate()
    f.close()

# construct the argument parse and parse the arguments to the next modules of the code

ap = argparse.ArgumentParser(description='Process command line arguments.')

#Directory of the images (string value)

ap.add_argument("-d", "--directory", help = "path to the image file")
 
#Altitude where the the UAV flight obtained the imagaes 

ap.add_argument("-r", "--altitude", type = int, help = "altitude of the selected images") 
args = vars(ap.parse_args())

#store the arguments into variables

#image directory 

directory=args["directory"]

#flight altitude 

altitude=args["altitude"]


# define the name of the directory to be created
#For the visible images
current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'Visible_images')

if not os.path.exists(final_directory):
   os.makedirs(final_directory)


#outpath directory (maybe optional)
'''
outpath="C:\\Users\\ArsGk\\Desktop\\PV_SCOUT\\try_1\\vis"
'''
'''
path="*.*"
image_list=glob.glob(path+'\\*.tiff') #assuming τif
'''

#Image Processor initializing depending on the altitude of the flight

if  altitude >=20 :

    print('\n \n#################### Image processor module initializing ######################')
    print('#################### Performing close insepction #############################')
    time.sleep(0.5)
    print('Path for the thermal images:',directory)
    print('####################')
    time.sleep(0.5)
    print('The altitude of the selected images is:',altitude,'meters')
    print('####################')
    time.sleep(0.5)
   
    print('image path and altitude succesufully stored')
    print('####################')
    
#Image Processor initializing depending on the altitude of the flight

if  altitude <=15 :

    print('\n \n#################### Image processor module initializing ######################')
    print('#################### Performing close insepction #############################')
    time.sleep(0.5)
    print('Path for the thermal images:',directory)
    print('####################')
    time.sleep(0.5)
    print('The altitude of the selected images is:',altitude,'meters')
    print('####################')
    time.sleep(0.5)
   
    print('image path and altitude succesufully stored')
    print('####################')


for n,file in enumerate (glob.glob(directory)):

    #Reading images in file
    
    img = cv2.imread(file,-1)
    path=os.path.split(directory)[1]
    basename = os.path.basename(file)
    
    #if all images are read 
    
    if img is None:
        print('####################')
        print('All images have been converted and scaled. See Results.csv for a detailed analysis')
        print('####################')
        break
    
    else:
        #printing the name of each image  
        print('reading image',os.path.basename(file))
    
    

    
    #initialize the temperature conversion module

    dT_PV=0
    
    #call the temperature conversion module

    dT_PV=temp_conversion(img,dT_PV)
    
    #print(dT_PV)
        
    #first scale to visible range (.tiff format) 
    
    img_scaled = cv2.normalize(img, dst=None, alpha=0, beta=65553, norm_type=cv2.NORM_MINMAX)
    
    #second scale to visible range (for .jpg format)  
    
    img_scaled2 = cv2.normalize(img_scaled, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX,dtype=cv2.CV_8U)
    
    #apply colormap to scaled and normalized images 
    
    #differemt colormap Inferno
    #image= cv2.applyColorMap(img_scaled2,cv2.COLORMAP_INFERNO)
    
    image = cv2.applyColorMap(img_scaled2,cv2.COLORMAP_BONE)
    
    #call colormap module
    
    colorMap = generateColourMap()
    
    #colorize image with the colorize module
    colorized_img = cv2.LUT(image, colorMap)  # Colorize the gray image with "false colors".
    
    
    #save the images with the colormap applied (maybe optional)
    
    cv2.imwrite(os.path.join(final_directory,'{}.jpg'.format(n)), colorized_img)
    
    #call marking module
    
    hotspots(image,directory,basename,dT_PV)


