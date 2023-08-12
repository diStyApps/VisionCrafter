import PySimpleGUI as sg
from util.const import *
import util.colors as color

import os
models_list = [
    ""
]
lora_models_list = [
    ""
]
def set_models_path(file_list, extensions, models_path_directory):
    if models_path_directory:
        # print('models_path_directory set',models_path_directory)
        for filename in os.listdir(models_path_directory):
            if filename.endswith(tuple(extensions)):
                file_list.append(filename)    
    else:
        # print('no models_path_directory set yet')
        sg.user_settings_set_entry("models_path", 'models/checkpoints')
        models_path_directory = sg.user_settings_get_entry("models_path", '')
        if models_path_directory:
            for filename in os.listdir(models_path_directory):
                if filename.endswith(tuple(extensions)):
                    file_list.append(filename)

def set_lora_models_path(file_list, extensions, lora_models_path_directory):
    if lora_models_path_directory:
        # print('lora_models_path_directory set',lora_models_path_directory)
        for filename in os.listdir(lora_models_path_directory):
            if filename.endswith(tuple(extensions)):
                file_list.append(filename)    
    else:
        # print('no lora_models_path_directory set yet')
        sg.user_settings_set_entry("lora_models_path", 'models/checkpoints')
        lora_models_path_directory = sg.user_settings_get_entry("lora_models_path", '')
        if lora_models_path_directory:
            for filename in os.listdir(lora_models_path_directory):
                if filename.endswith(tuple(extensions)):
                    file_list.append(filename)

set_models_path(models_list, extensions, sg.user_settings_get_entry("models_path", ''))
set_models_path(lora_models_list, extensions, sg.user_settings_get_entry("lora_models_path", ''))

def create_layout():

    layout = [
            [
                sg.Text('Model'),
                sg.Combo(sorted(models_list), default_value=sg.user_settings_get_entry("selected_model", ''), size=(80, 1), key="-selected_model-",expand_x=False,enable_events=True, readonly=True),  
                sg.I(visible=False,key='-models_path-',enable_events=True),
                sg.FolderBrowse('Set models folder',enable_events=True),


                sg.In(0.8,k='-lora_alpha-',s=(5,5),justification='center',disabled=True,use_readonly_for_disable=True,disabled_readonly_background_color=color.GRAY),
                sg.Slider(default_value=0.8,range=((0,1)),resolution=0.1,
                orientation='horizontal',disable_number_display=True,enable_events=True,k='-lora_alpha_slider-',expand_x=False,s=(15,10)),                                 
                sg.Text('Lora'),
                sg.Combo(sorted(lora_models_list), default_value=sg.user_settings_get_entry("selected_lora", ''), size=(40, 1), key="-selected_lora-",expand_x=False,enable_events=True, readonly=True),  
                sg.I(visible=False,key='-lora_path-',enable_events=True),
                sg.FolderBrowse('Set lora folder',enable_events=True)                            
            ],  
    ]
    return layout


def events(event, values, window):
        if event == '-models_path-':
            models_path_directory = sg.user_settings_get_entry("models_path", sg.user_settings_set_entry("models_path", values['-models_path-']))
            models_list = []
            if models_path_directory:
                for filename in os.listdir(models_path_directory):
                    if filename.endswith(tuple(extensions)):
                        models_list.append(filename)
                window['-selected_model-'].update(values=sorted(models_list))
                
        if event == '-selected_model-':
            sg.user_settings_set_entry("selected_model", values['-selected_model-'])


        if event == '-lora_path-':
            lora_models_path_directory = sg.user_settings_get_entry("lora_models_path", sg.user_settings_set_entry("lora_models_path", values['-lora_path-']))
            print("lora_models_path_directory",lora_models_path_directory)
            models_list = []
            if lora_models_path_directory:
                for filename in os.listdir(lora_models_path_directory):
                    if filename.endswith(tuple(extensions)):
                        models_list.append(filename)
                window['-selected_lora-'].update(values=sorted(models_list))

        if event == '-selected_lora-':
            sg.user_settings_set_entry("selected_lora", values['-selected_lora-'])            