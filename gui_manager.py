import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.simpledialog import askstring  # Import askstring from simpledialog
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

        merge_btn = tk.Button(self.root, text="Split PDF", command=self.split_pdf)
        merge_btn.pack(pady=5)

        split_btn = tk.Button(self.root, text="Extract PDF", command=self.extract_pdf)
        split_btn.pack(pady=5)

        extract_txt_btn = tk.Button(self.root, text="Extract txt", command=self.extract_txt)
        extract_txt_btn.pack(pady=5)

        extract_img_btn = tk.Button(self.root, text="Extract images", command=self.extract_img)
        extract_img_btn.pack(pady=5)

        password_protect_btn = tk.Button(self.root, text="Protect with password", command=self.password_protect)
        password_protect_btn.pack(pady=5)

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
