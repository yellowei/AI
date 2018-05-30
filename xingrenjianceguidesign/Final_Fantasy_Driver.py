#Author:HuangLiang
#Time:2018/5/20

# import the necessary packages
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import imutils
import cv2

def imagetovideo(img_root,video_root,size):
    fps = 30  # 保存视频的FPS，可以适当调整
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    videoWriter = cv2.VideoWriter(video_root,fourcc,fps,size)  # 最后一个是保存图片的尺寸
    for imagePath in paths.list_images(img_root):
        frame = cv2.imread(imagePath)
        videoWriter.write(frame)
    videoWriter.release()

# 定义旋转rotate函数
def rotate(image, angle, center=None, scale=1.0):
    # 获取图像尺寸
    (h, w) = image.shape[:2]
    # 若未指定旋转中心，则将图像中心设为旋转中心
    if center is None:
        center = (w / 2, h / 2)
    # 执行旋转
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
    # 返回旋转后的图像
    return rotated

def main(Vpath):
    # initialize the HOG descriptor/person detector
    # hog = cv2.HOGDescriptor() #初始化方向梯度直方图描述子
    # hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector()) #设置支持向量机使得它成为一个预先训练好了的行人检测器。
    print("正在加载训练模型\n正在初始化HOG算子……")
    hog = cv2.HOGDescriptor()
    hog.load('myHogDector.bin')
    print('HOG特征描述子维度是', hog.getDescriptorSize())
    print("正在获取原始视频")
    camera = cv2.VideoCapture(Vpath)
    frame_num = 0
    while True:
        # 获取当前帧并初始化occupied/unoccupied文本
        (grabbed, frame) = camera.read()
        text = "Unoccupied"
        # 如果不能抓取到一帧，说明我们到了视频的结尾

        if not grabbed:
            print("视频处理完成")
            break
        # 调整该帧的大小
        frame = imutils.resize(frame, width=430)
        frame_num += 1

        # 如果视频提取帧后是旋转的，再将其转回来
        newframe = rotate(frame, 270)
        # newframe = frame
        nmsFrame = newframe.copy()
        size = list(nmsFrame.shape)
        image_copy = newframe.copy()

        # detect people in the frame
        (rects, weights) = hog.detectMultiScale(newframe, winStride=(8, 8), padding=(8, 8), scale=1.03)
        # draw the original bounding boxes
        for (x, y, w, h) in rects:
            cv2.rectangle(newframe, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # apply non-maxima suppression to the bounding boxes using a
        # fairly large overlap threshold to try to maintain overlapping
        # boxes that are still people
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

        # draw the final bounding boxes
        for (xA, yA, xB, yB) in pick:
            pic = cv2.rectangle(nmsFrame, (xA, yA), (xB, yB), (0, 255, 0), 2)
            cv2.imwrite('./videotoimage/%03d.jpg' % frame_num, nmsFrame)

        pic = list(pick)
        if len(pic) == 0:
            cv2.imwrite('./videotoimage/%03d.jpg' % frame_num, nmsFrame)

        for i in range(len(pic)):
            image_save = image_copy[pic[i][1]:pic[i][3], pic[i][0]:pic[i][2]]
            cv2.imwrite('./result/{}_{}.jpg'.format(str(frame_num), str(i)), image_save)

        print("第{}帧:{}个原始窗口,{}个非极大值抑制窗口".format(str(frame_num), len(rects), len(pick)))
        if len(rects) > len(pick):
            print("该帧的检测中非极大值抑制生效")

        # cv2.imshow("Before NMS", newframe)
        # cv2.imshow("After NMS", nmsFrame)
        # cv2.waitKey(1)

    image_root = './videotoimage'
    video_root = './result_video/saveVideo.avi'
    newsize = [0, 0]
    newsize[0] = size[1]
    newsize[1] = size[0]
    newsize = tuple(newsize)
    imagetovideo(image_root, video_root, newsize)
    print("处理后视频保存在当前目录下result_video文件夹中，名为saveVideo.avi")