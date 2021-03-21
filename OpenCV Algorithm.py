import pydicom as pdcm
import PIL.Image as IMG
import numpy as np
import cv2
import os
pdcm.Sequence()
file_path = r"C:\Users\MERT\Desktop\Biokido\Bacak"
file_path_list = os.listdir(file_path)
cnt_volume_array = np.array([])
closed_cnt = []
pixel_counter = 0

def PolygonArea(corners):
    n = len(corners)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area



for i in range(len(file_path_list)):
    file_name = file_path_list[i]
    im = cv2.imread(file_path + "/" + file_name)
    im = cv2.fastNlMeansDenoisingColored(im, None, 10, 10, 7, 21)
    roi = cv2.selectROI("contour", im)
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    x, y, w, h = roi
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im_gray = im_gray[y:y + h, x:x + w]
    clahe = cv2.createCLAHE(clipLimit=5.5, tileGridSize=(8, 8))
    im_gray = clahe.apply(im_gray)
    ret, th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    #np.ones((5, 5), np.uint8)
    dilate = cv2.morphologyEx(th, cv2.MORPH_DILATE, kernel, 3)
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for k in range(len(contours)):
        if cv2.contourArea(contours[k]) > cv2.arcLength(contours[k], True):
            cv2.drawContours(im[y:y + h, x:x + w], contours[k], -1, (255, 0, 0), 3)
            hull = cv2.convexHull(contours[k])
            total_area = cv2.contourArea(hull)
            #cv2.fillConvexPoly(im[y:y + h, x:x + w], hull, (0, 255, 0))
            th_w, th_h = th.shape
            for q in range(th_w):
                for e in range(th_h):
                    if cv2.pointPolygonTest(contours[k], (q, e), False) == 1:
                        if th[q][e] == 0:
                            pixel_counter += 1


    cnt_area_array = np.array([cv2.contourArea(contours[j]) for j in range(len(contours))])
    total_cnt_area = np.sum(cnt_area_array)
    np.append(cnt_volume_array, total_cnt_area)
    print("Percentage of contour area is : " + str(int(pixel_counter / total_area * 100)) + "%")

    cv2.imshow("contour", im)
    cv2.imshow("mask", th)
    cv2.waitKey(1000)
    pixel_counter = 0
print(cnt_volume_array)

cv2.destroyAllWindows()
