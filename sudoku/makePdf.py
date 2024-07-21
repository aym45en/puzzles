import os
import subprocess

from PyPDF2 import PdfMerger
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.lib.units import inch, mm

def run_sudoku_maker():
    # Run the sudoku_maker.py script
    subprocess.run(["python3", "sudoku_maker.py"], check=True)

def create_pdf_from_svgs(svg_files, output_filename):
    # Set up the PDF canvas
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter


    for svg_file in svg_files:
        # Desired size for SVG in inches
        # Convert desired size to points (1 inch = 72 points)
        desired_width = 7 * 72
        desired_height = 10 * 72
        # Read SVG file and convert to ReportLab drawing
        svg_path = os.path.join(".", svg_file)
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
        renderPDF.draw(drawing, c, x, 200)

        # Finish the page
        c.showPage()

    # Save the PDF
    c.save()

def merge_pdfs(input_files, output_filename):
    merger = PdfMerger()
    for pdf in input_files:
        merger.append(pdf)
    merger.write(output_filename)
    merger.close()

# rm all svg

for f in os.listdir("."):
    if f.endswith('.svg'):
        path=os.path.join(".",f)
        os.remove(path)

# Run the sudoku_maker.py script
run_sudoku_maker()

# Get all SVG files in the current directory
svg_files = sorted([f for f in os.listdir(".") if f.lower().endswith('.svg')])

# Separate game and solution SVGs
game_svgs = [f for f in svg_files if 'game' in f]
solution_svgs = [f for f in svg_files if 'solution' in f]

# Create the game and solution PDFs
create_pdf_from_svgs(game_svgs, "games.pdf")
create_pdf_from_svgs(solution_svgs, "solutions.pdf")

# Merge the two PDFs into one
merge_pdfs(["games.pdf", "solutions.pdf"], "output.pdf")
