from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from datetime import datetime
import serial

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mode_name = ""  # 모드 이름 저장 변수
        self.target_temps = ["0.0", "0.0", "0.0"]  # 목표 온도 저장 변수
        # CSV 파일 경로 설정
        self.csv_path = 'temperature_log5.csv'
        self.check_csv_file()  # CSV 파일 존재 확인 및 생성

        # 시리얼 통신 설정
        try:
            self.serial = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # 아두이노 연결
        except:
            self.serial = None
            print("아두이노 연결 실패")
        
        self.temperatures = ['0.0', '0.0', '0.0']  # 초기 온도값
        self.initUI()
        
        # 온도 갱신 타이머 설정
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_temperatures)
        self.timer.start(1000)  # 5초마다 갱신
        
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
                painter.drawText(QRect(-100, -15, 200, 30), Qt.AlignCenter, self.text)

        text_box = QFrame()
        text_box.setFrameStyle(QFrame.Box | QFrame.Plain)
        text_box.setStyleSheet("""
            QFrame {
                border: 2px solid #ddd;
                background-color: white;
                border-radius: 8px;
            }
        """)
        text_box.setFixedSize(120, 225)

        # 현재 온도 텍스트 레이블
        text_layout = QVBoxLayout(text_box)
        text_label = RotatedLabel("현재 온도")
        text_layout.addWidget(text_label)
        top_layout.addWidget(text_box)

		# 상단 사각형 3개
        temperatures = self.temperatures  # 초기 온도값 사용
        for i, temp in enumerate(temperatures):
            box = QFrame()
            box.setFrameStyle(QFrame.Box | QFrame.Plain)
            box.setStyleSheet("""
                QFrame {
                    border: 2px solid #ddd;
                    background-color: white;
                    border-radius: 8px;
                }
            """)
            box.setFixedSize(150, 225)
            
            # 온도 라벨 추가
            layout = QVBoxLayout(box)
            label = RotatedLabel(temp)
            setattr(self, f'temp_label_{i}', label)  # 레이블 참조 저장
            layout.addWidget(label)
            top_layout.addWidget(box)
        
        # 중지 버튼
        exit_btn = QPushButton('×')
        exit_btn.setFixedSize(50, 50)  # 크기 축소
        exit_btn.clicked.connect(self.send_abort_msg)
        exit_btn.setStyleSheet("""
            QPushButton {
                font-size: 24px;`
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

        # 하단 영역 추가
        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout(bottom_widget)
        bottom_layout.setSpacing(10)  # 위젯 간 간격 설정
        bottom_layout.setContentsMargins(0, 0, 0, 0)  # 여백 제거

        self.mode_label = None  # 모드 표시 레이블
        self.target_temp_labels = []  # 목표 온도 표시 레이블들

        # 5개의 사각형 생성
        for i in range(5):
            box = QFrame()
            box.setFrameStyle(QFrame.Box | QFrame.Plain)
            box.setStyleSheet("""
                QFrame {
                    border: 2px solid #ddd;
                    background-color: white;
                    border-radius: 8px;
                }
            """)

            if i >= 2:
                box.setFixedSize(150, 225) 
            else:
                box.setFixedSize(120, 225)
            
            # 레이블 추가
            layout = QVBoxLayout(box)
            if i == 0:
                label = RotatedLabel(self.mode_name)  # 모드 이름 표시
                self.mode_label = label
            elif i == 1:
                label = RotatedLabel("목표 온도")
            else:
                label = RotatedLabel(self.target_temps[i-2])  # 목표 온도 표시
                self.target_temp_labels.append(label)
            
            layout.addWidget(label)
            bottom_layout.addWidget(box)
        
        main_layout.addWidget(bottom_widget)
        
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def update_temperatures(self):
        if self.serial is None:
            return
            
        try:
            if self.serial.in_waiting:
                # 시리얼에서 데이터 읽기
                line = self.serial.readline().decode().strip()
                temps = line.split(',')
                
                if len(temps) == 3:
                    # 유효한 온도값 처리
                    valid_temps = []
                    for i, temp in enumerate(temps):
                        try:
                            temp_float = float(temp)
                            self.temperatures[i] = f'{temp_float:.1f}'
                            valid_temps.append(temp_float)
                        except ValueError:
                            valid_temps.append(None)
                    
                    # 온도 표시 레이블 업데이트
                    for i, temp in enumerate(self.temperatures):
                        if hasattr(self, f'temp_label_{i}'):
                            getattr(self, f'temp_label_{i}').text = temp
                            getattr(self, f'temp_label_{i}').update()

                    # CSV 파일에 저장
                    self.save_to_csv(valid_temps)
        except:
            print("시리얼 통신 오류")
        
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

    # 예약 시간 전송 메서드
    def send_reservation_time(self, hour, minute):
        if self.serial is None:
            print("아두이노 연결되지 않음")
            return
            
        try:
            # 'R'은 예약 시간 설정 명령어를 나타냄
            command = f"R{hour:02d}{minute:02d}\n"
            self.serial.write(command.encode())
            print(f"예약 시간 전송: {hour:02d}:{minute:02d}")
        except:
            print("시리얼 통신 오류")

    # 정온 설정 온도 전송 메서드
    def send_temperature(self, temp):
        if self.serial is None:
            print("아두이노 연결되지 않음")
            return
            
        try:
            # 'T'는 정온 설정 명령어를 나타냄
            command = f"T{temp:.1f}\n"
            self.serial.write(command.encode())
            print(f"정온 설정 온도 전송: {temp:.1f}°C")
        except:
            print("시리얼 통신 오류")

    # 단계 설정값 전송 메서드
    def send_step_setting(self, step):
        if self.serial is None:
            print("아두이노 연결되지 않음")
            return
            
        try:
            # 'S'는 단계 설정 명령어를 나타냄
            command = f"S{step}\n"
            self.serial.write(command.encode())
            print(f"단계 설정값 전송: {step}단계")
        except:
            print("시리얼 통신 오류")

     # 사용자 설정 온도 전송 메서드
    def send_user_setting(self, temps):
        if self.serial is None:
            print("아두이노 연결되지 않음")
            return
            
        try:
            # 'U'는 사용자 설정 온도 명령어를 나타냄
            command = f"U{temps[0]:.1f},{temps[1]:.1f},{temps[2]:.1f}\n"
            self.serial.write(command.encode())
            print(f"사용자 설정 온도 전송: {temps[0]:.1f}°C, {temps[1]:.1f}°C, {temps[2]:.1f}°C")
        except:
            print("시리얼 통신 오류")

    # 모드와 온도를 업데이트하는 메서드 추가
    def update_mode_and_temps(self, mode_name, temps):
        self.mode_name = mode_name
        self.target_temps = temps
        
        # 레이블 업데이트
        if self.mode_label:
            self.mode_label.text = mode_name
            self.mode_label.update()
        
        for i, label in enumerate(self.target_temp_labels):
            if label:
                label.text = f"{temps[i]}"
                label.update()

    # 중지 명령 전송 메서드
    def send_abort_msg(self):
        if self.serial is None:
            print("아두이노 연결되지 않음")
            return
            
        try:
            # 'A'는 중지 명령어를 나타냄
            command = "A\n"
            self.serial.write(command.encode())
            print("중지 명령 전송")
            self.update_mode_and_temps("", ["0.0", "0.0", "0.0"])
        except:
            print("시리얼 통신 오류")

    # CSV 파일 존재 확인 및 생성
    def check_csv_file(self):
        import os
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, 'w', newline='') as f:
                import csv
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'Temperature1', 'Temperature2', 'Temperature3'])

    # CSV 파일에 온도 데이터 저장
    def save_to_csv(self, temperatures):
            import csv
            from datetime import datetime
            
            try:
                with open(self.csv_path, 'a', newline='') as f:
                    writer = csv.writer(f)
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    writer.writerow([timestamp] + [f'{t:.1f}' if t is not None else 'N/A' for t in temperatures])
            except Exception as e:
                print(f"CSV 파일 저장 오류: {e}")

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
        reserve_btn.clicked.connect(self.show_reservation)
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

    def show_reservation(self):
        self.close()
        self.reserve_window = ReservationWindow()
        
        # 화면 중앙에 위치 설정
        screen = QApplication.primaryScreen().geometry()
        window_size = self.reserve_window.geometry()
        center_x = (screen.width() - window_size.width()) // 2
        center_y = int(screen.height() * 0.4 - window_size.height() // 2)
        
        self.reserve_window.move(center_x, center_y)
        self.reserve_window.show()

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
            elif text == "사용자 설정":
                btn.clicked.connect(self.show_user_setting)
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

    def show_user_setting(self):
        self.close()
        self.user_window = UserSettingWindow()
        
        # 화면 중앙에 위치 설정
        screen = QApplication.primaryScreen().geometry()
        window_size = self.user_window.geometry()
        center_x = (screen.width() - window_size.width()) // 2
        center_y = int(screen.height() * 0.4 - window_size.height() // 2)
        
        self.user_window.move(center_x, center_y)
        self.user_window.show()

#정온 설정 창
class TemperatureSettingWindow(QWidget):
    saved_temperature = 30.0
    
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
        self.scroll.setMinimum(60)  # 30.0도
        self.scroll.setMaximum(110)  # 55.0도
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
        temp = self.scroll.value() / 2
        TemperatureSettingWindow.saved_temperature = temp
        
        # MainWindow 인스턴스 찾기
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, MainWindow):
                widget.update_mode_and_temps("정온 설정", [temp, temp, temp])
                # 정온 설정 온도 전송
                widget.send_temperature(temp)
                break
                
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
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #777777;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
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
        step = self.scroll.value()
        StepSettingWindow.saved_step = step
        # MainWindow 인스턴스 찾기
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, MainWindow):
                widget.update_mode_and_temps("단계 설정", [step, step, step])
                # 단계 설정값 전송
                widget.send_step_setting(step)
                break
                
        self.close()
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowDeactivate:
            self.close()
        return super().eventFilter(obj, event)

# 사용자 설정 창
class UserSettingWindow(QWidget):
    saved_temps = [30.0, 30.0, 30.0]
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.installEventFilter(self)
        self.initUI()

    def initUI(self):
        # 온도 표시를 위한 회전된 레이블 클래스
        class RotatedTempLabel(QWidget):
            def __init__(self, temp):
                super().__init__()
                self.temp = temp
                self.setFixedSize(100, 350)
                self.font = QFont()
                self.font.setPointSize(20)
                self.font.setBold(True)
            
            def paintEvent(self, event):
                painter = QPainter(self)
                painter.setFont(self.font)
                painter.translate(self.width()/2, self.height()/2)
                painter.rotate(-90)
                painter.drawText(QRect(-50, -15, 100, 30), Qt.AlignCenter, f'{self.temp:.1f}')

        self.setFixedSize(600, 400)
        
        layout = QHBoxLayout()
        layout.setSpacing(10)  # 간격을 20에서 10으로 줄임
        layout.setContentsMargins(10, 10, 10, 10)  # 전체 여백도 조정
        
        # 3개의 온도 조절 섹션 생성
        self.temp_displays = []
        self.scrolls = []
        
        for i in range(3):
            # 각 온도 조절 섹션을 위한 수평 레이아웃
            section_layout = QHBoxLayout()
            section_layout.setSpacing(5)  # 온도 표시와 스크롤바 사이 간격을 5로 설정
            
            # 온도 표시 레이블
            temp_display = RotatedTempLabel(self.saved_temps[i])
            self.temp_displays.append(temp_display)
            section_layout.addWidget(temp_display)
            
            # 스크롤바
            scroll = QScrollBar(Qt.Vertical)
            scroll.setMinimum(60)
            scroll.setMaximum(110)
            scroll.setValue(int(self.saved_temps[i] * 2))
            scroll.setFixedHeight(350)
            scroll.setFixedWidth(60)
            scroll.setInvertedAppearance(True)
            scroll.setStyleSheet("""
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
                    min-height: 30px;
                    max-height: 30px;
                    margin: 0px 4px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #777777;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0px;
                }
                QScrollBar::sub-page:vertical, QScrollBar::add-page:vertical {
                    background: white;
                }
            """)
            scroll.valueChanged.connect(lambda value, index=i: self.update_temperature(value, index))
            self.scrolls.append(scroll)
            section_layout.addWidget(scroll)
            
            # 섹션 레이아웃을 메인 레이아웃에 추가
            layout.addLayout(section_layout)
        
        # 버튼들을 위한 컨테이너 위젯과 레이아웃
        button_container = QWidget()
        button_container.setFixedSize(100, 350)
        button_layout = QVBoxLayout(button_container)
        button_layout.setSpacing(5)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        # 확인 버튼 (상단)
        confirm_btn = RotatedButton('확인')
        confirm_btn.setFixedSize(100, 110)
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
        
        # 불러오기 버튼 (중간)
        load_btn = RotatedButton('불러오기')
        load_btn.setFixedSize(100, 110)
        load_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        load_btn.clicked.connect(self.show_load_window)
        
        # 저장 버튼 (하단)
        save_btn = RotatedButton('저장')
        save_btn.setFixedSize(100, 110)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        save_btn.clicked.connect(self.show_save_window)
        
        # 버튼들을 레이아웃에 추가
        button_layout.addWidget(confirm_btn)
        button_layout.addWidget(load_btn)
        button_layout.addWidget(save_btn)
        
        # 버튼 컨테이너를 메인 레이아웃에 추가
        layout.addWidget(button_container)
        
        self.setLayout(layout)

    def show_save_window(self):
        # 현재 설정된 온도값들 가져오기
        temps = [scroll.value() / 2 for scroll in self.scrolls]
        
        # 저장 선택 창 표시
        self.save_window = SaveSelectWindow(temps)
        
        # 화면 중앙에 위치 설정
        screen = QApplication.primaryScreen().geometry()
        window_size = self.save_window.geometry()
        center_x = (screen.width() - window_size.width()) // 2
        center_y = int(screen.height() * 0.4 - window_size.height() // 2)
        
        self.save_window.move(center_x, center_y)
        self.save_window.show()

    def show_load_window(self):
        self.load_window = SaveSelectWindow(None)
        
        # 화면 중앙에 위치 설정
        screen = QApplication.primaryScreen().geometry()
        window_size = self.load_window.geometry()
        center_x = (screen.width() - window_size.width()) // 2
        center_y = int(screen.height() * 0.4 - window_size.height() // 2)
        
        self.load_window.move(center_x, center_y)
        self.load_window.show()

    def update_temperature(self, value, index):
        temp = value / 2
        self.temp_displays[index].temp = temp
        self.temp_displays[index].update()
    
    def save_and_close(self):
        temps = []
        for scroll in self.scrolls:
            temps.append(scroll.value() / 2)
        UserSettingWindow.saved_temps = temps
        
        # MainWindow 인스턴스 찾기
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, MainWindow):
                widget.update_mode_and_temps("사용자 설정", temps)
                # 사용자 설정 온도 전송
                widget.send_user_setting(temps)
                break
                
        self.close()
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowDeactivate:
            self.close()
        return super().eventFilter(obj, event)

# 저장 선택 창
class SaveSelectWindow(QWidget):
    def __init__(self, temps_to_save):
        super().__init__()
        self.temps_to_save = temps_to_save
        self.is_save_mode = temps_to_save is not None
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.installEventFilter(self)
        self.initUI()
    
    def initUI(self):
        self.setFixedSize(600, 400)
        
        # 버튼 레이아웃
        layout = QHBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 5개의 버튼 생성
        for i in range(5):
            btn_text = f'사용자 {i+1}'
            save_btn = RotatedButton(btn_text)
            save_btn.setFixedSize(100, 350)
            save_btn.setStyleSheet("""
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
            if self.is_save_mode:
                save_btn.clicked.connect(lambda checked, x=i: self.save_to_slot(x))
            else:
                save_btn.clicked.connect(lambda checked, x=i: self.load_from_slot(x))
            layout.addWidget(save_btn)
        
        self.setLayout(layout)
    
    def save_to_slot(self, slot):
        # 선택한 슬롯에 온도 저장
        filename = f'user_setting_{slot+1}.txt'
        with open(filename, 'w') as f:
            f.write(','.join(map(str, self.temps_to_save)))
        
        # UserSettingWindow의 saved_temps 업데이트
        UserSettingWindow.saved_temps = self.temps_to_save
        
        # 현재 열려있는 UserSettingWindow 찾기
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, UserSettingWindow):
                # 스크롤바와 디스플레이 업데이트
                for i, temp in enumerate(self.temps_to_save):
                    widget.scrolls[i].setValue(int(temp * 2))
                    widget.temp_displays[i].temp = temp
                    widget.temp_displays[i].update()

                # UserSettingWindow를 다시 보이게 함
                widget.show()
                break
        
        self.close()
    
    def load_from_slot(self, slot):
        # 선택한 슬롯에서 온도 불러오기
        filename = f'user_setting_{slot+1}.txt'
        try:
            with open(filename, 'r') as f:
                content = f.read().strip()  # 앞뒤 공백 제거
                if not content:  # 파일이 비어있는 경우
                    return
                
                temps = []
                for temp_str in content.split(','):
                    try:
                        temps.append(float(temp_str))
                    except ValueError:
                        continue  # 변환할 수 없는 값은 건너뜀
                
                # 유효한 온도값이 3개인 경우에만 업데이트
                if len(temps) == 3:
                    # UserSettingWindow의 saved_temps 업데이트
                    UserSettingWindow.saved_temps = temps
                    
                    # 현재 열려있는 UserSettingWindow 찾기
                    for widget in QApplication.topLevelWidgets():
                        if isinstance(widget, UserSettingWindow):
                            # 스크롤바와 디스플레이 업데이트
                            for i, temp in enumerate(temps):
                                widget.scrolls[i].setValue(int(temp * 2))
                                widget.temp_displays[i].temp = temp
                                widget.temp_displays[i].update()

                            # UserSettingWindow를 다시 보이게 함
                            widget.show()
                            break
        except FileNotFoundError:
            # 파일이 없는 경우 처리
            pass
        self.close()
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowDeactivate:
            self.close()
        return super().eventFilter(obj, event)


# 에약 설정 창
class ReservationWindow(QWidget):
    saved_hour = 0  # 초기값을 0시로 변경
    saved_minute = 0  # 초기값을 0분으로 변경
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.installEventFilter(self)
        self.initUI()
    
    def initUI(self):
        self.setFixedSize(500, 400)  # 너비를 늘려서 현재 시간도 표시
        
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        # 현재 시간 표시 레이블
        class RotatedCurrentTimeLabel(QWidget):
            def __init__(self):
                super().__init__()
                self.setFixedSize(100, 350)
                self.font = QFont()
                self.font.setPointSize(20)
                self.font.setBold(True)
                
                # 1초마다 시간 업데이트
                self.timer = QTimer()
                self.timer.timeout.connect(self.update)
                self.timer.start(1000)
            
            def paintEvent(self, event):
                current_time = datetime.now().strftime("%H:%M")
                painter = QPainter(self)
                painter.setFont(self.font)
                painter.translate(self.width()/2, self.height()/2)
                painter.rotate(-90)
                painter.drawText(QRect(-50, -15, 100, 30), Qt.AlignCenter, current_time)
        
        # 예약 시간 표시 레이블
        class RotatedSetTimeLabel(QWidget):
            def __init__(self, hour, minute):
                super().__init__()
                self.hour = hour
                self.minute = minute
                self.setFixedSize(100, 350)
                self.font = QFont()
                self.font.setPointSize(20)
                self.font.setBold(True)
            
            def paintEvent(self, event):
                painter = QPainter(self)
                painter.setFont(self.font)
                painter.translate(self.width()/2, self.height()/2)
                painter.rotate(-90)
                painter.drawText(QRect(-50, -15, 100, 30), Qt.AlignCenter, f'{self.hour:02d}:{self.minute:02d}')
        
        # 현재 시간 표시
        self.current_time = RotatedCurrentTimeLabel()
        layout.addWidget(self.current_time)
        
        # 예약 시간 표시
        self.time_display = RotatedSetTimeLabel(self.saved_hour, self.saved_minute)
        layout.addWidget(self.time_display)
        
        # 시간 스크롤바
        self.hour_scroll = QScrollBar(Qt.Vertical)
        self.hour_scroll.setMinimum(0)
        self.hour_scroll.setMaximum(24)  # 24시간으로 변경
        self.hour_scroll.setValue(self.saved_hour)
        self.hour_scroll.setFixedHeight(350)
        self.hour_scroll.setFixedWidth(60)
        self.hour_scroll.setInvertedAppearance(True)
        self.hour_scroll.setStyleSheet("""
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
                min-height: 30px;
                max-height: 30px;
                margin: 0px 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #777777;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::sub-page:vertical, QScrollBar::add-page:vertical {
                background: white;
            }
        """)
        self.hour_scroll.valueChanged.connect(self.update_time)
        layout.addWidget(self.hour_scroll)
        
        # 분 스크롤바
        self.minute_scroll = QScrollBar(Qt.Vertical)
        self.minute_scroll.setMinimum(0)
        self.minute_scroll.setMaximum(59)
        self.minute_scroll.setValue(self.saved_minute)
        self.minute_scroll.setFixedHeight(350)
        self.minute_scroll.setFixedWidth(60)
        self.minute_scroll.setInvertedAppearance(True)
        self.minute_scroll.setStyleSheet(self.hour_scroll.styleSheet())
        self.minute_scroll.valueChanged.connect(self.update_time)
        layout.addWidget(self.minute_scroll)
        
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
    
    def update_time(self):
        self.time_display.hour = self.hour_scroll.value()
        self.time_display.minute = self.minute_scroll.value()
        self.time_display.update()
    
    def save_and_close(self):
        ReservationWindow.saved_hour = self.hour_scroll.value()
        ReservationWindow.saved_minute = self.minute_scroll.value()
        
        # MainWindow 인스턴스 찾기
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, MainWindow):
                # 예약 시간 전송
                widget.send_reservation_time(
                    self.hour_scroll.value(),
                    self.minute_scroll.value()
                )
                break
                
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