#-------------------------------------------------------------------#
################ Source Code written by Aaron Schultz ###############
##################### Co-Writer: Falko Kristen ######################
####### All Rights Reserved, Copyright (c) 2023 Aaron Schultz #######
#-------------------------------------------------------------------#

################ SCRIPT IMPORTS ################

## extrern library imports ##
from operator import mul
import datetime
import cv2
import numpy as np
from PIL import Image, ImageTk
import os

## intern module imports ##
from modules.memory_states import MemoryStates as ms




################ FUNCTIONS OF MAIN WNDOW ################

class FunctionsMainWindow:
    

    ## Switch Functions ##

    def changeFilter1Switch():
        if ms.filter1Switch == False:
            ms.filter1Switch = True
            ms.filter2Switch = False
            ms.filter3Switch = False
            ms.filter4Switch = False
        else: ms.filter1Switch = True
    
    def changeFilter2Switch():
        if ms.filter2Switch == False:
            ms.filter1Switch = False
            ms.filter2Switch = True
            ms.filter3Switch = False
            ms.filter4Switch = False
        else: ms.filter2Switch = True

    def changeFilter3Switch():
        if ms.filter3Switch == False:
            ms.filter1Switch = False
            ms.filter2Switch = False
            ms.filter3Switch = True
            ms.filter4Switch = False
        else: ms.filter3Switch = True

    def changeFilter4Switch():
        if ms.filter4Switch == False:
            ms.filter1Switch = False
            ms.filter2Switch = False
            ms.filter3Switch = False
            ms.filter4Switch = True
        else: ms.filter4Switch = True

    def changeScreenshotSwitch():
        if ms.screenshotSwitch == False:
            ms.screenshotSwitch = True
        else: ms.screenshotSwitch = False




    ############################# 
    ### FILTER FUNCTIONS FLIR ###
    #############################


    ## Filter 1 ##

    def filter1_Flir(img,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas):
        # sets current min and max values to canvas
        img_colorbar = (img-27315)/100.0 # milli kelvin to °C
        FunctionsMainWindow.set_detected_min_max(img_colorbar,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas)
        
        img = (img-27315)/100.0 # milli kelvin to °C
        cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX)
        
        output = np.copy(img)
        output = np.uint8(output)
        output = cv2.applyColorMap(output, ms.current_cv2_colormap)
        output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        return output


    ## Filter 2 ##

    def filter2_Flir(img,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas):
        
        # sets current min and max values to canvas
        img_colorbar = (img-27315)/100.0 # milli kelvin to °C
        FunctionsMainWindow.set_detected_min_max(img_colorbar,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas)
        
        # applies cmap with detection
        output = FunctionsMainWindow.detect_fever(img)
        return output
    

    ## Filter 3 ##

    def filter3_Flir(img,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas):
        
        # sets current min and max values to canvas
        img_colorbar = (img-27315)/100.0 # milli kelvin to °C
        FunctionsMainWindow.set_detected_min_max(img_colorbar,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas)
        
        img = (img-27315)/100.0 # milli kelvin to °C
        output = FunctionsMainWindow.target(img)
        return output
    

    ## Filter 4 ##

    def filter4_Flir(img):
        output = img.copy()
        return output
    




    ############################# 
    ### FILTER FUNCTIONS MLX ###
    #############################

    ## Filter 1 ##
    def filter1_MLX(img,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas):
        # sets current min and max values to canvas
        FunctionsMainWindow.set_detected_min_max(img,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas)
        
        output = img.copy()
        output = FunctionsMainWindow.Apply_Scanned_Heatmap(output, ms.blank_rgb, ms.width, ms.height, ms.heatMap_array)
        return output

    ## Filter 2 ##
    def filter2_MLX(img,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas):
        # sets current min and max values to canvas
        FunctionsMainWindow.set_detected_min_max(img,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas)
        
        img_cel = np.copy(img)
        img_raw = np.copy(img_cel)
        
        
        output = img.copy()
        heatmapped_img = FunctionsMainWindow.Apply_Scanned_Heatmap(output, ms.blank_rgb, ms.width, ms.height, ms.heatMap_array)
                    
        if (cv2.inRange(img_cel,0.1,37.4).any() == True):
            mask = cv2.inRange(img_cel,37.5,38.0)
            fever_type = ""

        if (cv2.inRange(img_cel,37.5,38.0).any() == True):
            mask = cv2.inRange(img_cel,37.5,38.0)
            fever_type = "SUBFEBRIL"
            
        if (cv2.inRange(img_cel,38.1,38.5).any() == True):
            mask = cv2.inRange(img_cel,38.1,38.5)
            fever_type = "LOW"
            
        if (cv2.inRange(img_cel,38.5,39.0).any() == True):
            mask = cv2.inRange(img_cel,38.5,39.0)
            fever_type = "MODERATE"

        if (cv2.inRange(img_cel,39.1,39.9).any() == True):
            mask = cv2.inRange(img_cel,39.1,39.9)
            fever_type = "HIGH"   
            
        if (cv2.inRange(img_cel,40.0,42.0).any() == True):
            mask = cv2.inRange(img_cel,40.0,42.0)
            fever_type = "VERY HIGH"
            
        kernal = np.ones((5,5),"uint8")
        mask = cv2.dilate(mask,kernal)
        contours,hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 30:
                x,y,w,h = cv2.boundingRect(contour)
                heatmapped_img = cv2.rectangle(heatmapped_img,(x,y),(x+w,y+h),(255,255,255),1)
                cv2.putText(heatmapped_img, f"{fever_type}", (x,y),cv2.FONT_HERSHEY_SIMPLEX,0.2,(255,255,255))

        return heatmapped_img
        

    ## Filter 3 ##

    def filter3_MLX(img):
        output = FunctionsMainWindow.target(img)
        return output


    ## Filter 4 ##

    def filter4_MLX(img):
        output = img.copy()
        return output




    ###################################### 
    ### FILTER FUNCTIONS NORMAL CAMERA ###
    ######################################


    ## Filter 1 ##

    def filter1_NormalCamera(img,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas):
        FunctionsMainWindow.set_detected_min_max(img,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas)
        output = img.copy()
        output = np.uint8(output)
        output = cv2.applyColorMap(output, ms.current_cv2_colormap)
        output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        return output


    ## Filter 2 ##

    def filter2_NormalCamera(img,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas):
        FunctionsMainWindow.set_detected_min_max(img,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas)
        output = img.copy()
        output = np.uint8(output)
        output = cv2.applyColorMap(output, ms.current_cv2_colormap)
        output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        return output


    ## Filter 3 ##

    def filter3_NormalCamera(img):
        output = FunctionsMainWindow.target_normalCamera(img)
        return output


    ## Filter 4 ##

    def filter4_NormalCamera(img):
        output = np.copy(img)
        output = cv2.Laplacian(output, cv2.CV_8U)
        return output
    



    ###################################### 
    ########## OPEN FUNCTIONS ############
    ######################################


    def detect_fever(img):
        global r,g,b
        global thickness
        
        img_celsius = (img-27315)/100.0 # milli kelvin to °C
        
        output = (img-27315)/100.0 # milli kelvin to °C
        cv2.normalize(output, output, 0, 255, cv2.NORM_MINMAX)
        output = np.uint8(output)
        output = cv2.applyColorMap(output, ms.current_cv2_colormap)
        output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        heatmapped_img = output

        if (cv2.inRange(img_celsius,0.1,37.4).any() == True):
            range_mask = cv2.inRange(img_celsius,0.1,37.4)
            r = 152
            g = 255
            b = 51
            thickness = 4
            fever_type = ""
        if (cv2.inRange(img_celsius,37.5,38.0).any() == True):
            range_mask = cv2.inRange(img_celsius,37.5,38.0)
            r = 255
            g = 178
            b = 102
            thickness = 1
            fever_type = "SUBFEBRIL"
            
        if (cv2.inRange(img_celsius,38.1,38.5).any() == True):
            range_mask = cv2.inRange(img_celsius,38.1,38.5)
            r = 255
            g = 128
            b = 0
            thickness = 1
            fever_type = "LOW"
            
        if (cv2.inRange(img_celsius,38.5,39.0).any() == True):
            range_mask = cv2.inRange(img_celsius,38.5,39.0)
            r = 255
            g = 102
            b = 102
            thickness = 1
            fever_type = "MODERATE"

        if (cv2.inRange(img_celsius,39.1,39.9).any() == True):
            range_mask = cv2.inRange(img_celsius,39.1,39.9)
            r = 255
            g = 51
            b = 51
            thickness = 1
            fever_type = "HIGH"   
            
        if (cv2.inRange(img_celsius,40.0,42.0).any() == True):
            range_mask = cv2.inRange(img_celsius,40.0,42.0)
            r = 204
            g = 0
            b = 0
            thickness = 1
            fever_type = "VERY HIGH"                    
        
        kernal = np.ones((5,5),"uint8")
        dilated_mask = cv2.dilate(range_mask,kernal)
        
        contours,hierarchy = cv2.findContours(dilated_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 30:
                x,y,w,h = cv2.boundingRect(contour)
                heatmapped_img = cv2.rectangle(heatmapped_img,(x,y),(x+w,y+h),(r,g,b),thickness)
                cv2.putText(heatmapped_img, f"{fever_type}", (x,y),cv2.FONT_HERSHEY_SIMPLEX,0.3,(r,g,b))
        return heatmapped_img




    def detect_fever_normal_camera(img):
        global r,g,b
        global thickness
        
        img = img.astype(float)
        img_celsius = img
    
        output = img
        output = np.uint8(output)
        output = cv2.applyColorMap(output, ms.current_cv2_colormap)
        output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        heatmapped_img = output

        

        if (cv2.inRange(img_celsius,0.0,36.0).any() == True):
            range_mask = cv2.inRange(img_celsius,0.0,36.0)
            r = 152
            g = 255
            b = 51
            thickness = 4
            fever_type = ""

        if (cv2.inRange(img_celsius,37.0,72.0).any() == True):
            range_mask = cv2.inRange(img_celsius,37.0,72.0)
            r = 255
            g = 178
            b = 102
            thickness = 1
            fever_type = "SUB"

        if (cv2.inRange(img_celsius,73.0,108.0).any() == True):
            range_mask = cv2.inRange(img_celsius,73.0,108.0)
            r = 255
            g = 128
            b = 0
            thickness = 1
            fever_type = "LOW"
            
        if (cv2.inRange(img_celsius,109.0,144.0).any() == True):
            range_mask = cv2.inRange(img_celsius,109.0,144.0)
            r = 255
            g = 102
            b = 102
            thickness = 1
            fever_type = "MOD"

        if (cv2.inRange(img_celsius,145.0,177.0).any() == True):
            range_mask = cv2.inRange(img_celsius,145.0,177.0)
            r = 255
            g = 51
            b = 51
            thickness = 1
            fever_type = "HIGH"   
            
        if (cv2.inRange(img_celsius,178.0,213.0).any() == True):
            range_mask = cv2.inRange(img_celsius,178.0,213.0)
            r = 204
            g = 0
            b = 0
            thickness = 1
            fever_type = "VERY HIGH"
            
        if (cv2.inRange(img_celsius,214.0,255.0).any() == True):
            range_mask = cv2.inRange(img_celsius,214.0,255.0)
            r = 255
            g = 0
            b = 127
            thickness = 1
            fever_type = "LETHAL"           
        
        kernal = np.ones((5,5),"uint8")
        dilated_mask = cv2.dilate(range_mask,kernal)
        
        contours,hierarchy = cv2.findContours(dilated_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 30:
                x,y,w,h = cv2.boundingRect(contour)
                heatmapped_img = cv2.rectangle(heatmapped_img,(x,y),(x+w,y+h),(r,g,b),thickness)
                cv2.putText(heatmapped_img, f"{fever_type}", (x,y),cv2.FONT_HERSHEY_SIMPLEX,2,(r,g,b))
        return heatmapped_img

    
    def target(img):

        dim = img.shape
        height=dim[0]
        width=dim[1]
        measPoint=img[int(height/2)][int(width/2)]
        crosshairs_coord = (int(width/2), int(height/2))
        value_coord = (0, height-(int(height/10)))

        crosshairs_color = (255,255,255)
        
        cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX)
        img = np.uint8(img)
        
        
        output = img.copy()
        output = cv2.applyColorMap(output, ms.current_cv2_colormap)
        output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

        cv2.circle(output,crosshairs_coord,ms.crosshairs_radius,crosshairs_color,ms.crosshairs_thickness)
        cv2.putText(output,f"{round(measPoint,1)}",value_coord,cv2.FONT_HERSHEY_PLAIN,ms.textsize_target,crosshairs_color,ms.textthickness_target)

        return output

    def target_normalCamera(img):

        dim = img.shape
        height=dim[0]
        width=dim[1]
        measPoint=img[int(height/2)][int(width/2)]
        crosshairs_coord = (int(width/2), int(height/2))
        value_coord = (0, height-(int(height/10)))

        crosshairs_color = (255,255,255)
            
        output = img.copy()
        output = cv2.applyColorMap(output, ms.current_cv2_colormap)
        output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

        cv2.circle(output,crosshairs_coord,ms.crosshairs_radius,crosshairs_color,ms.crosshairs_thickness)
        cv2.putText(output,f"{round(measPoint,1)}",value_coord,cv2.FONT_HERSHEY_PLAIN,ms.textsize_target,crosshairs_color,ms.textthickness_target)

        return output


    ## Heatmap Functions ##
    
    def Apply_Scanned_Heatmap(img, blank_rgb, width, height, heatMap_array):
        # (no clipping included)
        index_matrix = blank_rgb
        index_matrix = cv2.normalize(img, img, 0, len(heatMap_array), cv2.NORM_MINMAX)
        index_matrix = index_matrix.astype(int)

        for x in range(width):
            for y in range(height):
                blank_rgb[x][y] = heatMap_array[index_matrix[x][y]-1]

        blank_rgb = np.uint8(blank_rgb)
        return blank_rgb
    
    

    def Apply_Graymap(img, minimum,maximum):
        
        dim = img.shape
        width = dim[0]
        height = dim[1]
        mini = minimum
        maxi = maximum
        miniHeatMap = 0
        maxiHeatMap = 255
        rang = maxi - mini
        unit = int(255 / rang)
        
        for i in range(width):
            for j in range(height):                                   
                factor_for_position = (abs(img[i][j] - mini))
                if img[i][j] < mini:
                    img[i][j] = miniHeatMap
                    
                elif img[i][j] > maxi:
                    img[i][j] = maxiHeatMap
                
                elif img[i][j] > mini and img[i][j] < maxi:
                    img[i][j] = int(unit) * factor_for_position
        return img
    
    


    ## Zoom ##

    def minusZoom():
        # Zoom Limiter
        if ms.currentZoomFactor - ms.zoomStep <= ms.minZoomFactor:
            ms.currentZoomFactor = ms.minZoomFactor
        else: 
            ms.currentZoomFactor = ms.currentZoomFactor - ms.zoomStep

            #tried to make cropped Image reversed
            #ms.croppedX1 = ms.croppedX1 - ms.cropUnitX
            #ms.croppedX2 = ms.croppedX2 + ms.cropUnitX
            #ms.croppedY1 = ms.croppedY1 - ms.cropUnitY
            #ms.croppedY2 = ms.croppedY2 + ms.cropUnitY

        ms.currentRes = tuple(map(mul, ms.StreamResolution, (ms.currentZoomFactor, ms.currentZoomFactor)))
        ms.currentRes = tuple(map(lambda x: int(x), ms.currentRes))

        

    def plusZoom():
        
        # Zoom Limiter
        if ms.currentZoomFactor + ms.zoomStep >= ms.maxZoomFactor:
            ms.currentZoomFactor = ms.maxZoomFactor
        else: 
            ms.currentZoomFactor = ms.currentZoomFactor + ms.zoomStep

            ## tried to calculate difference to Stream Resolution to crop Image
            #ms.croppedX1 = int((ms.currentRes[0]-ms.StreamResolution[0]) / 2)
            #ms.croppedX2 = int(ms.currentRes[0] - ((ms.currentRes[0]-ms.StreamResolution[0]) / 2))
            #ms.croppedY1 = int((ms.currentRes[1]-ms.StreamResolution[1]) / 2)
            #ms.croppedY2 = int(ms.currentRes[1] - ((ms.currentRes[1]-ms.StreamResolution[1]) / 2))

        ms.currentRes = tuple(map(mul, ms.StreamResolution, (ms.currentZoomFactor, ms.currentZoomFactor)))
        ms.currentRes = tuple(map(lambda x: int(x), ms.currentRes))

        
        
    
    def updateZoomLabel():
        ms.currentZoomDisplay = str(ms.currentZoomFactor) + 'x'
        

    ## Screenshot ##

    def takeScreenshot(img):
        output = img.copy()
        #output = output[ms.croppedY1:ms.croppedY2, ms.croppedX1:ms.croppedX2]
        output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
        output_name = str(datetime.datetime.now().today()).replace(":", " ") + ".jpg"
        cv2.imwrite(os.path.join(ms.foto_save_path, f'{output_name}'), output)
        ms.screenshotSwitch = False

    def set_detected_min_max(img,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas):
        img = np.round(img,1)
        ms.minimum = np.min(img)
        ms.maximum = np.max(img)
        cmapCanvas.itemconfig(MaximumCanvas,text=str(ms.maximum))
        cmapCanvas.itemconfig(MinimumCanvas,text=str(ms.minimum))

        middle_temp = ms.minimum + (ms.maximum-ms.minimum) / 2
        middle_temp = np.round(middle_temp,1)
        cmapCanvas.itemconfig(MiddleCanvas,text=str(middle_temp))
        
    def set_new_cmap(cmapCanvas, CmapCanvas):
        canvas_image=ImageTk.PhotoImage(Image.open(ms.current_cmap).resize((30,ms.StreamResolution[1])))
        cmapCanvas.itemconfig(CmapCanvas,image=canvas_image)






    ## Other Functions ##

    def edgeFilterLaplace(img):
        output = np.copy(img)
        output = cv2.Laplacian(output, cv2.CV_64F)
        output = np.uint8(output)
        return output
    
    def edgeFilterCanny(img):
        output = np.copy(img)
        output = cv2.Canny(output, 100, 100)

        (B, G, R) = cv2.split(img)
        B_cny = cv2.Canny(B, 50, 200)
        G_cny = cv2.Canny(G, 50, 200)
        R_cny = cv2.Canny(R, 50, 200)
        edgeFilteredCannyRGB = cv2.merge([B_cny, G_cny, R_cny]) 
        return edgeFilteredCannyRGB

    def redFilter(img2):
        red_img = np.copy(img2)
        red_filter = (red_img[:, :, 0] > 150) & (red_img[:, :, 1] < 100) & (red_img[:, :, 2] < 110) #red filter (threshhold)
        red_img[:, :, 0] = red_img[:, :, 0] * red_filter #apllying filter
        red_img[:, :, 1] = red_img[:, :, 1] * red_filter #apllying filter
        red_img[:, :, 2] = red_img[:, :, 2] * red_filter #apllying filter
        return red_img

    def combineEdgeAndRed(imgCanny, imgRed):
        imgCanny = cv2.cvtColor(imgCanny, cv2.COLOR_BGR2GRAY)
        result = np.dstack((imgRed, imgCanny))
        return result
        
        
        """
        #imgCanny = imgCanny.convert('RGB')
        for x in imgRed:
            for y in imgRed:
                imgRed = Image.fromarray(imgRed[x,y])
                r, g, b = imgRed.getpixel((x, y))
                a = (r, g, b)
                if a != (0,0,0):
                    imgCanny[x, y] = imgRed[x,y]
                else:
                    imgCanny[x,y] = imgCanny[x,y]
                    
        return imgCanny
        """

    def testPrint():
        print('test')






    
    