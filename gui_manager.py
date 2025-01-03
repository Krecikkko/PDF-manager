import tkinter as tk
from tkinter import filedialog, messagebox
from pdf_manager import PDFManager

class GUIManager:
    def __init__(self, root):
        self.root = root
        self.pdf_manager = PDFManager()

        self.root.title("PDF Manager - Merge and Split PDFs")
        self.create_widgets()

    def create_widgets(self):
        """Create GUI elements."""
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Selected Files:").grid(row=0, column=0, padx=5, pady=5)

        self.file_list = tk.Listbox(frame, width=50, height=10)
        self.file_list.grid(row=1, column=0, padx=5, pady=5)

        select_btn = tk.Button(frame, text="Select PDF Files", command=self.select_files)
        select_btn.grid(row=2, column=0, padx=5, pady=5)

        merge_btn = tk.Button(self.root, text="Merge PDFs", command=self.merge_pdfs)
        merge_btn.pack(pady=5)

        split_btn = tk.Button(self.root, text="Split PDF", command=self.split_pdf)
        split_btn.pack(pady=5)

    def select_files(self):
        """Open file dialog to select PDF files."""
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if files:
            self.pdf_manager.files = list(files)
            self.file_list.delete(0, tk.END)  # Clear previous entries
            for file in files:
                self.file_list.insert(tk.END, file)

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

        try:
            # Window for input of page ranges to split
            window = tk.Toplevel()
            window.title("PDF Manager - Merge and Split PDFs")
            self.pdf_manager.split_pdf(input_file, output_dir)
            messagebox.showinfo("Success", f"PDF split successfully. Pages saved in: {output_dir}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
