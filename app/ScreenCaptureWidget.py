import sys
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QRubberBand
from PIL import ImageGrab
import cv2
import numpy as np

class ScreenCaptureWidget(QWidget):
    def __init__(self, parent=None, areaChosencallback=None):
        super().__init__(parent)
        self.areaChosencallback = areaChosencallback
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.label = QLabel(self)
        self.layout.addWidget(self.label)

        self.rubber_band = QRubberBand(QRubberBand.Shape.Rectangle, self)
        self.origin = None
        self.selection_enabled = False

    def show(self):
        self.label.clear()
        # self.main_window.setWindowOpacity(0.5)
        # self.setWindowFlags(Qt.WindoStawysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setWindowOpacity(0.2)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)

        self.selection_enabled = True
        super().show()

    def store_coordinates(self):
        if not self.selection_enabled:
            return
        
        self.rect = self.rubber_band.geometry()

    def capture_screen(self):
        self.img = ImageGrab.grab(bbox=self.rect.getCoords())
        return self.img
    
    def display_sample(self):
        converted_img = cv2.cvtColor(np.array(self.img), cv2.COLOR_RGB2BGR)
        
        image = QImage(converted_img, converted_img.shape[1], converted_img.shape[0], converted_img.strides[0], QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        # self._pixmap = self.resizeImage(pixmap)
        self.label.setPixmap(pixmap)
        
    
    def capture_screen_and_display(self):
        screen = QApplication.primaryScreen()
        winId = self.window().winId()
        self.capture_screen()
        self.display_sample()


    def mousePressEvent(self, event):
        if not self.selection_enabled:
            return
        
        if event.button() == Qt.MouseButton.LeftButton:
            self.origin = event.pos()
            self.rubber_band.setGeometry(QRect(self.origin, QSize()))
            self.rubber_band.show()

    def mouseMoveEvent(self, event):
        if not self.selection_enabled:
            return

        if self.origin:
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        if not self.selection_enabled:
            return
        
        if event.button() == Qt.MouseButton.LeftButton:
            self.rubber_band.hide()
            self.store_coordinates()
            self.capture_screen_and_display()
            self.selection_enabled = False
            self.areaChosencallback()
            self.origin = None

