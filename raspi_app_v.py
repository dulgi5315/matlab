from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        # 윈도우가 표시된 후 모드 설정창 열기
        QTimer.singleShot(100, self.show_mode_window)
        
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
        menu_btn = RotatedButton('≡')
        menu_btn.setFixedSize(50, 50)
        menu_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 2px solid #ddd;
                border-radius: 8px;
            }
        """)
        # 여기에 클릭 이`벤트 연결 추가
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
        
        # 하단 사각형 영역
        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # 메뉴 버튼 너비만큼 왼쪽 여백 추가
        bottom_layout.addSpacing(20)  # 메뉴 버튼(50) + 간격(10)
        
        # 하단 사각형
        bottom_rect = QWidget()
        bottom_rect.setFixedWidth(180 * 3 + 45)  # 상단 사각형 3개의 너비(180*3) + 사이 간격(10*2)
        bottom_rect.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 2px solid #ddd;
                border-radius: 10px;
            }
        """)
        bottom_layout.addWidget(bottom_rect)
        bottom_layout.addSpacing(20)
        
        # 메인 레이아웃에 추가
        main_layout = QVBoxLayout()
        main_layout.addWidget(top_widget)
        main_layout.addWidget(bottom_widget)
        main_layout.addSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
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

    def show_mode_window(self):
        self.mode_window = ModeSettingWindow()
        
        # 화면 중앙에 위치 설정
        screen = QApplication.primaryScreen().geometry()
        window_size = self.mode_window.geometry()
        center_x = (screen.width() - window_size.width()) // 2
        center_y = int(screen.height() * 0.4 - window_size.height() // 2)
        
        self.mode_window.move(center_x, center_y)
        self.mode_window.show()

class MenuWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
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
        mode_btn.clicked.connect(self.show_mode_setting)
        
        layout.addWidget(reserve_btn)
        layout.addWidget(mode_btn)
        
        self.setLayout(layout)
        
    def show_mode_setting(self):
        self.close()  # 메뉴 창 닫기
        self.mode_window = ModeSettingWindow()
        
        # 화면 중앙에 위치 설정
        screen = QApplication.primaryScreen().geometry()
        window_size = self.mode_window.geometry()
        center_x = (screen.width() - window_size.width()) // 2
        center_y = (screen.height() - window_size.height()) // 2
        
        self.mode_window.move(center_x, center_y)
        self.mode_window.show()

class ModeSettingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.installEventFilter(self)
        self.initUI()
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowDeactivate:
            self.close()
        return super().eventFilter(obj, event)

    def initUI(self):
        self.setFixedSize(500, 400)  # 4개의 버튼이 들어갈 수 있도록 너비 증가
        
        layout = QHBoxLayout()
        
        # 버튼 텍스트와 크기 설정
        buttons_info = [
            "정온 설정",
            "단계 설정",
            "사용자 설정",
            "학습 설정"
        ]
        
        for text in buttons_info:
            btn = RotatedButton(text)
            btn.setFixedSize(100, 350)
            btn.setStyleSheet("""
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
            if text == "정온 설정":
                btn.clicked.connect(self.show_temperature_setting)
            elif text == "단계 설정":
                btn.clicked.connect(self.show_step_setting)
            layout.addWidget(btn)
        
        self.setLayout(layout)
    
    def show_temperature_setting(self):
        self.close()  # 모드 설정 창 닫기
        self.temp_window = TemperatureSettingWindow()
        
        # 화면 중앙에 위치 설정
        screen = QApplication.primaryScreen().geometry()
        window_size = self.temp_window.geometry()
        center_x = (screen.width() - window_size.width()) // 2
        center_y = int(screen.height() * 0.4 - window_size.height() // 2)
        
        self.temp_window.move(center_x, center_y)
        self.temp_window.show()

    def show_step_setting(self):
        self.close()
        self.step_window = StepSettingWindow()
        
        # 화면 중앙에 위치 설정
        screen = QApplication.primaryScreen().geometry()
        window_size = self.step_window.geometry()
        center_x = (screen.width() - window_size.width()) // 2
        center_y = int(screen.height() * 0.4 - window_size.height() // 2)
        
        self.step_window.move(center_x, center_y)
        self.step_window.show()

#정온 설정 창
class TemperatureSettingWindow(QWidget):
    saved_temperature = 25.0
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.installEventFilter(self)
        self.initUI()
    
    def initUI(self):
        self.setFixedSize(400, 400)  # 창 너비 증가
        
        # 메인 레이아웃을 수평으로 변경
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        # 온도 표시 레이블을 회전된 버튼으로 변경
        class RotatedTempLabel(QWidget):
            def __init__(self, temp):
                super().__init__()
                self.temp = temp
                self.setFixedSize(100, 350)  # 크기 조정
                self.font = QFont()
                self.font.setPointSize(40)
                self.font.setBold(True)
                
            def paintEvent(self, event):
                painter = QPainter(self)
                painter.setFont(self.font)
                painter.translate(self.width()/2, self.height()/2)
                painter.rotate(-90)
                painter.drawText(QRect(-100, -50, 200, 100), Qt.AlignCenter, f'{self.temp:.1f}°C')
        
        self.temp_display = RotatedTempLabel(self.saved_temperature)
        layout.addWidget(self.temp_display)
        
        # 스크롤바
        self.scroll = QScrollBar(Qt.Vertical)
        self.scroll.setMinimum(50)  # 25.0도
        self.scroll.setMaximum(80)  # 40.0도
        self.scroll.setValue(int(self.saved_temperature * 2))
        self.scroll.setFixedHeight(350)  # 스크롤바 길이 증가
        self.scroll.setFixedWidth(60)   # 스크롤바 너비
        self.scroll.setInvertedAppearance(True)
        self.scroll.setStyleSheet("""
            QScrollBar:vertical {
                border: 2px solid #ddd;
                border-radius: 5px;
                background: white;
                width: 60px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #888888;
                border-radius: 3px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #777777;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        self.scroll.valueChanged.connect(self.update_temperature)
        layout.addWidget(self.scroll)
        
        # 확인 버튼을 회전된 버튼으로 변경
        confirm_btn = RotatedButton('확인')
        confirm_btn.setFixedSize(100, 350)  # 크기 조정
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        confirm_btn.clicked.connect(self.save_and_close)
        layout.addWidget(confirm_btn)
        
        self.setLayout(layout)
    
    def update_temperature(self):
        temp = self.scroll.value() / 2
        self.temp_display.temp = temp
        self.temp_display.update()  # 화면 갱신
    
    def save_and_close(self):
        TemperatureSettingWindow.saved_temperature = self.scroll.value() / 2
        self.close()
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowDeactivate:
            self.close()
        return super().eventFilter(obj, event)

# 단계 설정 창 클래스 추가
class StepSettingWindow(QWidget):
    saved_step = 1  # 저장된 단계 값
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.installEventFilter(self)
        self.initUI()
    
    def initUI(self):
        self.setFixedSize(400, 400)
        
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        # 단계 표시 레이블
        class RotatedStepLabel(QWidget):
            def __init__(self, step):
                super().__init__()
                self.step = step
                self.setFixedSize(100, 350)
                self.font = QFont()
                self.font.setPointSize(20)
                self.font.setBold(True)
                
            def paintEvent(self, event):
                painter = QPainter(self)
                painter.setFont(self.font)
                painter.translate(self.width()/2, self.height()/2)
                painter.rotate(-90)
                painter.drawText(QRect(-50, -15, 100, 30), Qt.AlignCenter, f'{self.step}단계')
        
        self.step_display = RotatedStepLabel(self.saved_step)
        layout.addWidget(self.step_display)
        
        # 스크롤바
        self.scroll = QScrollBar(Qt.Vertical)
        self.scroll.setMinimum(1)  # 1단계
        self.scroll.setMaximum(8)  # 8단계
        self.scroll.setValue(self.saved_step)
        self.scroll.setFixedHeight(350)
        self.scroll.setFixedWidth(60)
        self.scroll.setInvertedAppearance(True)
        self.scroll.setStyleSheet("""
            QScrollBar:vertical {
                border: 2px solid #ddd;
                border-radius: 5px;
                background: white;
                width: 60px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #888888;
                border-radius: 3px;
                min-height: 30px;  /* 핸들의 최소 크기를 30px로 설정 */
                max-height: 30px;  /* 핸들의 최대 크기를 30px로 설정 */
                margin: 0px 4px;   /* 좌우 여백 추가 */
            }
            QScrollBar::handle:vertical:hover {
                background: #777777;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::sub-page:vertical, QScrollBar::add-page:vertical {
                background: white;  /* 스크롤바 배경색 설정 */
            }
        """)
        self.scroll.valueChanged.connect(self.update_step)
        layout.addWidget(self.scroll)
        
        # 확인 버튼
        confirm_btn = RotatedButton('확인')
        confirm_btn.setFixedSize(100, 350)
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        confirm_btn.clicked.connect(self.save_and_close)
        layout.addWidget(confirm_btn)
        
        self.setLayout(layout)
    
    def update_step(self):
        self.step_display.step = self.scroll.value()
        self.step_display.update()
    
    def save_and_close(self):
        StepSettingWindow.saved_step = self.scroll.value()
        self.close()
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowDeactivate:
            self.close()
        return super().eventFilter(obj, event)

# 버튼 세로방향 회전
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