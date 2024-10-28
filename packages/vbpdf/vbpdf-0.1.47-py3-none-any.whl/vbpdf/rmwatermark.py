import click
from PyPDF2 import PdfReader, PdfWriter


@click.command()
@click.option(
    '-i',
    '--input',
    type=click.Path(exists=True),
    default=None,
    required=True,
    help='Input PDF file'
)
@click.option(
    '-o',
    '--output',
    type=click.Path(),
    default='wmremoved.pdf',
    help='Output PDF file'
)
def rmwatermark(input, output):
    try:
        # Create PDF reader and writer objects
        reader = PdfReader(input)
        writer = PdfWriter()

        # Process each page
        for page in reader.pages:
            # Create a new page without annotations
            new_page = page
            if '/Annots' in new_page:
                del new_page['/Annots']
            writer.add_page(new_page)

        # Save the output PDF
        with open(output, 'wb') as output_file:
            writer.write(output_file)

        print(f"Watermark removed successfully. Output saved to: {output}")

    except Exception as e:
        print(f"Error processing PDF: {str(e)}")


if __name__ == "__main__":
    rmwatermark()
