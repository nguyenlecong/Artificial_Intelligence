import cv2
import imutils
import numpy as np

# Param
max_size = 5000
min_size = 900

# Load image
img = cv2.imread('0.jpg', cv2.IMREAD_COLOR)
cv2.imshow('og', img)

# Resize image
img = cv2.resize(img, (620, 480))
cv2.imshow('resize', img)

# Edge detection
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grey scale
gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Blur to reduce noise
edged = cv2.Canny(gray, 30, 200)  # Perform Edge detection
cv2.imshow('blackwhite', gray)
cv2.imshow('canny', edged)

# find contours in the edged image, keep only the largest
# ones, and initialize our screen contour
cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
screenCnt = None

# loop over our contours
for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.05 * peri, True)
    contours = cv2.drawContours(edged, [approx], 0, 255, -1)
    cv2.imshow('contours', contours)

    # if our approximated contour has four points, then
    # we can assume that we have found our screen
    if len(approx) == 4 and max_size > cv2.contourArea(c) > min_size:
        screenCnt = approx
        break

if screenCnt is None:
    detected = 0
    print ("No plate detected")
else:
    detected = 1

if detected == 1:
    cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

    # Masking the part other than the number plate
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
    #cv2.imshow('lp contour', new_image)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    #cv2.imshow('lp contour', new_image)

    # Now crop
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

    # Display image
    cv2.imshow('Detected', img)
    cv2.imshow('License plate', Cropped)

    cv2.waitKey(0)
    cv2.destroyAllWindows()