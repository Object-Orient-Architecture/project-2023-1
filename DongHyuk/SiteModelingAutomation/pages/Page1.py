from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLineEdit, QLabel, QMessageBox
import os

class Page1(QWidget):
                     
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.initUI()

    def initUI(self):
        #메세지
        instruction ='''어플리케이션의 정상적인 작동을 위해
                     \n국토정보플랫폼의 국토정보맵에서 간편지도 - 인덱스를 통해 
                     \n수치지형지도 Ver2.0을 다운로드 받은 후
                     \n.zip파일을 아래에서 선택해주세요.''' 
                     
        ngii_link = "<a href='https://www.ngii.go.kr/kor/main.do'>국토정보플랫폼 주소</a>"
        
        self.setLayout(QVBoxLayout())
        
        lbl = QLabel(instruction, self)
        self.layout().addWidget(lbl)
        
        link_lbl = QLabel(ngii_link, self)
        link_lbl.setOpenExternalLinks(True)
        self.layout().addWidget(link_lbl)

        hbox = QHBoxLayout()
        self.layout().addLayout(hbox)

        self.le = QLineEdit(self)
        hbox.addWidget(self.le)

        btn = QPushButton('파일 선택', self)
        btn.clicked.connect(self.select_file)
        hbox.addWidget(btn)
        
        hbox2 = QHBoxLayout()
        self.layout().addLayout(hbox2)
        
        next_btn = QPushButton('>다음', self)
        next_btn.clicked.connect(self.check_file_and_go_next)
        hbox2.addStretch(1)
        hbox2.addWidget(next_btn)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '지도 파일을 .zip형태로 선택해주세요', filter="Zip files (*.zip)")
        self.le.setText(file_path)
            
    def check_file_and_go_next(self):
        file_path = self.le.text()
        if os.path.exists(file_path):
            self.app.map_path = file_path
            self.app.stacked_widget.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, '파일 경로가 올바르지 않습니다', '파일을 다시 선택해주세요')
            
