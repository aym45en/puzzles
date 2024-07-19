import os
import glob
import scribus

# Get all SVG files in the current directory
svg_files = sorted(glob.glob("*.svg"))

# Function to add an SVG to the Scribus document
def add_svg(svg_file, x, y, width, height):
    scribus.createImage(x, y, width, height)
    scribus.loadImage(svg_file)
    scribus.setScaleImageToFrame(1, 1)

# Initialize Scribus
if scribus.haveDoc():
    scribus.closeDoc()

scribus.newDocument((210, 297), (5, 5, 5, 5), scribus.PORTRAIT, 1, scribus.UNIT_MM, scribus.PAGE_1)

# Variables for layout
x_margin = 5
y_margin = 5
page_width = 210 - 2 * x_margin
page_height = 297 - 2 * y_margin

# Counter for solutions
solution_counter = 0

# Iterate over SVG files and add them to the document
for i, svg_file in enumerate(svg_files):
    if i % 3 == 2:  # After every 2 pages, insert a solution on a new page
        solution_counter += 1
        scribus.newPage(-1)
        add_svg(svg_files[4 + solution_counter], x_margin, y_margin, page_width, page_height)
    else:
        scribus.newPage(-1)
        add_svg(svg_file, x_margin, y_margin, page_width, page_height)

# Save the document as PDF
scribus.saveDocAs("word_search_games.pdf")
