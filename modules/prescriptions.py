import tkinter as tk
from tkinter import ttk, messagebox
from utils import fetch_all, execute_query

class PrescriptionsWindow:
    def __init__(self, root, app):
        self.app = app
        self.root = root
        self.root.title("Prescriptions")
        self.root.geometry("900x540")

        header = ttk.Frame(root, padding=8); header.pack(fill=tk.X)
        ttk.Label(header, text="Customer:").pack(side=tk.LEFT)
        self.customer_var = tk.StringVar()
        self.customer_cb = ttk.Combobox(header, textvariable=self.customer_var, state="readonly", width=40)
        self.customer_cb.pack(side=tk.LEFT, padx=6)

        ttk.Label(header, text="Doctor:").pack(side=tk.LEFT)
        self.doctor_var = tk.StringVar()
        self.doctor_cb = ttk.Combobox(header, textvariable=self.doctor_var, state="readonly", width=30)
        self.doctor_cb.pack(side=tk.LEFT, padx=6)

        ttk.Label(header, text="Notes:").pack(side=tk.LEFT)
        self.notes_var = tk.StringVar()
        ttk.Entry(header, textvariable=self.notes_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)

        ttk.Label(root, text="Medicines (dosage/duration)").pack(anchor="w", padx=8)
        self.items = ttk.Treeview(root, columns=("medicine","dosage","duration","mid"), show="headings", height=14)
        for c,w in (("medicine",320),("dosage",160),("duration",160),("mid",1)):
            self.items.heading(c, text=c.capitalize()); self.items.column(c, width=w, stretch=(c!="mid"))
        self.items.pack(fill=tk.BOTH, expand=True, padx=8)

        btns = ttk.Frame(root, padding=8); btns.pack(fill=tk.X)
        ttk.Button(btns, text="Add Item", command=self.add_item_dialog).pack(side=tk.LEFT)
        ttk.Button(btns, text="Remove", command=self.remove_selected).pack(side=tk.LEFT, padx=6)
        ttk.Button(btns, text="Save Prescription", command=self.save_rx).pack(side=tk.RIGHT)

        self.load_refs()

    def load_refs(self):
        customers = fetch_all("SELECT id, name FROM customers ORDER BY name")
        doctors = fetch_all("SELECT id, name FROM doctors ORDER BY name")
        self.customer_cb["values"] = [f"{c['id']} - {c['name']}" for c in customers]
        self.doctor_cb["values"] = [f"{d['id']} - {d['name']}" for d in doctors]
        self.medicines = fetch_all("SELECT id, name FROM medicines ORDER BY name")

    def add_item_dialog(self):
        if not self.medicines:
            return messagebox.showinfo("Prescriptions", "No medicines available.")
        win = tk.Toplevel(self.root); win.title("Add RX Item")
        frm = ttk.Frame(win, padding=8); frm.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frm, text="Medicine:").grid(row=0, column=0, sticky="w")
        med_var = tk.StringVar()
        med_cb = ttk.Combobox(frm, textvariable=med_var, state="readonly", width=40,
                              values=[f"{m['id']} - {m['name']}" for m in self.medicines])
        med_cb.grid(row=0, column=1, sticky="ew", padx=6)

        ttk.Label(frm, text="Dosage:").grid(row=1, column=0, sticky="w")
        dose_var = tk.StringVar(); ttk.Entry(frm, textvariable=dose_var).grid(row=1, column=1, sticky="ew", padx=6)

        ttk.Label(frm, text="Duration:").grid(row=2, column=0, sticky="w")
        dur_var = tk.StringVar(); ttk.Entry(frm, textvariable=dur_var).grid(row=2, column=1, sticky="ew", padx=6)

        frm.columnconfigure(1, weight=1)

        def add():
            if not med_var.get(): return messagebox.showerror("Validation", "Select medicine.")
            mid = med_var.get().split(" - ")[0]
            name = next((m["name"] for m in self.medicines if m["id"] == mid), mid)
            self.items.insert("", tk.END, values=(name, dose_var.get().strip(), dur_var.get().strip(), mid))
            win.destroy()

        btns = ttk.Frame(frm); btns.grid(row=10, column=0, columnspan=2, sticky="e", pady=8)
        ttk.Button(btns, text="Add", command=add).pack(side=tk.RIGHT, padx=4)
        ttk.Button(btns, text="Cancel", command=win.destroy).pack(side=tk.RIGHT)

    def remove_selected(self):
        sel = self.items.selection()
        for s in sel: self.items.delete(s)

    def save_rx(self):
        if not self.customer_var.get(): return messagebox.showerror("Validation", "Select customer")
        cid = int(self.customer_var.get().split(" - ")[0])
        did = None
        if self.doctor_var.get():
            did = int(self.doctor_var.get().split(" - ")[0])
        notes = self.notes_var.get().strip()

        rx_id = execute_query("INSERT INTO prescriptions (customer_id, doctor_id, notes) VALUES (?, ?, ?)",
                              (cid, did, notes))
        rows = []
        for iid in self.items.get_children():
            rows.append((
                rx_id, self.items.set(iid, "mid"),
                self.items.set(iid, "dosage"),
                self.items.set(iid, "duration")
            ))
        if rows:
            execute_query("""
                INSERT INTO prescription_items (prescription_id, medicine_id, dosage, duration)
                VALUES (?, ?, ?, ?)
            """, params=rows, many=True)
        messagebox.showinfo("Prescriptions", f"Saved prescription #{rx_id}")
        for i in self.items.get_children(): self.items.delete(i)
