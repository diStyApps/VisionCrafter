import PySimpleGUI as sg
import textwrap
import os
import io
import subprocess
import shlex
from PIL import Image, ImageFilter, ImageOps,ImageTk
import threading
import time
from datetime import datetime as dt ,timedelta
# import requests
import math 
import numpy as np
from moviepy.editor import AudioFileClip, VideoFileClip 
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import pandas as pd
import webbrowser 
import uuid
import psutil
import util.json_tools as jt
from util.const import *
from repos.animatediff.scripts.animate import main as animate_main
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
from argparse import Namespace
from dataclasses import dataclass, field,asdict
from typing import List, Union
from omegaconf import OmegaConf
from threading import Thread
import vlc
from sys import platform as PLATFORM
import util.progress_bar_custom as cpbar
import timeit
import torch
import torchaudio
import soundfile as sf
from moviepy.editor import VideoFileClip, AudioFileClip
import numpy as np
import tempfile
from pydub import AudioSegment
import shutil
import tempfile
import logging
from pydub import AudioSegment
import tempfile
# -------------------------------------------------------------------
# Constants, defaults, Base64 icons

current_folder = os.getcwd()

def main(): 
    try:
        sg.theme('Dark Gray 15')
        total_steps_progress_bar = 0
        # jt.create_preferences_init()
        file_list = []

        add_music_post_video_path =''
        set_models_path(file_list, extensions, sg.user_settings_get_entry("models_path", ''))

        left_col_n = [
                        [
                            sg.Frame('Prompt',[
                                [    
                                    sg.Frame('',[
                                            [    
                                                sg.MLine("",key="-prompt-",visible=True,border_width=0,sbar_width=20,sbar_trough_color=0,no_scrollbar=True,
                                                autoscroll=False, auto_refresh=True,size=(40,10),pad=(5,5),expand_x=True,expand_y=True,font="Ariel 11"),
                                            ],    
                                                                
                                            ],expand_x=True,element_justification='center',vertical_alignment='center',s=(150,150),relief=sg.RELIEF_SOLID,border_width=0,visible=True,background_color=COLOR_DARK_GRAY
                                        ),
                                ],    
                                                    
                                ],expand_x=True,element_justification='center',vertical_alignment='center',s=(150,150),relief=sg.RELIEF_SOLID,border_width=0,visible=True,background_color=GRAY
                            ),
                        ],
                        [
                            sg.Frame('Negative',[
                                [    
                                    sg.Frame('',[
                                        [    
                                            sg.MLine("",key="-negative_prompt-",visible=True,border_width=0,sbar_width=20,sbar_trough_color=0,no_scrollbar=True,
                                            autoscroll=False, auto_refresh=True,size=(10,10),pad=(5,5),expand_x=True,expand_y=True,font="Ariel 11"),
                                        ],     
                                                                
                                            ],expand_x=True,element_justification='center',vertical_alignment='center',s=(150,150),relief=sg.RELIEF_SOLID,border_width=0,visible=True,background_color=COLOR_DARK_GRAY
                                        ),
                                ],    
                                                    
                                ],expand_x=True,element_justification='center',vertical_alignment='center',s=(150,150),relief=sg.RELIEF_SOLID,border_width=0,visible=True,background_color=GRAY
                            ),
                        ],     
                        [
                            sg.Combo(prompts_list, default_value=sg.user_settings_get_entry("selected_prompt", ''), size=(40, 10), key="-selected_prompt-",expand_x=True,enable_events=True, readonly=True), 
                            sg.Button('Set',k='-set_prompt-'),
                            
                            sg.Combo(prompts_neg_list, default_value=sg.user_settings_get_entry("selected_neg_prompt", ''), size=(40, 10), key="-selected_neg_prompt-",expand_x=True,enable_events=True, readonly=True),  
                            sg.Button('Set',k='-set_neg_prompt-') ,
                        ],                      
                        [
                            sg.Frame('Music',[
                                [    
                                        sg.Frame('Prompt',[
                                            [    
                                                sg.Frame('',[
                                                    [    
                                                        sg.MLine("Harp,bells,fluts,fantasy,nightelf,wind",key="-add_music_prompt-",visible=True,border_width=0,sbar_width=20,sbar_trough_color=0,no_scrollbar=True,
                                                        autoscroll=False, auto_refresh=True,size=(2,1),pad=(5,5),expand_x=True,expand_y=False,font="Ariel 11"),
                                                    ],     
                                                                            
                                                        ],expand_x=True,element_justification='center',vertical_alignment='center',relief=sg.RELIEF_SOLID,border_width=0,visible=True,background_color=COLOR_DARK_GRAY
                                                    ),
                                            ], 
                                            [
                                                sg.Combo(music_prompts_list, default_value=sg.user_settings_get_entry("selected_music_prompt", ''), size=(40, 10), key="-selected_music_prompt-",expand_x=True,enable_events=True, readonly=True), 
                                                sg.Button('Set',k='-set_music_prompt-'),    
                                            ],         
                                                                        
                                            ],expand_x=True,element_justification='center',vertical_alignment='center',relief=sg.RELIEF_SOLID,border_width=0,visible=True,background_color=GRAY
                                        ),
                                ],   
                                [ 
                                        sg.Frame('',[  
                                            [
                                                sg.T('Audio models'),
                                                sg.Combo(audio_model_list, default_value="melody", size=(40, 10), key="-selected_audio_model-",expand_x=False,enable_events=True, readonly=True),                                               
                                                sg.Checkbox('Add to video',k='-add_music_cb-',default=False),  
                                            ]  
                                                                
                                            ],expand_x=True,element_justification='l',vertical_alignment='l',relief=sg.RELIEF_SOLID,border_width=0,visible=True
                                        ),
                                ],                                            
                                ],expand_x=True,element_justification='l',vertical_alignment='l',relief=sg.RELIEF_SOLID,border_width=0,visible=True,background_color=GRAY
                            ),
                        ],                       
            
                        [
                            sg.Frame('',[
                                                            [
                                    sg.T('Seed',s=(10,1)),
                                    sg.In(-1,k='-seed-',s=(20,5),justification='center'),
                                    sg.Slider(default_value=-1,range=((-1,99999999999999)),resolution=1,
                                    orientation='horizontal',disable_number_display=True,enable_events=True,k='-seed_slider-',expand_x=True,s=(10,10)), 
                                ],  

                                [
                                    sg.T('Steps',s=(10,1)),
                                    sg.In(20,k='-sampling_steps-',s=(5,5),justification='center'),
                                    sg.Slider(default_value=20,range=((1,600)),resolution=1,
                                    orientation='horizontal',disable_number_display=True,enable_events=True,k='-sampling_steps_slider-',expand_x=True,s=(10,10)), 
                                    sg.T('Batch count',s=(20,1)),
                                    sg.In(1,k='-batch_count-',s=(5,5),justification='center'),
                                    sg.Slider(default_value=1,range=((1,100)),resolution=1,
                                    orientation='horizontal',disable_number_display=True,enable_events=True,k='-batch_count_slider-',expand_x=True,s=(10,10)),                 
                                ],    
                                [
                                    sg.T('Width',s=(10,1)),
                                    sg.In(512,k='-width-',s=(5,5),justification='center'),
                                    sg.Slider(default_value=512,range=((256,2048)),resolution=32,
                                    orientation='horizontal',disable_number_display=True,enable_events=True,k='-width_slider-',expand_x=True,s=(10,10)),   
                                    sg.T('Height',s=(10,1)),
                                    sg.In(512,k='-height-',s=(5,5),justification='center'),
                                    sg.Slider(default_value=512,range=((256,2048)),resolution=32,
                                    orientation='horizontal',disable_number_display=True,enable_events=True,k='-height_slider-',expand_x=True,s=(10,10)),                 
                                ],              
                                [
                                    sg.T('CFG Scale',s=(10,1)),
                                    sg.In(7.5,k='-cfg_scale-',s=(5,5),justification='center'),
                                    sg.Slider(default_value=7.5,range=((1,30)),resolution=0.5,
                                    orientation='horizontal',disable_number_display=True,enable_events=True,k='-cfg_scale_slider-',expand_x=True,s=(10,10)), 
                                ],  
            

                                [
                                    sg.T('Length in sec',s=(10,1)),
                                    sg.In(2,k='-length-',s=(5,5),justification='center',disabled=True,use_readonly_for_disable=True,disabled_readonly_background_color=GRAY),
                                    sg.Slider(default_value=2,range=((1,60)),resolution=1,
                                    orientation='horizontal',disable_number_display=True,enable_events=True,k='-length_slider-',expand_x=True,s=(10,10)),   
                                    sg.T('Motion modules',s=(15,1)),
                                    sg.Checkbox('1.4',k='-motion_module_1.4-',default=True),
                                    sg.Checkbox('1.5',k='-motion_module_1.5-',default=False),  

                                    sg.T('Context length',s=(12,1),visible=False),
                                    sg.In(0,k='-context_length-',s=(5,5),justification='center',visible=False),
                                    sg.Slider(default_value=0,range=((0,48)),resolution=1,
                                    orientation='horizontal',disable_number_display=True,enable_events=True,k='-context_length_slider-',expand_x=True,s=(10,10),visible=False),          
                                    sg.T('Context stride',s=(12,1),visible=False),
                                    sg.In(0,k='-context_stride-',s=(5,5),justification='center',visible=False),
                                    sg.Slider(default_value=0,range=((0,48)),resolution=1,
                                    orientation='horizontal',disable_number_display=True,enable_events=True,k='-context_stride_slider-',expand_x=True,s=(10,10),visible=False),   
                                ],          
                            ],expand_x=True,relief=sg.RELIEF_SOLID,border_width=0,visible=True),   
                        ],   
                        # terminal     
                        [
                            sg.MLine( k='-ML2-', reroute_stdout=True,write_only=False,reroute_cprint=True,
                            background_color='black', text_color='white', autoscroll=True, auto_refresh=True,expand_x=True,expand_y=True,visible=True)
                        ],
            ]

        center_col_n = [     
            [
                    sg.Frame('',[
                    
                        [sg.Image("",expand_x=True,k='-vid_out-',background_color="black")
                        ],               
                    ],expand_x=True,element_justification='center',relief=sg.RELIEF_FLAT,border_width=0,background_color=GRAY_9900,vertical_alignment='center',s=(400,400),visible=True), 
            ], 
            [
                
                btn('previous'), btn('play'), btn('next'), btn('stop'),sg.Button('Open Folder',k='-output_open_folder-',expand_x=True),
            ],        
            [
                sg.Button('Generate',k='-generate-',expand_x=True,expand_y=True,font='Arial 12 bold',button_color=('#69823c', None),visible=True),
            ],  
            [
                    sg.Frame('Add Post Music ',[
                    [
                        sg.T('File',s=(10,1)),
                        sg.Input(k='-add_music_post_video_file-',enable_events=True,expand_x=True),sg.FileBrowse(k=f'-post_process_FileBrowse-',file_types=(video_file_ext)) ,     
                    ],
                    [ 
                        sg.T('Folder',s=(10,1)),
                        sg.Input(k='-add_music_post_video_folder-',enable_events=True,expand_x=True),sg.FolderBrowse(k=f'-post_process_FolderBrowse-') ,        
                    ],                
                    [

                        sg.T('Duration',s=(20,1)),
                        sg.In(2,k='-duration_music_post-',s=(5,5),justification='center',disabled=True,use_readonly_for_disable=True,disabled_readonly_background_color=GRAY),
                        sg.Slider(default_value=2,range=((1,30)),resolution=1,
                        orientation='horizontal',disable_number_display=True,enable_events=True,k='-duration_music_post_slider-',expand_x=True,s=(10,10)),        


                    ],   
                    [
                        sg.Button('Add/Replace',k='-add_music_post-',expand_x=True),
                        # sg.Button('Play',k='-play_music_post-',expand_x=True),
                    ]            
                    ],expand_x=True,element_justification='center',relief=sg.RELIEF_FLAT,border_width=0,background_color=GRAY_9900,vertical_alignment='center',s=(400,400),visible=True), 
            ],            
        ]

        #Output
        right_col = [
            #Output display
            [
                sg.Frame('Output',[
                        # [sg.Text('FileName',k='-OUTPUT_IN-',enable_events=True,expand_x=True)],
                        [sg.Image('',expand_x=True,k='-OUTPUT_FILE-')],
                    ],expand_x=True,element_justification='center',vertical_alignment='center',s=(400,400),visible=True
                )    
            ],
            #Output controls
            [
                sg.Button('Preview',k='-output_preview-',expand_x=True),
                sg.Button('Open Folder',k='-output_reveal_folder-',expand_x=True),
            ],          

            [
                sg.Frame('Post Process',[
                        [
                            sg.Text('0 x 0',k='-post_process_file_size_display-',expand_x=True)
                        ],
                        [
                            sg.Input(k='-post_process_file_input-',enable_events=True,expand_x=True),sg.FileBrowse(initial_folder='./output/videos',k=f'-post_process_FileBrowse-',file_types=(video_file_ext)) 
                        ],
                    ],expand_x=True,visible=False
                )
            ],             
        ]

        layout = [ 

                [
                    sg.Frame('',[
                        [                      
                                sg.Text('Help support this project'),
                                sg.Button(image_data=patreon,key='PATREON_BTN_KEY',button_color=(GRAY_9900)),            
                        ],
                        ],expand_x=True,element_justification='r',border_width=0,pad=(0,0),relief=sg.RELIEF_FLAT
                    ),
                ],        
                [
                    [
                                sg.Text('Model'),
                                sg.Combo(sorted(file_list), default_value=sg.user_settings_get_entry("selected_model", ''), size=(80, 1), key="-selected_model-",expand_x=False,enable_events=True, readonly=True),  
                                sg.I(visible=False,key='-models_path-',enable_events=True),
                                sg.FolderBrowse('Set models folder',enable_events=True)
                    ],
                ],    
                [
                            cpbar.full_layout("-pbar_steps-",visible=True,it_name="step"),
                            cpbar.min_layout("-pbar_frames-",visible=True,it_name="fr"),
                            cpbar.full_layout("-pbar_samples-",visible=True,it_name="sample",show_it_per_sec=False),
                ],                          
                [
                    sg.Column(left_col_n, key='c1', element_justification='l', expand_x=True,expand_y=True,visible=True),
                    sg.Column(center_col_n, key='c2', element_justification='c', expand_x=True,expand_y=True,visible=True),
                    #Output
                    sg.Column(right_col, key='c3', element_justification='r', expand_x=True,expand_y=True,visible=False)
                ],      
        ]

        window = sg.Window(f'{NAME} - {VER}',layout,finalize=True, resizable=True)
        window.Maximize()
        flatten_ui_elements(window)
        window['-vid_out-'].expand(True, True)
        inst, list_player, media_list = init_vlc_player(window)

        while True:
            event, values = window.read(timeout=1000)
            if event == sg.WIN_CLOSED:
                break
            def setup():
                pass
            # setup()

            sliders(values,event,window)

            if event == '-models_path-':
                models_path_directory = sg.user_settings_get_entry("models_path", sg.user_settings_set_entry("models_path", values['-models_path-']))
                print("models_path_directory",models_path_directory)
                file_list = []
                if models_path_directory:
                    for filename in os.listdir(models_path_directory):
                        if filename.endswith(tuple(extensions)):
                            file_list.append(filename)
                    window['-selected_model-'].update(values=sorted(file_list))
                    
            if event == '-selected_model-':
                sg.user_settings_set_entry("selected_model", values['-selected_model-'])

            if event == '-generate-':
                prompts  = []
                negative_prompts = []
                batch_count = int(values['-batch_count-'])
                prompt = values['-prompt-']
                negative_prompt = values['-negative_prompt-']

                for i in range(batch_count):
                    prompts.append(prompt)
                    negative_prompts.append(negative_prompt)
                

                steps = int(values['-sampling_steps-'])
                cfg_scale = float(values['-cfg_scale-'])
                seed = int(values['-seed-'])
                width = int(values['-width-'])
                height = int(values['-height-'])
                length = int(values['-length-'])
                length = (length * 8)
                context_length=int(values['-context_length-'])
                context_stride = int(values['-context_stride-'])

                selected_model = sg.user_settings_get_entry("selected_model", '')
                models_path_directory = sg.user_settings_get_entry("models_path", '')
                models_path_directory = os.path.normpath(os.path.join(current_folder, f"{models_path_directory}/{selected_model}"))


                base = ""
                motion_modules_mm_sd_v14 = os.path.normpath(os.path.join(current_folder, "repos/animatediff/models/Motion_Module/mm_sd_v14.ckpt"))
                motion_modules_mm_sd_v15 = os.path.normpath(os.path.join(current_folder, "repos/animatediff/models/Motion_Module/mm_sd_v15.ckpt"))
                pretrained_model= os.path.normpath(os.path.join(current_folder, "repos/animatediff/models/StableDiffusion/stable-diffusion-v1-5"))
                # embeddings_folder= os.path.normpath(os.path.join(current_folder, "repos/animatediff/models/embeddings"))

                config_path = os.path.normpath(os.path.join(current_folder, "repos/animatediff/configs/prompts/result.yaml"))
                inference_config_path = os.path.normpath(os.path.join(current_folder, "repos/animatediff/configs/inference/inference.yaml"))
                motion_modules = []
                if values['-motion_module_1.4-']:
                    motion_modules.append(motion_modules_mm_sd_v14)
                if values['-motion_module_1.5-']:
                    motion_modules.append(motion_modules_mm_sd_v15)
                

                if motion_modules:    
                    config = ConfigInit(
                        path=models_path_directory,
                        base=base,
                        additional_networks=[],
                        motion_module=motion_modules,
                        seed=seed,
                        steps=steps,
                        guidance_scale=cfg_scale,
                        lora_alpha=0.8,
                        prompt=prompts,
                        n_prompt=negative_prompts
                    )        
                    config_dict = asdict(config)
                    config_dict = {"config": config_dict}
                    config_omega = OmegaConf.create(config_dict)
                    OmegaConf.save(config=config_omega, f=config_path)
                    args = Namespace(
                        pretrained_model_path=pretrained_model, 
                        inference_config=inference_config_path, 
                        config=config_path, 
                        fp32=False, 
                        disable_inversions=False, 
                        # context_length=context_length, 
                        context_length=16, 
                        # context_stride=context_stride, 
                        context_stride=0, 
                        context_overlap=-1, 
                        L=length, 
                        W=width, 
                        H=height,
                        # embeddings_folder=embeddings_folder
                    )            
                    def animate_main_t(args):
                        animate_main(args,window)

                    media_list = inst.media_list_new([])
                    # window['-pbar_steps_frame-'].update(visible=True)
                    
                    threading.Thread(target=animate_main_t, args=(args,), daemon=True).start() 
                else:
                    print("No motion module selected")

            if event == '-single_video_generated-':
                add_music_post_video_path = values['-single_video_generated-']
                add_and_play_video(list_player, media_list, add_music_post_video_path)

            if event == '-video_grid_generated-':
                if int(values['-batch_count-'])> 1:
                    add_music_post_video_path = values['-video_grid_generated-']
                    window['-add_music_post_video_file-'].update("")
                    window['-add_music_post_video_folder-'].update(add_music_post_video_path)
                    add_music_post_video_path_type = "folder"
                elif int(values['-batch_count-'])==1:
                    window['-add_music_post_video_file-'].update(add_music_post_video_path) 
                    window['-add_music_post_video_folder-'].update("")
                    add_music_post_video_path_type = "file" 
                if values['-add_music_cb-']:
                    window.write_event_value('-add_music_post-', add_music_post_video_path)

            if event == '-total_steps_progress_bar-':
                total_steps_start_time = dt.today().timestamp()

                total_steps_progress_bar = int(values['-total_steps_progress_bar-'])

            if event == '-total_frames_progress_bar-':
                total_frames_progress_bar = int(values['-total_frames_progress_bar-'])
                total_frames_start_time = dt.today().timestamp()

            if event == '-total_samples_progress_bar-':
                total_samples_progress_bar = int(values['-total_samples_progress_bar-'])
                total_samples_start_time = dt.today().timestamp()

            if event == '-steps_progress_bar-':
                step = int(values['-steps_progress_bar-'])
                cpbar.update_full(step,total_steps_progress_bar,total_steps_start_time,window,"-pbar_steps-","step")

            if event == '-frames_progress_bar-':
                frame = int(values['-frames_progress_bar-'])
                cpbar.update_min(frame,total_frames_progress_bar,total_frames_start_time,window,"-pbar_frames-","frame")

            if event == '-sample_progress_bar-':
                sample = int(values['-sample_progress_bar-'])
                cpbar.update_full(sample,total_samples_progress_bar,total_samples_start_time,window,"-pbar_samples-","sample")

            if event == '-output_open_folder-':    
                if add_music_post_video_path:
                    startfile_path = os.path.dirname(add_music_post_video_path)        
                    os.startfile(os.path.abspath(startfile_path))

            if event == '-set_prompt-':
                prompt = values['-selected_prompt-']
                window['-prompt-'].update(prompt)

            if event == '-set_neg_prompt-':
                prompt = values['-selected_neg_prompt-']
                window['-negative_prompt-'].update(prompt)

            if event == '-set_music_prompt-':
                prompt = values['-selected_music_prompt-']
                window['-add_music_prompt-'].update(prompt)

            if event == '-add_music_post_video_file-':
                add_music_post_video_path = values['-add_music_post_video_file-']
                add_music_post_video_path_type = "file"
                window['-add_music_post_video_folder-'].update("")

            if event == '-add_music_post_video_folder-':
                window['-add_music_post_video_file-'].update("")
                add_music_post_video_path = values['-add_music_post_video_folder-']
                add_music_post_video_path_type = "folder"


            if event == '-length_slider-': 
                length = int(values['-length_slider-'])
                window['-duration_music_post_slider-'].update(length)
            


            if event == '-add_music_post-':
                if values['-add_music_post_video_folder-'] or values['-add_music_post_video_file-']:
                    media_list = inst.media_list_new([])
                    audio_model_version = values['-selected_audio_model-']
                    add_music_prompt = values['-add_music_prompt-']
                    duration = int(values['-duration_music_post-'])

                    if add_music_post_video_path_type == "file":
                        output_video_filepath = add_audio_to_video(audio_model_version, add_music_prompt, "", duration, 250, 0, 1, 3, os.path.abspath(add_music_post_video_path))
                        add_and_play_video(list_player, media_list, output_video_filepath)
                        
                    elif add_music_post_video_path_type == "folder":
                        for filename in os.listdir(add_music_post_video_path):
                            # if filename.endswith(('.mp4', '.avi', '.mov', '.flv', '.wmv')): # add more formats if needed
                            if filename.endswith(('.mp4')): # add more formats if needed
                                full_file_path = os.path.join(add_music_post_video_path, filename)
                                output_video_filepath = add_audio_to_video(audio_model_version, add_music_prompt, "", duration, 250, 0, 1, 3, full_file_path)
                                add_and_play_video(list_player, media_list, output_video_filepath)
                else:    
                    sg.Popup('Please select a video file or folder')           

            if event == '-play_music_post-':
                if media_list.count() > 0:
                    add_and_play_video(list_player, media_list, output_video_filepath)
                else:
                    sg.Popup('Nothing to play')

            if event == 'play':
                list_player.play()
            if event == 'pause':
                list_player.pause()
            if event == 'stop':
                def stop():
                    list_player.stop()
                threading.Thread(target=stop, args=(), daemon=True).start() 
            if event == 'next':
                def next():
                    list_player.next()
                    list_player.play()
                threading.Thread(target=next, args=(), daemon=True).start()
            if event == 'previous':
                def previous():
                    list_player.previous()                 
                    list_player.previous()
                    list_player.play()
                threading.Thread(target=previous, args=(), daemon=True).start()

            if event == 'PATREON_BTN_KEY':
                webbrowser.open("https://www.patreon.com/distyx")   
        window.close()
    except Exception as e:
        print(f"An error occurred: {e}")


@dataclass
class ConfigInit:
    base: str
    path: str
    # init_image: str
    motion_module: Union[str, List[str]]
    steps: int
    guidance_scale: float
    lora_alpha: float
    additional_networks: List[str] = field(default_factory=list)
    prompt: List[str] = field(default_factory=list)
    n_prompt: List[str] = field(default_factory=list)
    seed: List[int] = field(default_factory=list)

def flatten_ui_elements(window):
    for widget_key in window.key_dict.keys():
        try: 
            window[widget_key].Widget.config(relief='flat')
        except:
            # print("error",widget_key)
            pass

def display_notification(title, message, icon, display_duration_in_ms=DEFAULT_DISPLAY_DURATION_IN_MILLISECONDS, use_fade_in=True, alpha=0.9, location=None):

    # Compute location and size of the window
    message = textwrap.fill(message, 50)
    win_msg_lines = message.count("\n") + 1

    screen_res_x, screen_res_y = sg.Window.get_screen_size()
    win_margin = WIN_MARGIN  # distance from screen edges
    win_width, win_height = 500, 100 + (14.8 * win_msg_lines)
    win_location = location if location is not None else (screen_res_x - win_width - win_margin, screen_res_y - win_height - win_margin)

    layout = [[sg.Graph(canvas_size=(win_width, win_height), graph_bottom_left=(0, win_height), graph_top_right=(win_width, 0), key="-GRAPH-",
                        background_color=WIN_COLOR, enable_events=True)]]

    window = sg.Window(title, layout, background_color=WIN_COLOR, no_titlebar=True,
                       location=win_location, keep_on_top=True, alpha_channel=0, margins=(0, 0), element_padding=(0, 0),
                       finalize=True)

    window["-GRAPH-"].draw_rectangle((win_width, win_height), (-win_width, -win_height), fill_color=WIN_COLOR, line_color=WIN_COLOR)
    window["-GRAPH-"].draw_image(data=icon, location=(20, 20))
    window["-GRAPH-"].draw_text(title, location=(64, 20), color=TEXT_COLOR, font=("Arial", 12, "bold"), text_location=sg.TEXT_LOCATION_TOP_LEFT)
    window["-GRAPH-"].draw_text(message, location=(64, 44), color=TEXT_COLOR, font=("Arial", 9), text_location=sg.TEXT_LOCATION_TOP_LEFT)

    # change the cursor into a "hand" when hovering over the window to give user hint that clicking does something
    window['-GRAPH-'].set_cursor('hand2')

    if use_fade_in == True:
        for i in range(1,int(alpha*100)):               # fade in
            window.set_alpha(i/100)
            event, values = window.read(timeout=20)
            if event != sg.TIMEOUT_KEY:
                window.set_alpha(1)
                break
        event, values = window(timeout=display_duration_in_ms)
        if event == sg.TIMEOUT_KEY:
            for i in range(int(alpha*100),1,-1):       # fade out
                window.set_alpha(i/100)
                event, values = window.read(timeout=20)
                if event != sg.TIMEOUT_KEY:
                    break
    else:
        window.set_alpha(alpha)
        event, values = window()

    window.close()
#region sliders

def slider(key,target_key,values,event,window):
    if event == key:
        slider = int(values[key])
        slider = slider_add_prefix_zero_for_time(slider)
        window[target_key].update(value=slider)    

def slider_float(key,target_key,values,event,window):
    if event == key:
        slider = values[key]
        window[target_key].update(value=slider)    

def slider_int(key,target_key,values,event,window):
    if event == key:
        slider = int(values[key])
        window[target_key].update(value=slider)  

def slider_add_prefix_zero_for_time(slider):
        if slider < 10:
            slider_prefi= f'0{slider}'
            slider_out = slider_prefi
        if slider >= 10:
            slider_out = slider
        return slider_out

def sliders(values,event,window):
    slider_int('-sampling_steps_slider-','-sampling_steps-',values,event,window)
    slider_float('-cfg_scale_slider-','-cfg_scale-',values,event,window)
    slider_int('-batch_count_slider-', '-batch_count-',values,event,window)
    slider_int('-width_slider-','-width-',values,event,window)
    slider_int('-height_slider-','-height-',values,event,window)
    slider_int('-seed_slider-','-seed-',values,event,window)
    slider_int('-length_slider-','-length-',values,event,window)
    slider_int('-context_length_slider-','-context_length-',values,event,window)
    slider_int('-context_stride_slider-','-context_stride-',values,event,window)
    slider_int('-duration_music_post_slider-','-duration_music_post-',values,event,window)
    slider_int('-length_slider-','-duration_music_post-',values,event,window)

#endregion sliders
    
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

def image_bio_video_player(image,size):
    image1 = image
    image1.thumbnail(size)
    bio = io.BytesIO()
    image1.save(bio,format="ppm")
    del image1
    return bio.getvalue()

def btn(name):
    return sg.Button(name, size=(6, 1),expand_x=True)

def init_vlc_player(window):
    inst = vlc.Instance('--quiet')
    list_player = inst.media_list_player_new()
    media_list = inst.media_list_new([])
    list_player.set_media_list(media_list)
    list_player.set_playback_mode(vlc.PlaybackMode.loop)
    player = list_player.get_media_player()

    if PLATFORM.startswith('linux'):
        player.set_xwindow(window['-vid_out-'].Widget.winfo_id())
    else:
        player.set_hwnd(window['-vid_out-'].Widget.winfo_id())
    return inst,list_player,media_list

def add_and_play_video(list_player, media_list, video_path):
    full_models_path_directory = os.path.normpath(os.path.join(current_folder, f"{video_path}"))
    media_list.add_media(full_models_path_directory)
    list_player.set_media_list(media_list)
    list_player.play()

def load_model(version):
    print("Loading model", version)
    return MusicGen.get_pretrained(version)

def predict(model, text, melody, duration, topk, topp, temperature, cfg_coef):
    global MODEL
    topk = int(topk)
    if MODEL is None or MODEL.name != model:
        MODEL = load_model(model)

    if duration > MODEL.lm.cfg.dataset.segment_duration:
        # raise gr.Error("MusicGen currently supports durations of up to 30 seconds!")
        print("MusicGen currently supports durations of up to 30 seconds!")
        return
    MODEL.set_generation_params(
        use_sampling=True,
        top_k=topk,
        top_p=topp,
        temperature=temperature,
        cfg_coef=cfg_coef,
        duration=duration,
    )

    if melody:
        sr, melody = melody[0], torch.from_numpy(melody[1]).to(MODEL.device).float().t().unsqueeze(0)
        # print(melody.shape)
        if melody.dim() == 2:
            melody = melody[None]
        melody = melody[..., :int(sr * MODEL.lm.cfg.dataset.segment_duration)]
        output = MODEL.generate_with_chroma(
            descriptions=[text],
            melody_wavs=melody,
            melody_sample_rate=sr,
            progress=False
        )
    else:
        output = MODEL.generate(descriptions=[text], progress=False)

    output = output.detach().cpu().numpy()
    return MODEL.sample_rate, output

def predict_and_save(model, text, melody, duration, topk, topp, temperature, cfg_coef, filename):
    global MODEL
    topk = int(topk)
    if MODEL is None or MODEL.name != model:
        MODEL = load_model(model)

    if duration > MODEL.lm.cfg.dataset.segment_duration:
        # raise gr.Error("MusicGen currently supports durations of up to 30 seconds!")
        print("MusicGen currently supports durations of up to 30 seconds!")
        return
    MODEL.set_generation_params(
        use_sampling=True,
        top_k=topk,
        top_p=topp,
        temperature=temperature,
        cfg_coef=cfg_coef,
        duration=duration,
    )

    if melody:
        sr, melody = melody[0], torch.from_numpy(melody[1]).to(MODEL.device).float().t().unsqueeze(0)
        # print(melody.shape)
        if melody.dim() == 2:
            melody = melody[None]
        melody = melody[..., :int(sr * MODEL.lm.cfg.dataset.segment_duration)]
        output = MODEL.generate_with_chroma(
            descriptions=[text],
            melody_wavs=melody,
            melody_sample_rate=sr,
            progress=False
        )
    else:
        output = MODEL.generate(descriptions=[text], progress=True)

    output = output.detach().cpu()
    output = output.squeeze()

    # Save the audio file
    audio_write(filename, output, MODEL.sample_rate, strategy="loudness", loudness_compressor=True)

    return MODEL.sample_rate, output

def save_audio(model, text, melody, duration, topk, topp, temperature, cfg_coef, filename):
    sample_rate, output = predict(model, text, melody, duration, topk, topp, temperature, cfg_coef)

    # Check the dimensions of the output and reduce if necessary
    if output.ndim > 2:
        output = output.squeeze()

    # Save the audio file
    audio_write(filename, torch.from_numpy(output), sample_rate, strategy="loudness", loudness_compressor=True)

def add_audio_to_video(model, text, melody, duration, topk, topp, temperature, cfg_coef, video_filepath, keep_audio=False, audio_format="mp3"):
    dir_path = os.path.dirname(video_filepath)
    logging.basicConfig(filename=os.path.join(dir_path, 'log.log'), level=logging.INFO)
    logging.info(f'Called add_audio_to_video with log: {locals()}')

    sample_rate, output = predict(model, text, melody, duration, topk, topp, temperature, cfg_coef)

    # Check the dimensions of the output and reduce if necessary
    if output.ndim > 2:
        output = output.squeeze()

    temp_audio_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_audio_filepath = temp_audio_file.name

    # Write the output audio data to the temporary file
    sf.write(temp_audio_file.name, output, sample_rate)

    # Create an AudioFileClip from the temporary audio file
    audio = AudioFileClip(temp_audio_file.name)

    # Load the original video
    video = VideoFileClip(video_filepath)

    # Set the audio of the video to the new audio
    video_with_audio = video.set_audio(audio)

    # Define the output video filename
    output_video_filepath = os.path.splitext(video_filepath)[0] + "_with_audio.mp4"

    # Write the video with audio to a file
    video_with_audio.write_videofile(output_video_filepath)

    # Close the resources
    audio.close()
    video.close()
    video_with_audio.close()
    temp_audio_file.close()  # Ensure the temporary file is also closed

    # If keep_audio is set to True, move the temp_audio_file to the output video directory
    if keep_audio:
        # Depending on the audio_format argument, save the file as .wav or .mp3
        if audio_format == "wav":
            output_audio_filepath = os.path.splitext(video_filepath)[0] + "_audio.wav"
            shutil.move(temp_audio_filepath, output_audio_filepath)
        elif audio_format == "mp3":
            output_audio_filepath = os.path.splitext(video_filepath)[0] + "_audio.mp3"
            audio = AudioSegment.from_wav(temp_audio_filepath)
            audio.export(output_audio_filepath, format="mp3")
            os.unlink(temp_audio_filepath)  # delete the temporary .wav file
        else:
            raise ValueError("Unsupported audio_format. Please choose either 'wav' or 'mp3'.")
        
    # output_video_filepath = add_text_to_video_ffmpeg(output_video_filepath, GITHUB, 'Bottom right', font_size=12, font_color='#817d73', font_file='fonts/roboto.ttf')
    
    return output_video_filepath

def add_text_to_video_ffmpeg(video_filepath, text, position, font_size=20, font_color='#FF02CC', font_file='fonts/roboto.ttf'):
    # Set position based on user input
    positions = {
        'Top center': 'x=(w-text_w)/2:y=10',
        'Bottom center': 'x=(w-text_w)/2:y=h-th-10',
        'Centered': 'x=(w-text_w)/2:y=(h-text_h)/2',
        'Top left': 'x=10:y=10',
        'Top right': 'x=w-tw-10:y=10',
        'Bottom left': 'x=10:y=h-th-10',
        'Bottom right': 'x=w-tw-10:y=h-th-10'
    }

    position_str = positions.get(position, 'x=10:y=10')  # Default to 'Top left' if input is not recognized
    
    output_filepath = os.path.splitext(video_filepath)[0] + "_with_text.mp4"

    part_1 = f"ffmpeg -y -i '{video_filepath}' -vf"
    part_2 = f'"drawtext=fontfile={font_file}:text={text}'
    part_3 = f':{position_str}:fontsize={font_size}:fontcolor={font_color}"'
    fin = f'{output_filepath}'

    call_string = f'{part_1} {part_2}{part_3} {fin}'

    call = shlex.split(call_string)
    subprocess.call(call)
    return output_filepath

prompts_list = [
    "",
    "a tiger sits in a magic forest,fantasy,magic,sparks,trees,grass", 
    "a beautiful landscape painting of a mountain and a lake",
    "best quality, masterpiece, 1girl, looking at viewer, blurry background, upper body, contemporary, dress",
    "masterpiece, best quality, 1girl, solo, cherry blossoms, hanami, pink flower, white flower, spring season, wisteria, petals, flower, plum blossoms, outdoors, falling petals, white hair, black eyes,",
    "best quality, masterpiece, 1boy, formal, abstract, looking at viewer, masculine, marble pattern",
    "best quality,single build,architecture, blue_sky, building,cloudy_sky, day, fantasy, fence, field, house, build,architecture,landscape, moss, outdoors, overgrown, path, river, road, rock, scenery, sky, sword, tower, tree, waterfall",
    "black_border, building, city, day, fantasy, ice, landscape, letterboxed, mountain, ocean, outdoors, planet, scenery, ship, snow, snowing, water, watercraft, waterfall, winter",
    "mysterious sea area, fantasy,build,concept",

    
    "Tomb Raider,Scenography,Old building",       
]
prompts_neg_list = [
     "",   
    "ugly,blur,jpeg artifacts,worst quality,low quality,normal quality,lowres,grayscale,EasyNegative,child",
    "badhandv4,easynegative,ng_deepnegative_v1_75t,verybadimagenegative_v1.3, bad-artist, bad_prompt_version2-neg, teeth",
    "easynegative,bad_construction,bad_structure,bad_wail,bad_windows,blurry,cloned_window,cropped,deformed,disfigured,error,extra_windows,extra_chimney,extra_door,extra_structure,extra_frame,fewer_digits,fused_structure,gross_proportions,jpeg_artifacts,long_roof,low_quality,structure_limbs,missing_windows,missing_doors,missing_roofs,mutated_structure,mutation,normal_quality,out_of_frame,owres,poorly_drawn_structure,poorly_drawn_house,signature,text,too_many_windows,ugly,username,uta,watermark,worst_quality",
    ]
audio_model_list = [
    "melody",
    "small",
    "medium",
    "large",
]
music_prompts_list = [
    "drum and bass beat with intense percussions",
    "classic reggae track with an electronic guitar solo",
    "80s electronic track with melodic synthesizers, catchy beat and groovy bass",
    "Pop dance track with catchy melodies, tropical percussion, and upbeat rhythms, perfect for the beach",
]
if __name__ == '__main__':
    
    main()
