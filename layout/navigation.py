import PySimpleGUI as sg
import util.colors as color
from util.const import *

nav_tab_mouseover_colors=(color.DARK_GRAY,color.DIM_BLUE)
nav_tab_button_color=(color.DIM_BLUE,color.DARK_GRAY)
nav_tab_button_active_color=(color.DARK_GRAY,color.DIM_BLUE)

def create_layout():
    nav_tabs = [       
        {
            'title':"Text to Animation",
            'key': TXT2VID_TAB_BTN,
            'size':(20,1),
            'disabled':False,
            'expand_x':True,
            'default':True,
            'visible':True,
        },
        {
            'title':"Image to Animation",
            'key': TOOLBOX_TAB_BTN,
            'size':(20,1),
            'disabled':False,
            'default':False,
            'visible':False,
        },
        {
            'title':SETTINGS_TITLE,
            'key': SETTINGS_TAB_BTN,
            'size':(20,1),
            'disabled':False,
            'default':False,
            'visible':False,            
        },
        {
            'title':ABOUT_TITLE,
            'key': ABOUT_TAB_BTN,
            'disabled':False,
            'size':(20,1),
            'default':False,
            'visible':False,            
        },
    ]

    layout = [
        [
            sg.Frame('', [
                [

                    sg.Button(tab['title'],
                              k=tab['key'],
                              disabled=tab['disabled'],
                              visible=tab['visible'],
                              font=FONT,expand_x=False,
                              size=tab['size'],
                              button_color=nav_tab_button_color if not tab['default'] else nav_tab_button_active_color,
                              mouseover_colors=nav_tab_mouseover_colors)
                    for tab in nav_tabs
                ],

            ], expand_x=True,key='-nav-', expand_y=False, border_width=0, relief=sg.RELIEF_FLAT, element_justification="l")
        ]
    ]
    return layout

def handle_tab_event(event,window):

    tab_elements = {
        # PROJECTS_TAB_BTN: [window[PROJECTS_COL_1],window[PROJECTS_COL_2]],
        ABOUT_TAB_BTN: [window[ABOUT_COL]],
        # SETTINGS_TAB_BTN: [window[SETTINGS_COL]],
        # TOOLBOX_TAB_BTN: [window[TOOLBOX_COL]]
    }

    if event in tab_elements:
        for tab_key, elements in tab_elements.items():
            is_target = tab_key == event
            for element in elements:
                element.update(visible=is_target)
            window[tab_key].update(button_color=(nav_tab_button_active_color if is_target else nav_tab_button_color))   
             
