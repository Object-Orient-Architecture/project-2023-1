from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox

class Page4(QWidget):

    def __init__(self, app):
        super().__init__()

        self.app = app
        self.initUI()
        self.method_called = False

    def initUI(self):
        self.setLayout(QVBoxLayout())
        self.loading_lbl = QLabel("작업 중...", self)
        self.layout().addWidget(self.loading_lbl)
        
    def showEvent(self, event):
        if not self.method_called:
            QMessageBox.warning(self,"작업이 곧 시작됩니다!","Rhino가 곧 실행될 예정입니다.잠시만 기다려주세요.")
            self.initUI()
            super().showEvent(event)
            self.app.do_process()

            self.method_called = True
            self.app.stacked_widget.setCurrentIndex(4)
        
