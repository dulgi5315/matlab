import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

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

class CustomSettingWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("사용자 설정")
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
        
        # 확인 버튼
        button_style = {"font": title_font, "bg": "skyblue", "fg": "navy"}
        confirm_btn = tk.Button(background, text="확인", 
                              command=self.destroy, **button_style)
        confirm_btn.place(relx=0.5, rely=0.85, relwidth=0.3, relheight=0.1, 
                         anchor="center")
        
        # ESC 키로 창 닫기
        self.bind('<Escape>', lambda e: self.destroy())
        
    def update_temp_value(self, part, value):
        temp = float(value)
        self.temp_values[part].config(text=f"{temp:.1f}°C")

class CustomSettingWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("사용자 설정")
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
        label_font = tkfont.Font(family="Helvetica", size=16)
        value_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        
        # 제목
        title_label = tk.Label(background, text="부위별 온도를 설정하세요", 
                             font=title_font, bg="white")
        title_label.place(relx=0.5, rely=0.1, anchor="center")
        
        # 각 부위별 온도 설정 프레임 생성
        parts = ["머리", "몸통", "다리"]
        self.temp_values = {}  # 온도 값 레이블을 저장할 딕셔너리
        
        for i, part in enumerate(parts):
            # 부위별 프레임
            frame = tk.Frame(background, bg="white")
            frame.place(relx=0.5, rely=0.25 + (i * 0.2), relwidth=0.8, relheight=0.15, 
                       anchor="center")
            
            # 부위 이름
            part_label = tk.Label(frame, text=f"{part}", font=label_font, bg="white")
            part_label.place(relx=0.1, rely=0.5, anchor="w")
            
            # 온도 값 표시
            self.temp_values[part] = tk.Label(frame, text="25.0°C", 
                                            font=value_font, bg="white")
            self.temp_values[part].place(relx=0.3, rely=0.5, anchor="w")
            
            # 온도 조절 바
            scale = ttk.Scale(frame, 
                            from_=25, 
                            to=40,
                            orient="horizontal",
                            length=400,
                            command=lambda v, p=part: self.update_temp_value(p, v))
            scale.set(25.0)
            scale.place(relx=0.5, rely=0.5, anchor="w")
        
        # 확인 버튼
        button_style = {"font": title_font, "bg": "skyblue", "fg": "navy"}
        confirm_btn = tk.Button(background, text="확인", 
                              command=self.destroy, **button_style)
        confirm_btn.place(relx=0.5, rely=0.85, relwidth=0.3, relheight=0.1, 
                         anchor="center")
        
        # ESC 키로 창 닫기
        self.bind('<Escape>', lambda e: self.destroy())
        
    def update_temp_value(self, part, value):
        temp = float(value)
        self.temp_values[part].config(text=f"{temp:.1f}°C")

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

        temp_frame = tk.Frame(background, bg="white")
        temp_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.3)

        label_font = tkfont.Font(family="Helvetica", size=14)
        temp_font = tkfont.Font(family="Helvetica", size=20, weight="bold")

        # 머리 온도
        head_label = tk.Label(temp_frame, text="머리", font=label_font, bg="white")
        head_label.place(relx=0.2, rely=0.1, anchor="center")
        head_temp_frame = tk.Frame(temp_frame, bg="lightgray", bd=2, relief="solid")
        head_temp_frame.place(relx=0.2, rely=0.5, relwidth=0.25, relheight=0.6, anchor="center")
        self.head_temp = tk.Label(head_temp_frame, text="36.5°C", font=temp_font, bg="lightgray")
        self.head_temp.place(relx=0.5, rely=0.5, anchor="center")

        # 몸통 온도
        body_label = tk.Label(temp_frame, text="몸통", font=label_font, bg="white")
        body_label.place(relx=0.5, rely=0.1, anchor="center")
        body_temp_frame = tk.Frame(temp_frame, bg="lightgray", bd=2, relief="solid")
        body_temp_frame.place(relx=0.5, rely=0.5, relwidth=0.25, relheight=0.6, anchor="center")
        self.body_temp = tk.Label(body_temp_frame, text="36.7°C", font=temp_font, bg="lightgray")
        self.body_temp.place(relx=0.5, rely=0.5, anchor="center")

        # 다리 온도
        leg_label = tk.Label(temp_frame, text="다리", font=label_font, bg="white")
        leg_label.place(relx=0.8, rely=0.1, anchor="center")
        leg_temp_frame = tk.Frame(temp_frame, bg="lightgray", bd=2, relief="solid")
        leg_temp_frame.place(relx=0.8, rely=0.5, relwidth=0.25, relheight=0.6, anchor="center")
        self.leg_temp = tk.Label(leg_temp_frame, text="36.3°C", font=temp_font, bg="lightgray")
        self.leg_temp.place(relx=0.5, rely=0.5, anchor="center")

        # 버튼 스타일 및 배치
        button_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        button_style = {"font": button_font, "bg": "skyblue", "fg": "navy"}

        # 정온 설정 버튼
        temp_settings_btn = tk.Button(background, text="정온 설정", 
                                    command=self.open_temp_settings,
                                    **button_style)
        temp_settings_btn.place(relx=0.5, rely=0.5, relwidth=0.6, relheight=0.12, 
                              anchor="center")

        # 단계 설정 버튼
        step_settings_btn = tk.Button(background, text="단계 설정", 
                                    command=self.open_step_settings,
                                    **button_style)
        step_settings_btn.place(relx=0.5, rely=0.65, relwidth=0.6, relheight=0.12, 
                              anchor="center")

        # 사용자 설정 버튼
        custom_settings_btn = tk.Button(background, text="사용자 설정", 
                              command=self.open_custom_settings,
                              **button_style)
        custom_settings_btn.place(relx=0.5, rely=0.8, relwidth=0.6, relheight=0.12, 
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