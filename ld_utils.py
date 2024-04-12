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

def convert_to_gray(image):
    if len(image.shape) > 2:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        return image

    return gray_image
    
def find_template_match(screenshot, template_image, threshold=0.8):
    #matches_dict = {}
    
    result = cv2.matchTemplate(screenshot, template_image, cv2.TM_CCOEFF_NORMED)
    
    locations = np.where(result >= threshold)
    matches = list(zip(*locations[::-1]))

    return matches

    
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
        
def scale_image(image, width=None, height=None, scale=None):
    # If both width and height are specified, resize the image to the specified dimensions
    if width is not None and height is not None:
        resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    # If only one of width or height is specified, calculate the aspect ratio and resize accordingly
    elif width is not None:
        aspect_ratio = width / float(image.shape[1])
        height = int(image.shape[0] * aspect_ratio)
        resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    elif height is not None:
        aspect_ratio = height / float(image.shape[0])
        width = int(image.shape[1] * aspect_ratio)
        resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    # If scale factor is specified, resize the image by that factor
    elif scale is not None:
        resized_image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    else:
        # If no resizing parameters are specified, return the original image
        resized_image = image
    
    return resized_image

list1 = get_window_titles()
print(list1)

ld_handle = check_for_ldplayer(list1)
print("The LDplayer handle is:", ld_handle)
ld = capture_ldplayer_screenshot(ld_handle)
ld_gray = convert_to_gray(ld)

template_folder_path = 'templates'
template_image_path = os.path.join(template_folder_path, 's3.png')
template = cv2.imread(template_image_path, cv2.IMREAD_GRAYSCALE)
#new_template = scale_image(template, scale=20)
template_name = os.path.splitext(os.path.basename(template_image_path))[0]


screen_path = os.path.join(template_folder_path, 'ex.png')
screen = cv2.imread(screen_path, cv2.IMREAD_GRAYSCALE)

#print(ld)
matches = find_template_match(screen, template)
print(f"The matches for {template_name} are:", matches)


ldplayer_click(ld_handle, 207, 553)
time.sleep(1)
ldplayer_click(ld_handle, 513, 553)
time.sleep(1)
ldplayer_click(ld_handle, 649, 553)
#matched_image = cv2.drawMatches(template, kp1, screen, kp2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)


print("This is my cursor's position:", pyautogui.position())

cv2.imshow("LDPlayer Screenshot", screen)
cv2.waitKey(0)
cv2.destroyAllWindows()