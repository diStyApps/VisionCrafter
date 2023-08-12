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
    slider_float('-lora_alpha_slider-','-lora_alpha-',values,event,window)
    slider_float('-init_img_strength_slider-','-init_img_strength-',values,event,window)
