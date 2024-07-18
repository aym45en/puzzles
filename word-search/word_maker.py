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
    if direction == 0:  # Horizontal
        if col + len_word > len(grid):
            return False
        return all(grid[row][col + i] in (' ', word[i]) for i in range(len_word))
    elif direction == 1:  # Vertical
        if row + len_word > len(grid):
            return False
        return all(grid[row + i][col] in (' ', word[i]) for i in range(len_word))
    elif direction == 2:  # Diagonal
        if row + len_word > len(grid) or col + len_word > len(grid):
            return False
        return all(grid[row + i][col + i] in (' ', word[i]) for i in range(len_word))
    return False

# Function to place the word on the grid
def place_word(grid, word, row, col, direction):
    for i in range(len(word)):
        if direction == 0:  # Horizontal
            grid[row][col + i] = word[i]
        elif direction == 1:  # Vertical
            grid[row + i][col] = word[i]
        elif direction == 2:  # Diagonal
            grid[row + i][col + i] = word[i]

# Function to fill the empty cells with random letters
def fill_random_letters(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == ' ':
                grid[row][col] = random.choice(string.ascii_uppercase)

# Function to create SVG of the grid with words
def create_svg(grid, words, grid_size, output_file):
    cell_size = 40
    font_size = 20
    grid_size_pixels = grid_size * cell_size
    word_area_height = len(words) * (font_size + 5) + 20

    dwg = svgwrite.Drawing(output_file, size=(grid_size_pixels, grid_size_pixels + word_area_height))
    dwg.add(dwg.rect(insert=(0, 0), size=(grid_size_pixels, grid_size_pixels), fill='white'))

    # Add text elements for grid letters
    for row in range(grid_size):
        for col in range(grid_size):
            x, y = col * cell_size, row * cell_size
            dwg.add(dwg.text(grid[row][col], insert=(x + 10, y + 30), font_size=font_size, font_family='Arial'))

    # Add text elements for words below the grid
    y_offset = grid_size_pixels + 20
    for word in words:
        dwg.add(dwg.text(word, insert=(10, y_offset), font_size=font_size, font_family='Arial'))
        y_offset += font_size + 5

    dwg.save()

# Function to create SVG of the solution grid
def create_solution_svg(solution_grid, grid_size, output_file):
    cell_size = 40
    font_size = 20
    grid_size_pixels = grid_size * cell_size

    dwg = svgwrite.Drawing(output_file, size=(grid_size_pixels, grid_size_pixels))
    dwg.add(dwg.rect(insert=(0, 0), size=(grid_size_pixels, grid_size_pixels), fill='white'))

    # Add text elements for solution grid letters
    for row in range(grid_size):
        for col in range(grid_size):
            x, y = col * cell_size, row * cell_size
            dwg.add(dwg.text(solution_grid[row][col], insert=(x + 10, y + 30), font_size=font_size, font_family='Arial'))

    dwg.save()

def main():
    file_path = 'words.txt'
    words = read_words(file_path)

    # Ask user for grid size
    grid_size = int(input("Enter the size of the grid (e.g., 10 for a 10x10 grid): "))

    # Divide words into chunks of 10
    for i in range(0, len(words), 10):
        chunk_words = words[i:i + 10]

        grid = create_empty_grid(grid_size)
        solution_grid = create_empty_grid(grid_size)

        for word in chunk_words:
            placed = False
            attempts = 0
            while not placed and attempts < 100:  # Limit the number of attempts to place each word
                row = random.randint(0, grid_size - 1)
                col = random.randint(0, grid_size - 1)
                direction = random.randint(0, 2)  # 0: Horizontal, 1: Vertical, 2: Diagonal
                if can_place_word(grid, word, row, col, direction):
                    place_word(grid, word, row, col, direction)
                    place_word(solution_grid, word, row, col, direction)
                    placed = True
                attempts += 1
            if not placed:
                print(f"Could not place the word: {word}")

        fill_random_letters(grid)

        game_output_file = f'word_search_game_{i // 10 + 1}.svg'
        solution_output_file = f'word_search_solution_{i // 10 + 1}.svg'
        create_svg(grid, chunk_words, grid_size, game_output_file)
        create_solution_svg(solution_grid, grid_size, solution_output_file)

if __name__ == '__main__':
    main()
