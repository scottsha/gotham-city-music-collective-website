from pdfrw import PdfReader, PdfWriter, PageMerge
from reportlab.lib.units import inch

def merge_pages_with_pdfrw(input_pdf_path, output_pdf_path):
    # Read the input PDF
    reader = PdfReader(input_pdf_path)
    pages = reader.pages

    if len(pages) != 2:
        raise ValueError("Input PDF must have exactly two pages.")

    # Page dimensions in points
    full_width = 11 * inch
    height = 8.5 * inch

    # Create a new blank page (11 x 8.5 inches)
    output_page = PageMerge().add()  # Empty canvas

    # Merge first page on the left
    left = PageMerge(pages[0])[0]
    left.x = 0
    left.y = 0
    output_page.add(left)

    # Merge second page on the right
    right = PageMerge(pages[1])[0]
    right.x = 5.5 * inch
    right.y = 0
    output_page.add(right)

    # Finalize merged page
    merged = output_page.render()

    # Write to output PDF
    writer = PdfWriter(output_pdf_path)
    writer.addpage(merged)
    writer.write()


if __name__ == '__main__':
    # Path to the input PDF with two pages
    input_pdf_path = '/home/scott/Programs/gotham-city-music-collective-website/out/gcmc_2025_may_29_program.pdf'
    # Path to the output combined PDF
    output_pdf_path = '/home/scott/Programs/gotham-city-music-collective-website/out/gcmc_2025_may_29_program_to_print.pdf'
    merge_pages_with_pdfrw(input_pdf_path, output_pdf_path)