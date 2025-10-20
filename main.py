# Starts the window
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Window Setup
window = tk.Tk()
window.title("Wild West Poster Generator")
window.geometry("1080x720")
window.config(bg="orange2")

# Window Customization
mainframe = tk.Frame(window, width=1060, height=700, bg="orange2")
mainframe.pack(padx=10, pady=10)

# -----------------Name and Location Input ----------------- #

# Labels and Entries for Name and Location
tk.Label(mainframe, text="Enter Name:", bg="orange2", font=("Helvetica", 14)).place(x=20, y=20)
name_entry = tk.Entry(mainframe, width=30, font=("Helvetica", 14))
name_entry.place(x=150, y=20)

tk.Label(mainframe, text="Enter Location:", bg="orange2", font=("Helvetica", 14)).place(x=20, y=60)
location_entry = tk.Entry(mainframe, width=30, font=("Helvetica", 14))
location_entry.place(x=150, y=60)

# ----------------- Upload Image and Preview ----------------- #

uploaded_image = None

def upload_image():
    global uploaded_image
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if path:
        uploaded_image = Image.open(path)
        uploaded_image.thumbnail((200, 200))  # Resize for preview
        img_preview = ImageTk.PhotoImage(uploaded_image)
        image_label.config(image=img_preview)
        image_label.image = img_preview

upload_btn = tk.Button(mainframe, text="Upload Photo", command=upload_image, font=("Helvetica", 14), bg="goldenrod")
upload_btn.place(x=20, y=100)

image_label = tk.Label(mainframe, bg="orange2")
image_label.place(x=400, y=20)

# ----------------- Run the App ----------------- #
window.mainloop()
