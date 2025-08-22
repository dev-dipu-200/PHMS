import tkinter as tk
from tkinter import messagebox
from db_config import init_db
# Importing modules
from modules.login import LoginWindow
from modules.main import MainWindow
from modules.medicines import MedicinesWindow
from modules.sales import SalesWindow
from modules.inventory import InventoryWindow
from modules.reports import ReportsWindow
from modules.settings import SettingsWindow
from modules.customers import CustomersWindow
from modules.suppliers import SuppliersWindow
from modules.purchases import PurchasesWindow
from modules.prescriptions import PrescriptionsWindow
from modules.payments import PaymentsWindow
from modules.users import UsersWindow


class PharmacyApp:
    def __init__(self):
        init_db()
        self.root = tk.Tk()
        self.root.withdraw()  # hide until login
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.show_login_window()

    def set_close_protocol(self, window):
        """Attach the same close behavior to any Toplevel window"""
        window.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------------- Windows ---------------- #

    def show_login_window(self):
        login_win = tk.Toplevel(self.root)
        self.set_close_protocol(login_win)
        LoginWindow(login_win, self)

    def show_main_window(self):
        main_win = tk.Toplevel(self.root)
        self.set_close_protocol(main_win)
        MainWindow(main_win, self)

    def show_medicines_window(self):
        medicines_win = tk.Toplevel(self.root)
        self.set_close_protocol(medicines_win)
        MedicinesWindow(medicines_win, self)

    def show_sales_window(self):
        sales_win = tk.Toplevel(self.root)
        self.set_close_protocol(sales_win)
        SalesWindow(sales_win, self)

    def show_inventory_window(self):
        inventory_win = tk.Toplevel(self.root)
        self.set_close_protocol(inventory_win)
        InventoryWindow(inventory_win, self)

    def show_reports_window(self):
        reports_win = tk.Toplevel(self.root)
        self.set_close_protocol(reports_win)
        ReportsWindow(reports_win, self)

    def show_settings_window(self):
        settings_win = tk.Toplevel(self.root)
        self.set_close_protocol(settings_win)
        SettingsWindow(settings_win, self)

    def show_customers_window(self):
        customers_win = tk.Toplevel(self.root)
        self.set_close_protocol(customers_win)
        CustomersWindow(customers_win, self)

    def show_suppliers_window(self):
        suppliers_win = tk.Toplevel(self.root)
        self.set_close_protocol(suppliers_win)
        SuppliersWindow(suppliers_win, self)

    def show_purchases_window(self):
        purchases_win = tk.Toplevel(self.root)
        self.set_close_protocol(purchases_win)
        PurchasesWindow(purchases_win, self)

    def show_prescriptions_window(self):
        prescriptions_win = tk.Toplevel(self.root)
        self.set_close_protocol(prescriptions_win)
        PrescriptionsWindow(prescriptions_win, self)

    def show_payments_window(self):
        payments_win = tk.Toplevel(self.root)
        self.set_close_protocol(payments_win)
        PaymentsWindow(payments_win, self)

    def show_users_window(self):
        users_win = tk.Toplevel(self.root)
        self.set_close_protocol(users_win)
        UsersWindow(users_win, self)

    # ---------------- Close ---------------- #

    def on_close(self):
        """Destroy the entire application cleanly with confirmation"""
        if messagebox.askokcancel("Exit", "Are you sure you want to exit the application?"):
            self.root.quit()
            self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = PharmacyApp()
    app.run()
