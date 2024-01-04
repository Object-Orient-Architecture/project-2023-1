from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLineEdit, QLabel, QMessageBox
import os

class Page2(QWidget):

    def __init__(self, app):
        super().__init__()

        self.app = app
        self.initUI()

    def initUI(self):
        self.setLayout(QVBoxLayout())

        self.page2_lbl = QLabel(self)
        self.layout().addWidget(self.page2_lbl)

        lbl2 = QLabel('''라이노 실행파일 Rhino(Version).exe를 선택해주세요
                      \n 일반적으로 C:\Program Files\Rhino (X)\System\Rhino.exe 에 위치합니다.
                      ''', self)
        self.layout().addWidget(lbl2)

        hbox1 = QHBoxLayout()
        self.layout().addLayout(hbox1)

        self.le2 = QLineEdit(self)
        self.le2.setText('C:\Program Files\Rhino 6\System\Rhino.exe')
        hbox1.addWidget(self.le2)

        btn2 = QPushButton('라이노 실행파일 선택', self)
        btn2.clicked.connect(self.select_file2)
        hbox1.addWidget(btn2)

        lbl3 = QLabel('결과를 저장할 위치를 선택해주세요', self)
        self.layout().addWidget(lbl3)
        
        hbox2 = QHBoxLayout()
        self.layout().addLayout(hbox2)

        self.le3 = QLineEdit(self)
        
        hbox2.addWidget(self.le3)

        btn3 = QPushButton('폴더 선택', self)
        btn3.clicked.connect(self.select_directory)
        hbox2.addWidget(btn3)

        hbox3 = QHBoxLayout()
        self.layout().addLayout(hbox3)

        back_btn = QPushButton('<뒤로', self)
        back_btn.clicked.connect(self.go_back)
        hbox3.addStretch(1)
        hbox3.addWidget(back_btn)

        next_btn = QPushButton('>다음', self)
        next_btn.clicked.connect(self.check_and_go_next)
        hbox3.addWidget(next_btn)
        
    def showEvent(self, event):
        self.le3.setText(os.path.dirname(self.app.map_path) + "\\result")
    
    def go_back(self):
        self.app.stacked_widget.setCurrentIndex(0)

    def select_file2(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '라이노 실행파일을 선택해주세요.', filter="Executable files (*.exe)")
        self.le2.setText(file_path)

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.le3.setText(dir_path)

    def check_and_go_next(self):
        file_path = self.le2.text()
        dir_path = self.le3.text()
        
        if os.path.exists(file_path) and file_path[-9:-4] == 'Rhino' and file_path.endswith(".exe"):
            if os.path.exists(dir_path):
                pass
            else:
                os.makedirs(dir_path)
            
            self.app.rhino_path = file_path
            self.app.target_path = dir_path
            self.app.stacked_widget.setCurrentIndex(2)
        else:
            QMessageBox.warning(self, "라이노 파일 선택 오류", "라이노 파일이 아니거나 경로가 올바르지 않습니다. 확인해주세요.")
