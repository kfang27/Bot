from ld_utils import *

def main():
    list1 = get_window_titles()
    print(list1)

    ld_handle = check_for_ldplayer(list1)
    print("The LDplayer handle is:", ld_handle)
    ld = capture_ldplayer_screenshot(ld_handle)

    template_folder_path = 'templates'
    template_image_path = os.path.join(template_folder_path, 'castoria_skill1.png')
    template = cv2.imread(template_image_path, cv2.IMREAD_COLOR)
    screen_path = os.path.join(template_folder_path, 'screen1.png')
    screen = cv2.imread(screen_path, cv2.IMREAD_COLOR)

    # Test Execution
    template_corners = detect_corners(template)
    screenshot_corners = detect_corners(screen)
    #cv2.imshow('Template Corners', template_corners)
    cv2.imshow('Screenshot Corners', screenshot_corners)

    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # Initialize ORB detector
    matched_image = detect_and_match_sift(template, screen)

    # Draw the top matches
    #matched_image = cv2.drawMatches(template, kp1, screen, kp2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    
    # Display the matched image
    cv2.imshow('Feature Matching Result', matched_image)

    # Cleanup
    print("This is my cursor's position:", pyautogui.position())
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
