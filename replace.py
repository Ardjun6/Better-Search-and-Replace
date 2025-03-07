import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to preserve case while replacing
def replace_preserve_case(text, old_word, new_word):
    def match_case(match):
        word = match.group()
        if word.isupper():
            return new_word.upper()
        elif word.istitle():
            return new_word.capitalize()
        else:
            return new_word.lower()
    
    return re.sub(re.escape(old_word), match_case, text, flags=re.IGNORECASE)

# Function to process a file
def process_file(file_path, old_word, new_word, count_dict):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    
    count_dict[old_word] += len(re.findall(re.escape(old_word), content, flags=re.IGNORECASE))
    new_content = replace_preserve_case(content, old_word, new_word)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

# Function to rename files and folders
def rename_item(old_path, old_word, new_word):
    dir_name, base_name = os.path.split(old_path)
    new_name = replace_preserve_case(base_name, old_word, new_word)
    new_path = os.path.join(dir_name, new_name)
    if new_path != old_path and not os.path.exists(new_path):
        os.rename(old_path, new_path)
    return new_path

# Function to process the folder recursively
def process_folder(folder_path, old_word, new_word):
    count_dict = {old_word: 0}
    
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            new_file_path = rename_item(file_path, old_word, new_word)
            process_file(new_file_path, old_word, new_word, count_dict)
        
        for name in dirs:
            dir_path = os.path.join(root, name)
            rename_item(dir_path, old_word, new_word)
    
    new_folder_path = rename_item(folder_path, old_word, new_word)
    return count_dict

# GUI Application
def browse_folder():
    folder_selected = filedialog.askdirectory()
    entry_folder.delete(0, tk.END)
    entry_folder.insert(0, folder_selected)

def start_replacement():
    folder_path = entry_folder.get()
    old_word = entry_old_word.get()
    new_word = entry_new_word.get()
    
    if not folder_path or not old_word or not new_word:
        messagebox.showwarning("Input Error", "Please provide all inputs: folder, old word, and new word.")
        return
    
    count_dict = process_folder(folder_path, old_word, new_word)
    messagebox.showinfo("Replacement Complete", f"Replaced '{old_word}' with '{new_word}' {count_dict[old_word]} times.")

# Setting up the GUI
root = tk.Tk()
root.title("Better Search and Replace")
root.geometry("400x200")

tk.Label(root, text="Select Folder:").pack(pady=5)
entry_folder = tk.Entry(root, width=50)
entry_folder.pack()
tk.Button(root, text="Browse", command=browse_folder).pack(pady=5)

tk.Label(root, text="Old Word:").pack()
entry_old_word = tk.Entry(root, width=30)
entry_old_word.pack()

tk.Label(root, text="New Word:").pack()
entry_new_word = tk.Entry(root, width=30)
entry_new_word.pack()

tk.Button(root, text="Start Replacement", command=start_replacement).pack(pady=10)

root.mainloop()
