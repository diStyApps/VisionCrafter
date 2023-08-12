import PySimpleGUI as sg
import util.colors as color
from util.const import *


def create_layout():
    layout = [
                   [
                        sg.Frame('Prompt',[
                            [    
                                sg.Frame('',[
                                        [    
                                            sg.MLine("",key="-prompt-",visible=True,border_width=0,sbar_width=20,sbar_trough_color=0,no_scrollbar=True,
                                            autoscroll=False, auto_refresh=True,size=(40,10),pad=(5,5),expand_x=True,expand_y=True,font="Ariel 11"),
                                        ],    
                                                            
                                        ],expand_x=True,element_justification='center',vertical_alignment='center',s=(150,150),relief=sg.RELIEF_SOLID,border_width=0,visible=True,background_color=color.DARK_GRAY
                                    ),
                            ],    
                                                
                            ],expand_x=True,element_justification='center',vertical_alignment='center',s=(150,150),relief=sg.RELIEF_SOLID,border_width=0,visible=True,background_color=color.GRAY
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
                                                            
                                        ],expand_x=True,element_justification='center',vertical_alignment='center',s=(150,150),relief=sg.RELIEF_SOLID,border_width=0,visible=True,background_color=color.DARK_GRAY
                                    ),
                            ],    
                                                
                            ],expand_x=True,element_justification='center',vertical_alignment='center',s=(150,150),relief=sg.RELIEF_SOLID,border_width=0,visible=True,background_color=color.GRAY
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
                                sg.Slider(default_value=20,range=((1,150)),resolution=1,
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
                                sg.In(2,k='-length-',s=(5,5),justification='center',disabled=True,use_readonly_for_disable=True,disabled_readonly_background_color=color.GRAY),
                                sg.Slider(default_value=2,range=((1,60)),resolution=1,
                                orientation='horizontal',disable_number_display=True,enable_events=True,k='-length_slider-',expand_x=True,s=(10,10),tooltip='Generating more than a 6-second animation may take a very long time and might not produce the desired results, so use with caution.'),   
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
    return layout

def events(event):
    pass


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