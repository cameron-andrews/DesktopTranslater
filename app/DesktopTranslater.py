import sys
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from RecognizerService import OCRProcessor
from ScreenCaptureWidget import ScreenCaptureWidget
from TranslationWidget import TranslationWidget

class WorkerThread(QThread):
    started_signal = pyqtSignal()
    stopped_signal = pyqtSignal()

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    def run(self):
        self.started_signal.emit()
        while not self.isInterruptionRequested():
            self.main_window.translate_area()
            # time.sleep(1)
        self.stopped_signal.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ocr_processor = OCRProcessor()
        self.worker_thread = None
        self.is_capturing = False
        self.original_geometry = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.screen_capture_widget = ScreenCaptureWidget(self.central_widget, self.on_area_chosen)
        layout.addWidget(self.screen_capture_widget)

        self.translation_widget = TranslationWidget()
        layout.addWidget(self.translation_widget)

        self.capture_button = QPushButton('Select Area', self.central_widget)
        self.capture_button.clicked.connect(self.show_screen_capture_widget)
        layout.addWidget(self.capture_button)

        self.continuous_button = QPushButton('Start', self.central_widget)
        self.continuous_button.clicked.connect(self.continuous_button_toggle)
        layout.addWidget(self.continuous_button)

    def show_screen_capture_widget(self):
        self.translation_widget.hide()
        self.original_geometry = self.geometry()
        screen_rect = QApplication.primaryScreen().availableGeometry()

        print("test3")
        self.setGeometry(screen_rect)
        self.setWindowOpacity(0.1)
        self.screen_capture_widget.show()

    def on_area_chosen(self):
        if self.original_geometry is None:
            self.setGeometry(100, 100, 800, 600)
        else:
            self.setGeometry(self.original_geometry)
        self.setWindowOpacity(1)
        extracted_text = self.ocr_processor.perform_ocr(self.screen_capture_widget.img)
        self.translation_widget.add_translation(extracted_text)
        self.translation_widget.show()    

    def start_translating(self):
        self.screen_capture_widget.hide()
        if self.worker_thread is None or not self.worker_thread.isRunning():
            self.worker_thread = WorkerThread(self)
            self.worker_thread.started_signal.connect(self.on_thread_started)
            self.worker_thread.stopped_signal.connect(self.on_thread_stopped)
            self.worker_thread.start()

    def stop_translating(self):
        if self.worker_thread is not None and self.worker_thread.isRunning():
            self.worker_thread.requestInterruption()
        self.screen_capture_widget.display_sample()
        self.screen_capture_widget.show()

    def translate_area(self):
        self.screen_capture_widget.capture_screen()
        extracted_text = self.ocr_processor.perform_ocr(self.screen_capture_widget.img)
        self.translation_widget.add_translation(extracted_text)

    def on_thread_started(self):
        print("Thread started")

    def on_thread_stopped(self):
        print("Thread stopped")

    def continuous_button_toggle(self):
        self.is_capturing = not self.is_capturing

        if self.is_capturing:
            self.continuous_button.setText('Stop')
            self.start_translating()
        else:
            self.continuous_button.setText('Start')
            self.stop_translating()

def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()