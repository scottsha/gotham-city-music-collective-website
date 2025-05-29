import copy
from PyPDF2 import PdfReader, PdfWriter, Transformation
from PyPDF2._page import PageObject
from reportlab.lib.units import inch

def merge_pages_side_by_side(input_pdf_path, output_pdf_path):
    # Define dimensions
    single_width = 5.5 * inch
    height = 8.5 * inch
    double_width = 11 * inch

    # Read input PDF
    reader = PdfReader(input_pdf_path)
    if len(reader.pages) != 2:
        raise ValueError("Input PDF must have exactly two pages.")

    # Get both pages
    page1 = reader.pages[0]
    page2 = reader.pages[1]

    # Create a blank output page
    output_page = PageObject.create_blank_page(width=double_width, height=height)

    # Copy and transform page1
    page1_copy = copy.copy(page1)
    page1_copy.add_transformation(Transformation().translate(tx=0, ty=0))
    output_page.merge_page(page1_copy)

    # Copy and transform page2
    page2_copy = copy.copy(page2)
    page2_copy.add_transformation(Transformation().translate(tx=single_width, ty=0))
    output_page.merge_page(page2_copy)

    # Save to output
    writer = PdfWriter()
    writer.add_page(output_page)
    with open(output_pdf_path, "wb") as f:
        writer.write(f)
# Example usage
if __name__ == '__main__':
    # Path to the input PDF with two pages
    input_pdf_path = '/home/scott/Programs/gotham-city-music-collective-website/out/gcmc_2025_may_29_program.pdf'
    # Path to the output combined PDF
    output_pdf_path = '/home/scott/Programs/gotham-city-music-collective-website/out/gcmc_2025_may_29_program_to_print.pdf'
    merge_pages_side_by_side(input_pdf_path, output_pdf_path)