import cv2, os, time
import win32gui, pyautogui, pydirectinput, pytesseract
import win32api, win32con
import autoit, ait
import numpy as np
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

def find_template_match(screenshot, template_image, threshold=0.8):
    matches_dict = {}
    
    result = cv2.matchTemplate(screenshot, template_image, cv2.TM_CCOEFF_NORMED)
    
    locations = np.where(result >= threshold)
    matches = list(zip(*locations[::-1]))

    return matches

def click_coordinate(x, y):
    pyautogui.click(x=x, y=y)
    
def ldplayer_click(ldplayer_handle, x, y):
# Find the child window of LDPlayer
    child_window_handle = win32gui.FindWindowEx(ldplayer_handle, None, None, None)

    # Check if the child window handle is valid
    if child_window_handle:
        # Calculate the lParam for the mouse click
        lParam = win32api.MAKELONG(x, y)

        # Send the mouse click messages to the child window
        win32gui.SendMessage(child_window_handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32gui.SendMessage(child_window_handle, win32con.WM_LBUTTONUP, None, lParam)
    else:
        print("Child window of LDPlayer not found.")
        
        
# Testing 
list1 = get_window_titles()
print(list1)

ld_handle = check_for_ldplayer(list1)
print("The LDplayer handle is:", ld_handle)
ld = capture_ldplayer_screenshot(ld_handle)



template_folder_path = 'templates'

template_image_path = os.path.join(template_folder_path, 'castoria_skill3.png')
template = cv2.imread(template_image_path, cv2.IMREAD_GRAYSCALE)

screen_path = os.path.join(template_folder_path, 'ex.png')
screen = cv2.imread(screen_path, cv2.IMREAD_GRAYSCALE)
matches = find_template_match(screen, template)
print("The matches are:", matches)


print(pyautogui.position())
#ldplayer_click(ld_handle, 375, 560)
ldplayer_click(ld_handle, 344, 553)

#cv2.imshow("LDPlayer Screenshot", screen)
cv2.waitKey(0)
cv2.destroyAllWindows()
