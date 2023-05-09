#######################################################################################
#              THIS MODULE READS THERMAL IMAGES AND CONVERTS THEM TO TEMPERATURE	  #
#              USING THE CONVERSION FACTOR FROM FLIR                                  #
#       >  READ .TIFF IMAGES 			                                              #
#       >  CONVERTS THE IMAGE TO TEMPERATURE                                          #
#       >  CALCULATES THE TEMPERATURE DIFFERENCE	 	                              #
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
#       Reads multiple thermal images from the image proccesor module                 #
#       and performs the pixel to temperature conversion from flir                    #
#                                                                                     #
#                                                                                     #
#                                                                                     #                             
#                                                                                     #
#                                                                                     #
#                                                                                     #
#######################################################################################





import tifffile as tiff
import numpy as np

def temp_conversion(img,dT_PV):

    #Read thermal image using the tifffile module
    #in order to convert to celsius degree 
    # Use the flir conversion ratio from the official website
    #link: https://flir.custhelp.com/app/answers/detail/a_id/3496/~/uas-image-pixel-to-temperature-conversion%3F
    image=img*0.04-273.15
    #temperature of healthy PV module
    healty_temp=25
    #get the minimum temperature value
    minElement = np.amin(image)
    #print('Minimum_Value = ',minElement)
    #get the maximum temperature value
    maxElement = np.amax(image)
    #print('Maximum_Value = ',maxElement)
    #Calculate the temperature difference
    dT_PV= maxElement-healty_temp
    return dT_PV
    #print('the temperature difference is :',dT_PV)

