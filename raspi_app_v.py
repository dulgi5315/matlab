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
        self.setGeometry(0, 0, 480, 800)  # 7인치 화면을 세로모드로 변경
        
        # 화면 회전 설정
        self.setFixedSize(480, 800)  # 크기 고정
        
        # 중앙 위젯 생성
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃 (세로 배치로 유지)
        layout = QVBoxLayout(central_widget)
        
        # 모드 선택 스택 위젯
        self.stack = QStackedWidget()
        
        # 메인 메뉴 페이지
        main_menu = QWidget()
        main_layout = QVBoxLayout(main_menu)
        
        # 메인 메뉴 버튼들 - 세로로 더 길게 조정
        menu_buttons = ['온도 설정', '단계', '사용자', '학습']
        for text in menu_buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(120)  # 버튼 높이 증가
            btn.setFixedWidth(400)   # 버튼 너비 설정
            main_layout.addWidget(btn, alignment=Qt.AlignCenter)
        
        self.stack.addWidget(main_menu)
        
        # 온도 설정 페이지
        temp_page = QWidget()
        temp_layout = QVBoxLayout(temp_page)
        
        temp_label = QLabel('온도 설정')
        temp_label.setAlignment(Qt.AlignCenter)
        temp_slider = QSlider(Qt.Vertical)  # 수평에서 수직으로 변경
        temp_slider.setRange(20, 40)
        temp_slider.setValue(36)
        temp_slider.setFixedHeight(400)  # 슬라이더 높이 조정
        
        temp_layout.addWidget(temp_label)
        temp_layout.addWidget(temp_slider, alignment=Qt.AlignCenter)
        
        self.stack.addWidget(temp_page)
        
        layout.addWidget(self.stack)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())