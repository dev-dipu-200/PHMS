import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont


class SettingsWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.master.title("Settings")
        self.master.geometry("600x500")
        self.master.configure(bg='#f5f5f5')
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header_frame = ttk.Frame(self.master)
        header_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(header_frame, text="System Settings", 
                 font=tkfont.Font(family="Helvetica", size=16, weight="bold")).pack(side='left')
        
        # Back button
        back_btn = ttk.Button(header_frame, text="Back to Main", command=self.master.destroy)
        back_btn.pack(side='right')
        
        # Create a notebook for settings tabs
        notebook = ttk.Notebook(self.master)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create tabs
        general_tab = ttk.Frame(notebook)
        inventory_tab = ttk.Frame(notebook)
        user_tab = ttk.Frame(notebook)
        
        notebook.add(general_tab, text="General")
        notebook.add(inventory_tab, text="Inventory")
        notebook.add(user_tab, text="Users")
        
        # Setup general tab
        self.setup_general_tab(general_tab)
        
        # Setup inventory tab
        self.setup_inventory_tab(inventory_tab)
        
        # Setup user tab
        self.setup_user_tab(user_tab)
    
    def setup_general_tab(self, parent):
        form_frame = ttk.Frame(parent)
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        settings = [
            ("Pharmacy Name:", "MediCare Pharmacy"),
            ("Address:", "123 Health St, Medical City"),
            ("Phone:", "(555) 123-4567"),
            ("Email:", "contact@medicare.example"),
            ("Tax Rate (%):", "8.5"),
            ("Currency:", "USD"),
        ]
        
        for i, (label, default_value) in enumerate(settings):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')
            entry.insert(0, default_value)
        
        save_btn = ttk.Button(form_frame, text="Save Settings", style='Success.TButton')
        save_btn.grid(row=len(settings), column=0, columnspan=2, pady=20)
    
    def setup_inventory_tab(self, parent):
        form_frame = ttk.Frame(parent)
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        settings = [
            ("Low Stock Threshold:", "20"),
            ("Expiry Alert Days:", "30"),
            ("Auto Backup (days):", "7"),
            ("Default Supplier:", "MediSupply Inc."),
        ]
        
        for i, (label, default_value) in enumerate(settings):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')
            entry.insert(0, default_value)
        
        # Checkboxes
        alerts_var = tk.BooleanVar(value=True)
        alerts_cb = ttk.Checkbutton(form_frame, text="Enable Low Stock Alerts", variable=alerts_var)
        alerts_cb.grid(row=len(settings), column=0, columnspan=2, pady=5, sticky='w')
        
        expiry_var = tk.BooleanVar(value=True)
        expiry_cb = ttk.Checkbutton(form_frame, text="Enable Expiry Alerts", variable=expiry_var)
        expiry_cb.grid(row=len(settings)+1, column=0, columnspan=2, pady=5, sticky='w')
        
        save_btn = ttk.Button(form_frame, text="Save Settings", style='Success.TButton')
        save_btn.grid(row=len(settings)+2, column=0, columnspan=2, pady=20)
    
    def setup_user_tab(self, parent):
        form_frame = ttk.Frame(parent)
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # User list
        ttk.Label(form_frame, text="Users", font=tkfont.Font(weight='bold')).grid(
            row=0, column=0, columnspan=2, pady=10, sticky='w')
        
        users = [
            ('admin', 'Administrator', 'Active'),
            ('pharmacist', 'John Doe', 'Active'),
            ('assistant', 'Jane Smith', 'Inactive'),
        ]
        
        for i, (username, name, status) in enumerate(users, start=1):
            ttk.Label(form_frame, text=f"{name} ({username})").grid(row=i, column=0, padx=5, pady=2, sticky='w')
            ttk.Label(form_frame, text=status).grid(row=i, column=1, padx=5, pady=2, sticky='e')
        
        # Add user button
        add_btn = ttk.Button(form_frame, text="Add New User", style='Primary.TButton')
        add_btn.grid(row=len(users)+1, column=0, columnspan=2, pady=20)