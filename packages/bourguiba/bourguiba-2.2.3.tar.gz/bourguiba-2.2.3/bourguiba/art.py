# bourguiba/art.py

import os

def display_ascii_art():
    ascii_art_path = 'ascii-art.ans'
    try:
        with open(ascii_art_path, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print(f"Error reading ASCII art: {ascii_art_path} not found.")

    # Specify the path to ASCII_ART.txt directly
    art_path = os.path.join(os.path.dirname(__file__), 'ASCII_ART.txt')  # This is correct

    print(f"Looking for ASCII art at: {art_path}")  # Debugging line
    
    try:
        with open(art_path, 'r') as f:
            art = f.read()
            print(art)  # Print the ASCII art
    except Exception as e:
        print(f"Error reading ASCII art: {e}")

if __name__ == "__main__":
    display_ascii_art()
