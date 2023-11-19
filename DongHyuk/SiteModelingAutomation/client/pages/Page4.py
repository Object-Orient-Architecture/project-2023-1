from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
import os

class ProcessThread(QThread):
    finished = pyqtSignal()

    def __init__(self, app):
        super().__init__()
        self.app = app

    def run(self):
        self.app.do_process()
        self.finished.emit()

class Page4(QWidget):

    def __init__(self, app):
        super().__init__()

        self.app = app
        self.initUI()
        self.method_called = False

    def initUI(self):
        self.setLayout(QVBoxLayout())
        self.loading_lbl = QLabel("작업 중...\n 곧 표시될 라이노 파일을 종료하면 프로그램도 종료됩니다.", self)
        self.layout().addWidget(self.loading_lbl)

    def showEvent(self, event):
        super().showEvent(event)
        if not self.method_called:
            QMessageBox.warning(self,"작업이 곧 시작됩니다!","Rhino가 곧 실행될 예정입니다.잠시만 기다려주세요.")
            self.method_called = True
            self.thread = ProcessThread(self.app)
            self.thread.finished.connect(self.on_process_finished)
            self.thread.start()

    def on_process_finished(self):
        self.app.stacked_widget.setCurrentIndex(4)
