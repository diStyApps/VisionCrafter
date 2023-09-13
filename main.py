import PySimpleGUI as sg
import os
import io
from PIL import Image, ImageFilter, ImageOps,ImageTk
import threading
from datetime import datetime as dt ,timedelta
from moviepy.editor import AudioFileClip, VideoFileClip 
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import webbrowser 

from argparse import Namespace
from dataclasses import dataclass, field,asdict
from typing import List, Union
from omegaconf import OmegaConf

from repos.animatediff.scripts.animate import main as animate_main
from repos.animatediff.scripts.animate import interrupt

import layout.navigation as navigation_layout
import layout.about as about_layout
import layout.txt2vid as txt2vid_layout
import layout.img2vid as img2vid_layout
import layout.models_bar as models_bar_layout

import util.json_tools as jt
from util.const import *
import util.colors as color
import util.icons as icon
import util.progress_bar_custom as cpbar
from util.sliders import sliders
from util.ui_tools import flatten_ui_elements,expand_column_helper,clear_items_keys
from util.vlc import init_vlc_player,add_and_play_video
from util.musicgen import add_audio_to_video
from util.wildcards import replace_wildcards_in_text

current_folder = os.getcwd()

def main(): 
    total_steps_progress_bar = 0
    # jt.create_preferences_init()
    length_warning_1 = True
    length_warning_2 = True
    add_music_post_video_path =''

    center_col_n = [     
        [
                sg.Frame('',[
                
                    [sg.Image("",expand_x=True,k='-vid_out-',background_color="black")
                    ],               
                ],expand_x=True,element_justification='center',relief=sg.RELIEF_FLAT,border_width=0,background_color=color.GRAY_9900,vertical_alignment='center',s=(400,400),visible=True), 
        ], 
        [
            
            btn('previous'), btn('play'), btn('next'), btn('stop'),sg.Button('Open Folder',k='-output_open_folder-',expand_x=True),
        ],        
        [
            sg.Button('Generate',k='-generate_validation-',expand_x=True,expand_y=True,font='Arial 12 bold',button_color=('#69823c', None),s=(10,2),visible=True),
            sg.Button('Interrupt',k='-interrupt-',expand_x=True,expand_y=True,font='Arial 12 bold',button_color=('#69823c', None),s=(10,2),visible=True),

        ],  
        [
 
                sg.Frame('Saving options',[
                [
                    sg.Checkbox('MP4',k='-save_mp4_format-',default=True,disabled=True),
                    sg.Checkbox('GIF',k='-save_gif_format-',default=True),
                    sg.Checkbox('Frames',k='-save_video_frames-',default=False),
                ],           
                ],expand_x=True,element_justification='l',relief=sg.RELIEF_FLAT,border_width=0,background_color=color.GRAY_9900,vertical_alignment='center',visible=True),                                 

        ],
                [
                    sg.Frame('Add Music',[
                        [    
                                sg.Frame('Prompt',[
                                    [    
                                        sg.Frame('',[
                                            [    
                                                sg.MLine("Harp,bells,fluts,fantasy,nightelf,wind",key="-add_music_prompt-",visible=True,border_width=0,sbar_width=20,sbar_trough_color=0,no_scrollbar=True,
                                                autoscroll=False, auto_refresh=True,size=(2,1),pad=(5,5),expand_x=True,expand_y=False,font="Ariel 11"),
                                            ],     
                                                                    
                                                ],expand_x=True,element_justification='center',vertical_alignment='center',relief=sg.RELIEF_SOLID,border_width=0,visible=True,background_color=color.DARK_GRAY
                                            ),
                                    ], 
                                    [
                                        sg.Combo(music_prompts_list, default_value=sg.user_settings_get_entry("selected_music_prompt", ''), size=(40, 10), key="-selected_music_prompt-",expand_x=True,enable_events=True, readonly=True), 
                                        sg.Button('Set',k='-set_music_prompt-'),    
                                    ],         
                                                                    
                                    ],expand_x=True,element_justification='center',vertical_alignment='center',relief=sg.RELIEF_SOLID,border_width=0,visible=True,background_color=color.GRAY
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
                        ],expand_x=True,element_justification='l',vertical_alignment='l',relief=sg.RELIEF_SOLID,border_width=0,visible=True,background_color=color.GRAY
                    ),
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
                    sg.In(2,k='-duration_music_post-',s=(5,5),justification='center',disabled=True,use_readonly_for_disable=True,disabled_readonly_background_color=color.GRAY),
                    sg.Slider(default_value=2,range=((1,30)),resolution=1,
                    orientation='horizontal',disable_number_display=True,enable_events=True,k='-duration_music_post_slider-',expand_x=True,s=(10,10)),        


                ],   
                [
                    sg.Button('Add/Replace',k='-add_music_post-',expand_x=True),
                    # sg.Button('Play',k='-play_music_post-',expand_x=True),
                ]            
                ],expand_x=True,element_justification='center',relief=sg.RELIEF_FLAT,border_width=0,background_color=color.GRAY_9900,vertical_alignment='center',s=(400,400),visible=True), 
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
                            sg.Button(image_data=icon.patreon,key='PATREON_BTN_KEY',button_color=(color.GRAY_9900)),            
                    ],
                    ],expand_x=True,element_justification='r',border_width=0,pad=(0,0),relief=sg.RELIEF_FLAT
                ),
            ],     
            # [
            #     sg.Column(models_bar_layout.create_layout(), key=MODELSBAR_COL, element_justification='l', expand_x=True,expand_y=True,visible=True),
            # ],                  
            [
                navigation_layout.create_layout()
            ],                
            [
                cpbar.full_layout("-pbar_steps-",visible=True,it_name="step"),
                cpbar.min_layout("-pbar_frames-",visible=True,it_name="fr"),
                cpbar.full_layout("-pbar_samples-",visible=True,it_name="sample",show_it_per_sec=False),
            ],                          

            [
                sg.Column(txt2vid_layout.create_layout(), key=TXT2VID_COL, element_justification='c', expand_x=True,expand_y=True,visible=True),
                sg.Column(img2vid_layout.create_layout(), key=IMG2VID_COL, element_justification='c', expand_x=True,expand_y=True,visible=False),
                sg.Column(about_layout.create_layout(), key=ABOUT_COL, element_justification='c', expand_x=True,expand_y=True,visible=False),
                # sg.Column(left_col_n, key='c1', element_justification='l', expand_x=True,expand_y=True,visible=False),
                sg.Column(center_col_n, key='c2', element_justification='c', expand_x=True,expand_y=True,visible=True),
                #Output
                # sg.Column(right_col, key='c3', element_justification='r', expand_x=True,expand_y=True,visible=False)
            ],      
    ]

    window = sg.Window(APP_TITLE,layout,finalize=True, resizable=True)
    window.Maximize()
    flatten_ui_elements(window)
    window['-vid_out-'].expand(True, True)
    inst, list_player, media_list = init_vlc_player(window)

    while True:
        event, values = window.read(timeout=1000)
        if event == sg.WIN_CLOSED:
            break
       
        setup()
        sliders(values,event,window)
        navigation_layout.handle_tab_event(event, window)
        about_layout.events(event)
        models_bar_layout.events(event,values,window)
        txt2vid_layout.events(event,values,window)

        if event == '-init_img_path-':
            if  len(values['-init_img_path-'].strip())>0:
                window['-use_init_img-'].update(True)
            else:
                window['-use_init_img-'].update(False)


        if event == '-generate_validation-':
            if values['-use_init_img-']:
                if all([values['-use_init_img-'], int(values['-height-']) == 512, int(values['-width-']) == 512]):
                    window.write_event_value('-generate-', values)
                else:
                    sg.Popup("The maximum init image generation size is 512x512")
            else:
                window.write_event_value('-generate-', values)
        if event == '-generate-':
            # print("generate",event)
            prompts  = []
            negative_prompts = []
            batch_count = int(values['-batch_count-'])
            prompt = values['-prompt-']
            negative_prompt = values['-negative_prompt-']

            for i in range(batch_count):
                # prompt = replace_wildcards_in_text(prompt)

                # print('prompt',[i],replace_wildcards_in_text(prompt))
                prompt_w = replace_wildcards_in_text(prompt)
                prompts.append(prompt_w)

                print(f'Prompt [#{i}] {prompt_w}') 
                print(f'')

                negative_prompts.append(negative_prompt)
            
            # print("prompts",prompts)
            steps = int(values['-sampling_steps-'])
            cfg_scale = float(values['-cfg_scale-'])
            seed = int(values['-seed-'])
            width = int(values['-width-'])
            height = int(values['-height-'])
            length = int(values['-length-'])
            length = (length * 8)
            context_length=int(values['-context_length-'])
            context_stride = int(values['-context_stride-'])
            lora_alpha = float(values['-lora_alpha-'])
            init_img_strength = float(values['-init_img_strength-'])
            init_img_path = values['-init_img_path-']
            save_gif_format = values['-save_gif_format-']
            save_video_frames = values['-save_video_frames-']
            use_lora = values['-use_lora-']

            selected_model = sg.user_settings_get_entry("selected_model", '')
            models_path_directory = sg.user_settings_get_entry("models_path", '')

            selected_lora = sg.user_settings_get_entry("selected_lora", '')
            lora_models_path_directory = sg.user_settings_get_entry("lora_models_path", '')

            selected_motion_module = sg.user_settings_get_entry("selected_motion_module", '')
            motion_modules_path_directory = sg.user_settings_get_entry("motion_modules_path", '')


            if selected_lora and use_lora:
                print("selected_lora",selected_lora)
                base = os.path.normpath(os.path.join(current_folder, f"{models_path_directory}/{selected_model}"))
                models_path_directory = os.path.normpath(os.path.join(current_folder, f"{lora_models_path_directory}/{selected_lora}"))                
            else:
                print("no lora")
                models_path_directory = os.path.normpath(os.path.join(current_folder, f"{models_path_directory}/{selected_model}"))
                base = ""

            # motion_modules_mm_sd_v14 = os.path.normpath(os.path.join(current_folder, "repos/animatediff/models/Motion_Module/mm_sd_v14.ckpt"))
            # motion_modules_mm_sd_v15 = os.path.normpath(os.path.join(current_folder, "repos/animatediff/models/Motion_Module/mm_sd_v15_v2.ckpt"))
            motion_module = os.path.normpath(os.path.join(current_folder, f"{motion_modules_path_directory}/{selected_motion_module}"))

            pretrained_model= os.path.normpath(os.path.join(current_folder, "repos/animatediff/models/StableDiffusion/stable-diffusion-v1-5"))
            # embeddings_folder= os.path.normpath(os.path.join(current_folder, "repos/animatediff/models/embeddings"))

            config_path = os.path.normpath(os.path.join(current_folder, "repos/animatediff/configs/prompts/result.yaml"))
            if is_v2(motion_module):
                inference_config_path = os.path.normpath(os.path.join(current_folder, "repos/animatediff/configs/inference/inference-v2.yaml"))
            else:
                inference_config_path = os.path.normpath(os.path.join(current_folder, "repos/animatediff/configs/inference/inference-v1.yaml"))
            if motion_module:    
                config = ConfigInit(
                    path=models_path_directory,
                    base=base,
                    additional_networks=[],
                    motion_module=motion_module,
                    seed=seed,
                    steps=steps,
                    guidance_scale=cfg_scale,
                    lora_alpha=lora_alpha,
                    prompt=prompts,
                    n_prompt=negative_prompts,
                    init_image=init_img_path,
                    init_img_strength=init_img_strength,

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
                    save_gif_format=save_gif_format,
                    save_video_frames=save_video_frames,                    
                    # embeddings_folder=embeddings_folder
                    init_image=init_img_path,
                    init_img_strength=init_img_strength,
                )            
                def animate_main_t(args):
                    stop_requested = False
                    animate_main(args,window)

                media_list = inst.media_list_new([])
                # window['-pbar_steps_frame-'].update(visible=True)
                
                threading.Thread(target=animate_main_t, args=(args,), daemon=True).start() 
            else:
                print("No motion module selected")

        if event == '-interrupt-':
            def interrupt_t():
                interrupt()

            media_list = inst.media_list_new([])
            # window['-pbar_steps_frame-'].update(visible=True)
            
            threading.Thread(target=interrupt_t, args=(), daemon=True).start()              

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
            if length > 6 and length_warning_1:
                sg.Popup("Warning", DURATION_WARN_1)
                length_warning_1 = False
            if length > 30 and length_warning_2:
                sg.Popup("Warning", DURATION_WARN_2)   
                length_warning_2 = False             
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


@dataclass
class ConfigInit:
    base: str
    path: str
    motion_module: Union[str, List[str]]
    steps: int
    guidance_scale: float
    lora_alpha: float
    additional_networks: List[str] = field(default_factory=list)
    prompt: List[str] = field(default_factory=list)
    n_prompt: List[str] = field(default_factory=list)
    seed: List[int] = field(default_factory=list)
    init_image: str = ""
    init_img_strength: float = 0.0

def setup():  
    pass

def image_bio_video_player(image,size):
    image1 = image
    image1.thumbnail(size)
    bio = io.BytesIO()
    image1.save(bio,format="ppm")
    del image1
    return bio.getvalue()

def btn(name):
    return sg.Button(name, size=(6, 1),expand_x=True)


def is_v2(filename):
    """Check if the filename (without extension) ends with 'v2'."""
    name_without_extension = filename.rsplit('.', 1)[0]
    return name_without_extension.endswith("v2")

if __name__ == '__main__':
    sg.set_options(
        sg.theme('Dark Gray 15'),

        # ttk_theme='alt',
        sbar_relief=sg.RELIEF_FLAT,        
        sbar_width=15,sbar_trough_color=0,
    )    
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
    main()
