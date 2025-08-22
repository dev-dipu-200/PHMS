import tkinter as tk
from tkinter import ttk, messagebox
from utils import fetch_all, execute_query

class SuppliersWindow:
    def __init__(self, root, app):
        self.app = app
        self.root = root
        self.root.title("Suppliers")
        self.root.geometry("750x480")

        top = ttk.Frame(root, padding=8)
        top.pack(fill=tk.BOTH, expand=True)

        toolbar = ttk.Frame(top)
        toolbar.pack(fill=tk.X)
        ttk.Button(toolbar, text="Add", command=self.add).pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="Edit", command=self.edit).pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="Delete", command=self.delete).pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="Refresh", command=self.load).pack(side=tk.LEFT, padx=4)

        self.tree = ttk.Treeview(top, columns=("id","name","contact","phone","email"), show="headings", height=18)
        for c,w in (("id",60),("name",180),("contact",160),("phone",120),("email",180)):
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=w, stretch=True)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.load()

    def load(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        rows = fetch_all("SELECT id, name, contact_person as contact, phone, email FROM suppliers ORDER BY created_at DESC")
        for r in rows:
            self.tree.insert("", tk.END, values=(r["id"], r["name"], r.get("contact",""), r.get("phone",""), r.get("email","")))

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel: return None
        return int(self.tree.item(sel[0], "values")[0])

    def add(self): self._form()
    def edit(self):
        sid = self._selected_id()
        if sid is None: return messagebox.showinfo("Suppliers", "Select a row.")
        self._form(sid)

    def delete(self):
        sid = self._selected_id()
        if sid is None: return messagebox.showinfo("Suppliers", "Select a row.")
        if not messagebox.askyesno("Confirm", "Delete supplier?"): return
        execute_query("DELETE FROM suppliers WHERE id = ?", (sid,))
        self.load()

    def _form(self, sid=None):
        data = {"name":"","contact_person":"","address":"","email":"","phone":""}
        if sid:
            row = fetch_all("SELECT * FROM suppliers WHERE id = ?", (sid,))
            if row: data.update(row[0])

        win = tk.Toplevel(self.root); win.title("Supplier")
        frm = ttk.Frame(win, padding=8); frm.pack(fill=tk.BOTH, expand=True)
        entries = {}
        for i,(lbl,key) in enumerate([("Name","name"),("Contact Person","contact_person"),("Phone","phone"),("Email","email"),("Address","address")]):
            ttk.Label(frm, text=lbl).grid(row=i, column=0, sticky="w", pady=3)
            ent = ttk.Entry(frm); ent.grid(row=i, column=1, sticky="ew", pady=3, padx=6)
            ent.insert(0, data.get(key,"") or ""); entries[key]=ent
        frm.columnconfigure(1, weight=1)

        def save():
            vals = {k: entries[k].get().strip() for k in entries}
            if not vals["name"]:
                return messagebox.showerror("Validation", "Name required")
            if sid:
                execute_query("""
                    UPDATE suppliers SET name=?, contact_person=?, phone=?, email=?, address=? WHERE id=?
                """, (vals["name"], vals["contact_person"], vals["phone"], vals["email"], vals["address"], sid))
            else:
                execute_query("""
                    INSERT INTO suppliers (name, contact_person, phone, email, address)
                    VALUES (?, ?, ?, ?, ?)
                """, (vals["name"], vals["contact_person"], vals["phone"], vals["email"], vals["address"]))
            win.destroy(); self.load()

        btns = ttk.Frame(frm); btns.grid(row=10, column=0, columnspan=2, sticky="e", pady=8)
        ttk.Button(btns, text="Save", command=save).pack(side=tk.RIGHT, padx=4)
        ttk.Button(btns, text="Cancel", command=win.destroy).pack(side=tk.RIGHT)
