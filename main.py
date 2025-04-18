import tkinter as tk
from pdf_manager.gui.gui_manager import GUIManager

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUIManager(root)
    root.mainloop()
