from aip import AipOcr
import cv2
from time import *
import os
from matplotlib import pyplot as plt

'''
功能：
调用百度接口，实现图片文字识别，如果文字识别正确，则进行图片比较，如果两者都匹配整个，则认为图片是一致的；

PicWord()：调用百度接口，实现图片文字识别
参数：无
返回值：无

PicCapture()：拍照功能，需要更新为最新的视频拍照
参数：无
返回值：无

PicSiftCompare(TemplePicPath,CapturePicPath)：实现图片比对，
参数：param TemplePicPath: 模板图片的位置
      param CapturePicPath: 拍照图片的位置 
返回值：返回两个图片的匹配分数

PicisSame(TemplePicPath,CapturePicPath):根据文字识别结果和图像识别结果，判断两个图片是否相同
参数：param TemplePicPath: 模板图片的位置
      param CapturePicPath: 拍照图片的位置 
返回值：返回两个图片的匹配结果
'''

def PicWord():
    """ 你的 APPID AK SK """
    APP_ID = '11470572' #你的 App ID
    API_KEY = 'o742Vcf0GdZ1nqsI1WfxkGyA' #你的 Api Key
    SECRET_KEY = 'GnKn7OpEFFTgzrWGKyokIG06OstRx4vM' #你的 Secret Key

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY) #获取百度文字识别的接口

    """ 读取图片 """
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    image = get_file_content('Screenshot_Capture.png')

    """ 调用通用文字识别, 图片参数为本地图片 """
    #results = client.basicGeneral(image)   #限50000次/Day

    """ 调用通用文字识别（高精度版） """
    results = client.basicAccurate(image)   #限500次/Day

    try:
        vals = results.get('words_result')
        finalresult = [item[k] for item in vals for k in item]
        print(finalresult)
        return finalresult
    except:
        print("get nothing")
        #需求重新获取图片

def PicCapture():
    '''
    获取截图
    '''
    global i
    i = 0
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    path = os.getcwd()

    picpath = path + '\\Capture\\'

    isExists = os.path.exists(picpath)

    print(picpath)

    if not isExists:
        # 不存在，则创建目录
        os.makedirs(picpath)
    else:
        pass

    cv2.imwrite(picpath + str(i) + '.jpg', frame)
    cap.release()
    i += 1

def PicSiftCompare(TemplePicPath,CapturePicPath):

    #img1 = cv2.imread('Screenshot_Capture.png', 0)  # queryImage
    #img2 = cv2.imread('Screenshot_Temple.png', 0)  # trainImage
    img1 = cv2.imread(CapturePicPath, 0)  # queryImage
    img2 = cv2.imread(TemplePicPath, 0)  # trainImage

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Apply ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.65 * n.distance:
            good.append([m])

    # cv2.drawMatchesKnn expects list of lists as matches.
    img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)

    Score = len(good) / len(matches)
    print(Score)
    #plt.imshow(img3), plt.show()   #Show the matching Pics
    return Score

def PicisSame(TemplePicPath,CapturePicPath):
    '''
    比较图片是否一致
    :param TemplePicPath: 模板图片的位置
    :param CapturePicPath: 拍照图片的位置
    :return: 返回两个图片是否匹配
    '''
    Words ={
        'Home1Words': [ '媒体','导航', '电话', '日历', '空调', '短信', '安吉星', ' Apple CarPlay']
    }

    ss = PicWord()

    Flg = [False for i in Words['Home1Words'] if i not in ss]

    if Flg:
        print("Not same")
    else:
        print("Word matching success")
        #执行图片比较，判断特征点是否匹配
        GetScore = PicSiftCompare(TemplePicPath,CapturePicPath)
        if GetScore <=0.4:
            print("Not Same")
        else:
            print("Same Pic")

if __name__ == '__main__':
    PicisSame('Screenshot_Temple.png','Screenshot_Capture.png')
