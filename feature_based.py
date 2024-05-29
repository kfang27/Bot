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

def match_lines(template_lines, target_lines):
    matched_lines = []

    for line1 in template_lines:
        min_distance = float('inf')
        matched_line = None

        for line2 in target_lines:
            # Compute some similarity metric between lines (e.g., distance between lines)
            distance = compute_distance(line1, line2)

            # Check if the distance is smaller than the minimum distance so far
            if distance < min_distance:
                min_distance = distance
                matched_line = line2

        # Check if a match was found
        if matched_line is not None:
            matched_lines.append((line1, matched_line))
    
    print("Number of matched lines:", len(matched_lines))
    print("Matched lines:", matched_lines)

    return matched_lines

def compute_distance(line1, line2):
    if len(line1) < 4 or len(line2) < 4:
        return float('inf')  # Return a large value if either line doesn't have enough values
    
    x1_1, y1_1, x1_2, y1_2 = line1
    x2_1, y2_1, x2_2, y2_2 = line2

    # Compute the distance between the midpoints of the lines
    mid_x1 = (x1_1 + x1_2) / 2
    mid_y1 = (y1_1 + y1_2) / 2
    mid_x2 = (x2_1 + x2_2) / 2
    mid_y2 = (y2_1 + y2_2) / 2

    distance = np.sqrt((mid_x1 - mid_x2)**2 + (mid_y1 - mid_y2)**2)

    return distance

def detect_lines(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)
    return lines


list1 = get_window_titles()
print(list1)

ld_handle = check_for_ldplayer(list1)
print("The LDplayer handle is:", ld_handle)
ld = capture_ldplayer_screenshot(ld_handle)


template_folder_path = 'templates'
template_image_path = os.path.join(template_folder_path, 'target.png')
template = cv2.imread(template_image_path, cv2.IMREAD_COLOR)
screen_path = os.path.join(template_folder_path, 'screenshot2.png')
screen = cv2.imread(screen_path, cv2.IMREAD_COLOR)

#saving to templates folder
# ld_path = os.path.join(template_folder_path, 'attack_screen.png')
# cv2.imwrite(ld_path, cv2.cvtColor(ld, cv2.COLOR_RGB2BGR))

screenpath2 = os.path.join(template_folder_path, 'ldplayer_screenshot.png')
screen2 = cv2.imread(screenpath2, cv2.IMREAD_COLOR)
attack_path = os.path.join(template_folder_path, 'attack_button.png')
attack_template = cv2.imread(attack_path, cv2.IMREAD_COLOR)
attack_image, attack_coords = detect_and_match_sift(attack_template, screen2)
#cv2.imshow('Attack Points', attack_image)
#print("The attack button is located at: ", attack_coords)
#ldplayer_single_click(ld_handle, 1018.885498046875, 615.6768798828125)

# Attack Phase for NP CARD
screenpath3 = os.path.join(template_folder_path, 'attack_screen.png')
attack_screen = cv2.imread(screenpath3, cv2.IMREAD_COLOR)
np_path = os.path.join(template_folder_path, 'npcard.png')
np_card = cv2.imread(np_path, cv2.IMREAD_COLOR)
np_match_image, np_coords = detect_and_match_sift(np_card, attack_screen)
cv2.imshow('NP_Match', np_match_image)
print("The NP card was found at: ", np_coords)

# Test Execution
template_corners = detect_corners(template)
screenshot_corners = detect_corners(screen)
#cv2.imshow('Template Corners', template_corners)
#cv2.imshow('Screenshot Corners', screenshot_corners)

template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

# Initialize ORB detector
matched_image, matched_coords = detect_and_match_sift(template, screen)
#print(matched_coords)
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
#cv2.imshow('Matched Points', matched_points_image)
# match_path = os.path.join(template_folder_path, 'match.png')
# cv2.imwrite(match_path, cv2.cvtColor(matched_image, cv2.COLOR_RGB2BGR))

#Target
#ldplayer_single_click(ld_handle, 960.8262329101562, 365.5218200683594)

# Display the matched image
#cv2.imshow('Feature Matching Result', matched_image)


print("This is my cursor's position:", pyautogui.position())
cv2.waitKey(0)
cv2.destroyAllWindows()