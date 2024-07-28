import os
import random
import string

# Function to read paragraphs from a file
def read_paragraphs(file_path):
    with open(file_path, 'r') as file:
        paragraphs = [line.upper() for line in file]
    return paragraphs

# trod bin 1 l 3 random letters
def append_random_letters():
    letter = ''
    for _ in range(random.randint(2, 3)):
        random_letter = random.choice(shuffled_letters)
        letter += random_letter
    return letter

for fileT in os.listdir('cryptograms'):
    if fileT.endswith(".txt") and not fileT[:-4].isdigit():
        fileT = os.path.splitext(fileT)[0]
        i = 0
        while os.path.exists(os.path.join('cryptograms',f'{fileT}{i}.txt')):
            i += 1
        paragraphs = read_paragraphs(os.path.join('cryptograms',f'{fileT}.txt'))
        normal_letters = list(string.ascii_uppercase)
        for p in range(len(paragraphs)):
            # 1st crypting
            shuffled_letters = normal_letters[:]
            random.shuffle(shuffled_letters)
            key = dict(zip(normal_letters, shuffled_letters))
            new_paraghraph = ''
            for l in range(len(paragraphs[p])-1):
                if paragraphs[p][l] in string.ascii_uppercase:
                    new_paraghraph += key[paragraphs[p][l]]
                else:
                    new_paraghraph += paragraphs[p][l]
            # 2nd crypting
            shuffled_letters1 = shuffled_letters[:]
            random.shuffle(shuffled_letters1)
            # tjib random letters wt7thm fi shuffled_letters
            for letter in range(len(shuffled_letters1)):
                # check bah mijich key yt3awd martin
                while True:
                    append_random_letter = append_random_letters()
                    if not any(append_random_letter in elem for elem in shuffled_letters1):
                        shuffled_letters1[letter] = append_random_letter
                        break
            key2 = dict(zip(shuffled_letters, shuffled_letters1))
            new_paraghraph1 = ''
            for l in range(len(new_paraghraph)):
                if new_paraghraph[l] in string.ascii_uppercase:
                    new_paraghraph1 += key2[new_paraghraph[l]]
                else:
                    new_paraghraph1 += new_paraghraph[l]
            game = open(os.path.join('cryptograms',f'{fileT}{i}.txt'),'a')
            game.write(f"{paragraphs[p]}{new_paraghraph}\n")
            for v, k in list(key.items()):
                game.write(f"{k}<={v} ")
            game.write(f"\n{new_paraghraph1}\n")
            for v, k in list(key2.items()):
                game.write(f"{k}<={v} ")
            game.write("\n\n")
        game.close()
        
        