import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.lib.units import inch, mm

def create_pdf_from_svgs(output_filename):
    # Set up the PDF canvas
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter

    # Desired size for SVG in inches
    desired_width_inch = 10
    desired_height_inch = 13

    # Convert desired size to points (1 inch = 72 points)
    desired_width = desired_width_inch * 72
    desired_height = desired_height_inch * 72

    # Directory containing SVG files
    svg_dir = "."

    # Get all SVG files in the current directory
    svg_files = sorted([f for f in os.listdir(svg_dir) if f.lower().endswith('.svg')])

    for svg_file in svg_files:
        # Read SVG file and convert to ReportLab drawing
        svg_path = os.path.join(svg_dir, svg_file)
        drawing = svg2rlg(svg_path)
        
        # Calculate the scaling factor to fit SVG to desired size
        drawing_width = drawing.width
        drawing_height = drawing.height
        scale_x = desired_width / drawing_width
        scale_y = desired_height / drawing_height
        scale = min(scale_x, scale_y)

        # Resize the drawing with the calculated scale
        drawing.width *= scale
        drawing.height *= scale
        drawing.scale(scale, scale)

        # Calculate position to center the drawing on the page
        x = (width - drawing.width) / 2
        y = (height - drawing.height) / 2

        # Draw the SVG onto the canvas
        renderPDF.draw(drawing, c, x, -200)

        # Finish the page
        c.showPage()

    # Save the PDF
    c.save()

# Create the PDF
create_pdf_from_svgs("output.pdf")
