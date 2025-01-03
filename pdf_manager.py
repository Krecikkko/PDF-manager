from PyPDF2 import PdfMerger, PdfReader, PdfWriter


class PDFManager:
    def __init__(self):
        self.files = []

    def merge_pdfs(self, output_file):
        """Merge the selected PDF files into a single output file."""
        if len(self.files) < 2:
            raise ValueError("At least two PDF files are required to merge.")
        merger = PdfMerger()
        for file in self.files:
            merger.append(file)
        merger.write(output_file)
        merger.close()

    def split_pdfs(self, input_file, output_dir):
        """Split the selected PDF files into separate PDF files."""
        reader = PdfReader(input_file)
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            output_path = f"{output_dir}/page_{i+1}.pdf"
