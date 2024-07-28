import copy
import os
import re
import random
import string

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
        if len(cleaned_word)<=3:
            key.append(cleaned_word)
        else:
            # ta9sm word b 3 letters
            chunks = [cleaned_word[i:i+3] for i in range(0,len(cleaned_word),3)]
            # tvirifi ida kyn kach key rah deja kayn ida mknch dkhlo fl list key[]
            for char in chunks:
                if not any(char in elem for elem in key):
                    key.extend(chunks)
    return key
       
for fileTxT in os.listdir('cryptograms'):
    # t7aws 3la files li ikono .txt 
    if fileTxT.endswith(".txt") and not fileTxT[-5].isdigit():
        # tjib ism file bla .txt
        fileT = os.path.splitext(fileTxT)[0]
        i = 0
        while os.path.exists(os.path.join('cryptograms',f'{fileT}{i}.txt')):
            i += 1
        paragraphs = read_paragraphs(os.path.join('cryptograms',f'{fileT}.txt'))
        normal_letters = list(string.ascii_uppercase)
        puzzle_per_fileT = 0
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
            shuffled_letters_level2 = shuffled_letters[:]
            random.shuffle(shuffled_letters_level2)
            # tjib key mn jomla li 9bal letters wt7thm fi shuffled_letters_level2
            shuffled_letters_level2 = append_keys(paragraphs[p])
            # tvirifi ida n9dro njbdo key mn paragraph
            if len(shuffled_letters_level2) < 26:
                print(f"error in :{fileTxT} in paragraph {p+1} : {paragraphs[p]}") 
            else :
                key2 = dict(zip(shuffled_letters, shuffled_letters_level2))
                level_2_of_encryption = ''
                for l in range(len(level_1_of_encryption)):
                    if level_1_of_encryption[l] in string.ascii_uppercase:
                        level_2_of_encryption += key2[level_1_of_encryption[l]]
                    else:
                        level_2_of_encryption += level_1_of_encryption[l]
                game = open(os.path.join('cryptograms',f'{fileT}{i}.txt'),'a')
                game.write(f"{paragraphs[p]}{level_1_of_encryption}\n")
                for v, k in list(key.items()):
                    game.write(f"{v}=>{k} ")
                game.write(f"\n{level_2_of_encryption}\n")
                for v, k in list(key2.items()):
                    game.write(f"{v}=>{k} ")
                game.write("\n\n")
                puzzle_per_fileT += 1
                game.close()
        
        print(f'by {fileTxT} we make {puzzle_per_fileT}')
        