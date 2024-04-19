import cv2, os, time
import win32gui, pyautogui, pydirectinput, pytesseract
import win32api, win32con
import autoit, ait
import numpy as np
import pickle
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

def filter_coordinates_list(coordinates_list):
    # New list is initialized with the first coordinate of given list
    filtered_list = [coordinates_list[0]]
    for i in range(1, len(coordinates_list)):
        # Check if the x-coordinate difference between the current coordinate and the previous one is not 1
        if coordinates_list[i][0] - filtered_list[-1][0] != 1:
            filtered_list.append(coordinates_list[i])

    return filtered_list

def ldplayer_single_click(ldplayer_handle, x, y):
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
        
def ldplayer_multiclick(ldplayer_handle, coordinates):
    # Find the child window of LDPlayer
    child_window_handle = win32gui.FindWindowEx(ldplayer_handle, None, None, None)

    # Check if the child window handle is valid
    if child_window_handle:
        # Iterate over the coordinates
        for x, y in coordinates:
            # Calculate the lParam for the mouse click
            lParam = win32api.MAKELONG(x, y)

            # Send the mouse click messages to the child window
            win32gui.SendMessage(child_window_handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
            win32gui.SendMessage(child_window_handle, win32con.WM_LBUTTONUP, None, lParam)

            # Sleep for a short duration to prevent consecutive clicks
            time.sleep(0.1)
    else:
        print("Child window of LDPlayer not found.")

    
def create_unit_and_skills_dict(screenshot):
    units_skills_dict = {}
    unit_names_input = input("Enter the names of your units in order: ").strip().lower()
    
    if not unit_names_input:
        print("No unit names provided.")
        return units_skills_dict
    
        
    unit_names = []
    unit_instance_count = {}
    for name in unit_names_input.split(','):
        stripped_name = name.strip()
        # checks if it's an empty string now because the strip() before, removes any trailing whitespace, including strings such as ' '
        if stripped_name:
            split_result = stripped_name.split()
            for i in split_result:
                if i.capitalize() in unit_instance_count:
                    unit_instance_count[i.capitalize()] += 1
                    unit_names.append(f"{i.capitalize()} {unit_instance_count[i.capitalize()]}")
                else:
                    unit_instance_count[i.capitalize()] = 1
                    unit_names.append(i.capitalize())
    print(unit_names)
    print(unit_instance_count)
    
    skill_template_folder = 'skill_templates'
    skill_template_files_list = os.listdir(skill_template_folder)
    
    for filename in skill_template_files_list:
        if "_s" in filename:
            # splits name_s# into name and #.png
            file_unit_name, skill_number = filename.split('_s')
            
            # splits into # and file extension (like png, jpg...), then only uses #
            skill_number = int(skill_number.split('.')[0])

            if (file_unit_name.capitalize() in unit_instance_count):
                template_image = cv2.imread(os.path.join(skill_template_folder, filename), cv2.IMREAD_GRAYSCALE)
                coordinates_list = find_template_match(screenshot, template_image)
                filtered_list = filter_coordinates_list(coordinates_list)
                
                instance_count = unit_instance_count[file_unit_name.capitalize()]
                
                if instance_count > 1:
                    if filtered_list:
                        name_list = []
                        for name in unit_names:
                            if file_unit_name.capitalize() in name.split()[0]:
                                name_list.append(name)
                                
                        for index,coord in zip(name_list, filtered_list):
                            unit_key = f"{index}'s Skill{skill_number}"
                            units_skills_dict[unit_key] = coord
                else:
                    if filtered_list:
                        for coord in filtered_list:
                            unit_key = f"{file_unit_name.capitalize()}'s Skill{skill_number}"
                            units_skills_dict[unit_key] = coord
            
        else:
            skill_name = filename.split('.')[0]
            
            template_image = cv2.imread(os.path.join(skill_template_folder, filename), cv2.IMREAD_GRAYSCALE)
            coordinates_list = find_template_match(screenshot, template_image)
            filtered_list = filter_coordinates_list(coordinates_list)
            
            if filtered_list:
                for unit_name, coord in zip(unit_names, filtered_list):
                    while True:
                        skill_number = input(f"Enter the skill number of {skill_name} for {unit_name}: ")
                        if skill_number.isdigit():
                            skill_number = int(skill_number)
                            if 1 <= skill_number <= 3:
                                break
                            else:
                                print("Skill number must be between 1 and 3.")
                        else:
                            print("Please enter a valid number.")
                    unit_key = f"{unit_name}'s Skill{skill_number}"
                    units_skills_dict[unit_key] = coord
                
    return units_skills_dict
        
def organize_skills_dict(original_dict):
    organized_dict = {}
    for key, value in original_dict.items():
        unit_name, skill = key.split("'s Skill")
        skill_number = f"Skill{skill}"
        if unit_name not in organized_dict:
            organized_dict[unit_name] = {}
        organized_dict[unit_name][skill_number] = value
    return organized_dict

def write_dict_to_file(dictionary, file_path):
    with open(file_path, 'w') as file:
        file.write("{\n")
        for key, value in dictionary.items():
            file.write(f'    "{key}": {{\n')
            for inner_key, inner_value in value.items():
                file.write(f'        "{inner_key}": {list(inner_value)},\n')
            file.write("    },\n")
        file.write("}\n")

            
list1 = get_window_titles()
print(list1)

ld_handle = check_for_ldplayer(list1)
print("The LDplayer handle is:", ld_handle)
# ld = capture_ldplayer_screenshot(ld_handle)
#ld_gray = convert_to_gray(ld)

template_folder_path = 'templates'
template_image_path = os.path.join(template_folder_path, 's2.png')
template = cv2.imread(template_image_path, cv2.IMREAD_GRAYSCALE)
#new_template = scale_image(template, scale=20)
template_name = os.path.splitext(os.path.basename(template_image_path))[0]


screen_path = os.path.join(template_folder_path, 'ldplayer_screenshot.png')
screen = cv2.imread(screen_path, cv2.IMREAD_GRAYSCALE)

#print(ld)
matches = find_template_match(screen, template)
filtered_matches = filter_coordinates_list(matches)
print(f"The matches for {template_name} are:", matches)
print(f"The filtered matches for {template_name} are:", filtered_matches)
#print(create_unit_and_skills_dict(screen))

skills_dict = create_unit_and_skills_dict(screen)
organized = organize_skills_dict(skills_dict)

print(organized)

#write_dict_to_file(organized, "skill_coords.txt")

# ldplayer_single_click(ld_handle, 207, 553)
# time.sleep(1)
# ldplayer_single_click(ld_handle, 513, 553)
# time.sleep(1)
# ldplayer_single_click(ld_handle, 649, 553)
#matched_image = cv2.drawMatches(template, kp1, screen, kp2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)


print("This is my cursor's position:", pyautogui.position())

#cv2.imshow("LDPlayer Screenshot", screen)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
