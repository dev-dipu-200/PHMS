import tkinter as tk
from tkinter import messagebox

from modules.login import LoginWindow
from modules.main import MainWindow
from modules.medicines import MedicinesWindow
from modules.sales import SalesWindow
from modules.inventory import InventoryWindow
from modules.reports import ReportsWindow
from modules.settings import SettingsWindow


class PharmacyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.show_login_window()

    def set_close_protocol(self, window):
        """Attach the same close behavior to any Toplevel window"""
        window.protocol("WM_DELETE_WINDOW", self.on_close)

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
