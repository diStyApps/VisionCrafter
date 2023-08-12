
from sys import platform as PLATFORM
import vlc
import os

current_folder = os.getcwd()

def init_vlc_player(window):
    inst = vlc.Instance('--quiet --no-xlib')
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
