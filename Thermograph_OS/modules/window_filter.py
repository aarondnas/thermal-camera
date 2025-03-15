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




################ MENU WINDOW (SECOND WINDOW) ################

class FilterWindow(customtkinter.CTkToplevel):

        def __init__(FilterWindow, parent):
                super().__init__(parent)

                FilterWindow.title("Thermograph Betriebssoftware - Filter Window")
                FilterWindow.geometry(str(ms.raspberryPieDisplayResolution[0]) + 'x' + str(ms.raspberryPieDisplayResolution[1]))
                FilterWindow.overrideredirect(ds.NoWindowBorder) # TURN ON/OFF WINDOW BORDER FOR MENU

                tkinter.Grid.rowconfigure(FilterWindow, 0, weight=1)
                tkinter.Grid.rowconfigure(FilterWindow, 1, weight=0)
                tkinter.Grid.rowconfigure(FilterWindow, 2, weight=1)
                tkinter.Grid.rowconfigure(FilterWindow, 3, weight=0)

                tkinter.Grid.columnconfigure(FilterWindow, 0, weight=0)
                tkinter.Grid.columnconfigure(FilterWindow, 1, weight=1)
                tkinter.Grid.columnconfigure(FilterWindow, 2, weight=1)

                ################# WIDGETS MENU ################
                
                ## Back Button ##
                backButton = customtkinter.CTkButton(master=FilterWindow,
                        fg_color=ds.button_fg_color,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.button_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text=ds.button_text,
                        text_color=ds.button_text_color,
                        image=ImageTk.PhotoImage(Image.open(ms.back_button_path).resize((32, 32))),
                        command=FilterWindow.destroy)
                backButton.grid(row=0, rowspan=5, column=0, sticky='nesw')

                ## Filter 1 Button ##
                filterButton1 = customtkinter.CTkButton(master=FilterWindow,
                        fg_color=ds.currentButtonColor,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.button_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text=ds.button_text,
                        text_color=ds.button_text_color,
                        image=ImageTk.PhotoImage(Image.open(ms.filter1_button_path).resize((38, 38))),
                        command=fMain.changeFilter1Switch)
                filterButton1.grid(row=0, column=1, sticky='nesw')

                ## Filter 2 Button ##
                filterButton2 = customtkinter.CTkButton(master=FilterWindow,
                        fg_color=ds.button_fg_color,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.button_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text=ds.button_text,
                        text_color=ds.button_text_color,
                        image=ImageTk.PhotoImage(Image.open(ms.filter2_button_path).resize((38, 38))),
                        command=fMain.changeFilter2Switch)
                filterButton2.grid(row=0, column=2, sticky='nesw')

                ## Filter Button 3 ##
                filterButton3 = customtkinter.CTkButton(master=FilterWindow,
                        fg_color=ds.button_fg_color,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.button_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text=ds.button_text,
                        text_color=ds.button_text_color,
                        image=ImageTk.PhotoImage(Image.open(ms.filter3_button_path).resize((38, 38))),
                        command=fMain.changeFilter3Switch)
                #filterButton3.grid(row=2, column=1, sticky='nesw')

                ## Filter Button 4 ##
                filterButton4 = customtkinter.CTkButton(master=FilterWindow,
                        fg_color=ds.button_fg_color,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.button_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text=ds.button_text,
                        text_color=ds.button_text_color,
                        image=ImageTk.PhotoImage(Image.open(ms.filter4_button_path).resize((38, 38))),
                        command=fMain.changeFilter4Switch)
                #filterButton4.grid(row=2, column=2, sticky='nesw')


                ## Filter 1 Description Label ##
                descriptionLabel_f1 = customtkinter.CTkLabel(master=FilterWindow,
                        text="Normal Mode",
                        corner_radius=ds.button_corner_radius)
                descriptionLabel_f1.grid(row=1, column=1, sticky='nesw')

                ## Filter 2 Description Label ##
                descriptionLabel_f2 = customtkinter.CTkLabel(master=FilterWindow,
                        text="Fever Mode",
                        corner_radius=ds.button_corner_radius)
                descriptionLabel_f2.grid(row=1, column=2, sticky='nesw')

                ## Filter 3 Description Label ##
                descriptionLabel_f3 = customtkinter.CTkLabel(master=FilterWindow,
                        text="Filter 3",
                        corner_radius=ds.button_corner_radius)
                #descriptionLabel_f3.grid(row=3, column=1, sticky='nesw')


                ## Filter 4 Description Label ##
                descriptionLabel_f4 = customtkinter.CTkLabel(master=FilterWindow,
                        text="Filter 4",
                        corner_radius=ds.button_corner_radius)
                #descriptionLabel_f4.grid(row=3, column=2, sticky='nesw')

                descriptionButton_f3 = customtkinter.CTkButton(master=FilterWindow,
                        text='Target',
                        text_color='black',
                        text_font=('Helvetica',8,'bold'),
                        corner_radius=ds.button_corner_radius,
                        bg_color=ds.button_bg_color,
                        fg_color=ds.info_button_fg_color,
                        hover_color=ds.info_button_hover_color,
                        image = ImageTk.PhotoImage(Image.open(ms.info_button_path).resize((20, 20))),
                        command=lambda:[FilterWindow.openFilterInfoWindow(3)])
                descriptionButton_f3.grid(row=4, column=1, sticky='nesw')



                
                ################### CHANGES FILTER BUTTON COLOR WHEN PRESSED ##################
                
                def changeButtonColor(button):
                        if ds.currentButtonColor == ds.button_fg_color:
                                ds.currentButtonColor = ds.button_pressed_color
                                button.configure(fg_color=ds.currentButtonColor)
                                button.configure(hover_color=ds.currentButtonColor)
                        else:
                                ds.currentButtonColor = ds.button_fg_color
                                button.configure(fg_color=ds.button_fg_color)
                                button.configure(hover_color=ds.button_hover_color)