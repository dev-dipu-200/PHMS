import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import time


class MainWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app

        # Colors & Fonts
        self.primary_color = "#3498db"
        self.secondary_color = "#9b59b6"
        self.accent_color = "#e67e22"
        self.success_color = "#27ae60"

        self.title_font = tkfont.Font(size=18, weight="bold")
        self.header_font = tkfont.Font(size=14, weight="bold")
        self.normal_font = tkfont.Font(size=11)

        # Configure window
        self.master.title("PharmaCare Management System")
        self.master.geometry("1100x760")
        self.master.configure(bg="white")

        # Apply ttk styles
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="white")
        style.configure("TLabel", background="white", font=self.normal_font)
        style.configure("Title.TLabel", font=self.title_font, foreground=self.primary_color, background="white")
        style.configure("Primary.TButton", font=self.normal_font, padding=6, relief="flat")

        # Build UI
        self.setup_ui()

    def setup_ui(self):
        # Header
        header_frame = ttk.Frame(self.master, style="TFrame")
        header_frame.pack(fill="x", padx=20, pady=10)

        title_label = ttk.Label(header_frame, text="PharmaCare Management System", style="Title.TLabel")
        title_label.pack(side="left")

        self.time_label = ttk.Label(header_frame, text="", style="TLabel")
        self.time_label.pack(side="right")
        self.update_time()

        # Navigation - Row 1
        nav_frame = ttk.Frame(self.master, style="TFrame")
        nav_frame.pack(fill="x", padx=20, pady=10)

        buttons = [
            ("💊 Medicines", self.app.show_medicines_window),
            ("💰 Sales", self.app.show_sales_window),
            ("📦 Inventory", self.app.show_inventory_window),
            ("📈 Reports", self.app.show_reports_window),
            ("⚙️ Settings", self.app.show_settings_window),
        ]
        for text, command in buttons:
            btn = ttk.Button(nav_frame, text=text, command=command, style="Primary.TButton")
            btn.pack(side="left", padx=5)

        # Navigation - Row 2 (new buttons you requested)
        bar = ttk.Frame(self.master, style="TFrame")
        bar.pack(fill="x", padx=20, pady=5)

        ttk.Button(bar, text="👥 Customers", command=self.app.show_customers_window,
                   style="Primary.TButton").pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text="🏢 Suppliers", command=self.app.show_suppliers_window,
                   style="Primary.TButton").pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text="🛒 Purchases", command=self.app.show_purchases_window,
                   style="Primary.TButton").pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text="📜 Prescriptions", command=self.app.show_prescriptions_window,
                   style="Primary.TButton").pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text="💳 Payments", command=self.app.show_payments_window,
                   style="Primary.TButton").pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text="👤 Users", command=self.app.show_users_window,
                   style="Primary.TButton").pack(side=tk.LEFT, padx=4)

        # Content
        content_frame = ttk.Frame(self.master, style="TFrame")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        welcome_label = ttk.Label(content_frame, text="Welcome to PharmaCare Management System",
                                  font=self.header_font)
        welcome_label.pack(pady=20)

        # Stats Section
        stats_frame = ttk.Frame(content_frame, style="TFrame")
        stats_frame.pack(fill="x", pady=10)

        stats = [
            ("Total Medicines", "128", self.primary_color),
            ("Low Stock Items", "5", self.accent_color),
            ("Today's Sales", "$1,240", self.success_color),
            ("Total Sales", "$12,580", self.secondary_color),
        ]
        for i, (title, value, color) in enumerate(stats):
            stat_frame = ttk.Frame(stats_frame, relief="raised", borderwidth=1)
            stat_frame.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            stats_frame.columnconfigure(i, weight=1)
            ttk.Label(stat_frame, text=title, font=self.normal_font).pack(padx=10, pady=(10, 5))
            ttk.Label(stat_frame, text=value,
                      font=tkfont.Font(size=16, weight="bold"), foreground=color).pack(padx=10, pady=(5, 10))

        # Recent Activity
        activity_frame = ttk.LabelFrame(content_frame, text="Recent Activity", padding=10)
        activity_frame.pack(fill="both", expand=True, pady=10)

        activities = [
            "Sold 2 packs of Paracetamol to John Doe",
            "Added new stock of Amoxicillin",
            "Generated monthly sales report",
            "Updated pricing for Antibiotics category",
            "Low stock alert for Vitamin C tablets",
        ]
        for activity in activities:
            ttk.Label(activity_frame, text=f"• {activity}", style="TLabel").pack(anchor="w", pady=2)

    def update_time(self):
        """Update time label every second"""
        current_time = time.strftime("%H:%M:%S %p")
        self.time_label.config(text=current_time)
        self.master.after(1000, self.update_time)


# # Run directly for testing
# if __name__ == "__main__":
#     class DummyApp:
#         def show_medicines_window(self): print("Medicines Window")
#         def show_sales_window(self): print("Sales Window")
#         def show_inventory_window(self): print("Inventory Window")
#         def show_reports_window(self): print("Reports Window")
#         def show_settings_window(self): print("Settings Window")
#         def show_customers_window(self): print("Customers Window")
#         def show_suppliers_window(self): print("Suppliers Window")
#         def show_purchases_window(self): print("Purchases Window")
#         def show_prescriptions_window(self): print("Prescriptions Window")
#         def show_payments_window(self): print("Payments Window")
#         def show_users_window(self): print("Users Window")

#     root = tk.Tk()
#     app = DummyApp()
#     MainWindow(root, app)
#     root.mainloop()
