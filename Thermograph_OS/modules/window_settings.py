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


## intern module imports ##
from modules.memory_states import MemoryStates as ms
from modules.design_states import DesignStates as ds
from modules.window_settings_cmap import SettingsWindowCmap
#from modules.window_settings_color_theme import SettingsWindowColorTheme




################ SETTINGS WINDOW  ################

class SettingsWindow(customtkinter.CTkToplevel):

        def __init__(SettingsWindow, parent):
                super().__init__(parent)

                #SettingsWindow = customtkinter.CTkToplevel(parent)
                SettingsWindow.title("Thermograph Betriebssoftware - Settings")
                SettingsWindow.geometry(str(ms.raspberryPieDisplayResolution[0]) + 'x' + str(ms.raspberryPieDisplayResolution[1]))
                SettingsWindow.overrideredirect(ds.NoWindowBorder) # TURN ON/OFF WINDOW BORDER FOR MENU

                tkinter.Grid.rowconfigure(SettingsWindow, 0, weight=1)
                tkinter.Grid.rowconfigure(SettingsWindow, 1, weight=1)
                tkinter.Grid.rowconfigure(SettingsWindow, 2, weight=1)

                tkinter.Grid.columnconfigure(SettingsWindow, 0, weight=0)
                tkinter.Grid.columnconfigure(SettingsWindow, 1, weight=1)

                ################# WIDGETS MENU ################
                
                ## Back Button ##
                backButton = customtkinter.CTkButton(master=SettingsWindow,
                        fg_color=ds.button_fg_color,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.button_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text=ds.button_text,
                        text_color=ds.button_text_color,
                        image=ImageTk.PhotoImage(Image.open(ms.back_button_path).resize((32, 32))),
                        command=SettingsWindow.destroy)
                backButton.grid(row=0, rowspan=4, column=0, sticky='nesw')

                ## Cmap Settings Button ##
                CmapSettingsWindowButton = customtkinter.CTkButton(master=SettingsWindow,
                        fg_color=ds.currentButtonColor,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.button_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text='Heatmap Settings',
                        text_font=('Helvetica',16),
                        text_color=ds.button_text_color,
                        #image=ImageTk.PhotoImage(Image.open(ms.settings_window_button_path).resize((38, 38))),
                        command=SettingsWindow.open_cmap_window)
                CmapSettingsWindowButton.grid(row=0, column=1, columnspan=2, sticky='nesw')

                ## Color Theme Window Button ##
                ColorThemeSettingsWindowButton = customtkinter.CTkButton(master=SettingsWindow,
                        fg_color=ds.button_fg_color,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.button_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text='Color Theme Settings',
                        text_font=('Helvetica',16),
                        text_color=ds.button_text_color,
                        #image=ImageTk.PhotoImage(Image.open(ms.settings_window_button_path).resize((38, 38))),
                        command=print('SettingsWindow.open_color_window'))
                #ColorThemeSettingsWindowButton.grid(row=1, column=1, columnspan=2, sticky='nesw')

                ## Sensor Settings Window Button ##
                SensorSettingsWindowButton = customtkinter.CTkButton(master=SettingsWindow,
                        fg_color=ds.button_fg_color,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.button_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text='Sensor Settings',
                        text_font=('Helvetica',16),
                        text_color=ds.button_text_color,
                        #image=ImageTk.PhotoImage(Image.open(ms.settings_window_button_path).resize((38, 38))),
                        command=print('SettingsWindow.open_sensor_window'))
                #SensorSettingsWindowButton.grid(row=2, column=1, columnspan=2, sticky='nesw')


        def open_cmap_window(SettingsWindow):
                settings_window_cmap = SettingsWindowCmap(SettingsWindow)