from ld_utils import *

# Feature based registration
def detect_corners(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect corners using Shi-Tomasi corner detection
    corners = cv2.goodFeaturesToTrack(gray, maxCorners=1000000, qualityLevel=0.01, minDistance=10)

    # Convert corners to integers
    corners = np.int0(corners)

    # Draw circles around detected corners
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(image, (x, y), 3, (0, 0, 255), -1)

    return image

def detect_and_match_sift(template, screenshot):
    # Convert images to grayscale
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    
    # Initialize SIFT detector
    sift = cv2.SIFT_create()

    # Detect and compute key points and descriptors
    kp1, des1 = sift.detectAndCompute(template_gray, None)
    kp2, des2 = sift.detectAndCompute(screenshot_gray, None)

    # Initialize a FLANN-based matcher
    flann = cv2.FlannBasedMatcher()

    # Match descriptors
    matches = flann.knnMatch(des1, des2, k=2)

    # Filter matches using ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    # Draw matches
    matched_image = cv2.drawMatches(template, kp1, screenshot, kp2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    return matched_image

list1 = get_window_titles()
print(list1)

ld_handle = check_for_ldplayer(list1)
print("The LDplayer handle is:", ld_handle)
ld = capture_ldplayer_screenshot(ld_handle)

template_folder_path = 'templates'
template_image_path = os.path.join(template_folder_path, 's3.png')
template = cv2.imread(template_image_path, cv2.IMREAD_COLOR)
screen_path = os.path.join(template_folder_path, 'ldplayer_screenshot.png')
screen = cv2.imread(screen_path, cv2.IMREAD_COLOR)

# Test Execution
template_corners = detect_corners(template)
screenshot_corners = detect_corners(screen)
#cv2.imshow('Template Corners', template_corners)
#cv2.imshow('Screenshot Corners', screenshot_corners)

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