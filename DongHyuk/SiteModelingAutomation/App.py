from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget
from client.pages.Page1 import Page1
from client.pages.Page2 import Page2
from client.pages.Page3 import Page3
from client.pages.Page4 import Page4
from client.pages.Page5 import Page5
from model.process import Proccess

class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.map_path = None
        self.rhino_path = None
        self.target_path = None

        self.initUI()

    def initUI(self):
        self.stacked_widget = QStackedWidget(self)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stacked_widget)

        # 첫 번째 페이지
        self.page1 = Page1(self)
        # 두 번째 페이지
        self.page2 = Page2(self)

        # 세 번째 페이지
        self.page3 = Page3(self)
        
        # 네 번째 페이지
        self.page4 = Page4(self)
        
        # 다섯 번째 페이지
        self.page5 = Page5(self)

        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.page3)
        self.stacked_widget.addWidget(self.page4)
        self.stacked_widget.addWidget(self.page5)

        self.setWindowTitle('File Selector')
        self.setGeometry(300, 300, 1000, 200)
        self.show()
        
    def do_process(self):
        try:
            process = Proccess(self.map_path,self.rhino_path,self.target_path)
            process.call()
        except Exception as e:
            print(e)
            
        

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
