import click
from PyPDF2 import PdfReader, PdfWriter

from PyPDF2.generic import ContentStream, NameObject, TextStringObject


def remove_watermarks(input_file, output_file):
    # Load PDF into pyPDF
    reader = PdfReader(input_file)
    writer = PdfWriter()

    for page in reader.pages:
        # Get the current page's contents
        content_object = page["/Contents"]
        content = ContentStream(content_object, reader)

        # Loop over all pdf elements
        for operands, operator in content.operations:
            # Handle both TJ and Tj operators (different text rendering methods)
            if operator == b"TJ":
                for i in range(len(operands[0])):
                    if isinstance(operands[0][i], TextStringObject):
                        operands[0][i] = TextStringObject('')
            elif operator == b"Tj":
                if isinstance(operands[0], TextStringObject):
                    operands[0] = TextStringObject('')

        # Set the modified content as content object on the page
        page.__setitem__(NameObject("/Contents"), content)

        # Add the page to the output
        writer.add_page(page)

    # Write the stream
    with open(output_file, "wb") as fh:
        writer.write(fh)


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
        remove_watermarks(input, output)
        print(f"Watermarks removed successfully. Output saved to: {output}")
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")


if __name__ == "__main__":
    rmwatermark()
