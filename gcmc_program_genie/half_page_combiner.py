import PyPDF2

# Path to the input PDF with two pages
input_pdf_path = '/home/scott/Downloads/gmcm_2023_oct_13_program_printit.pdf'

# Path to the output combined PDF
output_pdf_path = '/home/scott/Programs/gotham-city-music-collective-website/out/gmcm_2023_oct_13_program_toprint.pdf'

# Create a PDF merger object
pdf_merger = PyPDF2.PdfMerger()

# Open the input PDF
with open(input_pdf_path, 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Extract the two pages from the input PDF
    page1 = pdf_reader.pages[0]

    # Create a new PDF with an 8.5 x 11 page size
    output_pdf = PyPDF2.PdfWriter()
    output_pdf.add_page(page1)
    output_pdf.add_page(page1)

    # Write the output PDF to a file
    with open(output_pdf_path, 'wb') as output_file:
        output_pdf.write(output_file)

print(f'Combined PDF saved to {output_pdf_path}')