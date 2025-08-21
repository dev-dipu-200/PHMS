from tkinter import ttk, messagebox, scrolledtext
from tkinter import font as tkfont
from datetime import datetime, timedelta

class ReportsWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.master.title("Reports & Analytics")
        self.master.geometry("900x600")
        self.master.configure(bg='#f5f5f5')
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header_frame = ttk.Frame(self.master)
        header_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(header_frame, text="Reports & Analytics", 
                 font=tkfont.Font(family="Helvetica", size=16, weight="bold")).pack(side='left')
        
        # Back button
        back_btn = ttk.Button(header_frame, text="Back to Main", command=self.master.destroy)
        back_btn.pack(side='right')
        
        # Report selection frame
        report_frame = ttk.Frame(self.master)
        report_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(report_frame, text="Select Report:").pack(side='left')
        
        report_combo = ttk.Combobox(report_frame, width=20, state='readonly')
        report_combo.pack(side='left', padx=5)
        report_combo['values'] = (
            'Sales Report', 
            'Inventory Report', 
            'Expiry Report', 
            'Customer Sales', 
            'Top Selling Items'
        )
        report_combo.set('Sales Report')
        
        ttk.Label(report_frame, text="Date Range:").pack(side='left', padx=(20, 5))
        
        start_date = ttk.Entry(report_frame, width=12)
        start_date.pack(side='left', padx=5)
        start_date.insert(0, "2024-01-01")
        
        ttk.Label(report_frame, text="to").pack(side='left', padx=5)
        
        end_date = ttk.Entry(report_frame, width=12)
        end_date.pack(side='left', padx=5)
        end_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        generate_btn = ttk.Button(report_frame, text="Generate Report", style='Primary.TButton')
        generate_btn.pack(side='left', padx=10)
        
        export_btn = ttk.Button(report_frame, text="Export to PDF")
        export_btn.pack(side='right')
        
        # Report display area
        report_display = scrolledtext.ScrolledText(self.master, width=80, height=20)
        report_display.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Sample report content
        report_content = """
                                SALES REPORT
                                ============
        
        Period: 2024-01-01 to 2024-03-15
        
        Summary:
        - Total Sales: $12,580.00
        - Number of Transactions: 248
        - Average Transaction Value: $50.73
        - Most Sold Item: Paracetamol (320 units)
        
        Daily Sales Breakdown:
        Date          Sales     Transactions
        2024-03-15    $1,240.00   24
        2024-03-14    $1,180.50   22
        2024-03-13    $1,050.75   20
        2024-03-12    $980.25     19
        
        Category Performance:
        Category          Sales      % of Total
        Pain Relief       $4,520.00   35.9%
        Antibiotics       $3,150.00   25.0%
        Supplements       $1,880.00   14.9%
        Digestive         $1,250.00   9.9%
        Allergy           $980.00     7.8%
        Diabetes          $800.00     6.4%
        
        Top Selling Items:
        Item            Units Sold   Revenue
        Paracetamol     320          $1,920.00
        Amoxicillin     215          $2,687.50
        Vitamin C       180          $1,575.00
        Ibuprofen       175          $1,093.75
        Omeprazole      120          $1,836.00
        """
        
        report_display.insert('1.0', report_content)
        report_display.config(state='disabled')  # Make it read-only