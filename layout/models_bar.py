import PySimpleGUI as sg
from util.const import *
import util.colors as color

import os
LORA_PATH ='lora_models_path'
MODEL_PATH ='models_path'

def set_models_path(extensions, models_path_directory=None, default_models_path='models/checkpoints', settings_key='models_path', recursive=False):

    file_list = [
        ""
    ]

    if not models_path_directory:
        sg.user_settings_set_entry(settings_key, default_models_path)
        models_path_directory = sg.user_settings_get_entry(settings_key, '')

    if models_path_directory and os.path.isdir(models_path_directory):
        try:
            if recursive:
                for root, dirs, files in os.walk(models_path_directory):
                    for filename in files:
                        if isinstance(extensions, (list, tuple)) and filename.endswith(tuple(extensions)):
                            full_path = os.path.join(root, filename)
                            relative_path = os.path.relpath(full_path, models_path_directory)
                            file_list.append(relative_path)
            else:
                for filename in os.listdir(models_path_directory):
                    if isinstance(extensions, (list, tuple)) and filename.endswith(tuple(extensions)):
                        file_list.append(filename)
                    
        except PermissionError:
            sg.popup_error(f"Permission denied when accessing directory: {models_path_directory}")

    return file_list

use_sub_folders_model = sg.user_settings_get_entry("use_sub_folders_model")
use_sub_folders_model_lora = sg.user_settings_get_entry("use_sub_folders_lora")

models_list = set_models_path(extensions, sg.user_settings_get_entry(MODEL_PATH, ''), settings_key=MODEL_PATH, recursive=use_sub_folders_model)
lora_models_list = set_models_path(extensions, sg.user_settings_get_entry(LORA_PATH, ''), settings_key=LORA_PATH, recursive=use_sub_folders_model_lora)

def create_layout():

    layout = [
            [
                sg.Frame('Model',[
                    [    
                        sg.Combo(sorted(models_list), default_value=sg.user_settings_get_entry("selected_model", ''), size=(80, 1), key="-selected_model-",expand_x=True,enable_events=True, readonly=True),  
                        sg.Checkbox('Sub-Folders',k='-use_sub_folders_model-',default=use_sub_folders_model,enable_events=True),

                        sg.I(visible=False,key='-models_path-',enable_events=True),
                        sg.FolderBrowse('Set Folder',enable_events=True),
                        sg.Button('Reload',k='-reload_models_path-'),  
                        sg.Button('Open Folder',k='-open_models_path-'),                           
                    ],    
                                        
                    ],expand_x=True,element_justification='l',vertical_alignment='l',relief=sg.RELIEF_SOLID,border_width=0,visible=True,background_color=color.DARK_GRAY
                ),
            
                sg.Frame('LoRa',[
                    [    
                        sg.Combo(sorted(lora_models_list), default_value=sg.user_settings_get_entry("selected_lora", ''), size=(80, 1), key="-selected_lora-",expand_x=True,enable_events=True, readonly=True),  
                        sg.Checkbox('Sub-Folders',k='-use_sub_folders_lora-',default=use_sub_folders_model_lora,enable_events=True),
                        sg.I(visible=False,key='-lora_path-',enable_events=True),
                        sg.FolderBrowse('Set Folder',enable_events=True),  
                        sg.Button('Reload',k='-reload_lora_path-'),    
                        sg.Button('Open Folder',k='-open_lora_path-'),  
                    ],    
                                    
                    ],expand_x=True,element_justification='l',vertical_alignment='l',relief=sg.RELIEF_SOLID,border_width=0,visible=True,background_color=color.DARK_GRAY
                ),                                      
            ],  

    ]
    return layout

def events(event, values, window):    

    if event == '-use_sub_folders_model-':
        sg.user_settings_get_entry("use_sub_folders_model", sg.user_settings_set_entry("use_sub_folders_model", values['-use_sub_folders_model-']))

    if event == '-use_sub_folders_lora-':
        sg.user_settings_get_entry("use_sub_folders_lora", sg.user_settings_set_entry("use_sub_folders_lora", values['-use_sub_folders_lora-']))

    if event == '-models_path-':
        models_path_directory = sg.user_settings_get_entry(MODEL_PATH, sg.user_settings_set_entry(MODEL_PATH, values['-models_path-']))
        models_list = set_models_path(extensions, models_path_directory, settings_key=MODEL_PATH, recursive=values['-use_sub_folders_model-'])
        if models_list:
            window['-selected_model-'].update(values=sorted(models_list))
                
    if event == '-selected_model-':
        sg.user_settings_set_entry("selected_model", values['-selected_model-'])

    if event == '-lora_path-':
        lora_models_path_directory = sg.user_settings_get_entry(LORA_PATH, sg.user_settings_set_entry(LORA_PATH, values['-lora_path-']))
        lora_models_list = set_models_path(extensions, lora_models_path_directory, settings_key=LORA_PATH, recursive=values['-use_sub_folders_lora-'])
        if lora_models_list:
            window['-selected_lora-'].update(values=sorted(lora_models_list))
                
    if event == '-selected_lora-':
        sg.user_settings_set_entry("selected_lora", values['-selected_lora-'])

    if event == '-reload_models_path-':
        models_path_directory = sg.user_settings_get_entry(MODEL_PATH)
        models_list = set_models_path(extensions, models_path_directory, settings_key=MODEL_PATH, recursive=values['-use_sub_folders_model-'])
        if models_list:
            window['-selected_model-'].update(values=sorted(models_list))

    if event == '-reload_lora_path-':
        lora_models_path_directory = sg.user_settings_get_entry(LORA_PATH)
        lora_models_list = set_models_path(extensions, lora_models_path_directory, settings_key=LORA_PATH, recursive=values['-use_sub_folders_lora-'])
        if lora_models_list:
            window['-selected_lora-'].update(values=sorted(lora_models_list))

    if event == '-open_models_path-':    
        if sg.user_settings_get_entry(MODEL_PATH):
            os.startfile(os.path.abspath(sg.user_settings_get_entry(MODEL_PATH)))   
                     
    if event == '-open_lora_path-':    
        if sg.user_settings_get_entry(LORA_PATH):
            os.startfile(os.path.abspath(sg.user_settings_get_entry(LORA_PATH)))                 