VERSION = '0.0.6'
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

#nav cols

ABOUT_COL = '-about_col-'
TXT2VID_COL = '-txt2video_col-'
IMG2VID_COL = '-img2video_col-'
SETTINGS_COL = '-settings_col-'
MODELSBAR_COL = '-modelsbar_col-'

#nav buttons
TXT2VID_TAB_BTN = '-txt2video_tab-'
IMG2VID_TAB_BTN = '-img2video_tab-'
SETTINGS_TAB_BTN = '-settings_tab-'
ABOUT_TAB_BTN = '-about_tab-'

#nav titles
TXT2VID_TITLE = "Text to Animation"
IMG2VID_TITLE = "Image to Animation"
SETTINGS_TITLE = "Settings"
ABOUT_TITLE = "About"

DURATION_WARN_1="""Generating more than a 6-second animation may take a very long time and might not produce the desired results,
so use with caution.
 """
DURATION_WARN_2= """
Generating more than a 30-second animation may take a very long time and might not produce the desired results, so use with caution.

Music will be added only to the first 30 seconds of the video.
"""