import tkinter as tk
from tkinter import ttk, messagebox
from utils import fetch_all, execute_query

class UsersWindow:
    def __init__(self, root, app):
        self.app = app
        self.root = root
        self.root.title("Users")
        self.root.geometry("640x440")

        t = ttk.Frame(root, padding=8); t.pack(fill=tk.BOTH, expand=True)
        bar = ttk.Frame(t); bar.pack(fill=tk.X)
        ttk.Button(bar, text="Add", command=self.add).pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text="Edit", command=self.edit).pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text="Delete", command=self.delete).pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text="Refresh", command=self.load).pack(side=tk.LEFT, padx=4)

        self.tree = ttk.Treeview(t, columns=("id","username","role","created_at"), show="headings", height=16)
        for c,w in (("id",60),("username",160),("role",120),("created_at",180)):
            self.tree.heading(c, text=c.capitalize()); self.tree.column(c, width=w, stretch=True)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.load()

    def load(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        rows = fetch_all("SELECT id, username, role, created_at FROM users ORDER BY created_at DESC")
        for r in rows:
            self.tree.insert("", tk.END, values=(r["id"], r["username"], r["role"], r["created_at"]))

    def _sel(self):
        s = self.tree.selection()
        if not s: return None
        return int(self.tree.item(s[0], "values")[0])

    def add(self): self._form()
    def edit(self):
        uid = self._sel()
        if uid is None: return messagebox.showinfo("Users", "Select a row.")
        self._form(uid)
    def delete(self):
        uid = self._sel()
        if uid is None: return messagebox.showinfo("Users", "Select a row.")
        if not messagebox.askyesno("Confirm","Delete user?"): return
        execute_query("DELETE FROM users WHERE id = ?", (uid,))
        self.load()

    def _form(self, uid=None):
        data = {"username":"","password":"","role":"pharmacist"}
        if uid:
            row = fetch_all("SELECT * FROM users WHERE id = ?", (uid,))
            if row: data.update(row[0]); data["password"] = ""

        win = tk.Toplevel(self.root); win.title("User"); frm = ttk.Frame(win, padding=8); frm.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frm, text="Username").grid(row=0, column=0, sticky="w"); u=tk.StringVar(value=data["username"]); ttk.Entry(frm, textvariable=u).grid(row=0, column=1, sticky="ew", padx=6)
        ttk.Label(frm, text="Password").grid(row=1, column=0, sticky="w"); p=tk.StringVar(value=data["password"]); ttk.Entry(frm, show="*", textvariable=p).grid(row=1, column=1, sticky="ew", padx=6)
        ttk.Label(frm, text="Role").grid(row=2, column=0, sticky="w"); r=tk.StringVar(value=data["role"]); ttk.Combobox(frm, textvariable=r, state="readonly", values=["admin","pharmacist","cashier"]).grid(row=2, column=1, sticky="ew", padx=6)
        frm.columnconfigure(1, weight=1)

        def save():
            if not u.get().strip(): return messagebox.showerror("Validation", "Username required.")
            if uid:
                # Update password only if given
                if p.get().strip():
                    execute_query("UPDATE users SET username=?, password=?, role=? WHERE id=?", (u.get().strip(), p.get().strip(), r.get(), uid))
                else:
                    execute_query("UPDATE users SET username=?, role=? WHERE id=?", (u.get().strip(), r.get(), uid))
            else:
                execute_query("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (u.get().strip(), p.get().strip(), r.get()))
            win.destroy(); self.load()

        btns = ttk.Frame(frm); btns.grid(row=10, column=0, columnspan=2, sticky="e", pady=8)
        ttk.Button(btns, text="Save", command=save).pack(side=tk.RIGHT, padx=4)
        ttk.Button(btns, text="Cancel", command=win.destroy).pack(side=tk.RIGHT)
