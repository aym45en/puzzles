import argparse
import os
import subprocess

from PyPDF2 import PdfMerger
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.lib.units import inch, mm

import subprocess

def run_puzzle_maker(puzzle_type, number_puzzles, word_search_size=None, word_per_puzzle=None):
    """
    Run the puzzle maker script.

    Args:
        puzzle_type (int): The type of puzzle to generate (1 for Sudoku, 2 for Word Search).
        number_puzzles (int): The number of puzzles to generate.
        word_search_size (int, optional): The size of the word search puzzle. Defaults to None.
        word_per_puzzle (int, optional): The number of words per puzzle. Defaults to None.
    """
    script_path = ""
    args = []

    if puzzle_type == 1:
        script_path = "sudoku/sudoku_maker.py"
        args = [f"-n {number_puzzles}"]
    elif puzzle_type == 2:
        script_path = "word-search/word_maker.py"
        args = [f"-s {word_search_size}", f"-w {word_per_puzzle}"]
    else:
        raise ValueError("Invalid puzzle type")

    subprocess.run(["python", script_path] + args, check=True)

    

def create_pdf_from_svgs(game_path,svg_files, output_filename):
    # Set up the PDF canvas
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter


    for svg_file in svg_files:
        # Desired size for SVG in inches
        # Convert desired size to points (1 inch = 72 points)
        if game_path == "sudoku/" or 'solution' in svg_file:
            desired_width = 7 * 72
            desired_height = 10 * 72
        else:
            desired_width = 10 * 72
            desired_height = 13 * 72
        # Read SVG file and convert to ReportLab drawing
        svg_path = os.path.join(game_path, svg_file)
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
        if game_path == "sudoku/" or 'solution' in svg_file:
            renderPDF.draw(drawing, c, x, 200)
        else:
            renderPDF.draw(drawing, c, x, -200)

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


def main():
    parser = argparse.ArgumentParser(description='puzzle generator')
    parser.add_argument(
        '-t', '--type',
        type=int,
        required=True,
        help='The type of puzzle (1: Sudoku, 2: Word Search)'
    )

    parser.add_argument(
        '-n', '--number-puzzles',
        type=int,
        default=100,
        help='Number of puzzles'
    )

    parser.add_argument(
        '-s', '--word-search-size',
        type=int,
        default=20,
        help='Size of the word search grid (only applicable for Word Search)'
    )

    parser.add_argument(
        '-w', '--word-per-puzzle',
        type=int,
        default=21,
        help='number of the word in one Word Search puzzle (only applicable for Word Search)'
    )

    args = parser.parse_args()

    puzzle_type = args.type
    number_puzzles = args.number_puzzles
    word_search_size = args.word_search_size
    word_per_puzzle = args.word_per_puzzle

    # rm all svg
    puzzle_dir = "sudoku/" if puzzle_type == 1 else "word-search/"
    for f in os.listdir(f"{puzzle_dir}"):
        if f.endswith('.svg'):
            path = os.path.join(f"{puzzle_dir}", f)
            os.remove(path)

    # Run the puzzls maker script
    run_puzzle_maker(puzzle_type,number_puzzles,word_search_size,word_per_puzzle)

    if puzzle_type == 1:
        game_path = "sudoku/"
        args = [f"-n {number_puzzles}"]
    elif puzzle_type == 2:
        game_path = "word-search/"
    # Get all SVG files in the current directory
    svg_files = sorted([f for f in os.listdir(f"{game_path}") if f.lower().endswith('.svg')])

    # Separate game and solution SVGs
    game_svgs = [f for f in svg_files if 'game' in f]
    solution_svgs = [f for f in svg_files if 'solution' in f]

    # Create the game and solution PDFs
    create_pdf_from_svgs(game_path,game_svgs, f"{game_path}games.pdf")
    create_pdf_from_svgs(game_path,solution_svgs, f"{game_path}solutions.pdf")

    # Merge the two PDFs into one
    merge_pdfs([f"{game_path}games.pdf", f"{game_path}solutions.pdf"], f"{game_path}{"word-search" if puzzle_type == 2 else "sudoku"}.pdf")

if __name__ == '__main__':
    main()