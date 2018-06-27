import sys
import datetime
import cv2
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

showform_class = uic.loadUiType("Cam_Detail_Show.ui")[0]

class Detail_Show(QDialog, showform_class):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

    def takelog(self):
        sys.exit()
