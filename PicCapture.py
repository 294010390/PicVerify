import cv2
from time import *
import os

#ini_image=Image.open(r'C:\Users\ZhangJiankai\Desktop\13.jpg')
i = 0
def capture():
	'''
	获取截图
	'''
	global i
	cap = cv2.VideoCapture(0)
	ret, frame = cap.read()
	path = os.getcwd()

	picpath = path + '\\Capture\\'

	isExists = os.path.exists(picpath)

	print(picpath)

	if not isExists:
		#不存在，则创建目录
		os.makedirs(picpath)
	else:
		pass

	cv2.imwrite(picpath+str(i)+'.jpg', frame)
	cap.release()
	i += 1


if __name__ == '__main__':

	for i in range(20):
		capture()
		sleep(1)


	



