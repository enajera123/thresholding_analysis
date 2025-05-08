import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import os


class ImageProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        self.root.geometry("1200x700")
        self.image_path = None
        self.original_image = None
        self.processed_image = None
        self.create_interface()

    def create_interface(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        btn_frame = ttk.Frame(main_frame, padding="5")
        btn_frame.pack(fill=tk.X, pady=10)
        load_btn = ttk.Button(btn_frame, text="Load Image", command=self.load_image)
        load_btn.pack(side=tk.LEFT, padx=5)
        process_btn = ttk.Button(
            btn_frame, text="Process Image", command=self.process_image
        )
        process_btn.pack(side=tk.LEFT, padx=5)
        img_frame = ttk.Frame(main_frame)
        img_frame.pack(fill=tk.BOTH, expand=True)
        original_frame = ttk.LabelFrame(img_frame, text="Original Image", padding="10")
        original_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.canvas_original = tk.Canvas(original_frame, bg="lightgray")
        self.canvas_original.pack(fill=tk.BOTH, expand=True)
        processed_frame = ttk.LabelFrame(
            img_frame, text="Processed Image", padding="10"
        )
        processed_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.canvas_processed = tk.Canvas(processed_frame, bg="lightgray")
        self.canvas_processed.pack(fill=tk.BOTH, expand=True)
        img_frame.grid_columnconfigure(0, weight=1)
        img_frame.grid_columnconfigure(1, weight=1)
        img_frame.grid_rowconfigure(0, weight=1)
        self.status_label = ttk.Label(main_frame, text="Ready to load an image")
        self.status_label.pack(pady=5)

    def load_image(self):
        filetypes = [
            ("Images", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.gif"),
            ("All files", "*.*"),
        ]
        path = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)
        if path:
            self.image_path = path
            self.status_label.config(text=f"Image loaded: {os.path.basename(path)}")
            self.original_image = cv2.imread(path)
            self.display_original_image()
            self.canvas_processed.delete("all")
            self.processed_image = None

    def display_original_image(self):
        if self.original_image is not None:
            rgb_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            resized_image = self.resize_image(rgb_image, self.canvas_original)
            pil_image = Image.fromarray(resized_image)
            self.tk_original_image = ImageTk.PhotoImage(pil_image)
            self.canvas_original.delete("all")
            self.canvas_original.create_image(
                self.canvas_original.winfo_width() // 2,
                self.canvas_original.winfo_height() // 2,
                image=self.tk_original_image,
                anchor=tk.CENTER,
            )

    def process_image(self):
        if self.image_path is None:
            self.status_label.config(text="Error: You must load an image first")
            return

        try:
            self.status_label.config(text="Processing image...")
            self.processed_image = self.mark_concentration_area(self.original_image)
            self.display_processed_image()
            self.status_label.config(text="Image processed successfully")
        except Exception as e:
            self.status_label.config(text=f"Error processing the image: {str(e)}")

    def display_processed_image(self):
        if self.processed_image is not None:
            resized_image = self.resize_image(
                self.processed_image, self.canvas_processed
            )
            pil_image = Image.fromarray(resized_image)
            self.tk_processed_image = ImageTk.PhotoImage(pil_image)
            self.canvas_processed.delete("all")
            self.canvas_processed.create_image(
                self.canvas_processed.winfo_width() // 2,
                self.canvas_processed.winfo_height() // 2,
                image=self.tk_processed_image,
                anchor=tk.CENTER,
            )

    def resize_image(self, image, canvas):
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        if canvas_width <= 1:
            canvas_width = 500
        if canvas_height <= 1:
            canvas_height = 400
        height, width = image.shape[:2]
        aspect_ratio = width / height
        if canvas_width / canvas_height > aspect_ratio:
            new_height = canvas_height
            new_width = int(new_height * aspect_ratio)
        else:
            new_width = canvas_width
            new_height = int(new_width / aspect_ratio)
        return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    def mark_concentration_area(self, image):
        if len(image.shape) == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = image.copy()
        smoothed_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        _, threshold_image = cv2.threshold(smoothed_image, 127, 255, cv2.THRESH_BINARY)
        edges = cv2.Canny(threshold_image, 50, 150)
        contours, _ = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        if len(image.shape) == 3:
            contour_image = image.copy()
        else:
            contour_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
        return cv2.cvtColor(contour_image, cv2.COLOR_BGR2RGB)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessor(root)
    root.mainloop()
