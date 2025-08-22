# modules/medicines.py
#!/usr/bin/env python3
import faulthandler
faulthandler.enable()

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime, date

# utils functions: execute_query, fetch_one, fetch_all
from utils import execute_query, fetch_one, fetch_all


class MedicinesWindow:
    def __init__(self, master, app=None):
        self.master = master
        self.app = app
        self.master.title("Medicine Management")
        self.master.geometry("1000x640")
        self.master.minsize(900, 560)
        self.master.configure(bg='#f5f7fb')

        # UI
        self.setup_ui()

        # Data
        try:
            self.seed_if_empty()
            self.load_medicines()
        except Exception as e:
            messagebox.showerror("DB Error", f"Failed to initialize medicines view:\n{e}")

    # -------------------- DB helpers --------------------
    def seed_if_empty(self):
        """Insert sample products if products table is empty."""
        row = fetch_one("SELECT COUNT(*) AS cnt FROM products")
        cnt = 0
        if row and "cnt" in row:
            cnt = int(row["cnt"])
        elif row and len(row) > 0:
            # fallback if row is a tuple-like dict
            cnt = int(list(row.values())[0])
        if cnt == 0:
            sample = [
                ('M001', 'Paracetamol', 'Pain Relief', 5.99, 120, '2026-12-31'),
                ('M002', 'Amoxicillin', 'Antibiotic', 12.50, 45, '2026-10-15'),
                ('M003', 'Vitamin C', 'Supplements', 8.75, 12, '2026-03-20'),
            ]
            try:
                # many=True because we are inserting multiple rows
                execute_query("INSERT OR IGNORE INTO products (id,name,category,product_mrp,expiry) VALUES (?,?,?,?,?,?)",
                              sample, many=True)
            except Exception as e:
                # don't block UI, but inform in console
                print("Seed products failed:", e)

    def get_next_id(self) -> str:
        """Generate next product id like M001, M002..."""
        row = fetch_one("SELECT id FROM products WHERE id LIKE 'M%' "
                        "ORDER BY CAST(SUBSTR(id,2) AS INTEGER) DESC LIMIT 1")
        last_id = None
        if row:
            # row may be dict-like
            if isinstance(row, dict) and "id" in row:
                last_id = row["id"]
            else:
                # fallback: first value
                vals = list(row.values())
                if vals:
                    last_id = vals[0]
        if not last_id:
            return "M001"
        try:
            num = int(last_id[1:]) + 1
        except Exception:
            # fallback if parsing fails
            num = 1
        return f"M{num:03d}"

    # -------------------- UI --------------------
    def setup_ui(self):
        header = ttk.Frame(self.master)
        header.pack(fill='x', padx=12, pady=10)
        ttk.Label(header, text="Medicine Management", font=("TkDefaultFont", 16)).pack(side='left')
        back_btn = ttk.Button(header, text="Back To Main", command=self.master.destroy)
        back_btn.pack(side='right')

        # # Summary (stock analysis)
        # self.summary_label = ttk.Label(self.master, text="", font=("TkDefaultFont", 12), foreground="blue")
        # self.summary_label.pack(fill='x', padx=12, pady=(0, 6))

        # Search and action row
        controls = ttk.Frame(self.master)
        controls.pack(fill='x', padx=12, pady=(0, 8))
        ttk.Label(controls, text="Search:").pack(side='left')
        self.search_entry = ttk.Entry(controls, width=30)
        self.search_entry.pack(side='left', padx=6)
        self.search_entry.bind("<Return>", lambda e: self.search_medicines())
        ttk.Button(controls, text="Search", command=self.search_medicines).pack(side='left', padx=4)
        ttk.Button(controls, text="Clear", command=self.clear_search).pack(side='left', padx=4)
        ttk.Button(controls, text="Add New", command=self.add_medicine_dialog).pack(side='right', padx=4)
        ttk.Button(controls, text="Export CSV", command=self.export_csv).pack(side='right', padx=4)

        # Treeview
        container = ttk.Frame(self.master)
        container.pack(fill='both', expand=True, padx=12, pady=6)

        columns = ('id', 'name', 'category', 'product_mrp', 'expiry')
        self.tree = ttk.Treeview(container, columns=columns, show='headings', selectmode='browse')
        headings = {
            'id': 'ID', 'name': 'Medicine Name', 'category': 'Category',
            'product_mrp': 'MRP', 'expiry': 'Expiry Date'
        }
        for c, h in headings.items():
            self.tree.heading(c, text=h)

        self.tree.column('id', width=80, anchor='center')
        self.tree.column('name', width=260, anchor='w')
        self.tree.column('category', width=160, anchor='w')
        self.tree.column('product_mrp', width=100, anchor='e')
        self.tree.column('expiry', width=120, anchor='center')

        vsb = ttk.Scrollbar(container, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

        self.tree.bind("<Double-1>", lambda e: self.edit_selected())

        # Buttons
        btns = ttk.Frame(self.master)
        btns.pack(fill='x', padx=12, pady=8)
        ttk.Button(btns, text="Edit Selected", command=self.edit_selected).pack(side='left', padx=4)
        ttk.Button(btns, text="Delete Selected", command=self.delete_selected).pack(side='left', padx=4)

    # -------------------- Summary --------------------
    def update_summary(self):
        # Total medicines
        row = fetch_one("SELECT COUNT(*) AS cnt FROM products")
        total = int(row["cnt"]) if row and "cnt" in row else (int(list(row.values())[0]) if row else 0)

        # Expired medicines (expiry < today)
        today = date.today().strftime("%Y-%m-%d")
        row2 = fetch_one("SELECT COUNT(*) AS cnt FROM products WHERE expiry < ?", (today,))
        expired = int(row2["cnt"]) if row2 and "cnt" in row2 else (int(list(row2.values())[0]) if row2 else 0)

        self.summary_label.config(
            text=f"📦 Total Products: {total}   ⏳ Expired: {expired}"
        )

    # -------------------- Data load --------------------
    def load_medicines(self, search_query=""):
        # clear tree
        for r in self.tree.get_children():
            self.tree.delete(r)

        if search_query:
            like = f"%{search_query}%"
            rows = fetch_all("SELECT id,name,category,product_mrp,expiry FROM products "
                             "WHERE name LIKE ? OR category LIKE ? ORDER BY id ASC", (like, like))
        else:
            rows = fetch_all("SELECT id,name,category,product_mrp,expiry FROM products ORDER BY id ASC")

        # rows are list of dicts (fetch_all), but be robust if they're tuples
        for row in rows:
            if isinstance(row, dict):
                display = (row.get("id"), row.get("name"), row.get("category"),
                           f"{float(row.get('product_mrp',0)):.2f}", row.get("expiry"))
            else:
                # assume tuple-like
                display = (row[0], row[1], row[2], f"{float(row[3]):.2f}", row[4], row[5])
            self.tree.insert('', 'end', values=display)

        # update summary
        self.update_summary()

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.load_medicines()

    def search_medicines(self):
        self.load_medicines(self.search_entry.get().strip())

    # -------------------- Dialogs --------------------
    def _center_window(self, win, w=480, h=320):
        win.update_idletasks()
        sw = win.winfo_screenwidth(); sh = win.winfo_screenheight()
        x = (sw - w) // 2; y = (sh - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")

    def _create_form_dialog(self, title, values=None, save_callback=None):
        dialog = tk.Toplevel(self.master)
        dialog.title(title)
        dialog.resizable(True, True)
        self._center_window(dialog, 520, 360)
        dialog.grab_set()

        frame = ttk.Frame(dialog, padding=12)
        frame.pack(fill='both', expand=True)

        labels = ["ID", "Name", "Category", "MRP", "Packing", "Unit", "Expiry (YYYY-MM-DD)"]
        entries = {}
        for i, lbl in enumerate(labels):
            ttk.Label(frame, text=lbl).grid(row=i, column=0, sticky='e', padx=6, pady=6)
            ent = ttk.Entry(frame)
            ent.grid(row=i, column=1, sticky='ew', padx=6, pady=6)
            entries[lbl] = ent
        frame.columnconfigure(1, weight=1)

        # Calendar button (lazy import)
        cal_btn = ttk.Button(frame, text="Calendar", command=lambda: self._open_calendar(dialog, entries[labels[-1]]))
        cal_btn.grid(row=len(labels)-1, column=2, padx=6, pady=6)

        if values:
            # values might be tuple from treeview or dict-like
            if isinstance(values, dict):
                entries["ID"].insert(0, values.get("id"))
                entries["Name"].insert(0, values.get("name"))
                entries["Category"].insert(0, values.get("category"))
                entries["MRP"].insert(0, values.get("product_mrp", 0))
                entries["Expiry (YYYY-MM-DD)"].insert(0, values.get("expiry"))
            else:
                entries["ID"].insert(0, values[0]); entries["ID"].config(state='readonly')
                entries["Name"].insert(0, values[1])
                entries["Category"].insert(0, values[2])
                entries["MRP"].insert(0, values[3])
                entries["Expiry (YYYY-MM-DD)"].insert(0, values[4])
            entries["ID"].config(state='readonly')
        else:
            new_id = self.get_next_id()
            entries["ID"].insert(0, new_id)
            entries["ID"].config(state='readonly')

        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill='x', padx=12, pady=(6,12))
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side='right', padx=6)
        action_text = "Update" if values else "Save"
        ttk.Button(btn_frame, text=action_text, command=lambda: save_callback(entries, dialog)).pack(side='right', padx=6)

        return dialog

    def add_medicine_dialog(self):
        self._create_form_dialog("Add Medicine", values=None, save_callback=self._save_new)

    def edit_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "No item selected")
            return
        vals = self.tree.item(sel[0], 'values')
        # convert to dict for form convenience
        values = {"id": vals[0], "name": vals[1], "category": vals[2],
                  "price": vals[3], "expiry": vals[4],}
        self._create_form_dialog("Edit Medicine", values=values, save_callback=self._update_existing)

    def _open_calendar(self, parent, target_entry):
        try:
            from tkcalendar import Calendar
        except Exception as e:
            messagebox.showerror("Calendar Error", f"tkcalendar not available:\n{e}")
            return

        cal_win = tk.Toplevel(parent)
        cal_win.title("Choose Date")
        cal = Calendar(cal_win, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack(padx=8, pady=8)

        def set_date():
            target_entry.delete(0, tk.END)
            target_entry.insert(0, cal.get_date())
            cal_win.destroy()

        ttk.Button(cal_win, text="OK", command=set_date).pack(pady=6)

    # -------------------- Validation & CRUD --------------------
    def _validate(self, name, category, price_str, expiry_str):
        if not name.strip(): return "Name is required."
        if not category.strip(): return "Category is required."
        try:
            price = float(price_str)
            if price < 0: return "Price must be ≥ 0."
        except Exception:
            return "Price must be a number."
        try:
            datetime.strptime(expiry_str, "%Y-%m-%d")
        except Exception:
            return "Expiry must be in YYYY-MM-DD format."
        return None

    def _save_new(self, entries, dialog):
        med_id = entries["ID"].get()
        name = entries["Name"].get(); category = entries["Category"].get()
        product_mrp = entries["MRP"].get()
        expiry = entries["Expiry (YYYY-MM-DD)"].get()
        err = self._validate(name, category, product_mrp, expiry)
        if err:
            messagebox.showerror("Validation", err)
            return
        try:
            execute_query(
                "INSERT INTO products (id,name,category,product_mrp,expiry) VALUES (?,?,?,?,?,?)",
                (med_id, name.strip(), category.strip(), float(product_mrp), expiry)
            )
            self.load_medicines()
            dialog.destroy()
            messagebox.showinfo("Saved", "Product added successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _update_existing(self, entries, dialog):
        med_id = entries["ID"].get()
        name = entries["Name"].get(); 
        category = entries["Category"].get()
        product_mrp = entries["MRP"].get();
        expiry = entries["Expiry (YYYY-MM-DD)"].get()
        err = self._validate(name, category, product_mrp, expiry)
        if err:
            messagebox.showerror("Validation", err)
            return
        try:
            execute_query(
                "UPDATE products SET name=?, category=?, product_mrp=?, expiry=? WHERE id=?",
                (name.strip(), category.strip(), float(product_mrp), expiry, med_id)
            )
            self.load_medicines()
            dialog.destroy()
            messagebox.showinfo("Updated", "Product updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "No item selected")
            return
        vals = self.tree.item(sel[0], 'values')
        if not messagebox.askyesno("Confirm", f"Delete {vals[1]} ({vals[0]})?"):
            return
        try:
            execute_query("DELETE FROM products WHERE id=?", (vals[0],))
            self.load_medicines()
            messagebox.showinfo("Deleted", "Product deleted.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not file_path:
            return
        try:
            rows = fetch_all("SELECT id,name,category,product_mrp,expiry FROM products ORDER BY id ASC")
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Category", "MRP", "Expiry"])
                for r in rows:
                    # r is dict-like
                    if isinstance(r, dict):
                        writer.writerow([r.get("id"), r.get("name"), r.get("category"),
                                         f"{float(r.get('product_mrp',0)):.2f}", r.get("expiry")])
                    else:
                        writer.writerow([r[0], r[1], r[2], f"{float(r[3]):.2f}", r[4], r[5]])
            messagebox.showinfo("Export", "Exported successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# End of modules/medicines.py
