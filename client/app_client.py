import customtkinter as ctk
import tkinter 		 as tk
from PIL import Image, ImageTk
from hashlib import sha256
import socket

class GUI(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        ctk.CTk.__init__(self)
        self.genScreen()
        self.mainloop()

    def genScreen(self):

        def move(e):
            self.geometry(f'+{e.x_root}+{e.y_root}')

        def close_window():
            self.destroy()

        def send_message():
            msg = message_box.get()
            text_box.insert(tk.END,'  # ' + msg + '\n')
            message_box.delete(0, 'end')

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('127.0.0.1', 1900))
            sock.send('USER {}'.format(msg).encode('utf-8'))

            msg_recv = sock.recv(4096).decode('utf-8')
            text_box.insert(tk.END,'  # ' + msg_recv + '\n')
            sock.close()

        def login():
            username = input_1.get()
            password = sha256(input_2.get().encode()).hexdigest()
            payload = f'USER {username} {password}'
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('127.0.0.1', 1900))
            sock.send(payload.encode('utf-8'))
            sock.close()

        self.geometry("800x600")
        self.wm_attributes('-transparentcolor', "black")
        self.overrideredirect(1)
        self.title("#irc - Internet Relay Chat")
        colorTheme = "#f05c51"
        color_login_background = "#d9ead3"
        borderw = 2

        divisor = tk.ttk.PanedWindow(master=self, orient="horizontal")
        divisor.pack(fill="both", expand=True)

        loginScreen = ctk.CTkLabel(master=divisor, image=ImageTk.PhotoImage(Image.open('./assets/back.png').resize((1050, 1050))), fg_color="white", text="", anchor=tk.N)
        rightSide = ctk.CTkFrame(master=divisor, fg_color=colorTheme, corner_radius=20)

        frame_2 = ctk.CTkFrame(master=rightSide, border_color=color_login_background, border_width=borderw, corner_radius=15, fg_color=color_login_background)
        frame_2.place(relx=0.02, rely=0.03, relheight=0.94, relwidth=0.96)

        exit_button = ctk.CTkButton(master=loginScreen, text="", width=20, height=20, corner_radius=15, command=close_window, fg_color=colorTheme)
        exit_button.place(x=10, y=10)

        label_logo = ctk.CTkLabel(master=loginScreen, text="", image=ImageTk.PhotoImage(Image.open('./assets/hashtag.png').resize((150,150))), font=("Comic Sans MS", 12, "bold"), text_color=colorTheme)
        label_logo.place(relx=0.5, rely=0.3, anchor=tk.CENTER, relheight=0.5, relwidth=0.6)
        label_name = ctk.CTkLabel(master=loginScreen, text="Emanuel Firmino Abrantes\nTeleinformática e Redes 2\n#irc - Internet Relay Chat", font=("Comic Sans MS", 15), text_color="grey", fg_color='transparent')
        label_name.place(relx=0.5, rely=0.1, relwidth=0.7, anchor=tk.CENTER)
        input_1 = ctk.CTkEntry(master=loginScreen, placeholder_text="Usuário", width=200, corner_radius=30, border_color=colorTheme, fg_color=color_login_background, border_width=3,
                            text_color="black")
        input_1.place(relx=0.5, rely=0.45, anchor=tk.CENTER, relwidth=0.5)

        input_2 = ctk.CTkEntry(master=loginScreen, placeholder_text="Senha", show="*", width=200, corner_radius=30, border_color=colorTheme, fg_color=color_login_background, border_width=3,
                            text_color="black")
        input_2.place(relx=0.5, rely=0.52, anchor=tk.CENTER, relwidth=0.5)

        loginButton	= ctk.CTkButton(master=loginScreen, command=login, text="Entrar", corner_radius=30, fg_color=colorTheme)
        loginButton.place(relx=0.5, rely=0.6, anchor=tk.CENTER, relwidth=0.3)

        message_box = ctk.CTkEntry(master=frame_2, border_color=colorTheme, border_width=borderw, corner_radius=30, fg_color='#302a2a')
        message_box.place(relx=0.87, rely=0.95, anchor=tk.E, relwidth=0.85)
        button_send = ctk.CTkButton(master=frame_2, command=send_message, text=">>", corner_radius=30, fg_color=colorTheme, text_color="white")
        button_send.place(relx=0.88, rely=0.95, anchor=tk.W, relwidth=0.1)
        text_box = tk.Text(master=frame_2, font=("Comic Sans MS", 14), relief='sunken', yscrollcommand=True, bg='#302a2a', fg='white')
        text_box.place(relx=0.5, rely=0.465, anchor=tk.CENTER, relwidth=0.96, relheight=0.88)

        divisor.add(loginScreen)
        divisor.add(rightSide)

        loginScreen.bind('<B1-Motion>', move)
        label_logo.bind('<B1-Motion>', move)
        label_name.bind('<B1-Motion>', move)

if __name__ == "__main__": GUI()
