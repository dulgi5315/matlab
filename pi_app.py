import tkinter as tk
from tkinter import font as tkfont

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

        temp_font = tkfont.Font(family="Helvetica", size=20, weight="bold")

        # 머리 온도
        head_icon = self.create_icon(temp_frame, self.draw_head, 50, 50)
        head_icon.place(relx=0.2, rely=0.1, anchor="center")
        head_temp_frame = tk.Frame(temp_frame, bg="lightgray", bd=2, relief="solid")
        head_temp_frame.place(relx=0.2, rely=0.5, relwidth=0.25, relheight=0.6, anchor="center")
        self.head_temp = tk.Label(head_temp_frame, text="36.5°C", font=temp_font, bg="lightgray")
        self.head_temp.place(relx=0.5, rely=0.5, anchor="center")

        # 몸통 온도
        body_icon = self.create_icon(temp_frame, self.draw_body, 50, 50)
        body_icon.place(relx=0.5, rely=0.1, anchor="center")
        body_temp_frame = tk.Frame(temp_frame, bg="lightgray", bd=2, relief="solid")
        body_temp_frame.place(relx=0.5, rely=0.5, relwidth=0.25, relheight=0.6, anchor="center")
        self.body_temp = tk.Label(body_temp_frame, text="36.7°C", font=temp_font, bg="lightgray")
        self.body_temp.place(relx=0.5, rely=0.5, anchor="center")

        # 다리 온도
        leg_icon = self.create_icon(temp_frame, self.draw_legs, 50, 50)
        leg_icon.place(relx=0.8, rely=0.1, anchor="center")
        leg_temp_frame = tk.Frame(temp_frame, bg="lightgray", bd=2, relief="solid")
        leg_temp_frame.place(relx=0.8, rely=0.5, relwidth=0.25, relheight=0.6, anchor="center")
        self.leg_temp = tk.Label(leg_temp_frame, text="36.3°C", font=temp_font, bg="lightgray")
        self.leg_temp.place(relx=0.5, rely=0.5, anchor="center")

        # 버튼 스타일 및 배치
        button_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        button_style = {"font": button_font, "bg": "skyblue", "fg": "navy"}

        default_settings_btn = tk.Button(background, text="기본 설정", **button_style)
        default_settings_btn.place(relx=0.5, rely=0.6, relwidth=0.6, relheight=0.15, anchor="center")

        custom_settings_btn = tk.Button(background, text="사용자 지정설정", **button_style)
        custom_settings_btn.place(relx=0.5, rely=0.8, relwidth=0.6, relheight=0.15, anchor="center")

    def create_icon(self, parent, draw_function, width, height):
        canvas = tk.Canvas(parent, width=width, height=height, bg="white", highlightthickness=0)
        draw_function(canvas)
        return canvas

    def draw_head(self, canvas):
        canvas.create_oval(10, 10, 40, 40, outline="black", width=2)

    def draw_body(self, canvas):
        canvas.create_rectangle(15, 5, 35, 45, outline="black", width=2)

    def draw_legs(self, canvas):
        canvas.create_line(15, 10, 15, 40, fill="black", width=2)
        canvas.create_line(35, 10, 35, 40, fill="black", width=2)

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
