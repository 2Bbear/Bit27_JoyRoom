import sys
import datetime
import cv2
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

logform_class = uic.loadUiType("0626_DATE_LOAD_UI.ui")[0]

class HisTory_Log_Show(QDialog, logform_class):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.takelogbtn.clicked.connect(self.takelog)           #test

    def takelog(self):
        sys.exit()