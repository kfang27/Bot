import cv2
import numpy as np

# Create a simple grayscale image for testing
image = np.zeros((200, 200), dtype=np.uint8)
image[50:150, 50:150] = 255  # Add a white square in the center

# Create ORB detector object
orb = cv2.ORB_create()

# Detect keypoints in the image
keypoints = orb.detect(image)

# Draw keypoints on the image
image_with_keypoints = cv2.drawKeypoints(image, keypoints, None, color=(0, 255, 0), flags=cv2.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)

# Display the image with keypoints
cv2.imshow('Image with Keypoints', image_with_keypoints)
cv2.waitKey(0)
cv2.destroyAllWindows()
