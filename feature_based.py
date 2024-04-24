from ld_utils import *

# Feature based registration
def detect_corners(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    corners = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.01, minDistance=10)

    # Convert corners to integers
    corners = np.intp(corners)

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
    matched_coordinates = []
    for match in good_matches:
        matched_coordinates.append(kp2[match.trainIdx].pt)
    # print("Number of good matches:", len(good_matches))

    # # Print number of keypoints
    # print("Number of keypoints in template:", len(kp1))
    # print("Number of keypoints in screenshot:", len(kp2))

    # # Check dimensions of template and screenshot
    # print("Template shape:", template.shape)
    # print("Screenshot shape:", screenshot.shape)

    # # Check if good_matches is not empty
    # if len(good_matches) > 0:
    #     matched_image = cv2.drawMatches(template, kp1, screenshot, kp2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    # else:
    #     print("No good matches found.")
    # print("Matched Coordinates:", matched_coordinates)
    
    return matched_image, matched_coordinates

list1 = get_window_titles()
print(list1)

ld_handle = check_for_ldplayer(list1)
print("The LDplayer handle is:", ld_handle)
ld = capture_ldplayer_screenshot(ld_handle)
ld_file = 'screenshot2.png'


template_folder_path = 'templates'
template_image_path = os.path.join(template_folder_path, 'target.png')
template = cv2.imread(template_image_path, cv2.IMREAD_COLOR)
screen_path = os.path.join(template_folder_path, 'screenshot2.png')
screen = cv2.imread(screen_path, cv2.IMREAD_COLOR)

#saving to templates folder
# ld_path = os.path.join(template_folder_path, 'screenshot2.png')
# cv2.imwrite(ld_path, cv2.cvtColor(ld, cv2.COLOR_RGB2BGR))


# Test Execution
template_corners = detect_corners(template)
screenshot_corners = detect_corners(screen)
#cv2.imshow('Template Corners', template_corners)
#cv2.imshow('Screenshot Corners', screenshot_corners)

template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

# Initialize ORB detector
matched_image, matched_coords = detect_and_match_sift(template, screen)
print(matched_coords)
matched_points_image = screen.copy()

# Sort the coordinates by their y-coordinate to arrange them vertically
matched_coords.sort(key=lambda coord: coord[1])

# Define initial text position
text_x = 20
text_y = 20

# Spacing between each coordinate label
label_spacing = 20

# Calculate the height of the coordinate list
list_height = len(matched_coords) * label_spacing

# Adjust the text position if it exceeds the image height
if text_y + list_height > matched_points_image.shape[0]:
    text_y = matched_points_image.shape[0] - list_height

for x, y in matched_coords:
    # Draw a circle around the matched point
    cv2.circle(matched_points_image, (int(x), int(y)), 5, (0, 0, 255), -1)
    
    # Define the position for writing the coordinates (a few pixels to the right of the circle)
    text_position = (text_x + 2000, text_y)  # Adjust the offset as needed
    
    # Draw a line from the circle to the text position
    cv2.line(matched_points_image, (int(x), int(y)), text_position, (0, 255, 0), 1)
    
    # Write coordinates on the image
    cv2.putText(matched_points_image, f"• ({int(x)}, {int(y)})", text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    # Increment the y-coordinate for the next text position
    text_y += label_spacing  # Adjust the spacing as needed

# Display the matched points image
cv2.imshow('Matched Points', matched_points_image)
# match_path = os.path.join(template_folder_path, 'match.png')
# cv2.imwrite(match_path, cv2.cvtColor(matched_image, cv2.COLOR_RGB2BGR))

ldplayer_single_click(ld_handle, 960.8262329101562, 365.5218200683594)

# Display the matched image
#cv2.imshow('Feature Matching Result', matched_image)


print("This is my cursor's position:", pyautogui.position())
cv2.waitKey(0)
cv2.destroyAllWindows()