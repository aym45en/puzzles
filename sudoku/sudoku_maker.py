import copy
import random
import svgwrite

def check_for_valedty(grid,test,row,col):
    for i in range(9):
        if test == grid[row][i]:
            return False
    for i in range(9):
        if test == grid[i][col]:
            return False
    row = int(row/3)*3
    col = int(col/3)*3
    for i in range(3):
        for j in range(3):
            if test == grid[row+i][col+j]:
                return False
    return True

# Function to create an empty grid of given size
def create_grid(size):
    grid = [[' ' for _ in range(size)] for _ in range(size)]
    # Fill in the grid with random numbers
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            # gah kayn nomber for box
            num_cells_to_fill = 3
            for x in range(3):
                for y in range(3):
                    if num_cells_to_fill > 0 and random.choice([True, False]): #TODO : find solution better then random
                        while True :
                            test = random.randint(1, 9)
                            if check_for_valedty(grid,test,i+x,j+y) :
                                grid[i+x][j+y] = test
                                num_cells_to_fill -= 1
                                break
    return grid

def solved_grid(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == ' ':
                for test in range(1, 10):
                    if check_for_valedty(grid, test, i, j):
                        grid[i][j] = test
                        result = solved_grid(grid)
                        if result is not None:
                            return result
                        grid[i][j] = ' '
                return None
    return grid
    
# Function to create SVG of the grid with words
def create_svg(grid, grid_size, output_file):
    cell_size = 40
    font_size = 35
    grid_size_pixels = grid_size * cell_size

    dwg = svgwrite.Drawing(output_file, size=(grid_size_pixels, grid_size_pixels))
    
    # Add a border around the SVG
    border_width = 2
    border_color = 'black'
    
    dwg.add(dwg.rect(insert=(0, 0), size=(grid_size_pixels, grid_size_pixels), 
                      fill='white', stroke=border_color, stroke_width=border_width))

    # Add text elements for grid letters
    for row in range(grid_size):
        for col in range(grid_size):
            x, y = col * cell_size, row * cell_size
            text = dwg.text(grid[row][col], insert=(x + 10, y + 30), font_size=font_size, font_family='Arial')

            if ( row == 3 or row == 6 ) :
                dwg.add(dwg.line(start=(x, y), end=(x + cell_size, y), stroke='black', stroke_width=3))
            if ( col == 3 or col == 6 ) :
                dwg.add(dwg.line(start=(x, y), end=(x, y + cell_size), stroke='black', stroke_width=3))

            # Right border
            dwg.add(dwg.line(start=(x + cell_size, y), end=(x + cell_size, y + cell_size), stroke='black', stroke_width=1))

            # Bottom border
            dwg.add(dwg.line(start=(x, y + cell_size), end=(x + cell_size, y + cell_size), stroke='black', stroke_width=1))

            dwg.add(text)
    dwg.save()

# Function to create SVG of the solution grid
def create_solution_svg(solution_grid, grid_size, output_file):
    cell_size = 40
    font_size = 35
    grid_size_pixels = grid_size * cell_size

    dwg = svgwrite.Drawing(output_file, size=(grid_size_pixels, grid_size_pixels))
    
    # Add a border around the SVG
    border_width = 2
    border_color = 'black'
    dwg.add(dwg.rect(insert=(0, 0), size=(grid_size_pixels, grid_size_pixels), fill='white',stroke=border_color, stroke_width=border_width))
    
    # Add text elements for solution grid letters
    for row in range(grid_size):
        for col in range(grid_size):
            x, y = col * cell_size, row * cell_size
            dwg.add(dwg.text(solution_grid[row][col], insert=(x + 10, y + 30), font_size=font_size, font_family='Arial'))

            if ( row == 3 or row == 6 ) :
                dwg.add(dwg.line(start=(x, y), end=(x + cell_size, y), stroke='black', stroke_width=3))
            if ( col == 3 or col == 6 ) :
                dwg.add(dwg.line(start=(x, y), end=(x, y + cell_size), stroke='black', stroke_width=3))

            # Right border
            dwg.add(dwg.line(start=(x + cell_size, y), end=(x + cell_size, y + cell_size), stroke='black', stroke_width=1))

            # Bottom border
            dwg.add(dwg.line(start=(x, y + cell_size), end=(x + cell_size, y + cell_size), stroke='black', stroke_width=1))

    dwg.save()

def main():

    num_pages = int(input("Enter the number of the pages: "))
    attempt, successful_attempt= 0, 0
    while successful_attempt <= num_pages:
        grid = create_grid(9)
        copy_grid = copy.deepcopy(grid)
        grid_solved = solved_grid(copy_grid)
        attempt += 1
        print(f"\rAttempt {attempt}, Successful attempt {successful_attempt}", end="")
        
        if grid_solved is None:
            continue
        successful_attempt += 1
        game_output_file = f'sudoku_game_{successful_attempt}.svg'
        solution_output_file = f'sudoku_solution_{successful_attempt}.svg'
        create_svg(grid,9, game_output_file)
        create_solution_svg(grid_solved,9, solution_output_file)

if __name__ == '__main__':
    main()
