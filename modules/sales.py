import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import font as tkfont
from datetime import datetime, timedelta



class SalesWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.master.title("Sales Management")
        self.master.geometry("900x600")
        self.master.configure(bg='#f5f5f5')
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header_frame = ttk.Frame(self.master)
        header_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(header_frame, text="Sales Management", 
                 font=tkfont.Font(family="Helvetica", size=16, weight="bold")).pack(side='left')
        
        # Back button
        back_btn = ttk.Button(header_frame, text="Back to Main", command=self.master.destroy)
        back_btn.pack(side='right')
        
        # Create a notebook for tabs
        notebook = ttk.Notebook(self.master)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create tabs
        new_sale_tab = ttk.Frame(notebook)
        sales_history_tab = ttk.Frame(notebook)
        
        notebook.add(new_sale_tab, text="New Sale")
        notebook.add(sales_history_tab, text="Sales History")
        
        # Setup new sale tab
        self.setup_new_sale_tab(new_sale_tab)
        
        # Setup sales history tab
        self.setup_sales_history_tab(sales_history_tab)
    
    def setup_new_sale_tab(self, parent):
        # Form frame
        form_frame = ttk.Frame(parent)
        form_frame.pack(fill='x', padx=20, pady=10)
        
        # Customer info
        ttk.Label(form_frame, text="Customer Information", font=tkfont.Font(weight='bold')).grid(
            row=0, column=0, columnspan=2, pady=10, sticky='w')
        
        ttk.Label(form_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        customer_name = ttk.Entry(form_frame, width=30)
        customer_name.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(form_frame, text="Phone:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        customer_phone = ttk.Entry(form_frame, width=20)
        customer_phone.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        # Medicine selection
        ttk.Label(form_frame, text="Select Medicine", font=tkfont.Font(weight='bold')).grid(
            row=3, column=0, columnspan=2, pady=(20, 10), sticky='w')
        
        ttk.Label(form_frame, text="Medicine:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        medicine_combo = ttk.Combobox(form_frame, width=27, state='readonly')
        medicine_combo.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        medicine_combo['values'] = ('Paracetamol', 'Amoxicillin', 'Vitamin C', 'Ibuprofen', 'Omeprazole')
        
        ttk.Label(form_frame, text="Quantity:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
        quantity_spin = ttk.Spinbox(form_frame, from_=1, to=100, width=10)
        quantity_spin.grid(row=5, column=1, padx=5, pady=5, sticky='w')
        quantity_spin.set(1)
        
        ttk.Label(form_frame, text="Price:").grid(row=6, column=0, padx=5, pady=5, sticky='e')
        price_entry = ttk.Entry(form_frame, width=15, state='readonly')
        price_entry.grid(row=6, column=1, padx=5, pady=5, sticky='w')
        price_entry.insert(0, "$0.00")
        
        # Add to cart button
        add_btn = ttk.Button(form_frame, text="Add to Cart", style='Primary.TButton')
        add_btn.grid(row=7, column=1, padx=5, pady=10, sticky='w')
        
        # Cart frame
        cart_frame = ttk.LabelFrame(parent, text="Shopping Cart", padding=10)
        cart_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Cart treeview
        columns = ('medicine', 'quantity', 'price', 'total')
        cart_tree = ttk.Treeview(cart_frame, columns=columns, show='headings', height=6)
        
        cart_tree.heading('medicine', text='Medicine')
        cart_tree.heading('quantity', text='Quantity')
        cart_tree.heading('price', text='Unit Price')
        cart_tree.heading('total', text='Total')
        
        cart_tree.column('medicine', width=200)
        cart_tree.column('quantity', width=100, anchor='center')
        cart_tree.column('price', width=100, anchor='e')
        cart_tree.column('total', width=100, anchor='e')
        
        cart_tree.pack(fill='both', expand=True)
        
        # Total frame
        total_frame = ttk.Frame(cart_frame)
        total_frame.pack(fill='x', pady=10)
        
        ttk.Label(total_frame, text="Grand Total:", font=tkfont.Font(weight='bold')).pack(side='left')
        total_label = ttk.Label(total_frame, text="$0.00", font=tkfont.Font(weight='bold'))
        total_label.pack(side='left', padx=5)
        
        # Checkout button
        checkout_btn = ttk.Button(cart_frame, text="Process Payment", style='Success.TButton')
        checkout_btn.pack(pady=10)
    
    def setup_sales_history_tab(self, parent):
        # Filter frame
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(filter_frame, text="Filter by Date:").pack(side='left')
        
        start_date = ttk.Entry(filter_frame, width=12)
        start_date.pack(side='left', padx=5)
        start_date.insert(0, "2024-01-01")
        
        ttk.Label(filter_frame, text="to").pack(side='left', padx=5)
        
        end_date = ttk.Entry(filter_frame, width=12)
        end_date.pack(side='left', padx=5)
        end_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        filter_btn = ttk.Button(filter_frame, text="Apply Filter", style='Primary.TButton')
        filter_btn.pack(side='left', padx=10)
        
        export_btn = ttk.Button(filter_frame, text="Export Report")
        export_btn.pack(side='right')
        
        # Sales history treeview
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('id', 'date', 'customer', 'items', 'total')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        tree.heading('id', text='Sale ID')
        tree.heading('date', text='Date')
        tree.heading('customer', text='Customer')
        tree.heading('items', text='Items')
        tree.heading('total', text='Total Amount')
        
        tree.column('id', width=80, anchor='center')
        tree.column('date', width=100, anchor='center')
        tree.column('customer', width=150)
        tree.column('items', width=100, anchor='center')
        tree.column('total', width=100, anchor='e')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Sample data
        sales = [
            ('S1001', '2024-03-15', 'John Doe', '3', '$42.50'),
            ('S1002', '2024-03-15', 'Jane Smith', '2', '$28.75'),
            ('S1003', '2024-03-14', 'Robert Johnson', '5', '$89.20'),
            ('S1004', '2024-03-14', 'Sarah Wilson', '1', '$12.50'),
            ('S1005', '2024-03-13', 'Michael Brown', '4', '$64.30'),
        ]
        
        for sale in sales:
            tree.insert('', 'end', values=sale)