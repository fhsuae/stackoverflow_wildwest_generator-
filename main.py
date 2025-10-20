# Starts the window
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

# Window Setup

window = tk.Tk()
window.title("Wild West Poster Generator")
window.geometry("1080x720")
window.config(bg="orange2")

# Main frame to hold GUI elements
mainframe = tk.Frame(window, width=1060, height=700, bg="orange2")
mainframe.pack(padx=10, pady=10)


# Name and Location Input

tk.Label(mainframe, text="Enter Name:", bg="orange2", font=("Helvetica", 14)).place(x=20, y=20)
name_entry = tk.Entry(mainframe, width=30, font=("Helvetica", 14))
name_entry.place(x=150, y=20)

tk.Label(mainframe, text="Enter Location:", bg="orange2", font=("Helvetica", 14)).place(x=20, y=60)
location_entry = tk.Entry(mainframe, width=30, font=("Helvetica", 14))
location_entry.place(x=150, y=60)


# Upload Image and Preview

uploaded_image = None


def upload_image():
    """Allow user to upload an image and show a preview."""
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


# Generate Poster with Border and Preview

def generate_poster():
    """Generate poster with border, name, location, and preview."""
    if not uploaded_image:
        print("No image uploaded yet!")
        return

    # Copy the uploaded image to create poster
    poster = uploaded_image.copy()
    poster = poster.convert("RGB")
    draw = ImageDraw.Draw(poster)
    w, h = poster.size

    # Draw simple brown border
    border_thickness = 5
    for i in range(border_thickness):
        draw.rectangle([i, i, w - i, h - i], outline="brown")

    # Add name and location text
    font = ImageFont.load_default()
    draw.text((10, h - 40), f"WANTED: {name_entry.get()}", fill="red", font=font)
    draw.text((10, h - 20), f"LOCATION: {location_entry.get()}", fill="yellow", font=font)

    # Save poster to file
    poster.save("poster.jpg")

    # Show poster in GUI
    poster_img = ImageTk.PhotoImage(poster)
    poster_label.config(image=poster_img)
    poster_label.image = poster_img
    print("Poster generated and saved as poster.jpg")


generate_btn = tk.Button(mainframe, text="Generate Poster", command=generate_poster, font=("Helvetica", 16), bg="red",
                         fg="white")
generate_btn.place(x=20, y=150)

# Label to preview generated poster
poster_label = tk.Label(mainframe, bg="orange2")
poster_label.place(x=400, y=300)

# ----------------- Run the App ----------------- #
window.mainloop()
