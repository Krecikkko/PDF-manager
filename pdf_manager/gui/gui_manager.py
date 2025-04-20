import tkinter as tk
import os
from tkinter import filedialog, messagebox, ttk
from tkinter.simpledialog import askstring
from pdf_manager.core.pdf_manager import PDFManager

class GUIManager:
    def __init__(self, root):
        self.root = root
        self.pdf_manager = PDFManager()
        self.file_list = [] # File list for storing selected by user files
        self.context_menu = tk.Menu(self.root, tearoff=0)

        self.root.title("PDF Manager")

        # Load icon
        icon_path = os.path.join("assets", "icon.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)

        self.create_widgets()
        self.update_buttons_state()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Selected Files:").pack()
        self.file_list = tk.Listbox(frame, width=70, height=5)
        self.file_list.pack(pady=5)

        # Horizontal frame for the main buttons
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=5)

        # Original and sample buttons
        tk.Button(button_frame, text="Select PDF Files", command=self.select_files).pack(side=tk.LEFT, padx=5)
        self.move_up_button = tk.Button(button_frame, text="Move up", command=self.move_up_selected_file)
        self.move_up_button.pack(side=tk.LEFT, padx=5)

        self.move_down_button = tk.Button(button_frame, text="Move down", command=self.move_down_selected_file)
        self.move_down_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = tk.Button(button_frame, text="Remove", command=self.remove_selected_file)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        # Track selection
        self.file_list.bind("<<ListboxSelect>>", self.update_buttons_state)

        # Notebook for operations
        tab_control = ttk.Notebook(self.root)
        tab_control.pack(expand=1, fill="both", padx=10, pady=10)

        # Merge Tab
        merge_tab = ttk.Frame(tab_control)
        tab_control.add(merge_tab, text="Merge")
        tk.Button(merge_tab, text="Merge PDFs", command=self.merge_pdfs).pack(pady=10)

        # Split Tab
        split_tab = ttk.Frame(tab_control)
        tab_control.add(split_tab, text="Split")
        tk.Button(split_tab, text="Split PDF", command=self.split_pdf).pack(pady=10)

        # Extract Tab
        extract_tab = ttk.Frame(tab_control)
        tab_control.add(extract_tab, text="Extract")

        # Button frame to place buttons horizontally
        extract_button_frame = tk.Frame(extract_tab)
        extract_button_frame.pack(pady=10)

        tk.Button(extract_button_frame, text="Extract PDF", command=self.extract_pdf).pack(side=tk.LEFT, padx=5)
        tk.Button(extract_button_frame, text="Extract text", command=self.extract_txt).pack(side=tk.LEFT, padx=5)
        tk.Button(extract_button_frame, text="Extract images", command=self.extract_img).pack(side=tk.LEFT, padx=5)

        # Protect Tab
        protect_tab = ttk.Frame(tab_control)
        tab_control.add(protect_tab, text="Protect")

        # Button frame to place buttons horizontally
        protect_button_frame = tk.Frame(protect_tab)
        protect_button_frame.pack(pady=10)

        tk.Button(protect_button_frame, text="Protect with password", command=self.password_protect).pack(side=tk.LEFT,
                                                                                                          padx=5)
        tk.Button(protect_button_frame, text="Remove password", command=self.remove_password).pack(side=tk.LEFT,
                                                                                                   padx=5)

    def select_files(self):
        """Open the file dialog to select PDF files."""
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if files:
            self.pdf_manager.files = list(files)
            self.file_list.delete(0, tk.END)  # Clear previous entries
            for file in files:
                self.file_list.insert(tk.END, file)
        self.update_buttons_state()

    def merge_pdfs(self):
        """Handle merging of PDFs."""
        if len(self.pdf_manager.files) < 2:
            messagebox.showwarning("No Files", "Please select at least two PDF files to merge.")
            return
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not output_file:
            return

        try:
            self.pdf_manager.merge_pdfs(output_file)
            messagebox.showinfo("Success", f"PDFs merged successfully into: {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def split_pdf(self):
        """Handle splitting of a PDF."""
        if not self.pdf_manager.files:
            messagebox.showwarning("No File", "Please select a PDF file to split.")
            return
        if len(self.pdf_manager.files) > 1:
            messagebox.showwarning("Single File Required", "Please select only one file to split.")
            return

        input_file = self.pdf_manager.files[0]
        output_dir = filedialog.askdirectory()
        if not output_dir:
            return

        page_range_str = askstring("Page Ranges", "Enter page ranges (e.g., 1-3, 5-10, 11):")
        if not page_range_str:
            return

        try:
            page_range_arr = [item.strip() for item in page_range_str.split(",")]
            for idx, page_range in enumerate(page_range_arr):
                page_ranges = PDFManager.parse_page_ranges(page_range)
                self.pdf_manager.split_pdf(input_file, output_dir, [page_ranges], idx)
            messagebox.showinfo("Success", f"PDF split successfully. Pages saved in: {output_dir}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def extract_pdf(self):
        """Handle extracting of a PDF."""
        if not self.pdf_manager.files:
            messagebox.showwarning("No File", "Please select a PDF file to extract.")
            return
        if len(self.pdf_manager.files) > 1:
            messagebox.showwarning("Single File Required", "Please select only one file to extract.")
            return

        input_file = self.pdf_manager.files[0]
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not output_file:
            return

        page_range_str = askstring("Page Ranges", "Enter page ranges (e.g., 1-3, 5-10, 11):")
        if not page_range_str:
            return

        try:
            page_ranges = PDFManager.parse_page_ranges(page_range_str)
            self.pdf_manager.extract_pdf(input_file, output_file, [page_ranges])
            messagebox.showinfo("Success", f"PDF extract successfully. Pages saved in: {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def extract_txt(self):
        """Handle extracting of a text from a PDF."""
        if not self.pdf_manager.files:
            messagebox.showwarning("No File", "Please select a PDF file to extract text.")
            return
        if len(self.pdf_manager.files) > 1:
            messagebox.showwarning("Single File Required", "Please select only one file to extract text.")
            return

        input_file = self.pdf_manager.files[0]
        output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if not output_file:
            return

        try:
            self.pdf_manager.extract_txt(input_file, output_file)
            messagebox.showinfo("Success", f"Text extracted successfully. Saved in: {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def extract_img(self):
        """Handle extracting of images from a PDF."""
        if not self.pdf_manager.files:
            messagebox.showwarning("No File", "Please select a PDF file to extract images.")
            return
        if len(self.pdf_manager.files) > 1:
            messagebox.showwarning("Single File Required", "Please select only one file to extract images.")
            return

        input_file = self.pdf_manager.files[0]
        output_dir = filedialog.askdirectory()
        if not output_dir:
            return

        try:
            self.pdf_manager.extract_img(input_file, output_dir)
            messagebox.showinfo("Success", f"Image split successfully. Pages saved in: {output_dir}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def password_protect(self):
        """Handle adding password to a PDF."""
        if not self.pdf_manager.files:
            messagebox.showwarning("No File", "Please select a PDF file to secure with a password.")
            return

        input_files = self.pdf_manager.files

        password = askstring("Enter password", "Enter password:")
        if not password:
            return

        try:
            for input_file in input_files:
                self.pdf_manager.password_protect(input_file, password)
            messagebox.showinfo("Success", f"Files protected with password created in the same directory.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def remove_password(self):
        """Handle removing password from a PDF."""
        if not self.pdf_manager.files:
            messagebox.showwarning("No File", "Please select a PDF file to remove password.")
            return

        input_files = self.pdf_manager.files

        password = askstring("Enter password", "Enter current password:")
        if not password:
            return

        try:
            for input_file in input_files:
                self.pdf_manager.remove_password(input_file, password)
            messagebox.showinfo("Success", f"Decrypted PDF(s) saved in the same directory.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


    def show_context_menu(self, event):
        """Show a context menu on right-click."""
        try:
            index = self.file_list.nearest(event.y)
            self.file_list.selection_clear(0, tk.END)
            self.file_list.selection_set(index)
            self.file_list.activate(index)
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def remove_selected_file(self):
        """Remove a selected file from listbox and internal file list."""
        selected_index = self.file_list.curselection()
        if selected_index:
            index = selected_index[0]
            self.file_list.delete(index)
            del self.pdf_manager.files[index]
        self.update_buttons_state()

    def move_up_selected_file(self):
        """Move a selected file up in the list."""
        selected_index = self.file_list.curselection()
        if selected_index:
            index = selected_index[0]
            if index > 0:
                # Swap in the listbox
                item = self.file_list.get(index)
                self.file_list.delete(index)
                self.file_list.insert(index - 1, item)
                self.file_list.select_set(index - 1)

                # Swap in the internal file list
                self.pdf_manager.files[index], self.pdf_manager.files[index - 1] = \
                    self.pdf_manager.files[index - 1], self.pdf_manager.files[index]

    def move_down_selected_file(self):
        """Move a selected file down in the list."""
        selected_index = self.file_list.curselection()
        if selected_index:
            index = selected_index[0]
            if index < self.file_list.size() - 1:
                # Swap in the listbox
                item = self.file_list.get(index)
                self.file_list.delete(index)
                self.file_list.insert(index + 1, item)
                self.file_list.select_set(index + 1)

                # Swap in the internal file list
                self.pdf_manager.files[index], self.pdf_manager.files[index + 1] = \
                    self.pdf_manager.files[index + 1], self.pdf_manager.files[index]

    def update_buttons_state(self, event=None):
        """Enable or disable buttons based on selection."""
        selected = bool(self.file_list.curselection())
        state = tk.NORMAL if selected else tk.DISABLED
        self.move_up_button.config(state=state)
        self.move_down_button.config(state=state)
        self.remove_button.config(state=state)