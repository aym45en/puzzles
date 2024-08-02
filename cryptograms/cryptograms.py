import copy
import os
import re
import random
import string

# before start sort paragraphs
def sort_lines_by_length(input_file ):
    with open(input_file, 'r') as f_in:
        lines = [line.strip() for line in f_in.readlines()]

    lines.sort(key=len)

    with open(input_file, 'w') as f_out:
        for line in lines:
            f_out.write(line + '\n')

# tvirifi ida n9dro njbdo key mn paragraph
def check_paragraph_for_key(p):
    if len(append_keys(p)) < 26:
        error_file = open(os.path.join('cryptograms',f'error.txt'),'a')
        error_file.write(f"error 'key < 26' in :{fileTxT} in paragraph : {p}") 
        error_file.close()
        return True
    else:
        return False

# check ida paragraph tji fi 6 stor
def count_lines(paragraph, line_width):
    words = paragraph.split()
    lines = 0
    current_line_length = 0

    for word in words:
        if current_line_length + len(word) <= line_width:
            current_line_length += len(word) + 1 # +1 for the space
        else:
            lines += 1
            current_line_length = len(word) + 1
    
    # Add the last line if there are remaining words
    if current_line_length > 0:
        lines += 1
    
    return lines

def check_paragraph(paragraph, line_width, max_lines):
    # num_lines = count_lines(paragraph, line_width)
    return 1==1

# Function to read paragraphs from a file
def read_paragraphs(file_path):
    with open(file_path, 'r') as file:
        paragraphs = [line.upper() for line in file]
    return paragraphs

# tjib letters mn paragraph li 9bal
def append_keys(line):
    words = line.split()
    key=[]
    for w in words:
        if len(key) >26:
            break
        # tna7i ay non alphabical char
        cleaned_word = re.sub(r'[^a-zA-Z]','',w)
        if len(cleaned_word)<=2:
            # tvirifi ida kyn kach key rah deja kayn ida mknch dkhlo fl list key[]
            if not any(cleaned_word in elem for elem in key):
                key.append(cleaned_word)
        else:
            # ta9sm word b 3 letters
            chunks = [cleaned_word[i:i+2] for i in range(0,len(cleaned_word),3)]
            # tvirifi ida kyn kach key rah deja kayn ida mknch dkhlo fl list key[]
            for char in chunks:
                if not any(char in elem for elem in key):
                    key.extend(chunks)
    return key
# tnahi ls game li kaynin wdir jdod
for f in os.listdir('cryptograms'):
        if (f.endswith(".txt") and f[-5].isdigit() ) or f == 'error.txt':
            path = os.path.join('cryptograms', f)
            os.remove(path)

for fileTxT in os.listdir('cryptograms'):
    # t7aws 3la files li ikono .txt 
    if fileTxT.endswith(".txt") and not fileTxT[-5].isdigit():
        # tjib ism file bla .txt
        fileT = os.path.splitext(fileTxT)[0]
        i = 0
        while os.path.exists(os.path.join('cryptograms',f'{fileT}{i}.txt')):
            i += 1
        sort_lines_by_length(os.path.join('cryptograms',f'{fileT}.txt'))
        paragraphs = read_paragraphs(os.path.join('cryptograms',f'{fileT}.txt'))
        normal_letters = list(string.ascii_uppercase)
        puzzle_per_fileT = 0
        game = open(os.path.join('cryptograms',f'{fileT}{i}.txt'),'a')
        game.write(f"first paragraph to start is : {paragraphs[0]}")
        p=0
        while check_paragraph_for_key(paragraphs[p]):
                del paragraphs[p]
        while p<len(paragraphs):
            if check_paragraph_for_key(paragraphs[p]):
                del paragraphs[p]
                continue
            # 1st crypting
            shuffled_letters = normal_letters[:]
            random.shuffle(shuffled_letters)
            key = dict(zip(normal_letters, shuffled_letters))
            level_1_of_encryption = ''
            # ta7km paragraph wt7awl kol 7arf b 7arf khlaf mn key
            # ndiro paragraphs[p])-1 bah mndiwch \n mn paragraph
            for l in range(len(paragraphs[p])-1):
                # tvirifi ida char fl paragraph rah 7arf t7t key t3o ida nn t7to ho nrml kima numbers
                if paragraphs[p][l] in string.ascii_uppercase:
                    level_1_of_encryption += key[paragraphs[p][l]]
                else:
                    level_1_of_encryption += paragraphs[p][l]
            # 2nd crypting
            # tjib key mn jomla li 9bal letters wt7thm fi shuffled_letters_level2
            shuffled_letters_level2 = append_keys(paragraphs[p-1])
            key2 = dict(zip(shuffled_letters, shuffled_letters_level2))
            level_2_of_encryption = ''
            for l in range(len(level_1_of_encryption)):
                if level_1_of_encryption[l] in string.ascii_uppercase:
                    level_2_of_encryption += key2[level_1_of_encryption[l]]
                else:
                    level_2_of_encryption += level_1_of_encryption[l]
            # check ida level 2 iji mrigl ki nhatoh fi pdf
            line_width = 50 # Adjust based on your actual line width
            max_lines = 6
            if check_paragraph(level_2_of_encryption, line_width, max_lines) :
                game_sulition = open(os.path.join('cryptograms',f'{fileT}_sulition_{i}.txt'),'a')
                game_sulition.write(f"{paragraphs[p]}{level_1_of_encryption}\n")
                for v, k in list(key.items()):
                    game_sulition.write(f"{v}=>{k} ")
                game_sulition.write("\n")
                for v, k in list(key2.items()):
                    game_sulition.write(f"{v}=>{k} ")
                game_sulition.write("\n\n")
                game_sulition.close()
                game.write(f"{level_2_of_encryption}\n")
                puzzle_per_fileT += 1
                p += 1
            else :
                error_file = open(os.path.join('cryptograms',f'error.txt'),'a')
                error_file.write(f"error 'paragraph > {max_lines} lins' in :{fileTxT} in paragraph : {paragraphs[p]}") 
                error_file.close()
                del paragraphs[p]
        game.close()

        print(f'by {fileTxT} we make {puzzle_per_fileT}')
        