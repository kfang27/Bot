from ld_utils import *

def main():
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


    screen_path = os.path.join(template_folder_path, 'ldplayer_screenshot.png')
    screen = cv2.imread(screen_path, cv2.IMREAD_GRAYSCALE)

    #print(ld)
    matches = find_template_match(screen, template)
    print(f"The matches for {template_name} are:", matches)


    ldplayer_single_click(ld_handle, 207, 553)
    time.sleep(1)
    ldplayer_single_click(ld_handle, 513, 553)
    time.sleep(1)
    ldplayer_single_click(ld_handle, 649, 553)
    #matched_image = cv2.drawMatches(template, kp1, screen, kp2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)


    print("This is my cursor's position:", pyautogui.position())

    #cv2.imshow("LDPlayer Screenshot", screen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
