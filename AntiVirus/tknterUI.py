import tkinter as tk
from tkinter import filedialog

class TknterUI:
    def __init__(self, master, apiClient):
        self.master = master
        self.apiClient = apiClient
        self.filename = None
        self.foldername = None

        self.master.title("AntiVirus Scanner")
        self.master.geometry("400x300")

        self.label = tk.Label(master, text="Welcome to the AntiVirus Scanner")
        self.label.pack(pady=20)

        self._select_folder = tk.Button(master, text="Select Folder", command=self.button_select_folder)
        self._select_folder.pack(pady=5)

        self._select_file = tk.Button(master, text="Select File", command=self.button_select_file)
        self._select_file.pack(pady=5)

        self._scan = tk.Button(master, text="Scan", command=self.button_scan)
        self._scan.pack(pady=20)

    def button_select_folder(self):
        self.foldername = filedialog.askdirectory(title="Select folder", mustexist=True)
        if self.foldername:
            self.label.config(text=f"Selected folder: {self.foldername}")

    def button_select_file(self):
        self.filename = filedialog.askopenfilename(
            title="Select file",
            filetypes=(("Executable files", "*.exe"), ("All files", "*.*"))
        )
        if self.filename:
            self.label.config(text=f"Selected file: {self.filename}")

    def button_scan(self):
        if not self.foldername and not self.filename:
            self.label.config(text="Please select a folder or file to scan.")
            return

        try:
            if self.foldername:
                self.apiClient.scan_folder(self.foldername)
            elif self.filename:
                if self.apiClient.scan_file(self.filename) == True:
                    self.label.config(text="Virus detected in the selected file!")
                else:
                    self.label.config(text="No virus detected in the selected file.")
                    
        except Exception as e:
            self.label.config(text=f"Error during scan: {e}")