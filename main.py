from ld_utils import *

def main():
    list1 = get_window_titles()
    print(list1)

    ld_handle = check_for_ldplayer(list1)
    print("The LDplayer handle is:", ld_handle)
    ld = capture_ldplayer_screenshot(ld_handle)

    template_folder_path = 'templates'
    template_image_path = os.path.join(template_folder_path, 's1.png')
    template = cv2.imread(template_image_path, cv2.IMREAD_GRAYSCALE)
    screen_path = os.path.join(template_folder_path, 'screen1.png')
    screen = cv2.imread(screen_path, cv2.IMREAD_GRAYSCALE)

   
    matches = find_template_match(screen, template)
    print("The matches are:", matches)
    

    #matched_image = cv2.drawMatches(template, kp1, screen, kp2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    
    # Display the matched image
    

    # Cleanup
    print("This is my cursor's position:", pyautogui.position())
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
