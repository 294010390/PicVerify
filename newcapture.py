import cv2
from PIL import Image
#使用第三方库：Pillow
import math
import operator
from functools import reduce
import os
import sys

#ini_image=Image.open(r'C:\Users\ZhangJiankai\Desktop\13.jpg')

class PicVerify(object):
	
	'''
	拍照和默认图片是否一致；
	参数pic：默认图片的路径；
	'''
	def __init__(self,pic):

		self.ini_image = Image.open(pic)
		self.path = '..\\Picture\\ScreenShot\\'
		#self.picpath = self.path + '14.jpg'



	def capture(self):
		'''
		获取截图
		'''
		cap = cv2.VideoCapture(0)
		ret, frame = cap.read()
		#path = os.getcwd()
		#newpath = '..\\Picture\\Screenshot\\'
		#picpath = self.path + '14.jpg'

		#cv2.imwrite(r'C:\Users\ZhangJiankai\Desktop\14.jpg', frame)
		cv2.imwrite(self.path+'14.jpg', frame)
		print(os.path.dirname(self.path))
		print ("sys.argv[0]=%s" % sys.argv[0])
		cap.release()


	def verify(self):
		'''
		对比图片是否相同
		'''
		new_image=Image.open(self.path+'14.jpg')
		h1=self.ini_image.histogram()
		h2=new_image.histogram()
		h3=[]

		for i in range(len(h1)):
			h3.append(0)

		result1 = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
		result2 = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h3)))/len(h1) )
		'''
		sqrt:计算平方根，reduce函数：前一次调用的结果和sequence的下一个元素传递给operator.add
		operator.add(x,y)对应表达式：x+y
		这个函数是方差的数学公式：S^2= ∑(X-Y) ^2 / (n-1)
		'''
		print(result1/result2 )
		#result的值越大，说明两者的差别越大；如果result=0,则说明两张图一模一样
		if result1/result2 < 1:
			print("Same")
		else:
			print("Different")

	def Verifyresult(self):
		'''
		验证截图与预存图片是否相同
		'''
		self.capture()
		self.verify()

if __name__ == '__main__':

	newpic = PicVerify(r'D:\Code\Python\Phone_Interuption\Picture\PicTemp\13.jpg')
	#newpic.capture()
	#newpic.verify()
	newpic.Verifyresult()



	



