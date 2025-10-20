import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import os

class WildWestPosterGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Wild West Poster Generator")
        self.root.geometry("1000x700")
        self.root.configure(bg='#F5F5DC')
        
        # Initialize variables
        self.original_image = None
        self.processed_image = None
        self.photo_image = None
        self.selected_template = "wanted"
        
        # Create the interface
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#8B4513', height=80)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Wild West Poster Generator",
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#8B4513'
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Create your own wanted poster in the style of the Old West",
            font=('Arial', 12, 'italic'),
            fg='#F5DEB3',
            bg='#8B4513'
        )
        subtitle_label.pack(expand=True)
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='#F5F5DC')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel - Controls
        controls_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        controls_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Name input
        name_frame = tk.Frame(controls_frame, bg='white')
        name_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            name_frame,
            text="Name:",
            font=('Arial', 11, 'bold'),
            bg='white'
        ).pack(anchor='w')
        
        self.name_var = tk.StringVar()
        self.name_var.trace('w', self.update_preview)
        name_entry = tk.Entry(
            name_frame,
            textvariable=self.name_var,
            font=('Arial', 11),
            width=25
        )
        name_entry.pack(fill='x', pady=(5, 0))
        
        # Location input
        location_frame = tk.Frame(controls_frame, bg='white')
        location_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            location_frame,
            text="Location:",
            font=('Arial', 11, 'bold'),
            bg='white'
        ).pack(anchor='w')
        
        self.location_var = tk.StringVar()
        self.location_var.trace('w', self.update_preview)
        location_entry = tk.Entry(
            location_frame,
            textvariable=self.location_var,
            font=('Arial', 11),
            width=25
        )
        location_entry.pack(fill='x', pady=(5, 0))
        
        # Photo upload
        photo_frame = tk.Frame(controls_frame, bg='white')
        photo_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            photo_frame,
            text="Upload Photo:",
            font=('Arial', 11, 'bold'),
            bg='white'
        ).pack(anchor='w')
        
        upload_btn = tk.Button(
            photo_frame,
            text="Choose Image",
            command=self.upload_image,
            font=('Arial', 10),
            bg='#8B4513',
            fg='white',
            relief='raised'
        )
        upload_btn.pack(fill='x', pady=(5, 0))
        
        # Template selection
        template_frame = tk.Frame(controls_frame, bg='white')
        template_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            template_frame,
            text="Select Template:",
            font=('Arial', 11, 'bold'),
            bg='white'
        ).pack(anchor='w')
        
        # Template buttons
        templates_frame = tk.Frame(template_frame, bg='white')
        templates_frame.pack(fill='x', pady=(5, 0))
        
        self.template_var = tk.StringVar(value="wanted")
        self.template_var.trace('w', self.update_preview)
        
        templates = [
            ("Wanted Poster", "wanted"),
            ("Sheriff's Notice", "sheriff"),
            ("Reward Poster", "reward"),
            ("Wild West Show", "show")
        ]
        
        for text, value in templates:
            rb = tk.Radiobutton(
                templates_frame,
                text=text,
                variable=self.template_var,
                value=value,
                command=self.update_preview,
                bg='white',
                font=('Arial', 10)
            )
            rb.pack(anchor='w', pady=2)
        
        # Action buttons
        actions_frame = tk.Frame(controls_frame, bg='white')
        actions_frame.pack(fill='x', padx=10, pady=20)
        
        generate_btn = tk.Button(
            actions_frame,
            text="Generate Poster",
            command=self.generate_poster,
            font=('Arial', 12, 'bold'),
            bg='#D2691E',
            fg='white',
            relief='raised',
            height=2
        )
        generate_btn.pack(fill='x', pady=5)
        
        download_btn = tk.Button(
            actions_frame,
            text="Download Poster",
            command=self.download_poster,
            font=('Arial', 12, 'bold'),
            bg='#CD853F',
            fg='white',
            relief='raised',
            height=2
        )
        download_btn.pack(fill='x', pady=5)
        
        # Right panel - Preview
        preview_frame = tk.Frame(main_frame, bg='white', relief='sunken', bd=2)
        preview_frame.pack(side='right', fill='both', expand=True)
        
        tk.Label(
            preview_frame,
            text="Preview",
            font=('Arial', 16, 'bold'),
            bg='white'
        ).pack(pady=10)
        
        # Preview canvas
        self.preview_canvas = tk.Canvas(
            preview_frame,
            bg='#f0f0f0',
            width=500,
            height=400,
            relief='sunken',
            bd=1
        )
        self.preview_canvas.pack(pady=10, padx=10)
        
        # Preview text elements
        self.name_text_id = self.preview_canvas.create_text(
            250, 100,
            text="YOUR NAME HERE",
            font=('Times New Roman', 24, 'bold'),
            fill='white',
            width=400
        )
        
        self.location_text_id = self.preview_canvas.create_text(
            250, 300,
            text="LOCATION",
            font=('Times New Roman', 16),
            fill='white',
            width=400
        )
        
        # Status label
        self.status_label = tk.Label(
            preview_frame,
            text="Upload a photo and customize your poster",
            font=('Arial', 10),
            bg='white',
            fg='#666666'
        )
        self.status_label.pack(pady=10)
        
        # Set initial template
        self.apply_template_style("wanted")
        
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                # Resize image to fit preview
                self.original_image.thumbnail((400, 300), Image.Resampling.LANCZOS)
                self.update_preview()
                self.status_label.config(text="Image uploaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {str(e)}")
    
    def apply_template_style(self, template):
        colors = {
            "wanted": "#8B4513",
            "sheriff": "#5D4037", 
            "reward": "#D2691E",
            "show": "#CD853F"
        }
        
        font_sizes = {
            "wanted": (24, 16),
            "sheriff": (22, 14),
            "reward": (26, 17),
            "show": (23, 15)
        }
        
        # Update canvas background
        self.preview_canvas.configure(bg=colors.get(template, "#8B4513"))
        
        # Update text fonts
        name_size, location_size = font_sizes.get(template, (24, 16))
        self.preview_canvas.itemconfig(
            self.name_text_id, 
            font=('Times New Roman', name_size, 'bold')
        )
        self.preview_canvas.itemconfig(
            self.location_text_id,
            font=('Times New Roman', location_size)
        )
    
    def update_preview(self, *args):
        # Update text
        name = self.name_var.get() or "YOUR NAME HERE"
        location = self.location_var.get() or "LOCATION"
        
        self.preview_canvas.itemconfig(self.name_text_id, text=name)
        self.preview_canvas.itemconfig(self.location_text_id, text=location)
        
        # Update template style
        template = self.template_var.get()
        self.apply_template_style(template)
        
        # Update image if available
        if self.original_image:
            self.processed_image = self.apply_image_effects(
                self.original_image.copy(), 
                template
            )
            self.photo_image = ImageTk.PhotoImage(self.processed_image)
            
            # Clear previous image
            self.preview_canvas.delete("image")
            
            # Add new image to canvas
            self.preview_canvas.create_image(
                250, 200,
                image=self.photo_image,
                tags="image"
            )
    
    def apply_image_effects(self, image, template):
        """Apply different effects based on template"""
        effects = {
            "wanted": {"sepia": 0.7, "contrast": 1.2},
            "sheriff": {"grayscale": 0.5, "sepia": 0.3},
            "reward": {"sepia": 0.5, "brightness": 0.9},
            "show": {"sepia": 0.4, "contrast": 1.1}
        }
        
        effect = effects.get(template, effects["wanted"])
        
        # Apply grayscale if specified
        if effect.get("grayscale"):
            image = image.convert("L")
            image = image.convert("RGB")
        
        # Apply sepia effect
        if effect.get("sepia"):
            # Simple sepia effect
            sepia = Image.new('RGB', image.size, (112, 66, 20))
            image = Image.blend(image, sepia, effect["sepia"])
        
        # Apply contrast
        if effect.get("contrast"):
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(effect["contrast"])
        
        # Apply brightness
        if effect.get("brightness"):
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(effect["brightness"])
        
        return image
    
    def generate_poster(self):
        if not self.original_image:
            messagebox.showwarning("Warning", "Please upload an image first!")
            return
        
        # Create final poster
        try:
            # Create a larger version for the final poster
            final_image = self.original_image.copy()
            final_image = final_image.resize((800, 600), Image.Resampling.LANCZOS)
            final_image = self.apply_image_effects(final_image, self.template_var.get())
            
            # In a complete implementation, you would add text overlays here
            # and save the final composition
            
            messagebox.showinfo("Success", "Poster generated successfully!\nClick 'Download Poster' to save it.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate poster: {str(e)}")
    
    def download_poster(self):
        if not self.processed_image:
            messagebox.showwarning("Warning", "Please generate a poster first!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
            title="Save Poster As"
        )
        
        if file_path:
            try:
                # Create final composition
                final_width, final_height = 800, 600
                final_image = Image.new('RGB', (final_width, final_height), '#8B4513')
                
                # Add processed image
                img = self.original_image.copy()
                img.thumbnail((500, 400), Image.Resampling.LANCZOS)
                img = self.apply_image_effects(img, self.template_var.get())
                
                # Calculate position to center the image
                x = (final_width - img.width) // 2
                y = (final_height - img.height) // 2 - 50
                final_image.paste(img, (x, y))
                
                # Save the image
                final_image.save(file_path)
                messagebox.showinfo("Success", f"Poster saved as:\n{file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not save poster: {str(e)}")

def main():
    root = tk.Tk()
    app = WildWestPosterGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()