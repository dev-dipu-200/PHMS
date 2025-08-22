import tkinter as tk
from tkinter import ttk, messagebox
from utils import fetch_all, execute_query, get_last_bill, get_customer_bills, format_currency

class CustomersWindow:
    def __init__(self, root, app):
        self.app = app
        self.root = root
        self.root.title("Customers")
        self.root.geometry("900x520")

        # Left: list + actions
        left = ttk.Frame(root, padding=8)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        toolbar = ttk.Frame(left)
        toolbar.pack(fill=tk.X)
        ttk.Button(toolbar, text="Add", command=self.add_customer).pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="Edit", command=self.edit_customer).pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="Delete", command=self.delete_customer).pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="Refresh", command=self.load_customers).pack(side=tk.LEFT, padx=4)

        search_frm = ttk.Frame(left)
        search_frm.pack(fill=tk.X, pady=4)
        ttk.Label(search_frm, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        ent = ttk.Entry(search_frm, textvariable=self.search_var)
        ent.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
        ent.bind("<Return>", lambda e: self.load_customers())

        self.tree = ttk.Treeview(left, columns=("id","name","phone","email"), show="headings", height=18)
        for c in ("id","name","phone","email"):
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=120 if c=="id" else 160, stretch=True)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select_customer)

        # Right: last bill
        right = ttk.Frame(root, padding=8)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(right, text="Last Bill (Selected Customer)", style="Header.TLabel").pack(anchor="w")
        self.bill_info = tk.Text(right, height=8)
        self.bill_info.pack(fill=tk.X, pady=6)

        ttk.Label(right, text="Items:").pack(anchor="w")
        self.items = ttk.Treeview(right, columns=("medicine","qty","price","subtotal"), show="headings", height=10)
        for c, w in (("medicine",240), ("qty",60), ("price",90), ("subtotal",100)):
            self.items.heading(c, text=c.capitalize())
            self.items.column(c, width=w, stretch=True)
        self.items.pack(fill=tk.BOTH, expand=True)

        bottom = ttk.Frame(right)
        bottom.pack(fill=tk.X, pady=6)
        ttk.Button(bottom, text="View All Bills", command=self.show_all_bills_dialog).pack(side=tk.RIGHT)

        self.load_customers()

    def load_customers(self):
        q = self.search_var.get().strip()
        if q:
            rows = fetch_all("""
                SELECT id, name, phone, email
                FROM customers
                WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
                ORDER BY created_at DESC
            """, (f"%{q}%", f"%{q}%", f"%{q}%"))
        else:
            rows = fetch_all("SELECT id, name, phone, email FROM customers ORDER BY created_at DESC")

        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in rows:
            self.tree.insert("", tk.END, values=(r["id"], r["name"], r.get("phone",""), r.get("email","")))

        self.clear_bill_preview()

    def get_selected_customer_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        values = self.tree.item(sel[0], "values")
        return int(values[0])

    def on_select_customer(self, _evt=None):
        cid = self.get_selected_customer_id()
        if cid is None:
            self.clear_bill_preview()
            return
        bill = get_last_bill(cid)
        self.render_last_bill(bill)

    def clear_bill_preview(self):
        self.bill_info.delete("1.0", tk.END)
        for i in self.items.get_children():
            self.items.delete(i)

    def render_last_bill(self, bill):
        self.clear_bill_preview()
        if not bill:
            self.bill_info.insert(tk.END, "No bills found for this customer.")
            return
        info = (
            f"Bill ID: {bill['id']}\n"
            f"Date: {bill['bill_date']}\n"
            f"Total: {format_currency(bill['total_amount'])}\n"
            f"Status: {bill['payment_status']}\n"
        )
        self.bill_info.insert(tk.END, info)
        for it in bill["items"]:
            subtotal = float(it["price"]) * int(it["quantity"])
            self.items.insert("", tk.END, values=(
                f"{it['medicine_name']} ({it['medicine_id']})",
                it["quantity"],
                format_currency(it["price"]),
                format_currency(subtotal),
            ))

    def show_all_bills_dialog(self):
        cid = self.get_selected_customer_id()
        if cid is None:
            messagebox.showinfo("Customers", "Please select a customer.")
            return
        bills = get_customer_bills(cid)
        win = tk.Toplevel(self.root)
        win.title("All Bills")
        tree = ttk.Treeview(win, columns=("id","date","total","status"), show="headings", height=15)
        for c,w in (("id",80),("date",160),("total",120),("status",100)):
            tree.heading(c, text=c.capitalize())
            tree.column(c, width=w, stretch=True)
        tree.pack(fill=tk.BOTH, expand=True)
        for b in bills:
            tree.insert("", tk.END, values=(b["id"], b["bill_date"], format_currency(b["total_amount"]), b["payment_status"]))

    # ---------- CRUD ----------
    def add_customer(self):
        self._customer_form_dialog("Add Customer")

    def edit_customer(self):
        cid = self.get_selected_customer_id()
        if cid is None:
            messagebox.showinfo("Customers", "Select a row to edit.")
            return
        self._customer_form_dialog("Edit Customer", cid)

    def delete_customer(self):
        cid = self.get_selected_customer_id()
        if cid is None:
            messagebox.showinfo("Customers", "Select a row to delete.")
            return
        if not messagebox.askyesno("Confirm", "Delete this customer?"):
            return
        execute_query("DELETE FROM customers WHERE id = ?", (cid,))
        self.load_customers()

    def _customer_form_dialog(self, title, cid=None):
        data = {"name":"", "gender":"", "dob":"", "address":"", "email":"", "phone":""}
        if cid:
            row = fetch_all("SELECT * FROM customers WHERE id = ?", (cid,))
            if row:
                data.update(row[0])

        win = tk.Toplevel(self.root)
        win.title(title)
        frm = ttk.Frame(win, padding=8)
        frm.pack(fill=tk.BOTH, expand=True)

        entries = {}
        for i,(label,key) in enumerate([
            ("Name","name"),("Gender","gender"),("DOB (YYYY-MM-DD)","dob"),
            ("Address","address"),("Email","email"),("Phone","phone")
        ]):
            ttk.Label(frm, text=label).grid(row=i, column=0, sticky="w", pady=3)
            ent = ttk.Entry(frm)
            ent.grid(row=i, column=1, sticky="ew", pady=3, padx=5)
            ent.insert(0, data.get(key,"") or "")
            entries[key] = ent
        frm.columnconfigure(1, weight=1)

        def save():
            vals = {k: entries[k].get().strip() for k in entries}
            if not vals["name"]:
                messagebox.showerror("Validation", "Name is required.")
                return
            if cid:
                execute_query("""
                    UPDATE customers
                    SET name=?, gender=?, dob=?, address=?, email=?, phone=?, updated_at=datetime('now','localtime')
                    WHERE id=?
                """, (vals["name"], vals["gender"], vals["dob"], vals["address"], vals["email"], vals["phone"], cid))
            else:
                execute_query("""
                    INSERT INTO customers (name, gender, dob, address, email, phone)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (vals["name"], vals["gender"], vals["dob"], vals["address"], vals["email"], vals["phone"]))
            win.destroy()
            self.load_customers()

        btns = ttk.Frame(frm)
        btns.grid(row=10, column=0, columnspan=2, sticky="e", pady=8)
        ttk.Button(btns, text="Save", command=save).pack(side=tk.RIGHT, padx=4)
        ttk.Button(btns, text="Cancel", command=win.destroy).pack(side=tk.RIGHT)
