from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFileDialog, QLineEdit, QMessageBox

class Page3(QWidget):

    def __init__(self, app):
        super().__init__()

        self.app = app
        self.initUI()

    def initUI(self):
        self.setLayout(QVBoxLayout())
        
        self.info_lbl = QLabel("경로가 모두 올바른지 확인하시고, 진행을 원하시는 경우 >다음 버튼을 눌러주세요!",self)
        self.layout().addWidget(self.info_lbl)

        self.map_path_lbl = QLabel(self)
        self.layout().addWidget(self.map_path_lbl)

        self.rhino_path_lbl = QLabel(self)
        self.layout().addWidget(self.rhino_path_lbl)

        self.target_path_lbl = QLabel(self)
        self.layout().addWidget(self.target_path_lbl)
        
        hbox = QHBoxLayout()
        self.layout().addLayout(hbox)
        
        next_btn = QPushButton('>다음', self)
        next_btn.clicked.connect(self.go_next)
        hbox.addStretch(1)
        hbox.addWidget(next_btn)

    def display_paths(self):
        self.map_path_lbl.setText(f"Map path: {self.app.map_path}")
        self.rhino_path_lbl.setText(f"Rhino path: {self.app.rhino_path}")
        self.target_path_lbl.setText(f"Target path: {self.app.target_path}")

    def showEvent(self, event):
        self.display_paths()
        
    def go_next(self):
        self.app.stacked_widget.setCurrentIndex(3)
