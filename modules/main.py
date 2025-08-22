import customtkinter as ctk
import time


class MainWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app

        # Theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Configure window
        self.master.title("PharmaCare Management System")
        self.master.geometry("1100x700")

        # Colors
        self.primary_color = "#3498db"
        self.secondary_color = "#9b59b6"
        self.accent_color = "#e67e22"
        self.success_color = "#27ae60"

        # Build UI
        self.setup_ui()

    def setup_ui(self):
        # ===== Header =====
        header_frame = ctk.CTkFrame(self.master, fg_color="white")
        header_frame.pack(fill="x", padx=10, pady=10)

        title_label = ctk.CTkLabel(
            header_frame,
            text="PharmaCare Management System",
            text_color=self.primary_color,
            font=ctk.CTkFont(size=20, weight="bold"),
            pady=10,
            padx=10
        )
        title_label.pack(side="left")

        self.time_label = ctk.CTkLabel(header_frame, text="", font=ctk.CTkFont(size=14), pady=10, padx=10)
        self.time_label.pack(side="right")
        self.update_time()

        # ===== Navigation Row 1 =====
        nav_frame = ctk.CTkFrame(self.master, fg_color="white")
        nav_frame.pack(fill="x", padx=20, pady=10)

        buttons = [
            ("💊 Medicines", self.app.show_medicines_window),
            ("💰 Sales", self.app.show_sales_window),
            ("📦 Inventory", self.app.show_inventory_window),
            ("📈 Reports", self.app.show_reports_window),
            ("⚙️ Settings", self.app.show_settings_window),
        ]
        for text, command in buttons:
            ctk.CTkButton(nav_frame, text=text, command=command).pack(side="left", padx=5)

        # ===== Navigation Row 2 =====
        bar = ctk.CTkFrame(self.master, fg_color="white")
        bar.pack(fill="x", padx=20, pady=5)

        second_buttons = [
            ("👥 Customers", self.app.show_customers_window),
            ("🏢 Suppliers", self.app.show_suppliers_window),
            ("🛒 Purchases", self.app.show_purchases_window),
            ("📜 Prescriptions", self.app.show_prescriptions_window),
            ("💳 Payments", self.app.show_payments_window),
            ("👤 Users", self.app.show_users_window),
        ]
        for text, command in second_buttons:
            ctk.CTkButton(bar, text=text, command=command).pack(side="left", padx=4)

        # ===== Content =====
        content_frame = ctk.CTkFrame(self.master, fg_color="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        welcome_label = ctk.CTkLabel(
            content_frame,
            text="Welcome to PharmaCare Management System",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        welcome_label.pack(pady=20)

        # ===== Stats Section =====
        stats_frame = ctk.CTkFrame(content_frame, fg_color="white")
        stats_frame.pack(fill="x", pady=10)

        stats = [
            ("Total Medicines", "128", self.primary_color),
            ("Low Stock Items", "5", self.accent_color),
            ("Today's Sales", "$1,240", self.success_color),
            ("Total Sales", "$12,580", self.secondary_color),
        ]
        for i, (title, value, color) in enumerate(stats):
            stat_frame = ctk.CTkFrame(stats_frame, border_width=1, corner_radius=8)
            stat_frame.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            stats_frame.grid_columnconfigure(i, weight=1)

            ctk.CTkLabel(stat_frame, text=title, font=ctk.CTkFont(size=13)).pack(padx=10, pady=(10, 5))
            ctk.CTkLabel(
                stat_frame, text=value,
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=color
            ).pack(padx=10, pady=(5, 10))

        # ===== Recent Activity =====
        activity_frame = ctk.CTkFrame(content_frame, corner_radius=8)
        activity_frame.pack(fill="both", expand=True, pady=10)

        ctk.CTkLabel(activity_frame, text="Recent Activity",
                     font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=10, pady=5)

        activities = [
            "Sold 2 packs of Paracetamol to John Doe",
            "Added new stock of Amoxicillin",
            "Generated monthly sales report",
            "Updated pricing for Antibiotics category",
            "Low stock alert for Vitamin C tablets",
        ]
        for activity in activities:
            ctk.CTkLabel(activity_frame, text=f"• {activity}", anchor="w").pack(anchor="w", padx=20, pady=2)

    def update_time(self):
        current_time = time.strftime("%H:%M:%S %p")
        self.time_label.configure(text=current_time)
        self.master.after(1000, self.update_time)
