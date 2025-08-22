# modules/medicines.py
#!/usr/bin/env python3
import faulthandler
faulthandler.enable()

import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime, date

from utils import execute_query, fetch_one, fetch_all


class MedicinesWindow:
    def __init__(self, master, app=None):
        self.master = master
        self.app = app
        self.master.title("Medicine Management")
        self.master.geometry("1000x640")
        self.master.minsize(900, 560)
        ctk.set_appearance_mode("light")

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
        row = fetch_one("SELECT COUNT(*) AS cnt FROM products")
        cnt = int(row["cnt"]) if row and "cnt" in row else (int(list(row.values())[0]) if row else 0)
        if cnt == 0:
            sample = [
                ('M001', 'Paracetamol', 'Pain Relief', 5.99, '2026-12-31'),
                ('M002', 'Amoxicillin', 'Antibiotic', 12.50, '2026-10-15'),
                ('M003', 'Vitamin C', 'Supplements', 8.75, '2026-03-20'),
            ]
            try:
                execute_query(
                    "INSERT OR IGNORE INTO products (id,name,category,product_mrp,product_expiry) VALUES (?,?,?,?,?)",
                    sample, many=True
                )
            except Exception as e:
                print("Seed products failed:", e)

    def get_next_id(self) -> str:
        row = fetch_one("SELECT id FROM products WHERE id LIKE 'M%' "
                        "ORDER BY CAST(SUBSTR(id,2) AS INTEGER) DESC LIMIT 1")
        last_id = None
        if row:
            last_id = row.get("id") if isinstance(row, dict) else list(row.values())[0]
        if not last_id:
            return "M001"
        try:
            num = int(last_id[1:]) + 1
        except Exception:
            num = 1
        return f"M{num:03d}"

    # -------------------- UI --------------------
    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self.master, fg_color="transparent")
        header.pack(fill='x', padx=12, pady=10)

        ctk.CTkLabel(header, text="💊 Medicine Management",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(side='left')
        ctk.CTkButton(header, text="Back To Main", command=self.master.destroy).pack(side='right')

        # Controls
        controls = ctk.CTkFrame(self.master, fg_color="transparent")
        controls.pack(fill='x', padx=12, pady=(0, 8))

        ctk.CTkLabel(controls, text="Search:").pack(side='left')
        self.search_entry = ctk.CTkEntry(controls, width=200, placeholder_text="Name or Category")
        self.search_entry.pack(side='left', padx=6)
        self.search_entry.bind("<Return>", lambda e: self.search_medicines())
        ctk.CTkButton(controls, text="Search", command=self.search_medicines).pack(side='left', padx=4)
        ctk.CTkButton(controls, text="Clear", command=self.clear_search).pack(side='left', padx=4)
        ctk.CTkButton(controls, text="Add New", command=self.add_medicine_dialog).pack(side='right', padx=4)
        ctk.CTkButton(controls, text="Export CSV", command=self.export_csv).pack(side='right', padx=4)

        # Table container
        container = ctk.CTkFrame(self.master)
        container.pack(fill='both', expand=True, padx=12, pady=6)

        columns = ('id', 'name', 'category', 'product_mrp', 'product_expiry')
        self.tree = ttk.Treeview(container, columns=columns, show='headings', selectmode='browse')
        headings = {
            'id': 'ID', 'name': 'Medicine Name', 'category': 'Category',
            'product_mrp': 'MRP', 'product_expiry': 'Expiry Date'
        }
        for c, h in headings.items():
            self.tree.heading(c, text=h)

        self.tree.column('id', width=80, anchor='center')
        self.tree.column('name', width=260, anchor='w')
        self.tree.column('category', width=160, anchor='w')
        self.tree.column('product_mrp', width=100, anchor='e')
        self.tree.column('product_expiry', width=120, anchor='center')

        vsb = ttk.Scrollbar(container, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

        self.tree.bind("<Double-1>", lambda e: self.edit_selected())

        # Buttons
        btns = ctk.CTkFrame(self.master, fg_color="transparent")
        btns.pack(fill='x', padx=12, pady=8)
        ctk.CTkButton(btns, text="Edit Selected", command=self.edit_selected).pack(side='left', padx=4)
        ctk.CTkButton(btns, text="Delete Selected", command=self.delete_selected).pack(side='left', padx=4)

    # -------------------- Data load --------------------
    def load_medicines(self, search_query=""):
        self.tree.delete(*self.tree.get_children())
        if search_query:
            like = f"%{search_query}%"
            rows = fetch_all(
                "SELECT id,name,category,product_mrp,product_expiry FROM products "
                "WHERE name LIKE ? OR category LIKE ? ORDER BY id ASC", (like, like)
            )
        else:
            rows = fetch_all("SELECT id,name,category,product_mrp,product_expiry FROM products ORDER BY id ASC")

        for row in rows:
            if isinstance(row, dict):
                display = (row.get("id"), row.get("name"), row.get("category"),
                           f"{float(row.get('product_mrp',0)):.2f}", row.get("product_expiry"))
            else:
                display = (row[0], row[1], row[2], f"{float(row[3]):.2f}", row[4])
            self.tree.insert('', 'end', values=display)

    def clear_search(self):
        self.search_entry.delete(0, 'end')
        self.load_medicines()

    def search_medicines(self):
        self.load_medicines(self.search_entry.get().strip())

    # -------------------- Dialogs --------------------
    def _create_form_dialog(self, title, values=None, save_callback=None):
        dialog = ctk.CTkToplevel(self.master)
        dialog.title(title)
        dialog.geometry("500x350")
        # dialog.grab_set()

        frame = ctk.CTkFrame(dialog)
        frame.pack(fill='both', expand=True, padx=12, pady=12)

        labels = ["ID", "Name", "Category", "MRP", "Expiry"]
        entries = {}
        for i, lbl in enumerate(labels):
            ctk.CTkLabel(frame, text=lbl).grid(row=i, column=0, sticky='e', padx=6, pady=6)
            ent = ctk.CTkEntry(frame)
            ent.grid(row=i, column=1, sticky='ew', padx=6, pady=6)
            entries[lbl] = ent
        frame.columnconfigure(1, weight=1)

        if values:
            entries["ID"].insert(0, values["id"]); entries["ID"].configure(state="disabled")
            entries["Name"].insert(0, values["name"])
            entries["Category"].insert(0, values["category"])
            entries["MRP"].insert(0, values["product_mrp"])
            entries["Expiry"].insert(0, values["product_expiry"])
        else:
            new_id = self.get_next_id()
            entries["ID"].insert(0, new_id)
            entries["ID"].configure(state="disabled")

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(fill='x', padx=12, pady=(6,12))
        ctk.CTkButton(btn_frame, text="Cancel", command=dialog.destroy).pack(side='right', padx=6)
        action_text = "Update" if values else "Save"
        ctk.CTkButton(btn_frame, text=action_text,
                      command=lambda: save_callback(entries, dialog)).pack(side='right', padx=6)

    def add_medicine_dialog(self):
        self._create_form_dialog("Add Medicine", save_callback=self._save_new)

    def edit_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "No item selected")
            return
        vals = self.tree.item(sel[0], 'values')
        values = {"id": vals[0], "name": vals[1], "category": vals[2],
                  "product_mrp": vals[3], "product_expiry": vals[4]}
        self._create_form_dialog("Edit Medicine", values=values, save_callback=self._update_existing)

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
        name = entries["Name"].get()
        category = entries["Category"].get()
        product_mrp = entries["MRP"].get()
        product_expiry = entries["Expiry (YYYY-MM-DD)"].get()
        err = self._validate(name, category, product_mrp, product_expiry)
        if err:
            messagebox.showerror("Validation", err)
            return
        try:
            execute_query(
                "INSERT INTO products (id,name,category,product_mrp,product_expiry) VALUES (?,?,?,?,?)",
                (med_id, name.strip(), category.strip(), float(product_mrp), product_expiry)
            )
            self.load_medicines()
            dialog.destroy()
            messagebox.showinfo("Saved", "Product added successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _update_existing(self, entries, dialog):
        med_id = entries["ID"].get()
        name = entries["Name"].get()
        category = entries["Category"].get()
        product_mrp = entries["MRP"].get()
        product_expiry = entries["Expiry (YYYY-MM-DD)"].get()
        err = self._validate(name, category, product_mrp, product_expiry)
        if err:
            messagebox.showerror("Validation", err)
            return
        try:
            execute_query(
                "UPDATE products SET name=?, category=?, product_mrp=?, product_expiry=? WHERE id=?",
                (name.strip(), category.strip(), float(product_mrp), product_expiry, med_id)
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
            rows = fetch_all("SELECT id,name,category,product_mrp,product_expiry FROM products ORDER BY id ASC")
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Category", "MRP", "Expiry"])
                for r in rows:
                    if isinstance(r, dict):
                        writer.writerow([r.get("id"), r.get("name"), r.get("category"),
                                         f"{float(r.get('product_mrp',0)):.2f}", r.get("product_expiry")])
                    else:
                        writer.writerow([r[0], r[1], r[2], f"{float(r[3]):.2f}", r[4]])
            messagebox.showinfo("Export", "Exported successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
