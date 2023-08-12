import PySimpleGUI as sg
import util.colors as color
from util.const import *


def create_layout():
    layout = [
                [
                    sg.Frame('',[

                    ],expand_x=True,element_justification='center',vertical_alignment='center',s=(150,150),relief=sg.RELIEF_SOLID,border_width=0,visible=True,background_color=color.GRAY
                    ),
                ],

        ]
    return layout

def events(event):
    pass