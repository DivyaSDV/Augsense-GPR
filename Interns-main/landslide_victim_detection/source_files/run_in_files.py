# python code to run .in files to get .out files
import os

def func(folder_path):
    _files = os.listdir(folder_path)
    
    for file in _files:
        if file.endswith(".in"):
            command = f"python -m gprMax {folder_path}/{file}"
            os.system(command)
    return

if __name__ == "__main__":
    folder_path = input("Enter relative path of folder with A-scans from current directory (ending with /):\n")
    func(folder_path)
    print(".out files generated successfully. Merge files to generate B-scans.")
