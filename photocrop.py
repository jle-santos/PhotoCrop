import cv2
import numpy as np
import imutils

image = cv2.imread('../test2.png')

def getTransformation(box, cntr):

    width = int(cntr[1][0])
    height = int(cntr[1][1])

    src_pts = box.astype("int")
    # coordinate of the points in box points after the rectangle has been
    # straightened
    dst_pts = np.array([[0, height - 1],
                        [0, 0],
                        [width - 1, 0],
                        [width - 1, height - 1]], dtype="int")

    # the perspective transformation matrix
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)

    return M

def findImages(image):

    # Images
    imgList = []

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blur image (Low Pass Filter)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    ret, th = cv2.threshold(gray,210,235,1)

    # Edge Detection
    edged = cv2.Canny(th, 25, 200)


    contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by size
    contours = sorted(contours, key = cv2.contourArea, reverse = True)

    for c in contours:
        # Get area of box
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        Area = image.shape[0]*image.shape[1]
        if Area/10 < cv2.contourArea(box) < Area*2/3:
            cv2.drawContours(image, [box], -1, (0, 255, 0), 2)

            #mtrx = getTransformation(box, c)
            #warped = cv2.warpPerspective(image, mtrx, int(c[1][0]), int(c[1][1]))
            #imgList.append(warped)

    return image

foundImages = findImages(image.copy())
cv2.imshow("Images", foundImages)

cv2.imwrite("markedImg.png", foundImages)
cv2.waitKey(0)