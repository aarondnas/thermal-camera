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




################ HEATMAP SETTINGS WINDOW ################

class SettingsWindowCmap(customtkinter.CTkToplevel):

        def __init__(SettingsWindowCmap, parent):
                super().__init__(parent)

                #SettingsWindowCmap = customtkinter.CTkToplevel(parent)
                SettingsWindowCmap.title("Thermograph Betriebssoftware - Heatmap Settings")
                SettingsWindowCmap.geometry(str(ms.raspberryPieDisplayResolution[0]) + 'x' + str(ms.raspberryPieDisplayResolution[1]))
                SettingsWindowCmap.overrideredirect(ds.NoWindowBorder) # TURN ON/OFF WINDOW BORDER FOR MENU

                tkinter.Grid.rowconfigure(SettingsWindowCmap, 0, weight=1)
                tkinter.Grid.rowconfigure(SettingsWindowCmap, 1, weight=1)
                tkinter.Grid.rowconfigure(SettingsWindowCmap, 2, weight=1)
                tkinter.Grid.rowconfigure(SettingsWindowCmap, 3, weight=1)
                tkinter.Grid.rowconfigure(SettingsWindowCmap, 4, weight=1)

                tkinter.Grid.columnconfigure(SettingsWindowCmap, 0, weight=1)
                tkinter.Grid.columnconfigure(SettingsWindowCmap, 1, weight=1)

                ################# WIDGETS MENU ################
                
                ## Back Button ##
                backButton = customtkinter.CTkButton(master=SettingsWindowCmap,
                        fg_color=ds.button_fg_color,
                        bg_color=ds.button_bg_color,
                        hover_color=ds.button_hover_color,
                        border_width=ds.button_border_width,
                        border_color=ds.button_border_color,
                        corner_radius=ds.button_corner_radius,
                        text=ds.button_text,
                        text_color=ds.button_text_color,
                        image=ImageTk.PhotoImage(Image.open(ms.back_button_path).resize((32, 32))),
                        command=SettingsWindowCmap.destroy)
                backButton.grid(row=0, column=0, sticky='nesw')

                ## Title Lable ##
                titleLabel = customtkinter.CTkButton(master=SettingsWindowCmap,
                        text='Heatmap Settings',
                        text_font=  ('Helvetica',16,'bold'))
                titleLabel.grid(row=0, column=1, columnspan=3, sticky='nesw')




                ## Switches ##

                # Switch 1
                cmap_var1 = customtkinter.StringVar(value="on")
                
                def switch_cmap1():
                        switch_2.deselect()
                        switch_3.deselect()
                        switch_4.deselect()
                        ms.selected_cmap = switch_1.get()
                        ms.current_cmap, ms.current_cv2_colormap = ms.setup_cmap(ms.OS,ms.selected_cmap)

                        # setup new scanned heatmap
                        ms.heatMap_array, ms.temp_unit, ms.temp_range = ms.heatmap_setup(ms.current_cmap,ms.maximum,ms.minimum)

                        ms.cmapSwitch = True

                switch_1 = customtkinter.CTkSwitch(master=SettingsWindowCmap, text="Turbo  ", command=switch_cmap1,
                                                variable=cmap_var1, onvalue=int('1'), offvalue=0, text_font=('Helvetica',12), width=100, height=40)
                switch_1.grid(row=1, column=0, sticky='nesw')
                
                # Label 1
                global image1 
                image1 = ImageTk.PhotoImage(Image.open(ms.cmap1_flat))
                label1 = tkinter.Label(master=SettingsWindowCmap, image=image1)
                label1.grid(row=1, column=1, sticky='nesw')

                

                # Switch 2
                cmap_var2 = customtkinter.StringVar(value="on")

                def switch_cmap2():
                        switch_1.deselect()
                        switch_3.deselect()
                        switch_4.deselect()
                        ms.selected_cmap = int(cmap_var2.get())
                        ms.current_cmap, ms.current_cv2_colormap = ms.setup_cmap(ms.OS,ms.selected_cmap)

                        # setup new scanned heatmap
                        ms.heatMap_array, ms.temp_unit, ms.temp_range = ms.heatmap_setup(ms.current_cmap,ms.maximum,ms.minimum)

                        ms.cmapSwitch = True
                
                switch_2 = customtkinter.CTkSwitch(master=SettingsWindowCmap, text="Plasma  ", command=switch_cmap2,
                                                variable=cmap_var2, onvalue=int('2'), offvalue=0, text_font=('Helvetica',12), width=100, height=40)
                switch_2.grid(row=2, column=0, sticky='nesw')

                # Label 2
                global image2 
                image2 = ImageTk.PhotoImage(Image.open(ms.cmap2_flat))
                label2 = tkinter.Label(master=SettingsWindowCmap, image=image2)
                label2.grid(row=2, column=1, sticky='nesw')


                # Switch 3
                cmap_var3 = customtkinter.StringVar(value="on")

                def switch_cmap3():
                        switch_1.deselect()
                        switch_2.deselect()
                        switch_4.deselect()
                        ms.selected_cmap = int(cmap_var3.get())
                        ms.current_cmap, ms.current_cv2_colormap = ms.setup_cmap(ms.OS,ms.selected_cmap)

                        # setup new scanned heatmap
                        ms.heatMap_array, ms.temp_unit, ms.temp_range = ms.heatmap_setup(ms.current_cmap,ms.maximum,ms.minimum)

                        ms.cmapSwitch = True
                
                switch_3 = customtkinter.CTkSwitch(master=SettingsWindowCmap, text="Hot  ", command=switch_cmap3,
                                                variable=cmap_var3, onvalue=int('3'), offvalue=0, text_font=('Helvetica',12), width=100, height=40)
                switch_3.grid(row=3, column=0, sticky='nesw')

                # Label 3
                global image3 
                image3 = ImageTk.PhotoImage(Image.open(ms.cmap3_flat))
                label3 = tkinter.Label(master=SettingsWindowCmap, image=image3)
                label3.grid(row=3, column=1, sticky='nesw')


                # Switch 4
                cmap_var4 = customtkinter.StringVar(value="on")

                def switch_cmap4():
                        switch_1.deselect()
                        switch_2.deselect()
                        switch_3.deselect()
                        ms.selected_cmap = int(cmap_var4.get())
                        ms.current_cmap, ms.current_cv2_colormap = ms.setup_cmap(ms.OS,ms.selected_cmap)

                        # setup new scanned heatmap
                        ms.heatMap_array, ms.temp_unit, ms.temp_range = ms.heatmap_setup(ms.current_cmap,ms.maximum,ms.minimum)

                        ms.cmapSwitch = True

                switch_4 = customtkinter.CTkSwitch(master=SettingsWindowCmap, text="Cool  ", command=switch_cmap4,
                                                variable=cmap_var4, onvalue=int('4'), offvalue=0, text_font=('Helvetica',12), width=100, height=40)
                switch_4.grid(row=4, column=0, sticky='nesw')

                # Label 4
                global image4 
                image4 = ImageTk.PhotoImage(Image.open(ms.cmap4_flat))
                label4 = tkinter.Label(master=SettingsWindowCmap, image=image4)
                label4.grid(row=4, column=1, sticky='nesw')
                

                # autoselect cmap when object is created
                if ms.selected_cmap == 1:
                        switch_1.select()
                elif ms.selected_cmap == 2:
                        switch_2.select()
                elif ms.selected_cmap == 3:
                        switch_3.select()
                elif ms.selected_cmap == 4:
                        switch_4.select()

                




