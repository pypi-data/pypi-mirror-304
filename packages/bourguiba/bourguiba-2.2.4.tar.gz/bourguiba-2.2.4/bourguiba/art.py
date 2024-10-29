# bourguiba/art.py

import os

def display_ascii_art():
    ascii_art_path = 'ascii-art.ans'
    try:
        with open(ascii_art_path, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print(f"Error reading ASCII art: {ascii_art_path} not found.")

if __name__ == "__main__":
    display_ascii_art()
