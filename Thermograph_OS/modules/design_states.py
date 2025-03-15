#-------------------------------------------------------------------#
################ Source Code written by Aaron Schultz ###############
##################### Co-Writer: Falko Kristen ######################
####### All Rights Reserved, Copyright (c) 2023 Aaron Schultz #######
#-------------------------------------------------------------------#

################ SCRIPT IMPORTS ################

## extrern library imports ##
import customtkinter




################ DESIGN STATES ################

class DesignStates:

    customtkinter.set_appearance_mode("dark") # Sets Customtkinter Color Appearance Theme
    NoWindowBorder = (False) # TURN ON/OFF WINDOW BORDER FOR ALL WINDOWS


    ## Buttons ##
    button_width = 20
    button_height = 20
    button_fg_color = "#4BB854"
    button_bg_color = "#212325"
    button_hover_color = "#35823C"
    button_border_width = 2
    button_border_color = button_bg_color
    button_corner_radius = 16
    button_text = ''
    button_text_color = None
    info_button_fg_color = '#CDCDCD'
    info_button_hover_color = '#A1A1A1'

    exitButton_fg_color = "#E8412E"
    exitButton_hover_color = "#B83425"

    button_pressed_color = '#FFFFFF'

    ## variable colors ##
    currentButtonColor = button_fg_color
    
    currentButtonColor1 = button_pressed_color
    currentButtonColor2 = button_fg_color
    currentButtonColor3 = button_fg_color
    
    currentButtonHoverColor1 = button_pressed_color
    currentButtonHoverColor2 = button_hover_color
    currentButtonHoverColor3 = button_hover_color