import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from tkinter import font as tkfont
import csv

class InventoryWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.master.title("Inventory Management")
        self.master.geometry("950x600")
        self.master.configure(bg='#f5f5f5')

        self.inventory = [
            ('M001', 'Paracetamol', 'Pain Relief', 120, 20, '✅ In Stock'),
            ('M002', 'Amoxicillin', 'Antibiotic', 45, 30, '✅ In Stock'),
            ('M003', 'Vitamin C', 'Supplements', 12, 15, '⚠️ Low Stock'),
            ('M004', 'Ibuprofen', 'Pain Relief', 80, 20, '✅ In Stock'),
            ('M005', 'Omeprazole', 'Digestive', 60, 25, '✅ In Stock'),
            ('M006', 'Aspirin', 'Pain Relief', 200, 30, '✅ In Stock'),
            ('M007', 'Loratadine', 'Allergy', 30, 20, '✅ In Stock'),
            ('M008', 'Metformin', 'Diabetes', 25, 30, '⚠️ Low Stock'),
            ('M009', 'Atorvastatin', 'Cholesterol', 18, 15, '⚠️ Low Stock'),
        ]

        self.setup_ui()

    def setup_ui(self):
        # --- Header ---
        header_frame = ttk.Frame(self.master)
        header_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(
            header_frame,
            text="💊 Inventory Management",
            font=tkfont.Font(family="Helvetica", size=18, weight="bold"),
        ).pack(side='left')

        ttk.Button(header_frame, text="Back to Main", command=self.master.destroy).pack(side='right')

        # --- Treeview ---
        tree_frame = ttk.Frame(self.master)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)

        columns = ('id', 'name', 'category', 'stock', 'min_stock', 'status')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)

        for col in columns:
            self.tree.heading(col, text=col.title())

        self.tree.column('id', width=70, anchor='center')
        self.tree.column('name', width=220)
        self.tree.column('category', width=150)
        self.tree.column('stock', width=110, anchor='center')
        self.tree.column('min_stock', width=110, anchor='center')
        self.tree.column('status', width=120, anchor='center')

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Style
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 11), rowheight=28)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        self.refresh_tree()

        # --- Action Buttons ---
        action_frame = ttk.Frame(self.master)
        action_frame.pack(fill='x', padx=20, pady=10)

        ttk.Button(action_frame, text="➕ Add New Item", command=self.add_item).pack(side='left', padx=5)
        ttk.Button(action_frame, text="✏️ Update Stock", command=self.update_stock).pack(side='left', padx=5)
        ttk.Button(action_frame, text="📤 Export Inventory", command=self.export_inventory).pack(side='right', padx=5)

    def refresh_tree(self):
        """Refresh TreeView with current inventory"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in self.inventory:
            tag = "low" if "⚠️" in item[5] else "ok"
            self.tree.insert('', 'end', values=item, tags=(tag,))

        # Color coding
        self.tree.tag_configure("low", background="#ffe6e6", foreground="#e74c3c")
        self.tree.tag_configure("ok", background="#eaffea", foreground="#2ecc71")

    def add_item(self):
        """Add new inventory item"""
        id_ = simpledialog.askstring("Add Item", "Enter Item ID:")
        if not id_:
            return
        name = simpledialog.askstring("Add Item", "Enter Medicine Name:")
        category = simpledialog.askstring("Add Item", "Enter Category:")
        try:
            stock = int(simpledialog.askstring("Add Item", "Enter Stock Quantity:"))
            min_stock = int(simpledialog.askstring("Add Item", "Enter Minimum Stock:"))
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Invalid stock or minimum stock value")
            return

        status = "⚠️ Low Stock" if stock < min_stock else "✅ In Stock"
        self.inventory.append((id_, name, category, stock, min_stock, status))
        self.refresh_tree()

    def update_stock(self):
        """Update stock for selected item"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Update Stock", "Please select an item first.")
            return

        item_values = self.tree.item(selected[0], 'values')
        new_stock = simpledialog.askinteger("Update Stock", f"Enter new stock for {item_values[1]}:", initialvalue=item_values[3])

        if new_stock is not None:
            min_stock = int(item_values[4])
            status = "⚠️ Low Stock" if new_stock < min_stock else "✅ In Stock"

            # Update inventory list
            for i, item in enumerate(self.inventory):
                if item[0] == item_values[0]:
                    self.inventory[i] = (item[0], item[1], item[2], new_stock, min_stock, status)
                    break
            self.refresh_tree()

    def export_inventory(self):
        """Export inventory data to CSV"""
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files","*.csv")])
        if file_path:
            with open(file_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Category", "Stock", "Min Stock", "Status"])
                for row in self.inventory:
                    writer.writerow(row)
            messagebox.showinfo("Export Successful", f"Inventory exported to {file_path}")

