import sys
import cv2
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

subform_class = uic.loadUiType("Add_Target.ui")[0]

class Add_Target_Image(QDialog, subform_class):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.findimgfile.clicked.connect(self.FindImage)

    def FindImage(self):
        fname = QFileDialog.getOpenFileName(self)

        qformat = QImage.Format_Indexed8
        outimage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        
        #outimage = outimage.rgbSwapped()
        self.alreadyimage.setPixmap(QPixmap.fromImage(outimage))
        self.alreadyimage.setScaledContents(True)
        