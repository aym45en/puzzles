import argparse
import random
import string
import svgwrite

# Function to read words from a file
def read_words(file_path):
    with open(file_path, 'r') as file:
        words = [line.strip().upper() for line in file]
    return words

# Function to create an empty grid of given size
def create_empty_grid(size):
    return [[' ' for _ in range(size)] for _ in range(size)]

# Function to check if the word can be placed at the position
def can_place_word(grid, word, row, col, direction):
    len_word = len(word)
    if direction == 0:  # Horizontal up
        if col + len_word > len(grid):
            return False
        return all(grid[row][col + i] in (' ', word[i]) for i in range(len_word))
    elif direction == 1:  # Horizontal down
        if col + len_word > len(grid):
            return False
        return all(grid[row][col - i] in (' ', word[i]) for i in range(len_word))
    elif direction == 2:  # Vertical r
        if row + len_word > len(grid):
            return False
        return all(grid[row + i][col] in (' ', word[i]) for i in range(len_word))
    elif direction == 3:  # Vertical l
        if row + len_word > len(grid):
            return False
        return all(grid[row - i][col] in (' ', word[i]) for i in range(len_word))
    elif direction == 4:  # Diagonal r
        if row + len_word > len(grid) or col + len_word > len(grid):
            return False
        return all(grid[row + i][col + i] in (' ', word[i]) for i in range(len_word))
    elif direction == 5:  # Diagonal l
        if row + len_word > len(grid) or col + len_word > len(grid):
            return False
        return all(grid[row - i][col - i] in (' ', word[i]) for i in range(len_word))
    return False

# Function to place the word on the grid
def place_word(grid, word, row, col, direction):
    for i in range(len(word)):
        if direction == 0:  # Horizontal up
            grid[row][col + i] = word[i]
        if direction == 1:  # Horizontal down
            grid[row][col - i] = word[i]
        elif direction == 2:  # Vertical r
            grid[row + i][col] = word[i]
        elif direction == 2:  # Vertical l
            grid[row - i][col] = word[i]
        elif direction == 4:  # Diagonal r
            grid[row + i][col + i] = word[i]
        elif direction == 5:  # Diagonal l
            grid[row - i][col - i] = word[i]

# Function to fill the empty cells with random letters
def fill_random_letters(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == ' ':
                grid[row][col] = random.choice(string.ascii_uppercase)

# Function to create SVG of the grid with words
def create_svg(grid, words, word_search_size, output_file):
    cell_size = 40
    font_size = 35
    word_search_size_pixels = word_search_size * cell_size
    word_area_height = len(words) * (font_size + 5) + 20

    dwg = svgwrite.Drawing(output_file, size=(word_search_size_pixels, word_search_size_pixels + word_area_height))
    
    # Add a border around the SVG
    border_width = 2
    border_color = 'black'
    
    dwg.add(dwg.rect(insert=(0, 0), size=(word_search_size_pixels, word_search_size_pixels), 
                      fill='white', stroke=border_color, stroke_width=border_width))

    # Add text elements for grid letters
    for row in range(word_search_size):
        for col in range(word_search_size):
            x, y = col * cell_size, row * cell_size
            dwg.add(dwg.text(grid[row][col], insert=(x + 10, y + 30), font_size=font_size, font_family='Arial'))

    # Add text elements for words below the grid
    y_offset = word_search_size_pixels + 50
    x_offset = 20
    col_max = 0
    word_max = 0
    for word in words:
        dwg.add(dwg.text(word, insert=(x_offset, y_offset), font_size=font_size, font_family='Arial'))
        y_offset += font_size + 5
        col_max += 1

        if word_max < len(word) :
            word_max = len(word)

        if col_max >= 7 :
            y_offset = word_search_size_pixels + 50
            x_offset += word_max * (font_size * 0.65) + 50  # Adjust spacing between words
            col_max = 0

    dwg.save()

# Function to create SVG of the solution grid
def create_solution_svg(solution_grid, word_search_size, output_file):
    cell_size = 40
    font_size = 20
    word_search_size_pixels = word_search_size * cell_size

    dwg = svgwrite.Drawing(output_file, size=(word_search_size_pixels, word_search_size_pixels))
    
    # Add a border around the SVG
    border_width = 2
    border_color = 'black'
    dwg.add(dwg.rect(insert=(0, 0), size=(word_search_size_pixels, word_search_size_pixels), fill='white',stroke=border_color, stroke_width=border_width))
    
    # Add text elements for solution grid letters
    for row in range(word_search_size):
        for col in range(word_search_size):
            x, y = col * cell_size, row * cell_size
            dwg.add(dwg.text(solution_grid[row][col], insert=(x + 10, y + 30), font_size=font_size, font_family='Arial'))

    dwg.save()

def main():

    parser = argparse.ArgumentParser(description='puzzle generator')

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

    word_search_size = args.word_search_size
    word_per_puzzle = args.word_per_puzzle
    
    file_path = 'word-search/words.txt'
    words = read_words(file_path)

    # Divide words into chunks of the specified size
    for i in range(0, len(words), word_per_puzzle):
        chunk_words = words[i:i + word_per_puzzle]

        grid = create_empty_grid(word_search_size)
        solution_grid = create_empty_grid(word_search_size)

        word=0
        while word < len(chunk_words):
            placed = False
            attempts = 0
            while not placed and attempts < 200:  # Limit the number of attempts to place each word
                row = random.randint(0, word_search_size - 1)
                col = random.randint(0, word_search_size - 1)
                direction = random.randint(0, 5)  # 0-1: Horizontal, 2-3: Vertical, 4-5: Diagonal
                if can_place_word(grid, chunk_words[word], row, col, direction):
                    place_word(grid, chunk_words[word], row, col, direction)
                    place_word(solution_grid, chunk_words[word], row, col, direction)
                    placed = True
                attempts += 1
            if not placed:
                print(f"Could not place the word: {chunk_words[word]} in svg {i}")
            else :
                print(f"\rdone word {word} in svg {i}", end="")
                word += 1

        fill_random_letters(grid)

        game_output_file = f'word-search/word_search_game_{i // word_per_puzzle + 1}.svg'
        solution_output_file = f'word-search/word_search_solution_{i // word_per_puzzle + 1}.svg'
        create_svg(grid, chunk_words, word_search_size, game_output_file)
        create_solution_svg(solution_grid, word_search_size, solution_output_file)

if __name__ == '__main__':
    main()
