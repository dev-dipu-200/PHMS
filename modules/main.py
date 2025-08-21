import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
from datetime import datetime

class MainWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.master.title("PharmaCare - Pharmacy Management System")
        self.master.geometry("1000x700")
        self.master.configure(bg='#f5f5f5')

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        # self.master.bind("<Button-1>", self.on_click_background)

        # Fonts
        self.title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.header_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.normal_font = tkfont.Font(family="Helvetica", size=10)

        # Colors
        self.primary_color = '#2c3e50'
        self.secondary_color = '#3498db'
        self.accent_color = '#e74c3c'
        self.success_color = '#27ae60'
        self.light_bg = '#ecf0f1'

        self.setup_styles()
        self.setup_ui()

    def on_close(self):
        """Ask confirmation when closing."""
        if messagebox.askokcancel("Exit", "Do you really want to exit?"):
            self.master.destroy()
            self.app.root.quit()
            self.app.root.destroy()

    def on_click_background(self, event):
        """If user clicks on empty background area, ask to exit."""
        widget = event.widget
        if widget == self.master:
            self.on_close()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=self.light_bg)
        style.configure('TLabel', background=self.light_bg, font=self.normal_font)
        style.configure('Title.TLabel', background=self.light_bg, font=self.title_font, foreground=self.primary_color)
        style.configure('TButton', font=self.normal_font)
        style.configure('Primary.TButton', background=self.secondary_color, foreground='white')
        style.configure('Success.TButton', background=self.success_color, foreground='white')
        style.configure('Danger.TButton', background=self.accent_color, foreground='white')
        style.configure('TEntry', font=self.normal_font)
        style.configure('TCombobox', font=self.normal_font)

    def setup_ui(self):
        # Header
        header_frame = ttk.Frame(self.master, style='TFrame')
        header_frame.pack(fill='x', padx=20, pady=10)

        title_label = ttk.Label(header_frame, text="PharmaCare Management System", style='Title.TLabel')
        title_label.pack(side='left')

        self.time_label = ttk.Label(header_frame, text="", style='TLabel')
        self.time_label.pack(side='right')
        self.update_time()

        # Navigation buttons
        nav_frame = ttk.Frame(self.master, style='TFrame')
        nav_frame.pack(fill='x', padx=20, pady=10)

        buttons = [
            ("💊 Medicines", self.app.show_medicines_window),
            ("💰 Sales", self.app.show_sales_window),
            ("📦 Inventory", self.app.show_inventory_window),
            ("📈 Reports", self.app.show_reports_window),
            ("⚙️ Settings", self.app.show_settings_window)
        ]
        for text, command in buttons:
            btn = ttk.Button(nav_frame, text=text, command=command, style='Primary.TButton')
            btn.pack(side='left', padx=5)

        # Content
        content_frame = ttk.Frame(self.master, style='TFrame')
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)

        welcome_label = ttk.Label(content_frame, text="Welcome to PharmaCare Management System", font=self.header_font)
        welcome_label.pack(pady=20)

        # Stats
        stats_frame = ttk.Frame(content_frame, style='TFrame')
        stats_frame.pack(fill='x', pady=10)

        stats = [
            ("Total Medicines", "128", self.primary_color),
            ("Low Stock Items", "5", self.accent_color),
            ("Today's Sales", "$1,240", self.success_color),
            ("Total Sales", "$12,580", self.secondary_color)
        ]
        for i, (title, value, color) in enumerate(stats):
            stat_frame = ttk.Frame(stats_frame, relief='raised', borderwidth=1)
            stat_frame.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')
            stats_frame.columnconfigure(i, weight=1)
            ttk.Label(stat_frame, text=title, font=self.normal_font).pack(padx=10, pady=(10, 5))
            ttk.Label(stat_frame, text=value, font=tkfont.Font(size=16, weight='bold'),
                      foreground=color).pack(padx=10, pady=(5, 10))

        # Recent activity
        activity_frame = ttk.LabelFrame(content_frame, text="Recent Activity", padding=10)
        activity_frame.pack(fill='both', expand=True, pady=10)

        activities = [
            "Sold 2 packs of Paracetamol to John Doe",
            "Added new stock of Amoxicillin",
            "Generated monthly sales report",
            "Updated pricing for Antibiotics category",
            "Low stock alert for Vitamin C tablets"
        ]
        for activity in activities:
            ttk.Label(activity_frame, text=f"• {activity}", style='TLabel').pack(anchor='w', pady=2)

    def update_time(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=now)
        self.master.after(1000, self.update_time)

