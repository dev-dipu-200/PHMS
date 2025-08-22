import tkinter as tk
from tkinter import ttk, messagebox
from utils import fetch_all, create_purchase, format_currency

class PurchasesWindow:
    def __init__(self, root, app):
        self.app = app
        self.root = root
        self.root.title("Purchases (Stock In)")
        self.root.geometry("920x560")

        main = ttk.Frame(root, padding=8); main.pack(fill=tk.BOTH, expand=True)

        # Supplier + notes
        head = ttk.Frame(main); head.pack(fill=tk.X)
        ttk.Label(head, text="Supplier:").pack(side=tk.LEFT)
        self.supplier_var = tk.StringVar()
        self.supplier_cb = ttk.Combobox(head, textvariable=self.supplier_var, state="readonly", width=40)
        self.supplier_cb.pack(side=tk.LEFT, padx=6)

        ttk.Label(head, text="Notes:").pack(side=tk.LEFT, padx=6)
        self.notes_var = tk.StringVar()
        ttk.Entry(head, textvariable=self.notes_var).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Items grid
        ttk.Label(main, text="Items").pack(anchor="w", pady=(8,2))
        self.items = ttk.Treeview(main, columns=("medicine","qty","price","subtotal","mid"), show="headings", height=12)
        for c,w in (("medicine",280),("qty",80),("price",100),("subtotal",120),("mid",1)):
            self.items.heading(c, text=c.capitalize())
            self.items.column(c, width=w, stretch=(c!="mid"))
        self.items.pack(fill=tk.BOTH, expand=True)
        self.items.column("mid", width=1, stretch=False)  # hidden technical column

        buttons = ttk.Frame(main); buttons.pack(fill=tk.X, pady=6)
        ttk.Button(buttons, text="Add Item", command=self.add_item_dialog).pack(side=tk.LEFT)
        ttk.Button(buttons, text="Remove Selected", command=self.remove_selected).pack(side=tk.LEFT, padx=6)
        ttk.Button(buttons, text="Save Purchase", command=self.save_purchase).pack(side=tk.RIGHT)

        self.total_lbl = ttk.Label(main, text="Total: ₹0.00", anchor="e")
        self.total_lbl.pack(fill=tk.X)

        self.load_suppliers()

    def load_suppliers(self):
        rows = fetch_all("SELECT id, name FROM suppliers ORDER BY name")
        self.suppliers = rows
        self.supplier_cb["values"] = [f"{r['id']} - {r['name']}" for r in rows]

    def add_item_dialog(self):
        medicines = fetch_all("SELECT id, name, price FROM medicines ORDER BY name")
        if not medicines:
            return messagebox.showinfo("Purchases", "No medicines found. Add medicines first.")

        win = tk.Toplevel(self.root); win.title("Add Item")
        frm = ttk.Frame(win, padding=8); frm.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frm, text="Medicine:").grid(row=0, column=0, sticky="w")
        med_var = tk.StringVar()
        med_cb = ttk.Combobox(frm, textvariable=med_var, state="readonly", width=40,
                              values=[f"{m['id']} - {m['name']}" for m in medicines])
        med_cb.grid(row=0, column=1, sticky="ew", padx=6)

        ttk.Label(frm, text="Quantity:").grid(row=1, column=0, sticky="w")
        qty_var = tk.StringVar(value="1")
        ttk.Entry(frm, textvariable=qty_var).grid(row=1, column=1, sticky="ew", padx=6)

        ttk.Label(frm, text="Price (per unit):").grid(row=2, column=0, sticky="w")
        price_var = tk.StringVar(value=str(medicines[0]["price"] if medicines else "0"))
        ttk.Entry(frm, textvariable=price_var).grid(row=2, column=1, sticky="ew", padx=6)

        frm.columnconfigure(1, weight=1)

        def add():
            if not med_var.get():
                return messagebox.showerror("Validation", "Select medicine.")
            mid = med_var.get().split(" - ")[0]
            name = next((m["name"] for m in medicines if m["id"] == mid), mid)
            try:
                qty = int(qty_var.get()); price = float(price_var.get())
                if qty <= 0 or price < 0: raise ValueError()
            except Exception:
                return messagebox.showerror("Validation", "Invalid quantity or price.")
            subtotal = qty * price
            self.items.insert("", tk.END, values=(name, qty, f"{price}", f"{subtotal}", mid))
            self.update_total()
            win.destroy()

        btns = ttk.Frame(frm); btns.grid(row=10, column=0, columnspan=2, sticky="e", pady=8)
        ttk.Button(btns, text="Add", command=add).pack(side=tk.RIGHT, padx=4)
        ttk.Button(btns, text="Cancel", command=win.destroy).pack(side=tk.RIGHT)

    def remove_selected(self):
        sel = self.items.selection()
        for s in sel: self.items.delete(s)
        self.update_total()

    def update_total(self):
        total = 0.0
        for iid in self.items.get_children():
            qty = int(self.items.set(iid, "qty")); price = float(self.items.set(iid, "price"))
            total += qty * price
        self.total_lbl.config(text=f"Total: {format_currency(total)}")

    def save_purchase(self):
        if not self.supplier_var.get():
            return messagebox.showerror("Validation", "Select a supplier")
        if not self.items.get_children():
            return messagebox.showerror("Validation", "Add at least one item")

        supplier_id = int(self.supplier_var.get().split(" - ")[0])
        notes = self.notes_var.get().strip()
        items = []
        for iid in self.items.get_children():
            items.append({
                "medicine_id": self.items.set(iid, "mid"),
                "quantity": int(self.items.set(iid, "qty")),
                "price": float(self.items.set(iid, "price"))
            })
        pid = create_purchase(supplier_id, items, notes)
        messagebox.showinfo("Purchases", f"Purchase saved (ID: {pid}). Stock updated.")
        # clear
        for i in self.items.get_children(): self.items.delete(i)
        self.update_total()
