# Crops scanned photographs to proper size
import cv2 as cv

print("PhotoCrop Alpha V0.1 - May 12, 2020")

# Open File and show
photo = cv.imread("test.png")

imgray = cv.cvtColor(photo, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 254, 255, cv.THRESH_BINARY)
#cv.imshow("Grayscale", imgray)
#cv.imshow("Threshold", thresh)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
cv.drawContours(photo, contours, -1, (0, 0, 0), 3)

def cropPhoto(rawScan, photoData):
    (centerX, centerY), (width, height), theta = cv.minAreaRect(photoData)
    (cornerX, cornerY) = (int(centerX-width/2), int(centerY-height/2))
    print("Leftmost corner coordinates: ", (cornerX, cornerY))
    rangeX = cornerX+int(width)

    croppedPhoto = rawScan[cornerY:cornerY+int(height), cornerX:rangeX]
    return croppedPhoto

# Bounding Box
index = 0

for imBox in contours:
    index += 1
    center, size, theta = cv.minAreaRect(imBox)
    print(cv.minAreaRect(imBox))

    croppedPhoto = cropPhoto(photo, imBox)
    cv.imshow(str(index), croppedPhoto)

    # Number the photos in the scan
    cv.putText(photo, str(index) + " " + str(int(theta)) + "deg", (int(center[0]),int(center[1])), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2, cv.LINE_AA)

while(cv.waitKey(100)):
    cv.imshow("Raw", photo)
    #print("Photos found:", len(contours), "contours")
