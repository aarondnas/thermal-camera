#-------------------------------------------------------------------#
################ Source Code written by Aaron Schultz ###############
##################### Co-Writer: Falko Kristen ######################
####### All Rights Reserved, Copyright (c) 2023 Aaron Schultz #######
#-------------------------------------------------------------------#

################ SCRIPT IMPORTS ################

## extrern library imports ##
import cv2
import platform
import pickle
import socket
import struct
import numpy as np
from subprocess import call
import time




################ GLOBAL MEMORY STATES ################

class MemoryStates:

    def heatmap_setup(current_cmap, maximum, minimum):

        ## Loading PNG file as Heat Map
        color_arr = cv2.imread(current_cmap)
        color_arr = cv2.cvtColor(color_arr, cv2.COLOR_BGR2RGB)

        ## Analyzing Heat Map PNG and storing in array
        cmap_dim = color_arr.shape
        cmap_height = cmap_dim[0]
        cmap_width = cmap_dim[1]
        counter = 0
        heatMap_array = []
        while counter < cmap_height:
            for i in range(cmap_height):
                for j in range(1):
                    r = color_arr[i][1][0]
                    g = color_arr[i][1][1]
                    b = color_arr[i][1][2]
                    rgb_val = (r,g,b)
                    heatMap_array.append(rgb_val)
                    counter +=1

        ## reverses Heat Map Image
        heatMap_array = heatMap_array[::-1]
        temp_range = maximum - minimum

        temp_unit_range = maximum - minimum
        temp_unit=int(len(heatMap_array)/temp_unit_range)

        return heatMap_array, temp_unit, temp_range




    ## Setup Platform and Sensor ##
    OS = str(platform.system())
    print('OS: ' + OS)


    if OS == 'Windows':
        try:
            cameraInputNumber = 10
            for i in reversed(range(cameraInputNumber+1)):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    cameraInputNumber = i
                    print("Camera Input found: ", cameraInputNumber)
                    Sensor = 'Normal_Camera'
                    break
        except: print('Normal Camera could not be set up on ' + OS)

    elif OS == 'Darwin':
        try:
            cameraInputNumber = 10
            for i in reversed(range(cameraInputNumber+1)):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    cameraInputNumber = i
                    print("Camera Input found: ", cameraInputNumber)
                    Sensor = 'Normal_Camera'
                    break
        except: print('Normal Camera could not be set up on macOS')
    
    elif OS == 'Linux':
        try:
            import board,busio #available only for Linux
            import adafruit_mlx90640 #available only for Linux
            i2c = busio.I2C(board.SCL, board.SDA, frequency=800000) # I2C Setup
            mlx = adafruit_mlx90640.MLX90640(i2c) # begin communication MLX90640 with I2C
            Sensor = 'MLX'
        except:
            Sensor = 'Error'
            print('MLX Sensor could not be found.')
        try:
            cameraInputNumber = 10
            for i in reversed(range(cameraInputNumber+1)):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    cameraInputNumber = i
                    print("Camera Input found: ", cameraInputNumber)
                    Sensor = 'Flir'
                    break
        except: print('Flir Sensor could not be set up on ' + OS)

    else: 
        print('No known operating system was detected')
        OS = 'Error'
        Sensor = 'Error'
    print('Sensor: ' + Sensor)




    ## Resolution Variables ##

    flirPureThermalCameraResolution = (160, 120)
    flirResizeFactor = 2.65
    flirPureThermalCameraResolutionResized = tuple(2.65 * i for i in flirPureThermalCameraResolution)
    flirPureThermalCameraResolutionResized = tuple(map(lambda x: int(x), flirPureThermalCameraResolutionResized))

    mlxCameraResolution = (24,32)

    if OS == 'Windows' or OS == 'Darwin':
        cap = cv2.VideoCapture(cameraInputNumber)
        ret, img = cap.read()
        cameraHeight, cameraWidth, channel = img.shape
        originalCameraResolution = (cameraWidth, cameraHeight)
    elif OS == 'Linux':
        if Sensor == 'MLX':
            originalCameraResolution = mlxCameraResolution
        elif Sensor == 'Flir':
            originalCameraResolution = flirPureThermalCameraResolutionResized
        else: originalCameraResolution = flirPureThermalCameraResolutionResized
    else: print('No Resolution could be set up.')

    raspberryPieDisplayResolution = (480, 320)
    raspberryPieDisplayResolutionWidth = raspberryPieDisplayResolution[0]
    raspberryPieDisplayResolutionHeight = raspberryPieDisplayResolution[1]

    StreamResolution = (424,318) # Sets Resolution of Video Stream in Label of the Frame
    currentRes = StreamResolution # necessary for zoom

    ## Zoom Variables ##
    minZoomFactor = 1.0
    maxZoomFactor = 2.0
    zoomStep = 0.25
    currentZoomFactor = minZoomFactor
    currentZoomDisplay = str(currentZoomFactor) + 'x'

    '''
    croppedX1 = 0
    croppedX2 = StreamResolution[0]
    croppedY1 = 0
    croppedY2 = StreamResolution[1]
    cropUnitX = 0
    cropUnitY = 0
    cropUnitX = int((StreamResolution[0]*zoomStep) / 2)
    cropUnitY = int((StreamResolution[1]*zoomStep) / 2)
    '''

    ## Switches ##
    screenshotSwitch = False

    filter1Switch = True
    filter2Switch = False
    filter3Switch = False
    filter4Switch = False

    ShutdownSwitch = False
    streamStopSwitch = False

    


    ## Icon and other Paths ##

    if OS == 'Windows' or OS == 'Darwin':

        #share
        back_button_path = './icons/back.png'

        #window main
        plus_button_path = './icons/plus.png'
        minus_button_path = './icons/minus.png'
        screenshot_button_path = './icons/camera.png'
        menu_button_path = './icons/menu.png'
        exit_button_path = './icons/close.png'
        
        #window menu
        filter_window_button_path = './icons/filter.png'
        foto_window_button_path ='./icons/galerie.png'
        settings_window_button_path = './icons/settings.png'
        
        #window filter
        filter1_button_path = './icons/heatmap.png'
        filter2_button_path = './icons/thermometer.png'
        filter3_button_path = './icons/target.png'
        filter4_button_path = './icons/question_mark.png'

        #window galery
        arrow_button_path = './icons/arrow.png'
        delete_button_path = './icons/delete.png'
        foto_save_path = './Snapshots'
    
    elif OS == 'Linux':
        
        #share
        back_button_path = '/home/teamthermo/Desktop/gesundheitstechnik_thermograph/icons/back.png'

        #window main
        plus_button_path = '/home/teamthermo/Desktop/gesundheitstechnik_thermograph/icons/plus.png'
        minus_button_path = '/home/teamthermo/Desktop/gesundheitstechnik_thermograph/icons/minus.png'
        screenshot_button_path = '/home/teamthermo/Desktop/gesundheitstechnik_thermograph/icons/camera.png'
        menu_button_path = '/home/teamthermo/Desktop/gesundheitstechnik_thermograph/icons/menu.png'
        exit_button_path = '/home/teamthermo/Desktop/gesundheitstechnik_thermograph/icons/close.png'
        
        #window menu
        filter_window_button_path = '/home/teamthermo/Desktop/gesundheitstechnik_thermograph/icons/filter.png'
        foto_window_button_path ='/home/teamthermo/Desktop/gesundheitstechnik_thermograph/icons/galerie.png'
        settings_window_button_path = '/home/teamthermo/Desktop/gesundheitstechnik_thermograph/icons/settings.png'

        #window filter
        filter1_button_path = '/home/teamthermo/Desktop/gesundheitstechnik_thermograph/icons/heatmap.png'
        filter2_button_path = '/home/teamthermo/Desktop/gesundheitstechnik_thermograph/icons/thermometer.png'
        filter3_button_path = '/home/teamthermo/Desktop/gesundheitstechnik_thermograph/icons/target.png'
        filter4_button_path = '/home/teamthermo/Desktop/gesundheitstechnik_thermograph/icons/question_mark.png'

        #window galery
        arrow_button_path = '/home/teamthermo/Desktop/gesundheitstechnik_thermograph/icons/arrow.png'
        delete_button_path = '/home/teamthermo/Desktop/gesundheitstechnik_thermograph/icons/delete.png'
        foto_save_path = '/home/teamthermo/Desktop/gesundheitstechnik_thermograph/Snapshots'
    



    ## Heatmaps ##
    preselect_turbo = True
    selected_cmap = 1
    current_cmap = ''

    if OS == 'Windows' or OS == 'Darwin':
        if selected_cmap == 0:
            current_cmap = './assets/cmap1.png'
        if selected_cmap == 1:
            current_cmap = './assets/cmap_turbo.jpg'
            current_cv2_colormap = cv2.COLORMAP_TURBO
        if selected_cmap == 2:
            current_cmap = './assets/cmap_plasma.jpg'
            current_cv2_colormap = cv2.COLORMAP_PLASMA
    elif OS == 'Linux':
        if selected_cmap == 0:
            current_cmap = '/home/teamthermo/Desktop/gesundheitstechnik_thermograph/assets/cmap1.png'  
        if selected_cmap == 1:
            current_cmap = '/home/teamthermo/Desktop/gesundheitstechnik_thermograph/assets/cmap_turbo.jpg'
            current_cv2_colormap = cv2.COLORMAP_TURBO
        if selected_cmap == 2:
            current_cmap = '/home/teamthermo/Desktop/gesundheitstechnik_thermograph/assets/cmap_plasma.jpg'
            current_cv2_colormap = cv2.COLORMAP_PLASMA
    else: print('Selected cmap paths could not be set up.')
    
    Heatmap = current_cmap




    ## Galery ##

    list_index = 0
    select_path = ''
    current_list_size = 0




    ## Setup, and Memory States for each Sensor ##

    if Sensor == 'Flir':

        ## Flir Memory States ##
        
        crosshairs_thickness = 1 # Flir
        crosshairs_radius = 5 #Flir
        textsize_target = 1.0 #Flir
        textthickness_target = 1 #Flir
        
        minimum = 0.0
        maximum = 30.0
        
        ## Flir Setup ##
        attempts = 0
        while attempts < 10:
            try:
                HOST = 'localhost'
                PORT = 50007
                time.sleep(0.01)
                cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("Socket created")
                time.sleep(0.01)
                cs.bind((HOST,PORT))
                print("Socket bind complete")
                time.sleep(0.01)
                cs.listen(10)
                print("Socket now listening")
                time.sleep(0.01)
                call("/home/teamthermo/Desktop/gesundheitstechnik_thermograph/Thermograph_OS/start_client.sh", shell=True)
                time.sleep(0.01)

                conn, addr = cs.accept()
                dat = b''
                payload_size = struct.calcsize("L")
                cap = cv2.VideoCapture(cameraInputNumber)
                break
            except:
                print('Flir Sensor could not be set up.')
                attempts = attempts + 1
                
                call("/home/teamthermo/Desktop/gesundheitstechnik_thermograph/Thermograph_OS/purethermal1_uvc_capture_master/python/uvc_radiometry.py", shell = True)
                time.sleep(5)
                try:
                    HOST = 'localhost'
                    PORT = 50007
                    time.sleep(0.01)
                    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    print("Socket created")
                    time.sleep(0.01)
                    cs.bind((HOST,PORT))
                    print("Socket bind complete")
                    time.sleep(0.01)
                    cs.listen(10)
                    print("Socket now listening")
                    time.sleep(0.01)
                    call("/home/teamthermo/Desktop/gesundheitstechnik_thermograph/Thermograph_OS/start_client.sh", shell=True)
                    time.sleep(0.01)
                    
                    conn, addr = cs.accept()
                    dat = b''
                    payload_size = struct.calcsize("L")
                    cap = cv2.VideoCapture(cameraInputNumber)
                    break
                except:
                    print('Flir Sensor could not be set up.')
                    attempts = attempts + 1    
        
        heatMap_array, temp_unit, temp_range = heatmap_setup(Heatmap,maximum,minimum)
        time.sleep(3)
        while len(dat) < payload_size:
            dat += conn.recv(4096)
        packed_msg_size = dat[:payload_size]
        dat = dat[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]
        while len(dat) < msg_size:
            dat += conn.recv(4096)  
        frame_data = dat[:msg_size]
        dat = dat[msg_size:]
        img = pickle.loads(frame_data)
        img = (img-27315)/100.0
        
        img = img
        dim = img.shape
        width = dim[0]
        height = dim[1]
        blank_rgb = np.zeros((width, height, 3))
        
        


    elif Sensor == 'MLX':
        
        ## MLX Memory States ##
        
        crosshairs_thickness = 1 # MLX
        crosshairs_radius = 1 #MLX
        textsize_target = 0.5 #MLX
        textthickness_target = 1 #MLX
        
        minimum = 20.0
        maximum = 40.0

        ## MLX Setup ##
        import board,busio
        import adafruit_mlx90640
        i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)
        mlx = adafruit_mlx90640.MLX90640(i2c)
        mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ # sets refresh rate
        frame2d = np.zeros((24*32))

        mlx.getFrame(frame2d)
        img = np.reshape(frame2d, (24,32))

        heatMap_array, temp_unit, temp_range = heatmap_setup(Heatmap,maximum,minimum)

        img = img
        dim = img.shape
        width = dim[0]
        height = dim[1]
        blank_rgb = np.zeros((width, height, 3))




    elif Sensor == 'Normal_Camera':
        
        ## Normal Camera Memory States ##
        
        crosshairs_thickness = 2 # laptop
        crosshairs_radius = 10 #Laptop
        textsize_target = 3.0 #Laptop
        textthickness_target = 2 #Laptop
        
        minimum = 0
        maximum = 255

        ## Normal_Camera Setup ##
        cap = cv2.VideoCapture(cameraInputNumber)
        _, img = cap.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY, cv2.CV_8U)

        heatMap_array, temp_unit, temp_range = heatmap_setup(Heatmap,maximum,minimum)

        img = img
        dim = img.shape
        width = dim[0]
        height = dim[1]
        blank_rgb = np.zeros((width, height, 3))

    else:
        
        minimum = 0
        maximum = 255







    

