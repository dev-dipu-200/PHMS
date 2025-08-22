import tkinter as tk
from tkinter import ttk, messagebox
from utils import fetch_all, record_payment, format_currency

class PaymentsWindow:
    def __init__(self, root, app):
        self.app = app
        self.root = root
        self.root.title("Payments")
        self.root.geometry("720x420")

        top = ttk.Frame(root, padding=8); top.pack(fill=tk.X)
        ttk.Label(top, text="Bill:").pack(side=tk.LEFT)
        self.bill_var = tk.StringVar()
        self.bill_cb = ttk.Combobox(top, textvariable=self.bill_var, state="readonly", width=50)
        self.bill_cb.pack(side=tk.LEFT, padx=6)

        ttk.Label(top, text="Amount:").pack(side=tk.LEFT, padx=(12,4))
        self.amount_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.amount_var, width=12).pack(side=tk.LEFT)

        ttk.Label(top, text="Method:").pack(side=tk.LEFT, padx=(12,4))
        self.method_var = tk.StringVar(value="cash")
        self.method_cb = ttk.Combobox(top, textvariable=self.method_var, state="readonly",
                                      values=["cash","card","upi","insurance"], width=12)
        self.method_cb.pack(side=tk.LEFT)

        ttk.Label(top, text="Ref:").pack(side=tk.LEFT, padx=(12,4))
        self.ref_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.ref_var, width=16).pack(side=tk.LEFT)

        ttk.Button(top, text="Record Payment", command=self.save_payment).pack(side=tk.RIGHT)

        self.tree = ttk.Treeview(root, columns=("id","bill","amount","method","date","ref"), show="headings", height=14)
        for c,w in (("id",60),("bill",80),("amount",100),("method",100),("date",160),("ref",140)):
            self.tree.heading(c, text=c.capitalize()); self.tree.column(c, width=w, stretch=True)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.load_bills(); self.load_payments()

    def load_bills(self):
        rows = fetch_all("""
            SELECT id, bill_date, total_amount, payment_status FROM bills ORDER BY bill_date DESC, id DESC LIMIT 200
        """)
        self.bill_cb["values"] = [f"{r['id']} - {r['bill_date']} - {format_currency(r['total_amount'])} ({r['payment_status']})" for r in rows]

    def load_payments(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        rows = fetch_all("SELECT id, bill_id as bill, amount, method, payment_date as date, reference as ref FROM payments ORDER BY payment_date DESC")
        for r in rows:
            self.tree.insert("", tk.END, values=(r["id"], r["bill"], format_currency(r["amount"]), r["method"], r["date"], r.get("ref","")))

    def save_payment(self):
        if not self.bill_var.get(): return messagebox.showerror("Validation", "Select a bill")
        try:
            amount = float(self.amount_var.get())
            if amount <= 0: raise ValueError()
        except Exception:
            return messagebox.showerror("Validation", "Invalid amount.")
        bill_id = int(self.bill_var.get().split(" - ")[0])
        pid = record_payment(bill_id, amount, self.method_var.get(), self.ref_var.get().strip())
        messagebox.showinfo("Payments", f"Payment #{pid} recorded.")
        self.amount_var.set(""); self.ref_var.set("")
        self.load_bills(); self.load_payments()
