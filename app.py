import tkinter as tk
from tkinter import font as tkfont

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("라즈베리파이 애플리케이션")
        
        # 전체 화면 모드 설정
        self.attributes('-fullscreen', True)
        
        # ESC 키를 눌러 전체 화면을 종료할 수 있도록 설정
        self.bind('<Escape>', self.end_fullscreen)

        self.create_widgets()

    def create_widgets(self):
        # 배경 프레임 (하얀색)
        background = tk.Frame(self, bg="white")
        background.place(relwidth=1, relheight=1)

        # 온도 표시 프레임
        temp_frame = tk.Frame(background, bg="white")
        temp_frame.place(relx=0, rely=0, relwidth=1, relheight=0.2)

        # 온도 표시 스타일
        temp_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        temp_style = {"font": temp_font, "bg": "white", "fg": "black"}

        # 머리 온도
        head_temp = tk.Label(temp_frame, text="머리: 36.5°C", **temp_style)
        head_temp.place(relx=0.1, rely=0.5, anchor="w")

        # 몸통 온도
        body_temp = tk.Label(temp_frame, text="몸통: 36.7°C", **temp_style)
        body_temp.place(relx=0.5, rely=0.5, anchor="center")

        # 다리 온도
        leg_temp = tk.Label(temp_frame, text="다리: 36.3°C", **temp_style)
        leg_temp.place(relx=0.9, rely=0.5, anchor="e")

        # 버튼 스타일
        button_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
        button_style = {"font": button_font, "bg": "skyblue", "fg": "navy"}

        # 기본 설정 버튼
        default_settings_btn = tk.Button(background, text="기본 설정", **button_style)
        default_settings_btn.place(relx=0.3, rely=0.5, relwidth=0.4, relheight=0.1)

        # 사용자 지정설정 버튼
        custom_settings_btn = tk.Button(background, text="사용자 지정설정", **button_style)
        custom_settings_btn.place(relx=0.3, rely=0.7, relwidth=0.4, relheight=0.1)

    def end_fullscreen(self, event=None):
        self.attributes("-fullscreen", False)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
