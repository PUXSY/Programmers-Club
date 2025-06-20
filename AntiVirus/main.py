from apiClient import ApiClient
from tknterUI import TknterUI
from tkinter import *
import threading

if __name__ == "__main__":
    root = Tk()
    apiClient = ApiClient()
    app = TknterUI(root, apiClient)
    
    ui_thread = threading.Thread(target=root.mainloop())

    ui_thread.start()
    ui_thread.join()