from tkinter import Tk, filedialog
from IPython.display import clear_output

import sys
sys.path.append('')

from util.functions import askBooleanInput

def saveFiles(files=[], recursive=True):
    """
    
    Creates a list containing .wav file routes provided by the user through the file explorer.

    Parameters:
        files (list): A previous list of files to add routes into.
        visualize (boolean): A value to decide if the files should be plotted.
        save (boolean): A value to decide if the files should be saved to media/save_files.

    Returns:
        list: The list of the selected file routes.

    """                                
    clear_output()
    root = Tk()
    root.withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)
    files.append(filedialog.askopenfilename(filetypes=[("wav files", "*.wav")]))
    if recursive:
        anotherFile = askBooleanInput("Do you wish to add another file?")
        if anotherFile:
            saveFiles(files)
            
    return files

if __name__ == "__main__":
    routes = saveFiles()
    for route in routes:
        print(route)