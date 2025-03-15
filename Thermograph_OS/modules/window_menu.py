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
from modules.functions_main_window import FunctionsMainWindow as fMain
from modules.window_filter import FilterWindow
from modules.window_galery import GaleryWindow




################ MENU WINDOW (SECOND WINDOW) ################

class MenuWindow(customtkinter.CTkToplevel):

        def __init__(MenuWindow, parent):
                super().__init__(parent)

                #MenuWindow = customtkinter.CTkToplevel(parent)
                MenuWindow.title("Thermograph Betriebssoftware - Menu")
                MenuWindow.geometry(str(ms.raspberryPieDisplayResolution[0]) + 'x' + str(ms.raspberryPieDisplayResolution[1]))
                MenuWindow.overrideredirect(ds.NoWindowBorder) # TURN ON/OFF WINDOW BORDER FOR MENU

                tkinter.Grid.rowconfigure(MenuWindow, 0, weight=1)
                tkinter.Grid.rowconfigure(MenuWindow, 1, weight=1)
                tkinter.Grid.rowconfigure(MenuWindow, 2, weight=1)

                tkinter.Grid.columnconfigure(MenuWindow, 0, weight=0)
                tkinter.Grid.columnconfigure(MenuWindow, 1, weight=1)

                ################# WIDGETS MENU ################
                
                ## Back Button ##
                backButton = customtkinter.CTkButton(master=MenuWindow,
                        fg_color=ds.button_fg_color,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.button_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text=ds.button_text,
                        text_color=ds.button_text_color,
                        image=ImageTk.PhotoImage(Image.open(ms.back_button_path).resize((32, 32))),
                        command=MenuWindow.destroy)
                backButton.grid(row=0, rowspan=4, column=0, sticky='nesw')

                ## Filter Window Button ##
                FilterWindowButton = customtkinter.CTkButton(master=MenuWindow,
                        fg_color=ds.currentButtonColor,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.button_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text=ds.button_text,
                        text_color=ds.button_text_color,
                        image=ImageTk.PhotoImage(Image.open(ms.filter_window_button_path).resize((38, 38))),
                        command=MenuWindow.open_filter_window)
                FilterWindowButton.grid(row=0, column=1, columnspan=2, sticky='nesw')

                ## Foto Window Button ##
                FotoWindowButton = customtkinter.CTkButton(master=MenuWindow,
                        fg_color=ds.button_fg_color,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.button_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text=ds.button_text,
                        text_color=ds.button_text_color,
                        image=ImageTk.PhotoImage(Image.open(ms.foto_window_button_path).resize((42, 42))),
                        command=MenuWindow.open_foto_window)
                FotoWindowButton.grid(row=1, column=1, columnspan=2, sticky='nesw')

                ## Settings Button ##
                SettingsWindowButton = customtkinter.CTkButton(master=MenuWindow,
                        fg_color=ds.button_fg_color,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.button_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text=ds.button_text,
                        text_color=ds.button_text_color,
                        image=ImageTk.PhotoImage(Image.open(ms.settings_window_button_path).resize((38, 38))),
                        command=MenuWindow.open_settings_window)
                SettingsWindowButton.grid(row=2, column=1, columnspan=2, sticky='nesw')



        
        def open_filter_window(MenuWindow):
                filter_window = FilterWindow(MenuWindow)
        def open_foto_window(MenuWindow):
                galery_window = GaleryWindow(MenuWindow)
        def open_settings_window(MenuWindow):
                settings_window = SettingsWindow(MenuWindow)