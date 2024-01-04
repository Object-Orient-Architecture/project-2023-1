from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget
from os import remove, rmdir
from pages.Page1 import Page1
from pages.Page2 import Page2
from pages.Page3 import Page3
from pages.Page4 import Page4
from pages.Page5 import Page5
from model.A_process import Proccess

class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        # 파일 경로를 저장할 변수들을 초기화합니다.
        self.map_path = None
        self.rhino_path = None
        self.target_path = None
        
        # 프로그램이 종료할 때 성공 혹은 오류 발생을 알리는 메세지
        self.fin_message = "실행이 완료되었습니다!\n 작동 이상이 발생했다면 지도 파일(.Zip)을 보내주세요!\n이메일: dpemrk7@gmail.com" #type:str

        # UI를 초기화합니다.
        self.initUI()

    def initUI(self):
        # QStackedWidget을 생성합니다. 여러 페이지를 스택처럼 쌓아놓을 수 있습니다.
        self.stacked_widget = QStackedWidget(self)
        # 레이아웃을 설정합니다.
        self.setLayout(QVBoxLayout())
        # 스택 위젯을 레이아웃에 추가합니다.
        self.layout().addWidget(self.stacked_widget)

        # 각 페이지를 생성합니다. 생성자에 this를 전달하여 각 페이지가 이 앱 인스턴스를 참조할 수 있게 합니다.
        self.page1 = Page1(self)  # 첫 번째 페이지
        self.page2 = Page2(self)  # 두 번째 페이지
        self.page3 = Page3(self)  # 세 번째 페이지
        self.page4 = Page4(self)  # 네 번째 페이지
        self.page5 = Page5(self)  # 다섯 번째 페이지

        # 각 페이지를 스택 위젯에 추가합니다.
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.page3)
        self.stacked_widget.addWidget(self.page4)
        self.stacked_widget.addWidget(self.page5)

        # 창의 제목을 설정합니다.
        self.setWindowTitle('Site Modeling Automation')
        # 창의 위치와 크기를 설정합니다.
        self.setGeometry(300, 300, 1000, 200)
        # 창을 표시합니다.
        self.show()

    def do_process(self):
        # Proccess 객체를 생성하고 이를 호출하여 작업을 수행합니다.
        # 오류가 발생하면 콘솔에 출력합니다.
        try:
            process = Proccess(self.map_path,self.rhino_path,self.target_path)
            process.call_sma()
            print("APP | Process Done!")
        except Exception as e:
            self.fin_message = '''작동 중 오류가 발생했습니다! 아래 오류 메세지와 작업하고자 했던 파일(.Zip)을 같이 보내주세요!
                                  \n이메일 : dpemrk7@gmail.com\n\n''' + str(e)
            
            

if __name__ == '__main__':
    import sys
    # QApplication 객체를 생성합니다.
    app = QApplication(sys.argv)
    # MyApp 객체를 생성합니다.
    ex = MyApp()
    # 이벤트 루프를 시작합니다.
    sys.exit(app.exec_())
