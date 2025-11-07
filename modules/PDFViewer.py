import tkinter as tk
from tkinter import filedialog # Picking a file

import fitz  # PyMuPDF
import threading
from PIL import Image, ImageTk  # For handling images in Tkinter

class PDFViewer(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg='#1e1e1e')
        
        # Create a canvas to render the PDF inside this frame
        self.canvas = tk.Canvas(self, bg='#1e1e1e', bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Add left and right navigation buttons inside the frame
        self.left_button = tk.Button(self, text="<", command=self.go_previous_page, bg='#333', fg='white', font=('Arial', 14))
        self.left_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.right_button = tk.Button(self, text=">", command=self.go_next_page, bg='#333', fg='white', font=('Arial', 14))
        self.right_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Load button to open the PDF file inside the frame
        self.load_button = tk.Button(self, text="Load PDF", command=self.load_pdf, bg='#333', fg='white', font=('Arial', 14))
        self.load_button.pack(pady=20)

        # Store the original image to scale it later
        self.original_img = None
        self.original_width = 0
        self.original_height = 0
        self.scaled_img = None
        self.scaled_width = 0
        self.scaled_height = 0

        # Current page number
        self.page_num = 0

        # Bind arrow keys for navigation
        self.master.bind("<Left>", self.go_previous_page)
        self.master.bind("<Right>", self.go_next_page)

        # Bind resize event
        self.master.bind("<Configure>", self.on_resize)

        self.grid(row=0, column=0, sticky='news')

    def load_pdf(self):
        # Open a file dialog to choose a PDF
        file_path = tk.filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            # Open the PDF with PyMuPDF
            self.pdf_document = fitz.open(file_path)
            self.page_num = 0
            # Start a background thread to render the first page
            threading.Thread(target=self.render_page, daemon=True).start()

    def render_page(self):
        # This function runs in a background thread to load the page and render it
        if self.pdf_document:
            if 0 <= self.page_num < len(self.pdf_document):
                page = self.pdf_document.load_page(self.page_num)
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

                # Store original image and its dimensions
                self.original_img = img
                self.original_width = img.width
                self.original_height = img.height

                # Resize image based on the current canvas size
                self.resize_image()

    def resize_image(self):
        if self.original_img:
            # Get current canvas size
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            # Calculate the aspect ratio of the original image
            aspect_ratio = self.original_width / self.original_height

            # Resize logic that ensures the image scales proportionally
            if canvas_width / canvas_height > aspect_ratio:
                # Width is the limiting factor (resize based on height)
                new_height = canvas_height
                new_width = int(new_height * aspect_ratio)
            else:
                # Height is the limiting factor (resize based on width)
                new_width = canvas_width
                new_height = int(new_width / aspect_ratio)

            # Resize the image to match the canvas size
            img_resized = self.original_img.resize((new_width, new_height), Image.LANCZOS)

            # Store the resized image
            self.scaled_img = img_resized
            self.scaled_width = new_width
            self.scaled_height = new_height

            # Convert the resized image to Tkinter format
            img_tk = ImageTk.PhotoImage(img_resized)

            # Update the canvas with the resized image
            self.after(0, self.update_canvas, img_tk)

    def update_canvas(self, img_tk):
        # Update the canvas with the rendered image
        self.canvas.create_image(0, 0, image=img_tk, anchor=tk.NW)
        self.img = img_tk  # Keep a reference to prevent garbage collection

    def go_previous_page(self, event=None):
        # Go to the previous page, if possible
        if self.pdf_document and self.page_num > 0:
            self.page_num -= 1
            threading.Thread(target=self.render_page, daemon=True).start()

    def go_next_page(self, event=None):
        # Go to the next page, if possible
        if self.pdf_document and self.page_num < len(self.pdf_document) - 1:
            self.page_num += 1
            threading.Thread(target=self.render_page, daemon=True).start()

    def on_resize(self, event):
        # This method is called when the window is resized
        if self.original_img:
            # Get current canvas size
            canvas_width = event.width
            canvas_height = event.height

            # Calculate the aspect ratio of the original image
            aspect_ratio = self.original_width / self.original_height

            # Resize logic that ensures the image scales proportionally
            if canvas_width / canvas_height > aspect_ratio:
                # Width is the limiting factor (resize based on height)
                new_height = canvas_height
                new_width = int(new_height * aspect_ratio)
            else:
                # Height is the limiting factor (resize based on width)
                new_width = canvas_width
                new_height = int(new_width / aspect_ratio)

            # Resize the image to match the canvas size
            img_resized = self.original_img.resize((new_width, new_height), Image.LANCZOS)

            # Store the resized image
            self.scaled_img = img_resized
            self.scaled_width = new_width
            self.scaled_height = new_height

            # Convert the resized image to Tkinter format
            img_tk = ImageTk.PhotoImage(img_resized)

            # Update the canvas with the resized image
            self.after(0, self.update_canvas, img_tk)
