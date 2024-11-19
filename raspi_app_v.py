import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import os
import json
from datetime import datetime

class TemperatureSettingWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # 새 창 기본 설정
        self.title("정온 설정")
        self.attributes('-fullscreen', False)  # 먼저 일반 창으로 시작
        
        # 창 크기를 화면 크기로 설정
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        
        self.create_widgets()
        
        # 창이 완전히 로드된 후 전체 화면으로 전환
        self.after(100, self.set_fullscreen)
        
    def set_fullscreen(self):
        self.attributes('-fullscreen', True)
        
    def create_widgets(self):
        # 배경 프레임
        background = tk.Frame(self, bg="white")
        background.place(relwidth=1, relheight=1)
        
        # 폰트 설정
        title_font = tkfont.Font(family="Helvetica", size=20, weight="bold")
        value_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        
        # 제목
        title_label = tk.Label(background, text="원하는 온도를 설정하세요", 
                             font=title_font, bg="white")
        title_label.place(relx=0.5, rely=0.2, anchor="center")
        
        # 온도 값 표시 레이블
        self.temp_value = tk.Label(background, text="25.0°C", 
                                 font=value_font, bg="white")
        self.temp_value.place(relx=0.5, rely=0.35, anchor="center")
        
        # 온도 조절 바
        self.temp_scale = ttk.Scale(background, 
                                  from_=25, 
                                  to=40,
                                  orient="horizontal",
                                  length=400,
                                  command=self.update_temp_value)
        self.temp_scale.set(25.0)
        self.temp_scale.place(relx=0.5, rely=0.5, anchor="center")
        
        # 확인 버튼
        button_style = {"font": title_font, "bg": "skyblue", "fg": "navy"}
        confirm_btn = tk.Button(background, text="확인", 
                              command=self.destroy, **button_style)
        confirm_btn.place(relx=0.5, rely=0.7, relwidth=0.3, relheight=0.1, 
                         anchor="center")
        
        # ESC 키로 창 닫기
        self.bind('<Escape>', lambda e: self.destroy())
        
    def update_temp_value(self, value):
        temp = float(value)
        self.temp_value.config(text=f"{temp:.1f}°C")

class StepSettingWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("단계 설정")
        self.attributes('-fullscreen', False)
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        
        self.create_widgets()
        self.after(100, self.set_fullscreen)
        
    def set_fullscreen(self):
        self.attributes('-fullscreen', True)
        
    def create_widgets(self):
        background = tk.Frame(self, bg="white")
        background.place(relwidth=1, relheight=1)
        
        # 폰트 설정
        title_font = tkfont.Font(family="Helvetica", size=20, weight="bold")
        value_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        
        # 제목
        title_label = tk.Label(background, text="온도 단계를 설정하세요", 
                             font=title_font, bg="white")
        title_label.place(relx=0.5, rely=0.2, anchor="center")
        
        # 단계 값 표시 레이블
        self.step_value = tk.Label(background, text="1단계", 
                                 font=value_font, bg="white")
        self.step_value.place(relx=0.5, rely=0.35, anchor="center")
        
        # 스케일 바를 포함할 프레임 생성
        scale_frame = tk.Frame(background, bg="white")
        scale_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=80)
        
        # 단계 조절 바
        self.step_scale = ttk.Scale(scale_frame, 
                                  from_=1, 
                                  to=10,
                                  orient="horizontal",
                                  length=400,
                                  command=self.update_step_value)
        self.step_scale.set(1)
        self.step_scale.place(relx=0.5, rely=0, anchor="n")
        
        # 단계 표시 레이블들
        label_width = 30  # 레이블의 폭
        scale_width = 400  # 스케일의 전체 폭
        padding = 15  # 첫 번째와 마지막 레이블의 여백
        
        # 레이블 사이의 간격 계산
        spacing = (scale_width - 2 * padding) / 9
        
        for i in range(10):
            label = tk.Label(scale_frame, text=str(i+1), 
                           font=tkfont.Font(size=12), bg="white",
                           width=1)  # 레이블 폭 고정
            # x 위치 계산: 첫 번째 여백 + (간격 * 인덱스)
            x_pos = padding + (i * spacing)
            label.place(x=x_pos, rely=0.7, anchor="center")
        
        # 확인 버튼
        button_style = {"font": title_font, "bg": "skyblue", "fg": "navy"}
        confirm_btn = tk.Button(background, text="확인", 
                              command=self.destroy, **button_style)
        confirm_btn.place(relx=0.5, rely=0.7, relwidth=0.3, relheight=0.1, 
                         anchor="center")
        
        # ESC 키로 창 닫기
        self.bind('<Escape>', lambda e: self.destroy())
        
    def update_step_value(self, value):
        step = int(float(value))
        self.step_value.config(text=f"{step}단계")
        
class CustomSettingWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("사용자 설정")
        self.attributes('-fullscreen', False)
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        
		# UserSetting 폴더 생성
        self.setting_dir = "UserSetting"
        if not os.path.exists(self.setting_dir):
            os.makedirs(self.setting_dir)
        
        self.create_widgets()
        self.after(100, self.set_fullscreen)
        
    def set_fullscreen(self):
        self.attributes('-fullscreen', True)
        
    def create_widgets(self):
        background = tk.Frame(self, bg="white")
        background.place(relwidth=1, relheight=1)
        
        # 폰트 설정
        title_font = tkfont.Font(family="Helvetica", size=20, weight="bold")
        label_font = tkfont.Font(family="Helvetica", size=16)
        value_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        
        # 제목
        title_label = tk.Label(background, text="부위별 온도를 설정하세요", 
                             font=title_font, bg="white")
        title_label.place(relx=0.5, rely=0.1, anchor="center")
        
        # 컨테이너 프레임 생성 (모든 부위별 설정을 포함)
        container = tk.Frame(background, bg="white")
        container.place(relx=0.5, rely=0.45, relwidth=0.8, relheight=0.6, 
                       anchor="center")
        
        # 각 부위별 온도 설정
        parts = ["머리", "몸통", "다리"]
        self.temp_values = {}
        
        for i, part in enumerate(parts):
            # 부위별 프레임
            frame = tk.Frame(container, bg="white")
            frame.place(relx=0.5, rely=0.2 + (i * 0.25), relwidth=0.9, relheight=0.2, 
                       anchor="center")
            
            # 왼쪽 정보 프레임 (부위 이름과 온도 값)
            info_frame = tk.Frame(frame, bg="white")
            info_frame.place(relx=0, rely=0.5, relwidth=0.3, relheight=1, 
                           anchor="w")
            
            # 부위 이름
            part_label = tk.Label(info_frame, text=f"{part}", 
                                font=label_font, bg="white")
            part_label.place(relx=0, rely=0.5, anchor="w")
            
            # 온도 값 표시
            self.temp_values[part] = tk.Label(info_frame, text="25.0°C", 
                                            font=value_font, bg="white")
            self.temp_values[part].place(relx=1, rely=0.5, anchor="e")
            
            # 온도 조절 바 프레임
            scale_frame = tk.Frame(frame, bg="white")
            scale_frame.place(relx=0.35, rely=0.5, relwidth=0.65, relheight=1, 
                            anchor="w")
            
            # 온도 조절 바
            scale = ttk.Scale(scale_frame, 
                            from_=25, 
                            to=40,
                            orient="horizontal",
                            command=lambda v, p=part: self.update_temp_value(p, v))
            scale.set(25.0)
            # scale의 width를 프레임에 맞추어 설정
            scale.place(relx=0, rely=0.5, relwidth=1, anchor="w")
        
        # 버튼 프레임 생성
        button_frame = tk.Frame(background, bg="white")
        button_frame.place(relx=0.5, rely=0.85, relwidth=0.6, relheight=0.1, 
                         anchor="center")
        
        # 버튼 스타일
        button_style = {"font": title_font, "bg": "skyblue", "fg": "navy"}
        
        # 저장 버튼
        save_btn = tk.Button(button_frame, text="저장", 
                           command=self.save_settings,
                           **button_style)
        save_btn.place(relx=0.3, rely=0.5, relwidth=0.3, relheight=1, 
                      anchor="center")
        
        # 확인 버튼
        confirm_btn = tk.Button(button_frame, text="확인", 
                              command=self.destroy,
                              **button_style)
        confirm_btn.place(relx=0.7, rely=0.5, relwidth=0.3, relheight=1, 
                         anchor="center")
        
        # ESC 키로 창 닫기
        self.bind('<Escape>', lambda e: self.destroy())
        
    def update_temp_value(self, part, value):
        temp = float(value)
        self.temp_values[part].config(text=f"{temp:.1f}°C")
        
    def save_settings(self):
        # 현재 설정된 온도 값 가져오기
        settings = {
            "머리": float(self.temp_values["머리"].cget("text").replace("°C", "")),
            "몸통": float(self.temp_values["몸통"].cget("text").replace("°C", "")),
            "다리": float(self.temp_values["다리"].cget("text").replace("°C", ""))
        }
        
        # 현재 날짜와 시간으로 파일명 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"temperature_settings_{timestamp}.json"
        filepath = os.path.join(self.setting_dir, filename)
        
        # 설정을 JSON 파일로 저장
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
            
            # 저장 성공 메시지 표시
            self.show_message("저장 완료", "설정이 성공적으로 저장되었습니다.")
        except Exception as e:
            # 저장 실패 메시지 표시
            self.show_message("저장 실패", f"설정 저장 중 오류가 발생했습니다.\n{str(e)}")

    def show_message(self, title, message):
        message_window = tk.Toplevel(self)
        message_window.title(title)
        
        # 메시지 창 크기와 위치 설정
        window_width = 300
        window_height = 150
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        message_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 메시지 표시
        msg_label = tk.Label(message_window, text=message, 
                           wraplength=250, pady=20)
        msg_label.pack(expand=True)
        
        # 확인 버튼
        ok_button = tk.Button(message_window, text="확인", 
                            command=message_window.destroy)
        ok_button.pack(pady=10)
        
        # 모달 창으로 설정
        message_window.transient(self)
        message_window.grab_set()
        self.wait_window(message_window)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("라즈베리파이 애플리케이션")
        self.attributes('-fullscreen', False)  # 먼저 일반 창으로 시작
        
        # 창 크기를 화면 크기로 설정
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        
        self.create_widgets()
        
        # 창이 완전히 로드된 후 전체 화면으로 전환
        self.after(100, self.set_fullscreen)
        
        self.bind('<Escape>', self.end_fullscreen)

    def set_fullscreen(self):
        self.attributes('-fullscreen', True)
        
    def create_widgets(self):
        # 배경 프레임
        background = tk.Frame(self, bg="white")
        background.place(relwidth=1, relheight=1)

        # 온도 프레임 수직 배치로 변경
        temp_frame = tk.Frame(background, bg="white")
        temp_frame.place(relx=0, rely=0.05, relwidth=1, relheight=0.4)

        label_font = tkfont.Font(family="Helvetica", size=14)
        temp_font = tkfont.Font(family="Helvetica", size=20, weight="bold")

        # 머리 온도 - 세로 배치
        head_label = tk.Label(temp_frame, text="머리", font=label_font, bg="white")
        head_label.place(relx=0.5, rely=0.15, anchor="center")
        head_temp_frame = tk.Frame(temp_frame, bg="lightgray", bd=2, relief="solid")
        head_temp_frame.place(relx=0.5, rely=0.25, relwidth=0.8, relheight=0.15, anchor="center")
        self.head_temp = tk.Label(head_temp_frame, text="36.5°C", font=temp_font, bg="lightgray")
        self.head_temp.place(relx=0.5, rely=0.5, anchor="center")

        # 몸통 온도 - 세로 배치
        body_label = tk.Label(temp_frame, text="몸통", font=label_font, bg="white")
        body_label.place(relx=0.5, rely=0.45, anchor="center")
        body_temp_frame = tk.Frame(temp_frame, bg="lightgray", bd=2, relief="solid")
        body_temp_frame.place(relx=0.5, rely=0.55, relwidth=0.8, relheight=0.15, anchor="center")
        self.body_temp = tk.Label(body_temp_frame, text="36.7°C", font=temp_font, bg="lightgray")
        self.body_temp.place(relx=0.5, rely=0.5, anchor="center")

        # 다리 온도 - 세로 배치
        leg_label = tk.Label(temp_frame, text="다리", font=label_font, bg="white")
        leg_label.place(relx=0.5, rely=0.75, anchor="center")
        leg_temp_frame = tk.Frame(temp_frame, bg="lightgray", bd=2, relief="solid")
        leg_temp_frame.place(relx=0.5, rely=0.85, relwidth=0.8, relheight=0.15, anchor="center")
        self.leg_temp = tk.Label(leg_temp_frame, text="36.3°C", font=temp_font, bg="lightgray")
        self.leg_temp.place(relx=0.5, rely=0.5, anchor="center")

        # 버튼들의 세로 배치 조정
        button_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        button_style = {"font": button_font, "bg": "skyblue", "fg": "navy"}

        # 정온 설정 버튼
        temp_settings_btn = tk.Button(background, text="정온 설정", 
                                    command=self.open_temp_settings,
                                    **button_style)
        temp_settings_btn.place(relx=0.5, rely=0.55, relwidth=0.8, relheight=0.1, 
                              anchor="center")

        # 단계 설정 버튼
        step_settings_btn = tk.Button(background, text="단계 설정", 
                                    command=self.open_step_settings,
                                    **button_style)
        step_settings_btn.place(relx=0.5, rely=0.7, relwidth=0.8, relheight=0.1, 
                              anchor="center")

        # 사용자 설정 버튼
        custom_settings_btn = tk.Button(background, text="사용자 설정", 
                                    command=self.open_custom_settings,
                                    **button_style)
        custom_settings_btn.place(relx=0.5, rely=0.85, relwidth=0.8, relheight=0.1, 
                                anchor="center")

    def open_temp_settings(self):
        temp_window = TemperatureSettingWindow(self)
        temp_window.grab_set()
        
    def open_step_settings(self):
        step_window = StepSettingWindow(self)
        step_window.grab_set()
        
    def open_custom_settings(self):
        custom_window = CustomSettingWindow(self)
        custom_window.grab_set()

    def end_fullscreen(self, event=None):
        self.attributes("-fullscreen", False)

    def update_temperatures(self):
        # 여기에 실제 온도를 가져오는 코드를 추가합니다.
        head_temp = 36.5  # 예시 값
        body_temp = 36.7
        leg_temp = 36.3
        
        self.head_temp.config(text=f"{head_temp:.1f}°C")
        self.body_temp.config(text=f"{body_temp:.1f}°C")
        self.leg_temp.config(text=f"{leg_temp:.1f}°C")
        
        # 1초마다 업데이트
        self.after(1000, self.update_temperatures)

if __name__ == "__main__":
    app = Application()
    app.update_temperatures()  # 온도 업데이트 시작
    app.mainloop()