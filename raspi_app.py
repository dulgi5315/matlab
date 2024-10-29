import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

class TemperatureSettingWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # 새 창 설정
        self.title("정온 설정")
        self.attributes('-fullscreen', True)
        
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

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("라즈베리파이 애플리케이션")
        self.attributes('-fullscreen', True)
        self.bind('<Escape>', self.end_fullscreen)

        self.create_widgets()

    def create_widgets(self):
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
        step_settings_btn = tk.Button(background, text="단계 설정", **button_style)
        step_settings_btn.place(relx=0.5, rely=0.65, relwidth=0.6, relheight=0.12, 
                              anchor="center")

        # 사용자 설정 버튼
        custom_settings_btn = tk.Button(background, text="사용자 설정", **button_style)
        custom_settings_btn.place(relx=0.5, rely=0.8, relwidth=0.6, relheight=0.12, 
                                anchor="center")

    def open_temp_settings(self):
        temp_window = TemperatureSettingWindow(self)
        temp_window.grab_set()  # 새 창을 모달로 만듦

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