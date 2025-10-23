import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF
import threading
from PIL import Image, ImageTk  # For handling images in Tkinter

class PDFViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('PDF Viewer')
        self.geometry('800x600')

        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.load_button = tk.Button(self, text="Load PDF", command=self.load_pdf)
        self.load_button.pack()

        # Add left and right navigation buttons
        self.left_button = tk.Button(self, text="<", command=self.go_previous_page)
        self.left_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.right_button = tk.Button(self, text=">", command=self.go_next_page)
        self.right_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.pdf_document = None
        self.page_num = 0

        # Bind arrow keys to navigate between pages
        self.bind("<Left>", self.go_previous_page)
        self.bind("<Right>", self.go_next_page)

        # Bind the window resize event
        self.bind("<Configure>", self.on_resize)

        # Store the original image to scale it later
        self.original_img = None

    def load_pdf(self):
        # Open a file dialog to choose a PDF
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            # Open the PDF with PyMuPDF
            self.pdf_document = fitz.open(file_path)
            self.page_num = 0
            # Start a background thread to load and render the first page
            threading.Thread(target=self.render_page, daemon=True).start()

    def render_page(self):
        # This function runs in a background thread to load the page and render it
        if self.pdf_document:
            # Make sure the page number is valid
            if 0 <= self.page_num < len(self.pdf_document):
                page = self.pdf_document.load_page(self.page_num)
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

                # Store the original image to scale it later
                self.original_img = img

                # Convert the image to a format that Tkinter can handle
                img_tk = ImageTk.PhotoImage(img)
                # Use `after` to schedule the update on the Tkinter main thread
                self.after(0, self.update_canvas, img_tk)

    def update_canvas(self, img_tk):
        # This method is called from the main thread to update the canvas
        self.canvas.create_image(0, 0, image=img_tk, anchor=tk.NW)
        # Keep a reference to the image to prevent it from being garbage collected
        self.img = img_tk

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
            # Get the current size of the canvas
            canvas_width = event.width
            canvas_height = event.height

            # Scale the original image to fit the canvas size
            img_resized = self.original_img.resize((canvas_width, canvas_height), Image.LANCZOS)

            # Convert the resized image to a format that Tkinter can handle
            img_tk = ImageTk.PhotoImage(img_resized)
            
            # Update the canvas with the resized image
            self.after(0, self.update_canvas, img_tk)

if __name__ == "__main__":
    app = PDFViewer()
    app.mainloop()
