# Imports
import tkinter as tk

# Window Setup
window = tk.Tk()
window.title("Wild West Poster Generator")
window.geometry("1080x720")
window.resizable(True,True)
window.iconbitmap('./assets/horseshoe.ico')
window.config(bg="orange2")

# Window Customization
mainframe = tk.Frame(window, width=1060, height=700)
mainframe.pack(padx=10, pady=10)


# Starts the window
window.mainloop()