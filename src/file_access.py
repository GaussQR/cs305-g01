from zipfile import ZipFile 
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import *
import sys, os, shutil
from facrecog_core import *

def file_wrapper1():
	dlg = FileAccess1()

class FileAccess1(QWidget):

	def __init__(self, *args, **kwargs):
		super(FileAccess1).__init__()
		super(FileAccess1, self).__init__(*args, **kwargs)
		self.title = ' SELECT FILE '
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480
		self.initUI()
	
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.openFileNameDialog()
		self.show()

	def openFileNameDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","zip files (*.zip)", options=options)
		if fileName: print(fileName)
		npath = '/'.join(fileName.split('/')[:-1])
		print(npath)
		os.chdir(npath)
		with ZipFile(fileName, 'r') as zip:
			zip.extractall()
		folder_name = zip.namelist()[0][:-1]
		add_target_faces(folder_name)
		shutil.rmtree(folder_name)

def file_wrapper2():
	dlg = FileAccess2()
	# dlg.exec_()

class FileAccess2(QWidget):

	def __init__(self, *args, **kwargs):
		super(FileAccess2).__init__()
		super(FileAccess2, self).__init__(*args, **kwargs)
		self.title = ' SELECT FILE '
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480
		self.initUI()
	
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)		
		self.openFileNameDialog()
		# self.openFileNamesDialog()
		# self.saveFileDialog()
		self.show()

	
	def openFileNameDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","zip files (*.zip)", options=options)
		if fileName:
			print(fileName)
		npath = '/'.join(fileName.split('/')[:-1])
		print(npath)
		os.chdir(npath)
		with ZipFile(fileName, 'r') as zip:
			zip.extractall()
		folder_name = zip.namelist()[0][:-1]
		faces = load_encoded_faces()
		rs = identify_faces_images(folder_name, faces, 1)
		shutil.rmtree(folder_name)
		with open('output/output.pkl', 'wb') as fp:
			pickle.dump(rs, fp)
	# def saveFileDialog(self):
	# 	options = QFileDialog.Options()
	# 	options |= QFileDialog.DontUseNativeDialog
	# 	fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getOpenFileName()", "","zip files (*.zip)", options=options)
	# 	if fileName:
	# 		print(fileName)