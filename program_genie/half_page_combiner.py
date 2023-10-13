import PyPDF2

# Path to the input PDF with two pages
input_pdf_path = '/public_html/wp-content/uploads/concert_programs/gmcm_2023_oct_13_program.pdf'

# Path to the output combined PDF
output_pdf_path = '/home/scott/Programs/gotham-city-music-collective-website/out/gmcm_2023_oct_13_program_toprint.pdf'

# Create a PDF merger object
pdf_merger = PyPDF2.PdfMerger()

# Open the input PDF
with open(input_pdf_path, 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Extract the two pages from the input PDF
    page1 = pdf_reader.pages[0]
    page2 = pdf_reader.pages[1]

    # Create a new PDF with an 8.5 x 11 page size
    output_pdf = PyPDF2.PdfWriter()
    PyPDF2.PageObject.create_blank_page(output_pdf, width = 8.5 * 72, height = 11 * 72)

    # Merge the two pages onto the new PDF
    output_pdf.pages[0].mergeTranslatedPage(page1, 0, 11 * 72)
    output_pdf.pages[0].mergeTranslatedPage(page2, 0, 0)

    # Write the output PDF to a file
    with open(output_pdf_path, 'wb') as output_file:
        output_pdf.write(output_file)

print(f'Combined PDF saved to {output_pdf_path}')