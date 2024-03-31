import cv2
import pyautogui
import win32gui
import numpy as np
from PIL import Image

def callback(win_handle, titles_list):
    if win32gui.IsWindowVisible(win_handle):
        try:
            title = win32gui.GetWindowText(win_handle)
            if all(ord(character) < 128 for character in title):
                titles_list.append(title)
        
        except:
            return None
        
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
        return ldplayer_window_handle
        
    else:
        print("LDPlayer not found")
        return None
    
        
ld_handle = check_for_ldplayer(list)

def capture_ldplayer_screenshot(ldplayer_handle):
    if ldplayer_handle:
        rect = win32gui.GetWindowRect(ldplayer_handle)
        x, y, width, height = rect
        ld_screenshot = pyautogui.screenshot(region=(x, y, width, height))
        return np.array(ld_screenshot)
    
    else:
        print("LDPlayer not found")
        return None
