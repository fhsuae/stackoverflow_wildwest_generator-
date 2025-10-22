import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont, ExifTags


class WildWestPosterGenerator:
    def __init__(self):
        # Window Setup
        self.window = tk.Tk()
        self.window.title("Wild West Poster Generator - ")
        self.window.geometry("1200x800")
        self.window.config(bg="#2D1A0C")  # Dark brown background
        # self.window.eval('tk::PlaceWindow . center')  # Center window
        self.window.state('zoomed')

        # Initialize variables
        self.original_image = None
        self.processed_image = None
        self.preview_image = None
        self.selected_template = tk.StringVar(value="classic")
        self.user_name = tk.StringVar()
        self.user_location = tk.StringVar()

        # Build interface
        self.create_interface()

    # ------------------------- Interface -------------------------
    def create_interface(self):
        """Build GUI with Western styling"""
        # Header
        header_frame = tk.Frame(self.window, bg="#8B4513", height=100)
        header_frame.pack(fill="x", padx=10, pady=5)
        header_frame.pack_propagate(False)
        tk.Label(header_frame, text="WILD WEST POSTER GENERATOR", font=("Old English Text MT", 28, "bold"),
                 fg="#FFD700", bg="#8B4513").pack(expand=True)
        tk.Label(header_frame, text="Create Your Own Wild West Immersion", font=("Georgia", 12, "italic"),
                 fg="#F5DEB3", bg="#8B4513").pack(pady=(0, 10))

        # Main Frame
        main_frame = tk.Frame(self.window, bg="#2D1A0C")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left controls panel
        left_frame = tk.Frame(main_frame, bg="#3D2818", width=400, relief="ridge", bd=2)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        left_frame.pack_propagate(False)
        self.create_controls(left_frame)

        # Right preview panel
        right_frame = tk.Frame(main_frame, bg="#1A0F08", width=700, relief="ridge", bd=2)
        right_frame.pack(side="right", fill="both", expand=True)
        right_frame.pack_propagate(False)
        self.create_preview(right_frame)

    # ------------------------- Controls -------------------------
    def create_controls(self, parent):
        """Left panel: user input and buttons"""
        tk.Label(parent, text="POSTER SETTINGS", font=("Georgia", 16, "bold"),
                 fg="#FFD700", bg="#3D2818").pack(pady=20)

        # Name
        self.create_label_entry(parent, "Name:", self.user_name)
        # Location
        self.create_label_entry(parent, "Location:", self.user_location)

        # Image upload
        tk.Label(parent, text="Upload Photo:", font=("Georgia", 12, "bold"),
                 fg="#F5DEB3", bg="#3D2818").pack(anchor="w", padx=20, pady=(20, 0))
        upload_btn = tk.Button(parent, text="Choose Image File", font=("Georgia", 11, "bold"),
                               bg="#8B4513", fg="white", relief="raised", bd=3, padx=20, pady=8,
                               command=self.upload_image)
        upload_btn.pack(pady=10)

        # Template selection
        tk.Label(parent, text="Select Template:", font=("Georgia", 12, "bold"),
                 fg="#F5DEB3", bg="#3D2818").pack(anchor="w", padx=20, pady=(20, 0))
        templates = [("Classic Wanted", "classic"), ("Vintage Poster", "vintage"), ("Gold Rush", "gold")]
        for text, mode in templates:
            rb = tk.Radiobutton(parent, text=text, variable=self.selected_template, value=mode,
                                font=("Georgia", 10), fg="#F5DEB3", bg="#3D2818", selectcolor="#8B4513",
                                activebackground="#3D2818", activeforeground="#FFD700")
            rb.pack(anchor="w", padx=20, pady=2)

        # Generate & Save buttons
        generate_btn = tk.Button(parent, text="GENERATE POSTER", font=("Georgia", 14, "bold"),
                                 bg="#B8860B", fg="white", relief="raised", bd=4, padx=30, pady=12,
                                 command=self.generate_poster)
        generate_btn.pack(pady=30)

        save_btn = tk.Button(parent, text="SAVE POSTER", font=("Georgia", 12, "bold"),
                             bg="#CD853F", fg="white", relief="raised", bd=3, padx=20, pady=8,
                             command=self.save_poster)
        save_btn.pack(pady=10)

    def create_label_entry(self, parent, label_text, text_var):
        """Helper to create label + entry"""
        frame = tk.Frame(parent, bg="#3D2818")
        frame.pack(fill="x", padx=20, pady=10)
        tk.Label(frame, text=label_text, font=("Georgia", 12, "bold"),
                 fg="#F5DEB3", bg="#3D2818").pack(anchor="w")
        entry = tk.Entry(frame, textvariable=text_var, font=("Georgia", 12),
                         bg="#F5DEB3", fg="#2D1A0C", width=30)
        entry.pack(fill="x", pady=5)

    # ------------------------- Preview -------------------------
    def create_preview(self, parent):
        """Right panel for poster preview"""
        tk.Label(parent, text="POSTER PREVIEW", font=("Georgia", 16, "bold"),
                 fg="#FFD700", bg="#1A0F08").pack(pady=20)

        self.preview_frame = tk.Frame(parent, bg="#8B4513", relief="sunken", bd=3, width=600, height=500)
        self.preview_frame.pack(pady=20, padx=50, fill="both", expand=True)
        self.preview_frame.pack_propagate(False)

        self.preview_label = tk.Label(self.preview_frame,
                                      text="Your poster will appear here\n\nUpload an image and click 'Generate Poster'",
                                      font=("Georgia", 14), fg="#F5DEB3", bg="#8B4513", justify="center")
        self.preview_label.pack(expand=True, fill="both")

        tk.Label(parent, text="Tip: For best results, use square images (1:1 ratio)",
                 font=("Georgia", 10, "italic"), fg="#CD853F", bg="#1A0F08").pack(pady=10)

    # ------------------------- Image Upload -------------------------
    def upload_image(self):
        """Upload image and correct orientation"""
        file_path = filedialog.askopenfilename(title="Select an image",
                                               filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")])
        if file_path:
            try:
                img = Image.open(file_path)
                img = self.correct_orientation(img)
                self.original_image = img
                self.show_preview(img)
                messagebox.showinfo("Success", "Image uploaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open image: {str(e)}")

    def correct_orientation(self, image):
        """Correct image orientation using EXIF data"""
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = dict(image._getexif().items())
            if exif[orientation] == 3:
                image = image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                image = image.rotate(270, expand=True)
            elif exif[orientation] == 8:
                image = image.rotate(90, expand=True)
        except:
            pass
        return image

    def show_preview(self, image):
        """Show resized preview in GUI"""
        preview_size = (self.preview_frame.winfo_width(), self.preview_frame.winfo_height())
        img_copy = image.copy()
        img_copy.thumbnail(preview_size, Image.Resampling.LANCZOS)
        self.preview_image = ImageTk.PhotoImage(img_copy)
        self.preview_label.config(image=self.preview_image, text="")

    # ------------------------- Poster Generation -------------------------
    def generate_poster(self):
        """Generate poster with selected template"""
        if not self.original_image:
            messagebox.showwarning("Warning", "Please upload an image first!")
            return
        if not self.user_name.get() or not self.user_location.get():
            messagebox.showwarning("Warning", "Please enter both name and location!")
            return

        try:
            poster = self.original_image.copy()
            template = self.selected_template.get()
            if template == "classic":
                poster = self.apply_classic_style(poster)
            elif template == "vintage":
                poster = self.apply_vintage_style(poster)
            elif template == "gold":
                poster = self.apply_gold_style(poster)

            self.processed_image = poster
            self.show_preview(poster)
            messagebox.showinfo("Success", "Poster generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate poster: {str(e)}")

    def get_font(self, size, bold=False):
        """Get font with fallback options"""
        font_paths = [
            "old-english.ttf",
            "times.ttf",
            "timesbd.ttf",
            "arial.ttf",
            "arialbd.ttf",
            "/System/Library/Fonts/Times.ttc",
            "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
        ]

        try:
            if bold:
                # Try bold fonts first
                for path in ["timesbd.ttf", "arialbd.ttf", "georgiab.ttf"]:
                    try:
                        return ImageFont.truetype(path, size)
                    except:
                        continue
            # Try regular fonts
            for path in font_paths:
                try:
                    return ImageFont.truetype(path, size)
                except:
                    continue
        except:
            pass

        # Final fallback - use default font but with size scaling
        try:
            return ImageFont.load_default()
        except:
            # Ultimate fallback
            return ImageFont.load_default()

    # ------------------------- Poster Styles -------------------------
    def apply_classic_style(self, image):
        """Classic 'WANTED' poster style"""
        if image.mode != 'RGB':
            image = image.convert('RGB')
        width, height = image.size

        # Create larger poster with more space for text
        new_width, new_height = width + 120, height + 325
        poster = Image.new('RGB', (new_width, new_height), '#8B4513')
        poster.paste(image, (50, 125))  # Move image down to make room for larger header

        draw = ImageDraw.Draw(poster)

        # Get fonts with proper sizes - using our new font loading method
        wanted_font = self.get_font(80)  # Very large for WANTED
        dead_or_alive_font = self.get_font(28, bold=True)  # Bold for DEAD OR ALIVE
        name_font = self.get_font(26)  # Medium for name
        location_font = self.get_font(22)  # Smaller for location
        reward_font = self.get_font(32, bold=True)  # Bold for REWARD
        amount_font = self.get_font(42, bold=True)  # Largest for the amount

        # Text layout with proper font sizes:
        # 1. Big WANTED at the top
        self.draw_centered_text(draw, "WANTED", new_width // 2, 40, wanted_font, "#FFD700")

        # 2. DEAD OR ALIVE slightly below
        self.draw_centered_text(draw, "DEAD OR ALIVE", new_width // 2, 90, dead_or_alive_font,
                                "#FF0000")  # Red for emphasis

        # 3. User image (already placed)

        # 4. Name and location below image
        self.draw_centered_text(draw, self.user_name.get(), new_width // 2, height + 130, name_font, "white")
        self.draw_centered_text(draw, f"Last seen in {self.user_location.get()}", new_width // 2, height + 170,
                                location_font, "white")

        # 5. REWARD header
        self.draw_centered_text(draw, "REWARD", new_width // 2, height + 220, reward_font, "#FFD700")

        # 6. Large reward amount
        self.draw_centered_text(draw, "$2,000,000", new_width // 2, height + 270, amount_font, "#FFD700")

        return poster

    def apply_vintage_style(self, image):
        """Vintage poster style with sepia effect"""
        sepia = self.apply_sepia_filter(image)
        width, height = sepia.size
        border_size = 50
        vintage_bg = Image.new('RGB', (width + border_size * 2, height + border_size * 2), '#5D4037')
        vintage_bg.paste(sepia, (border_size, border_size))
        draw = ImageDraw.Draw(vintage_bg)

        # Use different font sizes for vintage style
        title_font = self.get_font(36, bold=True)
        subtitle_font = self.get_font(24)

        self.draw_centered_text(draw, f"{self.user_name.get()}",
                                width // 2 + border_size, height + border_size + 10, title_font, "#D7CCC8")
        self.draw_centered_text(draw, f"{self.user_location.get()}",
                                width // 2 + border_size, height + border_size + 50, subtitle_font, "#BCAAA4")
        return vintage_bg

    def apply_gold_style(self, image):
        """Gold Rush poster style with border and gold overlay"""
        width, height = image.size

        # Base poster with gold background and brown border
        gold_bg = Image.new('RGB', (width + 80, height + 150), '#FFD700')
        border = Image.new('RGB', (width + 60, height + 130), '#8B4513')
        gold_bg.paste(border, (10, 10))
        gold_bg.paste(image, (30, 30))

        # Apply gold filter overlay
        overlay = Image.new('RGB', gold_bg.size, (255, 215, 0))  # Gold color
        gold_bg = Image.blend(gold_bg, overlay, alpha=0.2)  # 20% gold tint

        draw = ImageDraw.Draw(gold_bg)

        # Fonts
        title_font = self.get_font(36, bold=True)
        text_font = self.get_font(28, bold=True)  # Larger font for name

        # Add "GOLD RUSH" at bottom
        self.draw_centered_text(draw, "GOLD RUSH", gold_bg.width // 2, height + 80, title_font, "#8B4513")

        # Add user's name under the image
        self.draw_centered_text(draw, f"{self.user_name.get()}", gold_bg.width // 2, height + 40, text_font, "#8B4513")

        return gold_bg

    def apply_sepia_filter(self, image):
        """Apply sepia color filter to give the image a warm, vintage look"""

        # Ensure the image is in RGB mode (3 color channels: Red, Green, Blue)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Make a copy so the original image isn't modified
        sepia = image.copy()

        # Access the pixel data of the image
        pixels = sepia.load()

        # Loop through every pixel in the image
        for i in range(sepia.width):
            for j in range(sepia.height):
                r, g, b = pixels[i, j]  # Get original red, green, blue values

                # Apply the sepia formula to calculate new RGB values
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)  # New red value
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)  # New green value
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)  # New blue value

                pixels[i, j] = (min(255, tr), min(255, tg), min(255, tb))

        # Return the sepia-toned image
        return sepia

    # ------------------------- Helpers -------------------------
    def draw_centered_text(self, draw, text, x, y, font, color):
        """Draw centered text"""
        draw.text((x, y), text, font=font, fill=color, anchor="mt")

    # ------------------------- Save Poster -------------------------
    def save_poster(self):
        """Save generated poster"""
        if not self.processed_image:
            messagebox.showwarning("Warning", "Please generate a poster first!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg"),
                                                            ("All files", "*.*")])
        if file_path:
            try:
                self.processed_image.save(file_path)
                messagebox.showinfo("Success", f"Poster saved successfully!\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save poster: {str(e)}")

    # ------------------------- Run GUI -------------------------
    def run(self):
        self.window.mainloop()


# ------------------------- Main -------------------------
if __name__ == "__main__":
    app = WildWestPosterGenerator()
    app.run()