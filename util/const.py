VERSION = '0.0.5'
APP_NAME =  'VisionCrafter'
APP_TITLE = f"{APP_NAME} - {VERSION}"
GITHUB = "github.com/diStyApps/VisionCrafter"

image_file_ext = {
    ("IMAGE Files", "*.png"),
    ("IMAGE Files", "*.jpg"),
    ("IMAGE Files", "*.jpeg"),
}

video_file_ext = {
    ("Video Files", "*.mp4"),
    ("Video Files", "*.webm"),
    ("Video Files", "*.gif"),
}

extensions = [".safetensors"]

FONT = 'Arial 12'
FONT_S = 'Arial 8'
FONT_M = 'Arial 9'
FONT_M_B = 'Arial 9 bold'
FONT_H1 = 'Arial 14'
FONT_H2_BOLD = 'Arial 14 bold'
FONT_H1_BOLD = 'Arial 18 bold'


# # colors
# WIN_COLOR = "#282828"
# TEXT_COLOR = "#ffffff"

# DEFAULT_DISPLAY_DURATION_IN_MILLISECONDS = 10000

# Base64 Images to use as icons in the window

# #nav 
# PROJECTS_COL_1 = '-projects_col_1-'
# PROJECTS_COL_2 = '-projects_col_2-'
ABOUT_COL = '-about_col-'
# SYSTEM_INFO_COL = '-system_stats_col-'

# SETTINGS_COL = '-settings_col-'
# TOOLBOX_COL = '-toolbox_col-'
# #layout
# PROJECTS_LIST_MENU = '-projects_list_menu-'
# PROJECTS_COL_PLACEHOLDER = '-projects_col_placeholder-'


#nav buttons
TXT2VID_TAB_BTN = '-txt2video_tab-'
SYSTEM_STATS_TAB_BTN = '-system_stats_tab-'
SETTINGS_TAB_BTN = '-settings_tab-'
TOOLBOX_TAB_BTN = '-toolbox_tab-'
ABOUT_TAB_BTN = '-about_tab-'


SETTINGS_TITLE = "Settings"
ABOUT_TITLE = "About"

# SELECTED_PROJECT = '-selected_project_'
# SELECT_PROJECT = '-select_project_'

# SET_APP_ARGS = "-set_app_args-"
# RUN_APP_FUNC = "-run_app_func-"
# SELECTED_APP_QUICK = '-selected_app_quick-'
# SET_PROJECT_PATH = "-set_project_path-"
# ACTIVATE_PROJECT_PATH = "-activate_project_path-"
# ADD_PROJECT_FOLDER_NAME = "-add_project_folder_name-"
# SAVE_DEFAULT_ARGS= "-save_default_args-"
# INSTALL_EXT = "-install_ext-"
# SELECT_APP = "-select_app_"
# SELECTED_APP = "-selected_app_"
# INIT_DEFAULT_PROJECT_ARGS = "-init_default_project_args-"




DURATION_WARN_1="""Generating more than a 6-second animation may take a very long time and might not produce the desired results,
so use with caution.
 """
DURATION_WARN_2= """
Generating more than a 30-second animation may take a very long time and might not produce the desired results, so use with caution.

Music will be added only to the first 30 seconds of the video.
"""