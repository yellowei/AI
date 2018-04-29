# USAGE# python detect.py --images images# import the necessary packagesfrom __future__ import print_functionfrom imutils.object_detection import non_max_suppressionfrom imutils import pathsimport numpy as npimport argparseimport imutilsimport cv2# initialize the HOG descriptor/person detectorhog = cv2.HOGDescriptor()hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())camera = cv2.VideoCapture('./videos/test01.mp4')# 初始化视频流的第一帧firstFrame = Nonewhile True:  # 获取当前帧并初始化occupied/unoccupied文本  (grabbed, frame) = camera.read()  text = "Unoccupied"  # 如果不能抓取到一帧，说明我们到了视频的结尾  if not grabbed:    break  # 调整该帧的大小，转换为灰阶图像并且对其进行高斯模糊  frame = imutils.resize(frame, width=500)  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  gray = cv2.GaussianBlur(gray, (21, 21), 0)  # 如果第一帧是None，对其进行初始化  if firstFrame is None:    firstFrame = gray    continue  # 计算当前帧和第一帧的不同  frameDelta = cv2.absdiff(firstFrame, gray)  thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]  # 扩展阀值图像填充孔洞，然后找到阀值图像上的轮廓  thresh = cv2.dilate(thresh, None, iterations=2)  cv2.imshow('thresh',frame)  cv2.waitKey(0)  # (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # # 遍历轮廓  # for c in cnts:  #   # if the contour is too small, ignore it  #   # if cv2.contourArea(c) < args["min_area"]:  #   #   continue  #   # compute the bounding box for the contour, draw it on the frame,  #   # and update the text  #   # 计算轮廓的边界框，在当前帧中画出该框  #   (x, y, w, h) = cv2.boundingRect(c)  #   cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  #   text = "Occupied"