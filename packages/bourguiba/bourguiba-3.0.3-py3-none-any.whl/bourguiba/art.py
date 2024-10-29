import pkg_resources

def display_ascii_art():
    art_file_path = '../ascii-art.ans '
    
    try:
        with pkg_resources.resource_stream(__name__, art_file_path) as art_file:
            ascii_art = art_file.read().decode('utf-8')  # Decode bytes to string
            print(ascii_art)
    except FileNotFoundError:
        print(f"Error reading ASCII art: {art_file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
