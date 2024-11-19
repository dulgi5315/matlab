from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # 메인 윈도우 설정
        self.setWindowTitle('전기매트 컨트롤러')
        
        # 전체화면 설정
        self.showFullScreen()  # 전체화면으로 표시
        
        # 화면 해상도 얻기
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        
        # ESC 키로 종료할 수 있도록 단축키 설정
        self.shortcut = QShortcut(QKeySequence('Esc'), self)
        self.shortcut.activated.connect(self.close)
        
        # 중앙 위젯 생성
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        layout = QVBoxLayout(central_widget)
        
        # 모드 선택 스택 위젯
        self.stack = QStackedWidget()
        
        # 메인 메뉴 페이지
        main_menu = QWidget()
        main_layout = QVBoxLayout(main_menu)
        self.stack.addWidget(main_menu)
        
        # 온도 설정 페이지
        temp_page = QWidget()
        temp_layout = QVBoxLayout(temp_page)
        self.stack.addWidget(temp_page)
        
        layout.addWidget(self.stack)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())