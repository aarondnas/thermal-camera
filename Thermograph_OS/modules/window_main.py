#-------------------------------------------------------------------#
################ Source Code written by Aaron Schultz ###############
##################### Co-Writer: Falko Kristen ######################
####### All Rights Reserved, Copyright (c) 2023 Aaron Schultz #######
#-------------------------------------------------------------------#

################ SCRIPT IMPORTS ################

## extrern library imports ##
import tkinter
import customtkinter
from PIL import Image, ImageTk
import cv2
import numpy as np
import pickle
import struct
from subprocess import call
import time


## intern module imports ##
from modules.design_states import DesignStates as ds
from modules.memory_states import MemoryStates as ms
from modules.functions_main_window import FunctionsMainWindow as fMain
from modules.window_menu import MenuWindow
from modules.window_shutdown import ShutdownWindow







############## MAIN WINDOW ################

class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
    

        ############## WINDOW MAIN (self) CONFIGURATIONS ################

        self.geometry(f"{ms.raspberryPieDisplayResolutionWidth}x{ms.raspberryPieDisplayResolutionHeight}")
        self.title("Thermograph Betriebssoftware")
        #self.resizable(False,False) # Turn On/Off Window Size Locked
        self.overrideredirect(ds.NoWindowBorder) # TURN ON/OFF WINDOW BORDER FOR MAIN WINDOW



        ############### GRID LAYOUT ################

        tkinter.Grid.rowconfigure(self, 0, weight=3)
        tkinter.Grid.rowconfigure(self, 1, weight=0)
        tkinter.Grid.rowconfigure(self, 2, weight=3)
        tkinter.Grid.rowconfigure(self, 3, weight=10)
        tkinter.Grid.rowconfigure(self, 4, weight=10)
        tkinter.Grid.rowconfigure(self, 5, weight=3)
        tkinter.Grid.rowconfigure(self, 6, weight=0)
        tkinter.Grid.rowconfigure(self, 7, weight=0)

        tkinter.Grid.columnconfigure(self, 0, weight=1000000)
        tkinter.Grid.columnconfigure(self, 1, weight=1)
        tkinter.Grid.columnconfigure(self, 2, weight=1)





        ################# WIDGETS MAIN ################

        ## Camera Label ##
        camLabel = tkinter.Label(self, 
                width = ms.StreamResolution[0], 
                height= ms.StreamResolution[1],
                borderwidth = 0)
        camLabel.grid(row=0, rowspan=7, column=1)
        
        def camLabelCallback(stopStreamSwitch):
            if ms.streamStopSwitch == False:
                ms.streamStopSwitch = True
            else : ms.streamStopSwitch = False
        camLabel.bind("<Button-1>", camLabelCallback)

        ## Zoom Label ##
        zoomLabel = customtkinter.CTkLabel(master=self,
                textvariable=tkinter.StringVar(value=str(ms.currentZoomFactor) + 'x'),
                text_font = ('Helvetica',8))
        zoomLabel.grid(row=1, column=0, sticky='nesw')
        
        ## Heatmap Canvas ##
        cmapCanvas = tkinter.Canvas(master=self,
                                    width = 30,
                                    height = ms.flirPureThermalCameraResolutionResized[1],
                                    bd = 0,
                                    highlightthickness=0,)
        cmapCanvas.grid(row=0,rowspan=7,column=2)

        canvas_image=ImageTk.PhotoImage(Image.open(ms.current_cmap).resize((30,ms.StreamResolution[1])))
        CmapCanvas = cmapCanvas.create_image(30, ms.StreamResolution[1], anchor='se', image=canvas_image)
        CelsiusCanvas = cmapCanvas.create_text(13,ms.StreamResolution[1]/4, anchor='center', text='°C', font=('Helvetica','10','bold'))
        MaximumCanvas = cmapCanvas.create_text(13,12, anchor='center', text=str(ms.maximum), font=('Helvetica','8'))
        middle_temp = ms.minimum + (ms.maximum-ms.minimum) / 2
        MiddleCanvas = cmapCanvas.create_text(13,ms.StreamResolution[1]/2, anchor='center', text=str(middle_temp), font=('Helvetica','8'))
        MinimumCanvas = cmapCanvas.create_text(13,ms.StreamResolution[1]-12, anchor='center', text=str(ms.minimum), font=('Helvetica','8'))

            

        ## PlusButton ##
        plusButton = customtkinter.CTkButton(master=self,
                fg_color=ds.button_fg_color,
                bg_color=ds.button_bg_color,
                hover_color=ds.button_hover_color,
                border_width=ds.button_border_width,
                border_color=ds.button_border_color,
                corner_radius=ds.button_corner_radius,
                text=ds.button_text,
                text_color=ds.button_text_color,
                image=ImageTk.PhotoImage(Image.open(ms.plus_button_path).resize((12, 12))),
                command=lambda:[fMain.plusZoom(), fMain.updateZoomLabel(), zoomLabel.configure(textvariable=tkinter.StringVar(value=ms.currentZoomDisplay))])
        plusButton.grid(row=0, column=0, sticky='nesw')

        ## Minus Button ##
        minusButton = customtkinter.CTkButton(master=self,
                fg_color=ds.button_fg_color,
                bg_color=ds.button_bg_color,
                hover_color=ds.button_hover_color,
                border_width=ds.button_border_width,
                border_color=ds.button_border_color,
                corner_radius=ds.button_corner_radius,
                text=ds.button_text,
                text_color=ds.button_text_color,
                image=ImageTk.PhotoImage(Image.open(ms.minus_button_path).resize((12, 12))),
                command=lambda:[fMain.minusZoom(), fMain.updateZoomLabel(), zoomLabel.configure(textvariable=tkinter.StringVar(value=ms.currentZoomDisplay))])
        minusButton.grid(row=2, column=0, sticky='nesw')

        ## Screenshot Button ##
        screenShotButton = customtkinter.CTkButton(master=self,
                fg_color=ds.button_fg_color,
                bg_color=ds.button_bg_color,
                hover_color=ds.button_hover_color,
                border_width=ds.button_border_width,
                border_color=ds.button_border_color,
                corner_radius=ds.button_corner_radius,
                text=ds.button_text,
                text_color=ds.button_text_color,
                image=ImageTk.PhotoImage(Image.open(ms.screenshot_button_path).resize((16, 16))),
                command= fMain.changeScreenshotSwitch)
        screenShotButton.grid(row=3, column=0, sticky='nesw')

        ## Menu Button ##
        MenuButton = customtkinter.CTkButton(master=self,
                fg_color=ds.button_fg_color,
                bg_color=ds.button_bg_color,
                hover_color=ds.button_hover_color,
                border_width=ds.button_border_width,
                border_color=ds.button_border_color,
                corner_radius=ds.button_corner_radius,
                text=ds.button_text,
                text_color=ds.button_text_color,
                image=ImageTk.PhotoImage(Image.open(ms.menu_button_path).resize((12, 12))),
                command=self.openMenu)
        MenuButton.grid(row=4, column=0, sticky='nesw')

        ## Exit Button ##
        exitButton = customtkinter.CTkButton(master=self,
                fg_color=ds.exitButton_fg_color,
                bg_color=ds.button_bg_color,
                hover_color=ds.exitButton_hover_color,
                border_width=ds.button_border_width,
                border_color=ds.button_border_color,
                corner_radius=ds.button_corner_radius,
                text=ds.button_text,
                text_color=ds.button_text_color,
                image=ImageTk.PhotoImage(Image.open(ms.exit_button_path).resize((12, 12))),
                command=self.openShutdown)
        exitButton.grid(row=5, column=0, sticky='nesw')





        frame_rate_counter = 0

        ################ MAIN VIDEO STREAM FLIR ################
        if ms.Sensor == 'Flir':
            
            #####SETUP#####
            conn = ms.conn
            dat = ms.dat
            payload_size = ms.payload_size
            cap = ms.cap
            
            frame_rate_counter = 0
            
            while True:

                
                if ms.ShutdownSwitch == True:
                    self.destroy()
                
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

                # if, else to controll framerate
                if frame_rate_counter%10 != 0:
                    frame_rate_counter = frame_rate_counter + 1
                else: 
                    frame_rate_counter = 0

                    
                    ## cmap Switch ##
                    if ms.cmapSwitch == True:
                        fMain.set_new_cmap(cmapCanvas, CmapCanvas)
                        self.update()
                    
                    ## Checking for Filter Switches ##
                    if ms.filter1Switch == True:
                        img = fMain.filter1_Flir(img,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas)
                    else: pass

                    if ms.filter2Switch == True:
                        img = fMain.filter2_Flir(img,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas)
                    else: pass
                    
                    if ms.filter3Switch == True:
                        img = fMain.filter3_Flir(img,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas)
                    else: pass

                    if ms.filter4Switch == True:
                        img = fMain.filter4_Flir(img)
                    else: pass
                    
                    ## Checking for Scrrenshot Switch
                    if ms.screenshotSwitch == True:
                        fMain.takeScreenshot(img)
                        ## Screenshot Animation ##
                        blank_image = np.zeros((ms.StreamResolution[1],ms.StreamResolution[0],3), np.uint8)
                        blank_image[:,:] = (255,255,255)
                        blank_image = ImageTk.PhotoImage(Image.fromarray(blank_image))
                        camLabel['image'] = blank_image
                        self.update()
                        time.sleep(0.15)
                    else: pass


                    img = cv2.resize(img, ms.currentRes, interpolation=cv2.INTER_LINEAR)
                    img = ImageTk.PhotoImage(Image.fromarray(img))
                    if ms.streamStopSwitch == False:
                        camLabel['image'] = img
                        frozen_image = img
                    if ms.streamStopSwitch == True:
                        camLabel['image'] = frozen_image
                    self.update()
                    frame_rate_counter = frame_rate_counter + 1




        ################ MAIN VIDEO STREAM MLX ################
        if ms.Sensor == 'MLX':

            if ms.ShutdownSwitch == True:
                self.destroy()
        
            #####SETUP#####
            mlx = ms.mlx
            frame2d = ms.frame2d
            
            while True:

            
                mlx.getFrame(frame2d)
                img = np.reshape(frame2d, (24,32))

                # if, else to controll framerate
                if frame_rate_counter%10 != 0:
                    frame_rate_counter = frame_rate_counter + 1
                else: 
                    frame_rate_counter = 0

                
                
                ## cmap Switch ##
                if ms.cmapSwitch == True:
                    fMain.set_new_cmap(cmapCanvas, CmapCanvas)
                    self.update()
                
                ## Checking for Filter Switches ##
                if ms.filter1Switch == True:
                    img = fMain.filter1_MLX(img,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas)
                else: pass

                if ms.filter2Switch == True:
                    img = fMain.filter2_MLX(img,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas)
                else: pass
                
                if ms.filter3Switch == True:
                    img = fMain.filter3_MLX(img)
                else: pass

                if ms.filter4Switch == True:
                    img = fMain.filter4_MLX(img)
                else: pass
                
                ## Checking for Scrrenshot Switch
                if ms.screenshotSwitch == True:
                    fMain.takeScreenshot(img)
                    ## Screenshot Animation ##
                    blank_image = np.zeros((ms.StreamResolution[1],ms.StreamResolution[0],3), np.uint8)
                    blank_image[:,:] = (255,255,255)
                    blank_image = ImageTk.PhotoImage(Image.fromarray(blank_image))
                    camLabel['image'] = blank_image
                    self.update()
                    time.sleep(0.15)
                else: pass


                img = cv2.resize(img, ms.currentRes, interpolation=cv2.INTER_LINEAR)
                img = ImageTk.PhotoImage(Image.fromarray(img))
                if ms.streamStopSwitch == False:
                    camLabel['image'] = img
                    frozen_image = img
                if ms.streamStopSwitch == True:
                    camLabel['image'] = frozen_image
                self.update()
                        
                    



        ################ MAIN VIDEO STREAM NORMAL_CAMERA ################
        if ms.Sensor == 'Normal_Camera':
           
        
            #####SETUP#####
            cap = cv2.VideoCapture(ms.cameraInputNumber)

            
            while True:


                if ms.ShutdownSwitch == True:
                    self.destroy()
                
                _, img = cap.read()
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                '''
                # if, else to controll framerate
                if frame_rate_counter%10 != 0:
                    frame_rate_counter = frame_rate_counter + 1
                else: 
                    frame_rate_counter = 0
                '''

                ## cmap Switch ##
                if ms.cmapSwitch == True:
                    fMain.set_new_cmap(cmapCanvas, CmapCanvas)
                    self.update()
                

                ## Checking for Filter Switches ##
                if ms.filter1Switch == True:
                    img = fMain.filter1_NormalCamera(img,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas)
                else: pass
                
                if ms.filter2Switch == True:
                    img = fMain.filter2_NormalCamera(img,cmapCanvas,MaximumCanvas,MiddleCanvas,MinimumCanvas)
                else: pass
                
                if ms.filter3Switch == True:
                    img = fMain.filter3_NormalCamera(img)
                else: pass

                if ms.filter4Switch == True:
                    img = fMain.filter4_NormalCamera(img)
                else: pass
                
            

                if ms.streamStopSwitch == False:

                    if ms.screenshotSwitch == True:
                        fMain.takeScreenshot(img)
                        ## Screenshot Animation ##
                        blank_image = np.zeros((ms.StreamResolution[1],ms.StreamResolution[0],3), np.uint8)
                        blank_image[:,:] = (255,255,255)
                        blank_image = ImageTk.PhotoImage(Image.fromarray(blank_image))
                        camLabel['image'] = blank_image
                        self.update()
                        time.sleep(0.15)
                    frozen_img = img
                    output = cv2.resize(img, ms.currentRes, interpolation=cv2.INTER_LINEAR)

                    # tried to crop Image
                    #output = output[ms.croppedY1:ms.croppedY2, ms.croppedX1:ms.croppedX2]
                    #output= output[ int(ms.StreamResolution[1]*(ms.currentZoomFactor-1)) : int(ms.StreamResolution[1] - (ms.StreamResolution[1]*(ms.currentZoomFactor-1))) , int(ms.StreamResolution[0]*(ms.currentZoomFactor-1)) : int(ms.StreamResolution[0] - (ms.StreamResolution[0]*(ms.currentZoomFactor-1)))]
                    
                    output = ImageTk.PhotoImage(Image.fromarray(output))
                    camLabel['image'] = output
                    

                if ms.streamStopSwitch == True:
                    
                    if ms.screenshotSwitch == True:
                        fMain.takeScreenshot(frozen_img)
                        ## Screenshot Animation ##
                        blank_image = np.zeros((ms.StreamResolution[1],ms.StreamResolution[0],3), np.uint8)
                        blank_image[:,:] = (255,255,255)
                        blank_image = ImageTk.PhotoImage(Image.fromarray(blank_image))
                        camLabel['image'] = blank_image
                        self.update()
                        time.sleep(0.15)
                    output = cv2.resize(frozen_img, ms.currentRes, interpolation=cv2.INTER_LINEAR)
                    # tried to crop Image
                    #output = output[ms.croppedY1:ms.croppedY2, ms.croppedX1:ms.croppedX2]
                    output = ImageTk.PhotoImage(Image.fromarray(output))
                    camLabel['image'] = output


                ## Checking for Screenshot Switch
                
                else: pass

            
                img = cv2.resize(img, ms.currentRes, interpolation=cv2.INTER_LINEAR)
                img = ImageTk.PhotoImage(Image.fromarray(img))
                if ms.streamStopSwitch == False:
                    camLabel['image'] = img
                    frozen_image = img
                if ms.streamStopSwitch == True:
                    camLabel['image'] = frozen_image
                self.update()
                frame_rate_counter = frame_rate_counter + 1
        









        else: 
            print('No video stream for any device could be set up.')
            print('New try by reseting USB port')
            try:
                call("sudo ./usbreset /dev/bus/usb/001/006", shell=True)
                print("RESETING THE PORT OF FLIR!")
                time.sleep(2)
                call("/home/teamthermo/start_thermograph.sh", shell=True)
            except:
                print("IMPOSSIBLE TO CONNECT!")



################### FUNCTION TO INITIALIZE FILTER MENU ####################

    def openMenu(self):
        menu = MenuWindow(self)

    def openShutdown(self):
        shutdown = ShutdownWindow(self)



