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


# Function to read paragraphs from a file
def read_paragraphs(file_path):
    with open(file_path, 'r') as file:
        paragraphs = [line.upper() for line in file]
    return paragraphs


# tnahi ls game li kaynin wdir jdod
for f in os.listdir('cryptograms'):
        if (f.endswith(".txt") and f[-5].isdigit() ) or f == 'error.txt':
            path = os.path.join('cryptograms', f)
            os.remove(path)

def initialize_wheel(key_letter):
    letters = list(string.ascii_uppercase)
    start_index = letters.index(key_letter)
    return {letters[i]: letters[(i + start_index) % 26] for i in range(26)}

def rotate_wheel(wheel):
    letters = list(string.ascii_uppercase)
    rotated_wheel = {}
    for k, v in wheel.items():
        rotated_wheel[k] = letters[(letters.index(v) + 1) % 26]
    return rotated_wheel

def enigma_encrypt(text, key):
    # Initialize the wheels
    wheel1 = initialize_wheel(key)
   
    encrypted_text = ""
   
    for letter in text.upper():
        if letter in string.ascii_uppercase:
            # Encrypt the letter using the current state of the wheels
            encrypted_letter = wheel1[letter]
            encrypted_text += encrypted_letter

            # Rotate the wheels
            wheel1 = rotate_wheel(wheel1)
        else:
            encrypted_text += letter
           
    return encrypted_text


for fileTxT in os.listdir('cryptograms'):
    # t7aws 3la files li ikono .txt 
    if fileTxT.endswith(".txt") and not fileTxT[-5].isdigit():
        # tjib ism file bla .txt
        fileT = os.path.splitext(fileTxT)[0]
        sort_lines_by_length(os.path.join('cryptograms',f'{fileT}.txt'))
        paragraphs = read_paragraphs(os.path.join('cryptograms',f'{fileT}.txt'))
        normal_letters = list(string.ascii_uppercase)
        game = open(os.path.join('cryptograms',f'{fileT}_45.txt'),'a')
        
        for p in range(len(paragraphs)):
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
            # ta7km level_1_of_encryption wtbdl kol 7arf b7arf khlaf mais key yb9a ytbdl hadi mara 
            if p >= 0:
                key_letter = 0
                while paragraphs[p-1][key_letter] not in normal_letters:
                    key_letter += 1
                level_2_of_encryption = enigma_encrypt(level_1_of_encryption, paragraphs[p-1][key_letter])
            else :
                level_2_of_encryption = enigma_encrypt(level_1_of_encryption, "K")
            
            game_sulition = open(os.path.join('cryptograms',f'{fileT}_sulition_45.txt'),'a')
            game_sulition.write(f"{paragraphs[p]}{level_1_of_encryption}\n")
            for v, k in list(key.items()):
                game_sulition.write(f"{v}=>{k} ")
            game_sulition.write("\n\n")
            game_sulition.close()

            game.write(f"{level_2_of_encryption}\n")
        game.close()
        