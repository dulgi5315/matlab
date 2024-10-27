import tkinter as tk
from tkinter import font as tkfont

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("라즈베리파이 애플리케이션")
        self.geometry("800x480")  # 7인치 터치스크린 해상도

        self.create_widgets()

    def create_widgets(self):
        # 배경 프레임
        background = tk.Frame(self, bg="lightblue")
        background.place(relwidth=1, relheight=1)

        # 버튼 스타일
        button_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
        button_style = {"font": button_font, "bg": "skyblue", "fg": "navy"}

        # 사용자 지정설정 버튼
        custom_settings_btn = tk.Button(background, text="사용자 지정설정", **button_style)
        custom_settings_btn.place(relx=0.3, rely=0.4, relwidth=0.4, relheight=0.1)

        # 기본 설정 버튼
        default_settings_btn = tk.Button(background, text="기본 설정", **button_style)
        default_settings_btn.place(relx=0.3, rely=0.6, relwidth=0.4, relheight=0.1)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
