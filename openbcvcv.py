import cv2
import numpy as np
from  poly_point_isect import *
import bentley_ottmann
from lsi import intersection
from imutils.perspective import four_point_transform


def clahe(gray):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl1 = clahe.apply(gray)
    return cl1

def warped(gray):
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Find contours and sort for largest contour
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    displayCnt = None

    for c in cnts:
        # Perform contour approximation
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            displayCnt = approx
            break


    # Obtain birds' eye view of image
    warped = four_point_transform(gray, displayCnt.reshape(4, 2))
    return warped

def adjust_gamma(image, gamma=2.0):
    th3 = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 5)
    blur = cv2.GaussianBlur(image, (5, 5), 0)
    ret3, th3 = cv2.threshold(image,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #scale_percent = 20  # percent of original size
    #width = int(th3.shape[1] * scale_percent / 100)
    #height = int(th3.shape[0] * scale_percent / 100)
    #dim = (width, height)
    #sack = cv2.resize(th3, dim, interpolation=cv2.INTER_AREA)
    #return sack
    return th3




def get_net(img1):

    scale_percent = 80  # percent of original size
    width = int(img1.shape[1] * scale_percent / 100)
    height = int(img1.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    img = cv2.resize(img1, dim, interpolation=cv2.INTER_AREA)



    kernel_size = 5
    blur_gray = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

    low_threshold = 30
    high_threshold = 100
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
    edges = cv2.dilate(edges, kernel, iterations=3)

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 30  # minimum number of pixels making up a line
    max_line_gap = 50  # maximum gap in pixels between connectable line segments

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)

    line_image = np.ones((edges.shape[0], edges.shape[1], 1), np.uint8)

    # print(lines)
    points = []
    i = 0
    lines_edges = np.copy(line_image)
    for line in lines:
        for x1, y1, x2, y2 in line:
            # if i is 10:
            # break
            points.append(((x1 + 0.0, y1 + 0.0), (x2 + 0.0, y2 + 0.0)))
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)
            # ines_edges = line_image#cv2.addWeighted(img, 0.8, line_image, 1, 0)


            #if i is 100:
                #scale_percent = 20  # percent of original size
                #width = int(lines_edges.shape[1] * scale_percent / 100)
                #height = int(lines_edges.shape[0] * scale_percent / 100)
                #dim = (width, height)
                #sack = cv2.resize(line_image, dim, interpolation=cv2.INTER_AREA)
                #cv2.imshow('edges', sack)
                #cv2.waitKey()
            i = i + 1
    scale_percent = 50  # percent of original size
    width = int(lines_edges.shape[1] * scale_percent / 100)
    height = int(lines_edges.shape[0] * scale_percent / 100)
    dim = (width, height)
    sack = cv2.resize(line_image, dim, interpolation=cv2.INTER_AREA)

    cv2.imshow('edges', sack)
    cv2.imwrite('what.png', line_image)
    cv2.waitKey()

img1 = cv2.imread(r'C:\Users\Kimi\Desktop\Defects pictures no big damage\D2085990023.jpg')
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#sack = adjust_gamma(img1)
#sack = warped(img1)
sack = clahe(img1)


cv2.imshow('1', img1)
cv2.waitKey()
get_net(sack)

img1 = adjust_gamma(img1)
cv2.imshow('2', img1)
#cv2.waitKey()

get_net(img1)

#img1 = cv2.imread(r'what.png')
#get_net(img1)






#lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
#isect = isect_segments(points)
#print(isect)

#for inter in isect:
#    a, b = inter
#    for i in range(3):
#        for j in range(3):
#            lines_edges[int(b) + i, int(a) + j] = [0, 255, 0]
#scale_percent = 80  # percent of original size
#width = int(img.shape[1] * scale_percent / 100)
#height = int(img.shape[0] * scale_percent / 100)
#dim = (width, height)
# resize image
#lines_edges = cv2.resize(lines_edges, dim, interpolation=cv2.INTER_AREA)
cv2.imshow('edges', lines_edges)
cv2.waitKey()
cv2.imwrite('line_parking.png', lines_edges)