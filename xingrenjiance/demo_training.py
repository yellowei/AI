#Author:Huangliang   
#Time:2018/5/5

import cv2
import numpy as np
import random


def load_images(dirname, amout = 9999): #默认有9999张图片
    img_list = []
    file = open(dirname)  #只读，把dirname加载到内存，用file接收，.lst文件估计是文本文件
    img_name = file.readline()
    while img_name != '':  # 文件尾
        img_name = dirname.rsplit(r'/', 1)[0] + r'/' + img_name.split('/', 1)[1].strip('\n')
        # rsplit 通过指定分隔符对字符串进行分割并返回一个列表，默认分隔符为所有空字符，包括空格、换行(\n)、制表符(\t)等。
        # 类似于 split() 方法，只不过是从字符串最后面开始分割。
        img_list.append(cv2.imread(img_name))
        #读取图片像素点阵列加载到列表，append()方法向列表的尾部添加一个新的元素，imread读取三维阵列
        img_name = file.readline() #下一行
        amout -= 1 #计数器更新
        if amout <= 0: # 控制读取图片的数量
            break
    return img_list #返回一个图片像素点阵列列表（内存中存在，未保存），这是一个四维列表？
                     # 不，这是一个一维列表，只是这个列表里面的元素为三维数组



# 从每一张没有人的原始图片中随机裁出10张64*128的图片作为负样本
def sample_neg(full_neg_lst, neg_list, size):
    random.seed(1) # random()方法返回随机生成的一个实数，它在[0,1)范围内。
    width, height = size[1], size[0]
    for i in range(len(full_neg_lst)):
        # full_neg_lst是一个列表，里面存在着len(full_neg_lst)张图片，
        # 每个图片都以三维数组存在（array），最内层数组[]是一个像素点三个通道的数值
        for j in range(10): #
            y = int(random.random() * (len(full_neg_lst[i]) - height))
            #len(full_neg_lst[i])是第i+1张图片高度
            # len(full_neg_lst[i])就是在计算list所包含的第i+1个array的长度。
            # 最内层的[]表示一个像素点，有三个通道的数值；次内层[[ ]]表示一行，即为列数、图像宽度；
            # 外层[[[ ]]]表示全行，即为行数、图像高度
            x = int(random.random() * (len(full_neg_lst[i][0]) - width))
            # len(full_neg_lst[i][0])是第i+1张图片宽度
            neg_list.append(full_neg_lst[i][y:y + height, x:x + width])
    return neg_list  #这也是类似于full_neg_lst的列表list


# wsize: 处理图片大小，通常64*128; 输入图片尺寸>= wsize
def computeHOGs(img_lst, gradient_lst, wsize=(128, 64)):
    hog = cv2.HOGDescriptor()
    # hog.winSize = wsize
    for i in range(len(img_lst)):
        if img_lst[i].shape[1] >= wsize[1] and img_lst[i].shape[0] >= wsize[0]:
            roi = img_lst[i][(img_lst[i].shape[0] - wsize[0]) // 2: (img_lst[i].shape[0] - wsize[0]) // 2 + wsize[0], \
                  (img_lst[i].shape[1] - wsize[1]) // 2: (img_lst[i].shape[1] - wsize[1]) // 2 + wsize[1]]
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            gradient_lst.append(hog.compute(gray))
    # return gradient_lst


def get_svm_detector(svm):
    sv = svm.getSupportVectors() #获取支持向量机
    rho, _, _ = svm.getDecisionFunction(0)  #没搞清楚什么意思
    sv = np.transpose(sv) #改变高维数组的形状
    return np.append(sv, [[-rho]], 0)


# 主程序
# 第一步：计算HOG特征
neg_list = []
pos_list = []
gradient_lst = []
labels = []
hard_neg_list = []
svm = cv2.ml.SVM_create() #创建svm分类器
# 打开一个.lst文件，读取里面事先写好的图片名列表，在一张大列表中存入所有图片的像素点信息，并返回该列表
pos_list = load_images(r'G:/python_project/INRIAPerson/96X160H96/Train/pos.lst')
full_neg_lst = load_images(r'G:/python_project/INRIAPerson/train_64x128_H96/neg.lst')
sample_neg(full_neg_lst, neg_list, [128, 64])
print(len(neg_list))
computeHOGs(pos_list, gradient_lst)
[labels.append(+1) for _ in range(len(pos_list))]
computeHOGs(neg_list, gradient_lst)
[labels.append(-1) for _ in range(len(neg_list))]

# 第二步：训练SVM
svm.setCoef0(0)
svm.setCoef0(0.0)
svm.setDegree(3)
criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 1000, 1e-3)
svm.setTermCriteria(criteria)
svm.setGamma(0)
svm.setKernel(cv2.ml.SVM_LINEAR)
svm.setNu(0.5)
svm.setP(0.1)  # for EPSILON_SVR, epsilon in loss function?
svm.setC(0.01)  # From paper, soft classifier
svm.setType(cv2.ml.SVM_EPS_SVR)  # C_SVC # EPSILON_SVR # may be also NU_SVR # do regression task
svm.train(np.array(gradient_lst), cv2.ml.ROW_SAMPLE, np.array(labels))

# 第三步：加入识别错误的样本，进行第二轮训练
# 参考 http://masikkk.com/article/SVM-HOG-HardExample/
hog = cv2.HOGDescriptor()
hard_neg_list.clear()
hog.setSVMDetector(get_svm_detector(svm))
for i in range(len(full_neg_lst)):
    rects, wei = hog.detectMultiScale(full_neg_lst[i], winStride=(4, 4),padding=(8, 8), scale=1.05)
    for (x,y,w,h) in rects:
        hardExample = full_neg_lst[i][y:y+h, x:x+w]
        hard_neg_list.append(cv2.resize(hardExample,(64,128)))
computeHOGs(hard_neg_list, gradient_lst)
[labels.append(-1) for _ in range(len(hard_neg_list))]
svm.train(np.array(gradient_lst), cv2.ml.ROW_SAMPLE, np.array(labels))


# 第四步：保存训练结果
hog.setSVMDetector(get_svm_detector(svm))
hog.save('myHogDector.bin')