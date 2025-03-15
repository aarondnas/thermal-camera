#-------------------------------------------------------------------#
################ Source Code written by Aaron Schultz ###############
##################### Co-Writer: Falko Kristen ######################
####### All Rights Reserved, Copyright (c) 2023 Aaron Schultz #######
#-------------------------------------------------------------------#

################ SCRIPT IMPORTS ################

## extrern library imports ##
import tkinter
import customtkinter
from subprocess import call

## intern module imports ##
from modules.memory_states import MemoryStates as ms
from modules.design_states import DesignStates as ds




################ MENU WINDOW (SECOND WINDOW) ################

class ShutdownWindow(customtkinter.CTkToplevel):

        def __init__(ShutdownWindow, parent):
                super().__init__(parent)

                #ShutdownWindow = customtkinter.CTkToplevel(parent)
                ShutdownWindow.title("Thermograph Betriebssoftware - Shutdown Window")
                ShutdownWindow.geometry(str(ms.raspberryPieDisplayResolution[0]) + 'x' + str(ms.raspberryPieDisplayResolution[1]))                
                ShutdownWindow.overrideredirect(ds.NoWindowBorder) # TURN ON/OFF WINDOW BORDER FOR MENU

                tkinter.Grid.rowconfigure(ShutdownWindow, 0, weight=1)
                tkinter.Grid.rowconfigure(ShutdownWindow, 1, weight=1)

                tkinter.Grid.columnconfigure(ShutdownWindow, 0, weight=1)
                tkinter.Grid.columnconfigure(ShutdownWindow, 1, weight=1)

                def destroy_and_shutdown():
                        if ms.OS == 'Linux':
                                ms.ShutdownSwitch = True
                                call("sudo shutdown now", shell=True)
                        else:
                                ms.ShutdownSwitch = True

                ################# WIDGETS MENU ################
                
                ## Question Label ##
                questionLabel = customtkinter.CTkLabel(master=ShutdownWindow,
                        text="Do you want to shut down the device?",
                        text_font=('Helvetica','14'),
                        corner_radius=ds.button_corner_radius)
                questionLabel.grid(row=0, column=0, columnspan=2, sticky='nesw')


                ## No Button ##
                noButton = customtkinter.CTkButton(master=ShutdownWindow,
                        fg_color=ds.button_fg_color,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.button_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text='NO',
                        text_font=('Helvetica','14','bold'),
                        text_color=ds.button_text_color,
                        command=ShutdownWindow.destroy)
                noButton.grid(row=1, column=0, sticky='nesw')

                ## Yes Button ##
                yesButton = customtkinter.CTkButton(master=ShutdownWindow,
                        fg_color=ds.exitButton_fg_color,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.exitButton_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text='YES',
                        text_font=('Helvetica','14','bold'),
                        text_color=ds.button_text_color,
                        command=destroy_and_shutdown)
                        #command=print('test'))
                yesButton.grid(row=1, column=1, sticky='nesw')

        