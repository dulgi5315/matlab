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
        
        # 7인치 디스플레이 해상도에 맞춤
        self.setGeometry(0, 0, 800, 480)
        
        # ESC 단축키
        self.shortcut = QShortcut(QKeySequence('Esc'), self)
        self.shortcut.activated.connect(self.close)
        
        # 중앙 위젯 및 메인 레이아웃
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)  # 여백 축소
        main_layout.setSpacing(10)  # 위젯 간 간격 축소
        
        # 상단 영역
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setSpacing(10)  # 위젯 간 간격 축소
        top_layout.setContentsMargins(0, 0, 0, 0)  # 여백 제거
        
        # 메뉴 버튼 생성 부분
        class RotatedMenuButton(QPushButton):
            def paintEvent(self, event):
                super().paintEvent(event)
                painter = QPainter(self)
                painter.setFont(QFont('', 24))
                painter.translate(self.width()/2, self.height()/2)
                painter.rotate(-90)
                painter.drawText(QRect(-15, -15, 30, 30), Qt.AlignCenter, '≡')

        menu_btn = RotatedMenuButton()
        menu_btn.setFixedSize(50, 50)
        menu_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 2px solid #ddd;
                border-radius: 8px;
            }
        """)
        # 여기에 클릭 이벤트 연결 추가
        menu_btn.clicked.connect(self.show_menu)
        top_layout.addWidget(menu_btn)
        
        # 회전된 텍스트를 표시할 커스텀 위젯
        class RotatedLabel(QWidget):
            def __init__(self, text, parent=None):
                super().__init__(parent)
                self.text = text
                self.font = QFont()
                self.font.setPointSize(20)
                self.font.setBold(True)
                
            def paintEvent(self, event):
                painter = QPainter(self)
                painter.setFont(self.font)
                painter.translate(self.width()/2, self.height()/2)
                painter.rotate(-90)
                painter.drawText(QRect(-50, -15, 100, 30), Qt.AlignCenter, self.text)

		# 상단 사각형 3개
        temperatures = ['36.5', '37.0', '37.5']
        for temp in temperatures:
            box = QFrame()
            box.setFrameStyle(QFrame.Box | QFrame.Plain)
            box.setStyleSheet("""
                QFrame {
                    border: 2px solid #ddd;
                    background-color: white;
                    border-radius: 8px;
                }
            """)
            box.setFixedSize(180, 180)
            
            # 온도 라벨 추가
            layout = QVBoxLayout(box)
            label = RotatedLabel(temp)
            layout.addWidget(label)
            top_layout.addWidget(box)
        
        # 종료 버튼
        exit_btn = QPushButton('×')
        exit_btn.setFixedSize(50, 50)  # 크기 축소
        exit_btn.clicked.connect(self.close)
        exit_btn.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                background-color: #ff6b6b;
                color: white;
                border: none;
                border-radius: 8px;
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
        bottom_layout.setContentsMargins(0, 0, 0, 0)  # 여백 제거
        
        # 하단 긴 사각형
        bottom_box = QFrame()
        bottom_box.setFrameStyle(QFrame.Box | QFrame.Plain)
        bottom_box.setStyleSheet("""
            QFrame {
                border: 2px solid #ddd;
                background-color: white;
                border-radius: 8px;
            }
        """)
        bottom_box.setFixedSize(590, 280)  # 너비를 540으로, 높이를 200으로 수정
        bottom_layout.addWidget(bottom_box)
        
        main_layout.addWidget(bottom_widget)
        
    def show_menu(self):
        def show_menu(self):
            self.menu_window = MenuWindow()
            
			# 화면의 중앙 위치 계산
			screen = QApplication.primaryScreen().geometry()
			menu_size = self.menu_window.geometry()
			
			# 화면 중앙에 위치하도록 x, y 좌표 계산
			center_x = (screen.width() - menu_size.width()) // 2
			center_y = (screen.height() - menu_size.height()) // 2
			
			# 메뉴 창 위치 설정
			self.menu_window.move(center_x, center_y)
			self.menu_window.show()

class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 창 속성을 Tool로 설정하여 작업 표시줄에 표시되지 않도록 함
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        # 창이 포커스를 잃으면 자동으로 닫히도록 설정
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.installEventFilter(self)
        self.initUI()
    
    def eventFilter(self, obj, event):
        # 창이 포커스를 잃으면 닫기
        if event.type() == QEvent.WindowDeactivate:
            self.close()
        return super().eventFilter(obj, event)

    def initUI(self):
        self.setFixedSize(300, 400)
        
        layout = QHBoxLayout()
        
        # 예약 버튼
        reserve_btn = RotatedButton('예약')
        reserve_btn.setFixedSize(120, 350)
        reserve_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 2px solid #ddd;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        
        # 모드 설정 버튼
        mode_btn = RotatedButton('모드 설정')
        mode_btn.setFixedSize(120, 350)
        mode_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 2px solid #ddd;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        
        layout.addWidget(reserve_btn)
        layout.addWidget(mode_btn)
        
        self.setLayout(layout)

class RotatedButton(QPushButton):
    def __init__(self, text):
        super().__init__()
        self.btn_text = text
        
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setFont(QFont('', 14))
        painter.translate(self.width()/2, self.height()/2)
        painter.rotate(-90)
        rect = QRect()
        rect.setWidth(100)  # 텍스트 영역의 너비
        rect.setHeight(20)  # 텍스트 영역의 높이
        rect.moveCenter(QPoint(0, 0))  # 중앙 정렬
        
        painter.drawText(rect, Qt.AlignCenter, self.btn_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())