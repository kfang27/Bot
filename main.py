import cv2
import pyautogui
import win32gui
import numpy as np
from PIL import Image

def callback(win_handle, titles_list):
    if win32gui.IsWindowVisible(win_handle):
        title = win32gui.GetWindowText(win_handle)
        titles_list.append(title)
        
def get_window_titles():
    window_titles = []

    # Passes the handle of every top-level window and the window_titles list to callback function
    win32gui.EnumWindows(callback, window_titles)

    return window_titles

list = get_window_titles()
print(list)

def check_for_ldplayer(windows_list):
    if "LDPlayer" in windows_list:
        print("LDPlayer found")
        ldplayer_window_handle = win32gui.FindWindow(None, "LDPlayer")
        print(ldplayer_window_handle)
        
    else:
        print("LDPlayer not found")
        return
    
        
check_for_ldplayer(list)