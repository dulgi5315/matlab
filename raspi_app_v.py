from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('전기매트 컨트롤러')
        self.showFullScreen()
        
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        
        # ESC 단축키
        self.shortcut = QShortcut(QKeySequence('Esc'), self)
        self.shortcut.activated.connect(self.close)
        
        # 중앙 위젯 및 메인 레이아웃
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)  # 여백 설정
        
        # 상단 영역
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setSpacing(20)  # 위젯 간 간격
        
        # 메뉴 버튼
        menu_btn = QPushButton('≡')  # 메뉴 아이콘
        menu_btn.setFixedSize(60, 60)
        menu_btn.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                background-color: #f0f0f0;
                border: 2px solid #ddd;
                border-radius: 10px;
            }
        """)
        top_layout.addWidget(menu_btn)
        
        # 상단 사각형 3개
        for _ in range(3):
            box = QFrame()
            box.setFrameStyle(QFrame.Box | QFrame.Plain)
            box.setStyleSheet("""
                QFrame {
                    border: 2px solid #ddd;
                    background-color: white;
                    border-radius: 10px;
                }
            """)
            box.setMinimumSize(200, 150)
            top_layout.addWidget(box)
        
        # 종료 버튼
        exit_btn = QPushButton('×')  # 종료 아이콘
        exit_btn.setFixedSize(60, 60)
        exit_btn.clicked.connect(self.close)
        exit_btn.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                background-color: #ff6b6b;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #ff5252;
            }
        """)
        top_layout.addWidget(exit_btn)
        
        main_layout.addWidget(top_widget)
        
        # 중간 여백
        main_layout.addStretch()
        
        # 하단 영역
        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout(bottom_widget)
        
        # 하단 긴 사각형
        bottom_box = QFrame()
        bottom_box.setFrameStyle(QFrame.Box | QFrame.Plain)
        bottom_box.setStyleSheet("""
            QFrame {
                border: 2px solid #ddd;
                background-color: white;
                border-radius: 10px;
            }
        """)
        bottom_box.setMinimumHeight(100)
        bottom_layout.addWidget(bottom_box)
        
        main_layout.addWidget(bottom_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())