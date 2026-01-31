from pdfrw import PdfReader, PdfWriter, PageMerge, PdfDict
from reportlab.lib.units import inch

def merge_pages_with_pdfrw(input_pdf_path, output_pdf_path):
    reader = PdfReader(input_pdf_path)
    pages = reader.pages

    if len(pages) != 2:
        raise ValueError("Input PDF must have exactly two pages.")

    # Page dimensions (letter landscape: 11 x 8.5 inches)
    full_width = 11 * inch
    height = 8.5 * inch

    # Create a blank page using a PDF dictionary
    blank_page = PdfDict(
        Type="/Page",
        MediaBox=[0, 0, full_width, height],
        Contents=[],
        Resources=PdfDict()
    )

    # Start merging into this blank page
    merger = PageMerge(blank_page)

    # Left page
    left = PageMerge().add(pages[0])[0]
    left.x = 0
    left.y = 0
    merger.add(left)

    # Right page
    right = PageMerge().add(pages[1])[0]
    right.x = 5.5 * inch
    right.y = 0
    merger.add(right)

    # Render finished page
    merger.render()

    # Write output
    writer = PdfWriter()
    writer.addpage(blank_page)
    writer.write(output_pdf_path)


if __name__ == '__main__':
    # Path to the input PDF with two pages
    input_pdf_path = '/home/scott/Programs/gotham-city-music-collective-website/out/gcmc_2025_nov_14_program_v4.pdf'
    # Path to the output combined PDF
    output_pdf_path = '/home/scott/Programs/gotham-city-music-collective-website/out/gcmc_2025_nov_14_program_v4_to_print.pdf'
    merge_pages_with_pdfrw(input_pdf_path, output_pdf_path)