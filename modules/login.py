import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont

class LoginWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.master.title("PharmaCare - Login")
        self.master.geometry("500x600")
        self.master.configure(bg='#2c3e50')
        self.master.resizable(False, False)
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        # Fonts
        self.title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.subtitle_font = tkfont.Font(family="Helvetica", size=12)
        self.normal_font = tkfont.Font(family="Helvetica", size=10)

        # Colors
        self.primary_color = '#3498db'
        self.bg_color = '#2c3e50'
        self.light_color = '#ecf0f1'
        self.dark_color = '#34495e'

        # Build UI
        self.setup_ui()

    def setup_ui(self):
        # Gradient background
        canvas = tk.Canvas(self.master, width=500, height=600, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        for i in range(0, 600, 2):
            r = 44 + i//20
            g = 62 + i//30
            b = 80 + i//25
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_rectangle(0, i, 500, i+2, outline="", fill=color)

        # Frame (login card)
        card = tk.Frame(self.master, bg="white", bd=0, relief="flat")
        card.place(relx=0.5, rely=0.5, anchor="center", width=350, height=400)

        # Title
        tk.Label(card, text="PharmaCare", font=self.title_font, bg="white", fg=self.primary_color).pack(pady=(20, 5))
        tk.Label(card, text="Pharmacy Management System", font=self.subtitle_font, bg="white", fg="gray").pack(pady=(0, 20))

        # Username
        tk.Label(card, text="Username", font=self.normal_font, bg="white", anchor="w").pack(fill="x", padx=40)
        self.username_entry = tk.Entry(card, font=self.normal_font, bg="#f5f5f5", bd=0)
        self.username_entry.pack(fill="x", padx=40, pady=(5, 15), ipady=8)
        self.username_entry.insert(0, "admin")

        # Password
        tk.Label(card, text="Password", font=self.normal_font, bg="white", anchor="w").pack(fill="x", padx=40)
        self.password_entry = tk.Entry(card, font=self.normal_font, bg="#f5f5f5", bd=0, show="•")
        self.password_entry.pack(fill="x", padx=40, pady=(5, 5), ipady=8)
        self.password_entry.insert(0, "admin123")

        # Show password
        self.show_pass = tk.BooleanVar()
        show_chk = tk.Checkbutton(card, text="Show Password", variable=self.show_pass, command=self.toggle_password,
                                  bg="white", font=('Helvetica', 9))
        show_chk.pack(pady=(0, 15))

        # Login button
        login_btn = tk.Button(card, text="Login", bg=self.primary_color, fg="white", font=("Helvetica", 12, "bold"),
                              bd=0, relief="flat", activebackground="#2980b9", cursor="hand2", command=self.login)
        login_btn.pack(fill="x", padx=40, pady=(5, 10), ipady=8)

        # Hover effect
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg="#2980b9"))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg=self.primary_color))

        # Forgot Password
        forgot = tk.Label(card, text="Forgot Password?", fg=self.primary_color, bg="white", cursor="hand2",
                          font=('Helvetica', 9, 'underline'))
        forgot.pack()
        forgot.bind("<Button-1>", lambda e: messagebox.showinfo("Info", "Please contact admin."))

    def toggle_password(self):
        if self.show_pass.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="•")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "admin123":
            self.master.destroy()
            self.app.show_main_window()
        else:
            messagebox.showerror("Error", "Invalid credentials")
    def on_close(self):
        self.app.root.quit()
        self.app.root.destroy()