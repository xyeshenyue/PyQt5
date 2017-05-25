# -*- coding: utf-8 -*-

"""
    【简介】
    测试用例


"""

import sys
import unittest
from PyQt5.QtWidgets import *
#from PyQt5.QtGui import *
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt , QThread  ,  pyqtSignal
import CallMatrixWinUi
import time

#继承 QThread 类
class BackWorkThread(QThread):  
	#声明一个信号，同时返回一个str
	finishSignal = pyqtSignal(str)
	#构造函数里增加形参
	def __init__(self, sleepTime,parent=None):
		super(BackWorkThread, self).__init__(parent)
		#储存参数
		self.sleepTime = sleepTime

	#重写 run() 函数，在里面定时执行业务。
	def run(self):
		#休眠一段时间
		time.sleep(self.sleepTime)
		#休眠结束，发送一个信号告诉主线程窗口
		self.finishSignal.emit('ok , begin to close Window')
		
class MatrixWinTest(unittest.TestCase):

    # 初始化工作  
	def setUp(self):  
		print('*** setUp ***')
		self.app = QApplication(sys.argv)	
		self.form = CallMatrixWinUi.CallMatrixWinUi()
		
		#新建对象，传入参数
		self.bkThread = BackWorkThread(int(3))
		#连接子进程的信号和槽函数
		#self.bkThread.finishSignal.connect(self.closeWindow)
		self.bkThread.finishSignal.connect(self.closeWindow)
		#开始执行 run() 函数里的内容
		self.bkThread.start()
		
		self.form.show()
		
        
	# 退出清理工作  
	def tearDown(self):  
		print('*** tearDown ***')
		self.app.exec_()  		
		
	def setFormToZero(self):
		print('* setFormToZero *')  
				
		self.form.ui.tequilaScrollBar.setValue(0)
		self.form.ui.tripleSecSpinBox.setValue(0)
		self.form.ui.limeJuiceLineEdit.setText("0.0")
		self.form.ui.iceHorizontalSlider.setValue(0)
		

	def closeWindow(self):
		#time.sleep(5)
		print( '*  closeWindow  *')
		#qApp = QApplication.instance()
		#qApp.quit()		
		self.app.quit()
		
		
	def test_defaults(self):
		'''测试GUI处于默认状态'''
		print('* test_defaults *')
		self.assertEqual(self.form.ui.tequilaScrollBar.value(), 8)
		self.assertEqual(self.form.ui.tripleSecSpinBox.value(), 4)
		self.assertEqual(self.form.ui.limeJuiceLineEdit.text(), "12.0")
		self.assertEqual(self.form.ui.iceHorizontalSlider.value(), 12)
		self.assertEqual(self.form.ui.speedButtonGroup.checkedButton().text(), "&Karate Chop")
		
		print('*** speedName='+ self.form.getSpeedName() )
	
		# 用鼠标左键按OK
		okWidget = self.form.ui.buttonBox.button(self.form.ui.buttonBox.Ok)
		QTest.mouseClick(okWidget, Qt.LeftButton)
		
		# 即使没有按OK，Class也处于默认状态
		self.assertEqual(self.form.getJiggers() , 36.0)
		self.assertEqual(self.form.getSpeedName(), "&Karate Chop")
		      	
		
	# 测试滚动条
	def test_moveScrollBar(self):		
		print('* test_moveScrollBar ---')
		self.setFormToZero()
		    			
        # Push OK with the left mouse button
		okWidget = self.form.ui.buttonBox.button(self.form.ui.buttonBox.Ok)
		QTest.mouseClick(okWidget, Qt.LeftButton)



	
if __name__ == "__main__":  
	#app = QApplication(sys.argv)	
	unittest.main() 	
	
	#suite = unittest.TestSuite()
	#suite.addTest(MatrixWinTest("test_defaults"))
	#runner = unittest.TextTestRunner()
	#runner.run(suite)
	
	#sys.exit(app.exec_())