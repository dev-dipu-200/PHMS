from tkinter import ttk

def set_theme(root):
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Treeview", rowheight=25)
    style.configure("TButton", padding=6)
