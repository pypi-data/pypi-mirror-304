import os

def display_ascii_art():
    # Get the directory of the setup.py file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the ASCII art file in the parent directory
    art_file_path = os.path.join(current_dir, '../ascii-art.ans')
    
    try:
        with open(art_file_path, 'r') as art_file:
            ascii_art = art_file.read()
            print(ascii_art)
    except FileNotFoundError:
        print(f"Error reading ASCII art: {art_file_path} not found.")
