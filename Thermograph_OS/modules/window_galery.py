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
import os
import fnmatch
import cv2
import numpy as np


## intern module imports ##
from modules.memory_states import MemoryStates as ms
from modules.design_states import DesignStates as ds
from modules.functions_main_window import FunctionsMainWindow as fMain




################ MENU WINDOW (SECOND WINDOW) ################

class GaleryWindow(customtkinter.CTkToplevel):
        
        def __init__(GaleryWindow, parent):
                super().__init__(parent)

                #GaleryWindow = customtkinter.CTkToplevel(parent)
                GaleryWindow.title("Thermograph Betriebssoftware - Galery Window")
                GaleryWindow.geometry(str(ms.raspberryPieDisplayResolution[0]) + 'x' + str(ms.raspberryPieDisplayResolution[1]))
                GaleryWindow.overrideredirect(ds.NoWindowBorder) # TURN ON/OFF WINDOW BORDER FOR MENU

                tkinter.Grid.rowconfigure(GaleryWindow, 0, weight=1)
                tkinter.Grid.rowconfigure(GaleryWindow, 1, weight=10)
                tkinter.Grid.rowconfigure(GaleryWindow, 2, weight=1)
                tkinter.Grid.rowconfigure(GaleryWindow, 3, weight=10)
                tkinter.Grid.rowconfigure(GaleryWindow, 4, weight=1)

                tkinter.Grid.columnconfigure(GaleryWindow, 0, weight=1000000)
                tkinter.Grid.columnconfigure(GaleryWindow, 1, weight=1)
                tkinter.Grid.columnconfigure(GaleryWindow, 2, weight=0)


                ## List ##
                def refresh_list():
                        lst.delete(0, tkinter.END) #delete all list elemts
                        list_images = [os.path.join(f)
                        for dirpath, dirnames, files in os.walk(ms.foto_save_path)
                                for extension in ['jpg', 'jpeg', 'png']
                                for f in fnmatch.filter(files, '*' + extension)]
                        for img in list_images:
                                lst.insert(tkinter.END, img)
                        ms.current_list_size = lst.size()
                        indLabel.configure(textvariable=tkinter.StringVar(value=str(ms.list_index+1) + '/' + str(ms.current_list_size)))
                        GaleryWindow.update()

                def delete_from_list():
                        item = lst.get(ms.list_index)
                        lst.delete(ms.list_index)
                        remove_path = f"{ms.foto_save_path}/{item}"
                        os.remove(remove_path)
                        refresh_list()
                        ms.list_index = ms.list_index - 1
                        if ms.list_index < 0:
                                ms.list_index = 0
                        ms.current_list_size = lst.size()
                        indLabel.configure(textvariable=tkinter.StringVar(value=str(ms.list_index+1) + '/' + str(ms.current_list_size)))
                        show_ind_list(ms.list_index)
                        GaleryWindow.update()

                def show_from_list(event):
                        global foto #doesn't work without global because of garbage collector
                        ms.list_index = event.widget.curselection()
                        ind = ms.list_index
                        if ms.OS == 'Linux':
                                item = lst.get(ind)
                                ms.select_path = str(ms.foto_save_path) + '/' +  str(item)
                        elif ms.OS == 'Windows':
                                item = lst.get(ind)
                                ms.select_path = str(ms.foto_save_path) + '/' +  str(item)
                        elif ms.OS == 'MacOS':
                                item = lst.get(ind)
                                ms.select_path = str(ms.foto_save_path) + '/' +  str(item)
                        else: 
                                ms.select_path = 'Could not set destination path.'
                        foto = cv2.imread(ms.select_path)
                        foto = cv2.resize(foto,(ms.StreamResolution),interpolation=cv2.INTER_LINEAR)
                        foto = cv2.cvtColor(foto, cv2.COLOR_BGR2RGB)
                        foto = ImageTk.PhotoImage(Image.fromarray(foto))
                        FotoLabel['image'] = foto
                        GaleryWindow.update()

                def show_ind_list(ind):
                        global foto #doesn't work without global because of garbage collector
                        lst.select_set(ind)
                        if ms.OS == 'Linux':
                                item = lst.get(ind)
                                ms.select_path = str(ms.foto_save_path) + '/' +  str(item)
                        elif ms.OS == 'Windows':
                                item = lst.get(ind)
                                ms.select_path = str(ms.foto_save_path) + '/' +  str(item)
                        elif ms.OS == 'MacOS':
                                item = lst.get(ind)
                                ms.select_path = str(ms.foto_save_path) + '/' +  str(item)
                        else: 
                                ms.select_path = 'Could not set destination path.'
                        try:
                                foto = cv2.imread(ms.select_path)
                                foto = cv2.resize(foto,(ms.StreamResolution),interpolation=cv2.INTER_LINEAR)
                                foto = cv2.cvtColor(foto, cv2.COLOR_BGR2RGB)
                                foto = ImageTk.PhotoImage(Image.fromarray(foto))
                        except: 
                                ## blank Image ##
                                blank_image = np.zeros((ms.StreamResolution[1],ms.StreamResolution[0],3), np.uint8)
                                blank_image[:,:] = (255,255,255)
                                blank_image = ImageTk.PhotoImage(Image.fromarray(blank_image))
                                indLabel.configure(textvariable=tkinter.StringVar(value='empty'))
                                foto = blank_image
                        FotoLabel['image'] = foto
                        GaleryWindow.update()

                def reset_index_and_path():
                        ms.list_index = 0
                        ms.select_path = ''
                
                def list_index_plus_one():
                        lst.select_clear(ms.list_index)
                        ms.list_index += 1
                        if ms.list_index > lst.size()-1:
                                ms.list_index = 0
                        ms.current_list_size = lst.size()
                        indLabel.configure(textvariable=tkinter.StringVar(value=str(ms.list_index+1) + '/' + str(ms.current_list_size)))
                        GaleryWindow.update()
                        
                def list_index_minus_one():
                        lst.select_clear(ms.list_index),
                        ms.list_index -= 1
                        if ms.list_index < 0:
                                ms.list_index = lst.size()-1
                        ms.current_list_size = lst.size()
                        indLabel.configure(textvariable=tkinter.StringVar(value=str(ms.list_index+1) + '/' + str(ms.current_list_size)))
                        GaleryWindow.update()

                ################# WIDGETS MENU ################
                
                ## Back Button ##
                backButton = customtkinter.CTkButton(master=GaleryWindow,
                        fg_color=ds.button_fg_color,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.button_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text=ds.button_text,
                        text_color=ds.button_text_color,
                        image=ImageTk.PhotoImage(Image.open(ms.back_button_path).resize((22, 22))),
                        command=lambda:[reset_index_and_path(),GaleryWindow.destroy()])
                backButton.grid(row=0, column=0, sticky='nesw')

                ## Up Button ##
                upButton = customtkinter.CTkButton(master=GaleryWindow,
                        fg_color=ds.currentButtonColor,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.button_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text=ds.button_text,
                        text_color=ds.button_text_color,
                        image=ImageTk.PhotoImage(Image.open(ms.arrow_button_path).resize((28, 28))),
                        command=lambda:[list_index_minus_one(), show_ind_list(ms.list_index)])
                upButton.grid(row=1, column=0, sticky='nesw')

                ## Down Button ##
                downButton = customtkinter.CTkButton(master=GaleryWindow,
                        fg_color=ds.button_fg_color,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.button_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text=ds.button_text,
                        text_color=ds.button_text_color,
                        image=ImageTk.PhotoImage(Image.open(ms.arrow_button_path).resize((28, 28)).rotate(180)),
                        command=lambda:[list_index_plus_one(), show_ind_list(ms.list_index)])
                downButton.grid(row=3, column=0, sticky='nesw')

                ## Delete Button ##
                deleteButton = customtkinter.CTkButton(master=GaleryWindow,
                        fg_color=ds.button_fg_color,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.button_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text=ds.button_text,
                        text_color=ds.button_text_color,
                        image=ImageTk.PhotoImage(Image.open(ms.delete_button_path).resize((20, 20))),
                        command=delete_from_list)
                deleteButton.grid(row=4, column=0, sticky='nesw')

                 ## Foto Label ##
                FotoLabel = tkinter.Label(master=GaleryWindow, 
                        width = ms.StreamResolution[0], 
                        height= ms.StreamResolution[1],
                        borderwidth = 0,
                        image=cv2.imread(ms.select_path))
                FotoLabel.grid(row=0, rowspan=5, column=1)

                ## Foto Number Label ##
                indLabel = customtkinter.CTkLabel(master=GaleryWindow,
                textvariable=tkinter.StringVar(value=str(ms.list_index+1) + '/' + str(ms.current_list_size)),
                text_font = ('Helvetica',8))
                indLabel.grid(row=2, column=0, sticky='nesw')
                
                
                ## List ##
                lst = tkinter.Listbox(GaleryWindow, highlightthickness=0)
                lst.bind("<<ListboxSelect>>", show_from_list)

                ctk_listbox_scrollbar = customtkinter.CTkScrollbar(GaleryWindow, command=lst.yview)
                lst.configure(yscrollcommand=ctk_listbox_scrollbar.set)

                refresh_list()
                show_ind_list(ms.list_index)
                GaleryWindow.update()




       