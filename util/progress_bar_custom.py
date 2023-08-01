import pandas as pd
from datetime import datetime  as dt
import datetime
import PySimpleGUI as sg

COLOR_GREEN = '#43CD80'
COLOR_DARK_GREEN2 = '#78BA04'
COLOR_DARK_GREEN = '#74a549'
COLOR_BLUE = '#69b1ef'
COLOR_RED = '#E74555'
COLOR_RED_ORANGE = '#C13515'
COLOR_GRAY_9900 = '#0A0A0A'
COLOR_ORANGE ='#FE7639'
COLOR_PURPLE = '#a501e8'
COLOR_DARK_GRAY = '#1F1F1F'
COLOR_DARK_BLUE = '#4974a5'
GRAY = "#2A2929"


def format_sec(sec):
    sec = round(sec,2)
    formated_sec_step_1 = str(datetime.timedelta(seconds=sec))
    formated_sec = pd.to_datetime(formated_sec_step_1).strftime('%H:%M:%S')
    return formated_sec

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    step_unit = 1000.0 #1024 bad the size

    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit

def full_layout(pbar_progress_bar_key_,visible=True,it_name="it",show_time_left=True,show_avg_time=True,show_estimated_time=True,show_it_per_sec=True,show_percentage=True,show_index_range=True,show_progress_bar=True):
    pbar_progress_bar_key = f'-pbar_progress_bar_{pbar_progress_bar_key_}-'
    pbar_index_range_key = f'-pbar_index_range_{pbar_progress_bar_key_}-'
    pbar_estimated_time_key = f'-pbar_estimated_time_{pbar_progress_bar_key_}-'
    pbar_iteration_per_sec_key = f'-pbar_it_per_sec_{pbar_progress_bar_key_}-'
    pbar_percentage_key = f'-pbar_percentage_{pbar_progress_bar_key_}-'
    layout = sg.Frame('',[
        [
            sg.Text('0%',k=pbar_percentage_key,size=(5, 1),background_color=COLOR_GRAY_9900),
            sg.ProgressBar(12, orientation='h', size=(20, 6),expand_y=False,expand_x=True, key=pbar_progress_bar_key,bar_color=(COLOR_DARK_GREEN,COLOR_DARK_GRAY)),
            sg.Text('0/0',k=pbar_index_range_key,expand_x=True,size=(3, 1),visible=True,background_color=COLOR_GRAY_9900),
            sg.Text(f'0.0 {it_name}/s',k=pbar_iteration_per_sec_key,expand_x=True,visible=show_it_per_sec,background_color=COLOR_GRAY_9900),
            sg.Text('00:00:00 / 00:00:00 < 00:00:00',k=pbar_estimated_time_key,expand_x=False,background_color=COLOR_GRAY_9900),
        ],
        ],expand_x=True,expand_y=False,relief=sg.RELIEF_FLAT,border_width=0,visible=visible,background_color=COLOR_GRAY_9900) #,element_justification='c',background_color=COLOR_GRAY_9900,title_color=COLOR_DARK_BLUE                         

    return layout

def min_layout(pbar_progress_bar_key_,visible=True,it_name="it"):
    pbar_progress_bar_key = f'-pbar_progress_bar_{pbar_progress_bar_key_}-'
    pbar_index_range_key = f'-pbar_index_range_{pbar_progress_bar_key_}-'
    pbar_percentage_key = f'-pbar_percentage_{pbar_progress_bar_key_}-'
    layout = sg.Frame('',[
        [
            sg.Text('0%',k=pbar_percentage_key,size=(5, 1),background_color=COLOR_GRAY_9900),
            sg.Text('0/0',k=pbar_index_range_key,size=(5, 1),visible=True,background_color=COLOR_GRAY_9900),
            sg.ProgressBar(12, orientation='h',expand_x=True,expand_y=False,s=(8,6), key=pbar_progress_bar_key,bar_color=(COLOR_DARK_GREEN,COLOR_DARK_GRAY),relief=sg.RELIEF_FLAT),
        ],
        ],expand_x=True,expand_y=False,relief=sg.RELIEF_FLAT,border_width=0,visible=visible,element_justification='c',background_color=COLOR_GRAY_9900) #,element_justification='c',background_color=COLOR_GRAY_9900,title_color=COLOR_DARK_BLUE                         
    return layout

def update_full(index, total, start_time, window, pbar_progress_bar_key_, it_name="it"):
    pbar_progress_bar_key = f'-pbar_progress_bar_{pbar_progress_bar_key_}-'
    pbar_index_range_key = f'-pbar_index_range_{pbar_progress_bar_key_}-'
    pbar_estimated_time_key = f'-pbar_estimated_time_{pbar_progress_bar_key_}-'
    pbar_iteration_per_sec_key = f'-pbar_it_per_sec_{pbar_progress_bar_key_}-'
    pbar_percentage_key = f'-pbar_percentage_{pbar_progress_bar_key_}-'

    index = min(max(1, index+1), total)
    window[pbar_progress_bar_key].UpdateBar(index, total)

    time_diff = dt.today().timestamp() - start_time
    it_per_sec = index / time_diff if time_diff else 0

    if it_per_sec > 0:
        time_left = format_sec((total / it_per_sec) - time_diff)
        avg_time = format_sec(total / it_per_sec)

        time_left_no_format = (total / it_per_sec) - time_diff
        avg_time_no_format = total / it_per_sec

        estimated_time_format = format_sec(avg_time_no_format - time_left_no_format)
        sec_per_it = 1 / it_per_sec if it_per_sec > 0 else float('inf')

        percentage = f'{round((index / total * 100))}%'
        index_range = f'{index}/{total}'
        # iteration_per_sec = f'{round(it_per_sec, 2)} {it_name}/s'
        iteration_per_sec = f'{round(sec_per_it, 2)}s/{it_name}'

        estimated_time = (f'{avg_time} / {estimated_time_format} < {time_left}')

        window[pbar_percentage_key].update(percentage)
        window[pbar_index_range_key].update(index_range)
        window[pbar_iteration_per_sec_key].update(iteration_per_sec)
        window[pbar_estimated_time_key].update(estimated_time)
    else:
        window[pbar_percentage_key].update('0%')
        window[pbar_index_range_key].update(f'{index}/{total}')
        window[pbar_iteration_per_sec_key].update('0.00 {it_name}/s')
        window[pbar_estimated_time_key].update('00:00:00')
        
def update_min(index, total, start_time, window, pbar_progress_bar_key_, it_name="it"):
    pbar_progress_bar_key = f'-pbar_progress_bar_{pbar_progress_bar_key_}-'
    pbar_index_range_key = f'-pbar_index_range_{pbar_progress_bar_key_}-'
    pbar_percentage_key = f'-pbar_percentage_{pbar_progress_bar_key_}-'

    index = min(max(1, index+1), total)
    window[pbar_progress_bar_key].UpdateBar(index, total)

    time_diff = dt.today().timestamp() - start_time
    it_per_sec = index / time_diff if time_diff else 0

    if it_per_sec > 0:
        percentage = f'{round((index / total * 100))}%'
        index_range = f'{index}/{total}'

        window[pbar_percentage_key].update(percentage)
        window[pbar_index_range_key].update(index_range)
    else:
        window[pbar_percentage_key].update('0%')
        window[pbar_index_range_key].update(f'{index}/{total}')


def progress_bar_reset(window,pbar_progress_bar_key_,it_name="it"):

    pbar_progress_bar_key = f'-pbar_progress_bar_{pbar_progress_bar_key_}-'
    pbar_index_range_key = f'-pbar_index_range_{pbar_progress_bar_key_}-'
    pbar_estimated_time_key = f'-pbar_estimated_time_{pbar_progress_bar_key_}-'
    pbar_iteration_per_sec_key = f'-pbar_it_per_sec_{pbar_progress_bar_key_}-'
    pbar_percentage_key = f'-pbar_percentage_{pbar_progress_bar_key_}-'

    window[pbar_progress_bar_key].UpdateBar(0, 0)

    window[pbar_percentage_key].update('0%')
    window[pbar_index_range_key].update('0/0')
    # window[pbar_iteration_per_sec_key].update(f'0.0 {it_name}/s')
    window[pbar_iteration_per_sec_key].update(f'Calculating...')

    
    window[pbar_estimated_time_key].update('00:00:00 / 00:00:00 < 00:00:00')          
