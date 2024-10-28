# bourguiba/art.py

import os

def display_ascii_art():
    current_dir = os.path.dirname(__file__)
    art_path = os.path.join(current_dir, '..', 'ASCII_ART.txt')
    try:
        with open(art_path, 'r') as f:
            art = f.read()
            print(art)
    except Exception as e:
        print(f"Error reading ASCII art: {e}")
