import customtkinter as ctk
from tkinter import messagebox


class LoginWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.master.title("PharmaCare - Login")
        self.center_window(500, 600)   # ⬅️ Center window
        self.master.resizable(False, False)
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        # Appearance and theme
        ctk.set_appearance_mode("dark")   # "light", "dark", "system"
        ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

        # Colors
        self.primary_color = "#3498db"

        # Build UI
        self.setup_ui()

    def center_window(self, w, h):
        """Center the window on the screen"""
        screen_w = self.master.winfo_screenwidth()
        screen_h = self.master.winfo_screenheight()
        x = int((screen_w / 2) - (w / 2))
        y = int((screen_h / 2) - (h / 2))
        self.master.geometry(f"{w}x{h}+{x}+{y}")

    def setup_ui(self):
        # Main frame (login card)
        frame = ctk.CTkFrame(self.master, corner_radius=15, width=350, height=400)
        frame.place(relx=0.5, rely=0.5, anchor="center")   # ⬅️ center login form

        # Grid inside frame
        frame.grid_rowconfigure(99, weight=1)  
        frame.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(frame, text="PharmaCare",
                     font=("Helvetica", 24, "bold"),
                     text_color=self.primary_color).grid(row=0, column=0, pady=(20, 5), sticky="n")
        ctk.CTkLabel(frame, text="Pharmacy Management System",
                     font=("Helvetica", 12), text_color="gray").grid(row=1, column=0, pady=(0, 20))

        # Username
        ctk.CTkLabel(frame, text="Username", anchor="w").grid(row=2, column=0, padx=40, sticky="w")
        self.username_entry = ctk.CTkEntry(frame, placeholder_text="Enter username", width=250)
        self.username_entry.grid(row=3, column=0, padx=40, pady=(5, 15))
        self.username_entry.insert(0, "admin")

        # Password
        ctk.CTkLabel(frame, text="Password", anchor="w").grid(row=4, column=0, padx=40, sticky="w")
        self.password_entry = ctk.CTkEntry(frame, placeholder_text="Enter password", show="•", width=250)
        self.password_entry.grid(row=5, column=0, padx=40, pady=(5, 5))
        self.password_entry.insert(0, "admin123")

        # Show password
        self.show_pass = ctk.CTkCheckBox(frame, text="Show Password", command=self.toggle_password)
        self.show_pass.grid(row=6, column=0, pady=(0, 15))

        # Login button
        self.login_btn = ctk.CTkButton(frame, text="Login",
                                       command=self.login,
                                       fg_color=self.primary_color, hover_color="#2980b9",
                                       width=250, height=35)
        self.login_btn.grid(row=7, column=0, padx=40, pady=(5, 10))

        # Forgot Password
        forgot = ctk.CTkLabel(frame, text="Forgot Password?",
                              text_color=self.primary_color, cursor="hand2",
                              font=("Helvetica", 9, "underline"))
        forgot.grid(row=8, column=0, pady=(5, 10))
        forgot.bind("<Button-1>", lambda e: messagebox.showinfo("Info", "Please contact admin."))

    def toggle_password(self):
        if self.show_pass.get() == 1:
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="•")

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