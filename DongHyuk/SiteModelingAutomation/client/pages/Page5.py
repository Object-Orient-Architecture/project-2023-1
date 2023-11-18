from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class Page5(QWidget):

    def __init__(self, app):
        super().__init__()

        self.app = app
        self.initUI()

    def initUI(self):
        self.setLayout(QVBoxLayout())

        self.thank_you_lbl = QLabel("실행이 완료되었습니다!", self)
        self.layout().addWidget(self.thank_you_lbl)

        self.finish_btn = QPushButton("종료", self)
        self.finish_btn.clicked.connect(self.app.close)
        self.layout().addWidget(self.finish_btn)
