import os
import re
import random

def replace_wildcards_in_text(original_text):
    # Replace wildcards with random words from files
    def replace_wildcards(match):
        wildcard = match.group()
        wildcard_name = wildcard.strip("_")
        filename = os.path.join("wildcards", f"{wildcard_name}.txt")
        
        try:
            with open(filename, 'r') as file:
                word_list = [line.strip() for line in file.readlines()]
                if word_list:
                    return random.choice(word_list)
        except FileNotFoundError:
            pass
        
        return wildcard
    
    replaced_text = re.sub(r"(__\w+__)", replace_wildcards, original_text)
    return replaced_text
