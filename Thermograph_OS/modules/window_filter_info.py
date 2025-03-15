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




################ MENU WINDOW (SECOND WINDOW) ################

class FilterInfoWindow(customtkinter.CTkToplevel):

        def __init__(FilterInfoWindow, parent, FilterNumber):
                super().__init__(parent)

                #FilterInfoWindow = customtkinter.CTkToplevel(parent)
                FilterInfoWindow.title("Thermograph Betriebssoftware - Filter Info Window")
                FilterInfoWindow.geometry(str(ms.raspberryPieDisplayResolution[0]) + 'x' + str(ms.raspberryPieDisplayResolution[1]))
                FilterInfoWindow.overrideredirect(ds.NoWindowBorder) # TURN ON/OFF WINDOW BORDER FOR MENU

                tkinter.Grid.rowconfigure(FilterInfoWindow, 0, weight=1)
                tkinter.Grid.rowconfigure(FilterInfoWindow, 1, weight=10000)
                tkinter.Grid.rowconfigure(FilterInfoWindow, 2, weight=10000)
             
                tkinter.Grid.columnconfigure(FilterInfoWindow, 0, weight=1)
                tkinter.Grid.columnconfigure(FilterInfoWindow, 1, weight=10000)
                tkinter.Grid.columnconfigure(FilterInfoWindow, 2, weight=10000)

                if ms.Sensor == 'Flir'  or ms.Sensor== 'MLX':
                        if FilterNumber == 1:
                                title="Map - Mode"
                                content='The Map-Mode mode is the default mode,\n when the camera is turned on.\n The Map-Mode maps the current measured temperatures\n on the selected Heatmap and displays\n the current maximum and minimum temperature on the sidebar.'
                        elif FilterNumber == 2:
                                title='Fever Detection - Mode'
                                content="The Fever Detection-Mode maps the current\n measured temperatures on the selected Heatmap\n and displays the current maximum and minimum temperature\n on the sidebar. Additionally this mode\n detects fever temperautres on 6 different levels.\n To guarantee a useful result,\n the camera should be focused on the patients forehead."
                                content_fever="37,5°C - 38,0°C: Subfebrile Temperature\n38,1°C - 38,5°C: Low Fever\n38,6°C - 39,0°C: Moderate Fever\n39,1°C - 39,9°C: High Fever\n40,0°C - 42,0°C: Very High Fever\n> 42,0°C: lethal Temperatur"
                                if ms.Sensor=="Flir":
                                        content_shortcuts="[SUB]\n[LOW]\n[MOD]\n[HIGH]\n[VERY HIGH]\n[LETHAL]"
                                if ms.Sensor=="MLX":
                                        content_shortcuts="[S]\n[L]\n[M]\n[H]\n[V H]\n[L E]"
                                else: content_shortcuts="[SUB]\n[LOW]\n[MOD]\n[HIGH]\n[VERY HIGH]\n[LETHAL]"
                        elif FilterNumber == 3:
                                title='Target - Mode'
                                content="The Fever Target-Mode maps the current\n measured temperatures on the selected Heatmap\n and displays the current maximum and minimum temperature\n on the sidebar. Additionally this mode\n shows the temperautre measured\n in the middle of the screen."
                                content_fever=""
                                content_shortcuts=""
                if ms.Sensor == 'Normal_Camera':
                        if FilterNumber == 1:
                                title="Map - Mode"
                                content='The Map-Mode mode is the default mode,\n when the camera is turned on.\n The Map-Mode maps the current measured temperatures\n on the selected Heatmap and displays\n the current maximum and minimum temperature on the sidebar.'
                        elif FilterNumber == 2:
                                title='Fever Detection - Mode'
                                content="The Fever Detection-Mode maps the current\n measured temperatures on the selected Heatmap\n and displays the current maximum and minimum temperature\n on the sidebar. Additionally this mode\n detects fever temperautres on 6 different levels.\n To guarantee a useful result,\n the camera should be focused on the patients forehead."
                                content_fever="37,0°C - 72,0°C: Subfebrile Temperature\n73,0°C - 108.0°C: Low Fever\n109,0°C - 144,0°C: Moderate Fever\n145,0°C - 177,0°C: High Fever\n178,0°C - 213,0°C: Very High Fever\n> 213,0°C: lethal Temperatur"
                                content_shortcuts="[SUB]\n[LOW]\n[MOD]\n[HIGH]\n[VERY HIGH]\n[LETHAL]"
                        elif FilterNumber == 3:
                                title='Target - Mode'
                                content="The Target-Mode maps the current\n measured temperatures on the selected Heatmap\n and displays the current maximum and minimum temperature\n on the sidebar. Additionally this mode\n shows the temperautre measured\n in the middle of the screen."
                                content_fever=""
                                content_shortcuts=""

                ################# WIDGETS MENU ################
                
                ## Back Button ##
                backButton = customtkinter.CTkButton(master=FilterInfoWindow,
                        fg_color=ds.button_fg_color,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.button_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text=ds.button_text,
                        text_color=ds.button_text_color,
                        image=ImageTk.PhotoImage(Image.open(ms.back_button_path).resize((32, 32))),
                        command=FilterInfoWindow.destroy)
                backButton.grid(row=0, column=0, sticky='nesw')


                ## Title Label ##
                titleLabel = customtkinter.CTkLabel(master=FilterInfoWindow,
                        text=title,
                        text_font=  ('Helvetica',16,'bold'),
                        corner_radius=ds.button_corner_radius)
                        #image = ImageTk.PhotoImage(Image.open(ms.info_button_path).resize((20, 20))))
                titleLabel.grid(row=0, column=1, columnspan=2, sticky='nesw')

                ## Body Label ##
                bodyLabel = customtkinter.CTkLabel(master=FilterInfoWindow,
                        text=content,
                        text_font= ('Helvetica',12),
                        corner_radius=ds.button_corner_radius)
                bodyLabel.grid(row=1, column=0, columnspan=3, sticky='nesw')

                ## BodyLabel 2 ##
                bodyLabel2 = customtkinter.CTkLabel(master=FilterInfoWindow,
                        text=content_fever,
                        text_font= ('Helvetica',12),
                        corner_radius=ds.button_corner_radius)
                bodyLabel2.grid(row=2, column=0, columnspan=2, sticky='nesw')

                ## BodyLabel 3 ##
                bodyLabel3 = customtkinter.CTkLabel(master=FilterInfoWindow,
                        text=content_shortcuts,
                        text_font= ('Helvetica',12,'bold'),
                        corner_radius=ds.button_corner_radius)
                bodyLabel3.grid(row=2, column=2, sticky='nesw')