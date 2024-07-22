#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>

// Function to check if a given number can be placed at a specific position in the grid
bool checkForValidity(std::vector<std::vector<int>> &grid, int test, int row, int col)
{
    for (int i = 0; i < 9; i++)
    {
        if (test == grid[row][i] || test == grid[i][col])
        {
            return false;
        }
    }
    int startRow = (row / 3) * 3;
    int startCol = (col / 3) * 3;
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            if (test == grid[startRow + i][startCol + j])
            {
                return false;
            }
        }
    }
    return true;
}

// Function to create a Sudoku grid of a given size and fill it with random numbers
std::vector<std::vector<int>> createGrid(int size)
{
    srand(time(0));
    std::vector<std::vector<int>> grid(size, std::vector<int>(size, 0));
    while (true)
    {
        int numNumbersToHave = 0;
        for (int i = 0; i < 9; i += 3)
        {
            for (int j = 0; j < 9; j += 3)
            {
                int numCellsToFill = 5;
                for (int x = 0; x < 3; x++)
                {
                    for (int y = 0; y < 3; y++)
                    {
                        if (numCellsToFill > 0 && rand() % 2 == 1)
                        {
                            for (int k = 0; k < 100; k++)
                            {
                                int test = rand() % 9 + 1;
                                if (checkForValidity(grid, test, i + x, j + y))
                                {
                                    grid[i + x][j + y] = test;
                                    numCellsToFill--;
                                    numNumbersToHave++;
                                    break;
                                }
                            }
                        }
                    }
                }
            }
        }
        if (numNumbersToHave > 24)
        {
            break;
        }
    }
    return grid;
}

// Function to solve the Sudoku grid using backtracking
bool solveGrid(std::vector<std::vector<int>> &grid)
{
    for (int i = 0; i < 9; i++)
    {
        for (int j = 0; j < 9; j++)
        {
            if (grid[i][j] == 0)
            {
                for (int test = 1; test <= 9; test++)
                {
                    if (checkForValidity(grid, test, i, j))
                    {
                        grid[i][j] = test;
                        if (solveGrid(grid))
                        {
                            return true;
                        }
                        grid[i][j] = 0;
                    }
                }
                return false;
            }
        }
    }
    return true;
}

int main()
{
    std::vector<std::vector<int>> grid;
    do
    {
        grid = createGrid(9);

        // Print initial grid
        for (const auto &row : grid)
        {
            for (const auto &cell : row)
            {
                std::cout << cell << " ";
            }
            std::cout << std::endl;
        }
    } while (solveGrid(grid));

    std::cout << "Solved Grid:" << std::endl;

    for (const auto &row : grid)
    {
        for (const auto &cell : row)
        {
            std::cout << cell << " ";
        }
        std::cout << std::endl;
    }
    return 0;
}
