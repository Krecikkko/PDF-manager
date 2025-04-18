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

    def split_pdf(self, input_file, output_dir, page_ranges, file_name_suffix):
        """Split the PDF based on the given page ranges."""
        reader = PdfReader(input_file)
        for page_range in page_ranges:
            writer = PdfWriter()
            for page in page_range:
                writer.add_page(reader.pages[page])
            output_path = f"{output_dir}/split_{file_name_suffix}.pdf"
            with open(output_path, "wb") as output_file:
                writer.write(output_file)

    def extract_pdf(self, input_file, output_file, page_ranges):
        """Extract pages from the PDF based on the given page ranges."""
        reader = PdfReader(input_file)
        for idx, page_range in enumerate(page_ranges):
            writer = PdfWriter()
            for page in page_range:
                writer.add_page(reader.pages[page])
            writer.write(output_file)
            writer.close()

    def extract_txt(self, input_file, output_file):
        reader = PdfReader(input_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        with open(output_file, "w") as f:
            f.write(text)

    def extract_img(self, input_file, output_dir):
        reader = PdfReader(input_file)
        idx = 0
        for page in  reader.pages:
            for image in page.images:
                with open(f"{output_dir}/image_{idx}.jpg", "wb") as f:
                    f.write(image.data)
                    idx += 1

    def password_protect(self, input_file, password):
        reader = PdfReader(input_file)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(password)
        output_file = input_file.replace(".pdf", "_encrypted.pdf")
        with open(output_file, "wb") as f:
            writer.write(f)

    @staticmethod
    def parse_page_ranges(page_range_str):
        """Parse a page range string like '1-3,5-7' into a list of page ranges."""
        ranges = []
        for part in page_range_str.split(","):
            if "-" in part:
                start, end = map(int, part.split("-"))
                ranges.extend(range(start - 1, end))  # Convert to zero-based index
            else:
                ranges.append(int(part) - 1)  # Convert to zero-based index
        return ranges
