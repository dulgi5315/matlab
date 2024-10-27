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

        # 버튼 스타일
        button_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
        button_style = {"font": button_font, "bg": "skyblue", "fg": "navy"}

        # 기본 설정 버튼
        default_settings_btn = tk.Button(background, text="기본 설정", **button_style)
        default_settings_btn.place(relx=0.3, rely=0.4, relwidth=0.4, relheight=0.1)

        # 사용자 지정설정 버튼
        custom_settings_btn = tk.Button(background, text="사용자 지정설정", **button_style)
        custom_settings_btn.place(relx=0.3, rely=0.6, relwidth=0.4, relheight=0.1)

    def end_fullscreen(self, event=None):
        self.attributes("-fullscreen", False)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
