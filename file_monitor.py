import os
import re
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil

# Configuration
CONFIG = {
    "target_directory": "",  # Directory for file operations
    "target_file": "",       # Selected file for file generation
    "filename_pattern": r"50.114.4.*",  # Regex pattern for file matching
}

def find_most_recent_file(directory, pattern):
    """
    Find the most recently modified file in the given directory matching the pattern.
    """
    try:
        files = [
            f for f in Path(directory).iterdir()
            if f.is_file() and re.match(pattern, f.name)
        ]
        if not files:
            return None
        return max(files, key=lambda f: f.stat().st_mtime)
    except Exception as e:
        print(f"Error finding recent file: {e}")
        return None

def replace_with_most_recent(directory, pattern):
    """
    Replace all files matching the pattern in the directory with the content of the most recent file.
    """
    try:
        # Find the most recent file
        most_recent = find_most_recent_file(directory, pattern)
        if not most_recent:
            print("No matching files found.")
            messagebox.showwarning("Warning", "No matching files found.")
            return

        # Replace the content of all matching files with the most recent file's content
        for file in Path(directory).iterdir():
            if file.is_file() and re.match(pattern, file.name) and file != most_recent:
                shutil.copy2(most_recent, file)
        
        print(f"All matching files in {directory} have been replaced with {most_recent.name}.")
        messagebox.showinfo("Success", "All matching files have been replaced.")
    except Exception as e:
        print(f"Error replacing files: {e}")
        messagebox.showerror("Error", f"Error replacing files: {e}")

def generate_files_with_regex(target_file, output_dir):
    """
    Generate 256 files named according to the regex pattern in the output directory.
    """
    try:
        # Read the content of the target file
        with open(target_file, 'rb') as f:
            content = f.read()

        # Create files 50.114.4.0 to 50.114.4.255
        for i in range(256):
            filename = CONFIG["filename_pattern"].replace("*", str(i))
            output_file = Path(output_dir) / filename
            with open(output_file, 'wb') as out_f:
                out_f.write(content)
        
        print("256 files successfully created!")
        messagebox.showinfo("Success", "256 files successfully created!")
    except Exception as e:
        print(f"Error creating files: {e}")
        messagebox.showerror("Error", f"Error creating files: {e}")

def browse_target_file():
    """
    Allow the user to select a target file.
    """
    target_file = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    if target_file:
        CONFIG["target_file"] = target_file
        print(f"Target file selected: {target_file}")
        messagebox.showinfo("Target File", f"Target file selected: {target_file}")

def browse_output_directory():
    """
    Allow the user to select an output directory.
    """
    directory = filedialog.askdirectory()
    if directory:
        CONFIG["target_directory"] = directory
        print(f"Output directory set to: {directory}")
        messagebox.showinfo("Output Directory", f"Output directory set to: {directory}")

def execute_file_generation():
    """
    Execute the file generation task.
    """
    target_file = CONFIG.get("target_file")
    output_dir = CONFIG.get("target_directory")

    if not target_file or not Path(target_file).is_file():
        messagebox.showwarning("Warning", "Please select a valid target file!")
        return

    if not output_dir or not Path(output_dir).is_dir():
        messagebox.showwarning("Warning", "Please select a valid output directory!")
        return

    generate_files_with_regex(target_file, output_dir)

def execute_file_replacement():
    """
    Execute the file replacement task.
    """
    output_dir = CONFIG.get("target_directory")

    if not output_dir or not Path(output_dir).is_dir():
        messagebox.showwarning("Warning", "Please select a valid target directory!")
        return

    replace_with_most_recent(output_dir, CONFIG["filename_pattern"])

# GUI for the Script
def create_gui():
    root = tk.Tk()
    root.title("File Operations Tool")

    # File Selection for Generation
    tk.Button(root, text="Select Target File", command=browse_target_file).pack(pady=10)

    # Directory Selection
    tk.Button(root, text="Select Target Directory", command=browse_output_directory).pack(pady=10)

    # Generate Files Button
    tk.Button(root, text="Generate 256 Files", command=execute_file_generation).pack(pady=10)

    # Replace Files Button
    tk.Button(root, text="Replace Files with Most Recent", command=execute_file_replacement).pack(pady=10)

    # Exit Button
    tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()