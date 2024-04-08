import cv2
import pyautogui
import win32gui
import numpy as np
import pytesseract
import os
import time
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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


def check_for_ldplayer(windows_list):
    if "LDPlayer" in windows_list:
        print("LDPlayer found")
        ldplayer_window_handle = win32gui.FindWindow(None, "LDPlayer")
        return ldplayer_window_handle
        
    else:
        print("LDPlayer not found")
        return None
    

def capture_ldplayer_screenshot(ldplayer_handle):
    if ldplayer_handle:
        rect = win32gui.GetWindowRect(ldplayer_handle)
        x, y, width, height = rect
        ld_screenshot = pyautogui.screenshot(region=(x, y, width, height))
        return np.array(ld_screenshot)
    
    else:
        print("LDPlayer not found")
        return None

def find_template_match(screenshot, template_image, threshold=0.4):
    matches_dict = {}
    
    result = cv2.matchTemplate(screenshot, template_image, cv2.TM_CCOEFF_NORMED)
    
    locations = np.where(result >= threshold)
    matches = list(zip(*locations[::-1]))

    return matches

def click_coordinate(x, y):
    pyautogui.click(x=x, y=y)
    
# Testing 
list1 = get_window_titles()
print(list1)

ld_handle = check_for_ldplayer(list1)

ld = capture_ldplayer_screenshot(ld_handle)



template_folder_path = 'templates'

template_image_path = os.path.join(template_folder_path, 'castoria_skill3.png')
template = cv2.imread(template_image_path, cv2.IMREAD_GRAYSCALE)

screen_path = os.path.join(template_folder_path, 'ex.png')
screen = cv2.imread(screen_path, cv2.IMREAD_GRAYSCALE)
matches = find_template_match(screen, template)
#print(matches)

#coordinate_to_click = (1658, 584)
print(pyautogui.position())

#click_coordinate(*coordinate_to_click)


pyautogui.moveTo(1658, 584)

pyautogui.sleep(0.1)

pyautogui.click()

pyautogui.moveTo(100, 100, duration=1)
time.sleep(2)
pyautogui.moveTo(200, 200, duration=1)


#text = pytesseract.image_to_string(ld)

#print("Recognized Text:")
#print(text)
#cv2.imshow("LDPlayer Screenshot", screen)
cv2.waitKey(0)
cv2.destroyAllWindows()
