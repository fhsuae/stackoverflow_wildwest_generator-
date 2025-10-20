import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import time

class WildWestPosterGenerator:
    def __init__(self):
        # ----------------- Window Setup -----------------
        self.window = tk.Tk()
        self.window.title("Wild West Poster Generator")
        self.window.geometry("1080x720")
        self.window.config(bg="orange2")

        # Initialize variables
        self.uploaded_image = None
        self.user_name = tk.StringVar()
        self.user_location = tk.StringVar()
        self.processed_image = None

        # Create the interface
        self.create_interface()

    def create_interface(self):
        """Create main GUI components"""
        # Main frame
        mainframe = tk.Frame(self.window, width=1060, height=700, bg="orange2")
        mainframe.pack(padx=10, pady=10)

        # Name input
        tk.Label(mainframe, text="Enter Name:", bg="orange2", font=("Helvetica", 14)).place(x=20, y=20)
        tk.Entry(mainframe, textvariable=self.user_name, width=30, font=("Helvetica", 14)).place(x=150, y=20)

        # Location input
        tk.Label(mainframe, text="Enter Location:", bg="orange2", font=("Helvetica", 14)).place(x=20, y=60)
        tk.Entry(mainframe, textvariable=self.user_location, width=30, font=("Helvetica", 14)).place(x=150, y=60)

        # Upload image button
        upload_btn = tk.Button(mainframe, text="Upload Photo", command=self.upload_image, font=("Helvetica", 14),
                               bg="goldenrod")
        upload_btn.place(x=20, y=100)
        self.add_hover_effect(upload_btn, "goldenrod", "#DAA520")

        # Image preview label with placeholder text
        self.image_label = tk.Label(mainframe, bg="orange2", text="Image preview will appear here",
                                    font=("Helvetica", 12), width=25, height=10)
        self.image_label.place(x=400, y=20)

        # Generate poster button
        generate_btn = tk.Button(mainframe, text="Generate Poster", command=self.generate_poster, font=("Helvetica", 16),
                                 bg="red", fg="white")
        generate_btn.place(x=20, y=150)
        self.add_hover_effect(generate_btn, "red", "#B22222")

        # Poster preview label
        self.poster_label = tk.Label(mainframe, bg="orange2")
        self.poster_label.place(x=400, y=300)

    # ----------------- Button Hover Effect -----------------
    def add_hover_effect(self, button, normal_bg, hover_bg):
        """Change button color on hover"""
        button.bind("<Enter>", lambda e: button.config(bg=hover_bg))
        button.bind("<Leave>", lambda e: button.config(bg=normal_bg))

    # ----------------- Image Handling -----------------
    def upload_image(self):
        """Upload an image and show a small preview"""
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if path:
            if not path.lower().endswith((".png", ".jpg", ".jpeg")):
                messagebox.showerror("Error", "Please upload a valid image file")
                return
            try:
                self.uploaded_image = Image.open(path)
                self.uploaded_image.thumbnail((200, 200))
                img_preview = ImageTk.PhotoImage(self.uploaded_image)
                self.image_label.config(image=img_preview, text="")
                self.image_label.image = img_preview
                messagebox.showinfo("Success", "Image uploaded!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    # ----------------- Poster Generation -----------------
    def generate_poster(self):
        """Generate poster with border, text, and animated WANTED"""
        if not self.uploaded_image:
            messagebox.showwarning("Warning", "Please upload an image first!")
            return
        if not self.user_name.get() or not self.user_location.get():
            messagebox.showwarning("Warning", "Please enter both name and location!")
            return

        # Copy image and convert
        poster = self.uploaded_image.copy()
        poster = poster.convert("RGB")
        draw = ImageDraw.Draw(poster)
        w, h = poster.size

        # Add border
        border_thickness = 5
        for i in range(border_thickness):
            draw.rectangle([i, i, w - i, h - i], outline="brown")

        # ----------------- Animated WANTED Text -----------------
        font = ImageFont.load_default()
        for i in range(0, 15, 3):  # small animation
            temp_poster = poster.copy()
            temp_draw = ImageDraw.Draw(temp_poster)
            temp_draw.text((w // 2, 10 + i), "WANTED", fill="red", font=font, anchor="mt")
            temp_img = ImageTk.PhotoImage(temp_poster)
            self.poster_label.config(image=temp_img)
            self.poster_label.image = temp_img
            self.window.update()
            time.sleep(0.05)  # short delay for animation

        # ----------------- Final Poster Text -----------------
        draw.text((w // 2, h - 40), f"WANTED: {self.user_name.get()}", fill="red", font=font, anchor="mt")
        draw.text((w // 2, h - 20), f"LOCATION: {self.user_location.get()}", fill="yellow", font=font, anchor="mt")

        # Save poster
        poster.save("poster.jpg")
        self.processed_image = poster

        # Show final poster
        poster_img = ImageTk.PhotoImage(poster)
        self.poster_label.config(image=poster_img)
        self.poster_label.image = poster_img

        messagebox.showinfo("Success", "Poster generated and saved as poster.jpg")

    # ----------------- Run Application -----------------
    def run(self):
        self.window.mainloop()


# ----------------- Run -----------------
if __name__ == "__main__":
    app = WildWestPosterGenerator()
    app.run()
