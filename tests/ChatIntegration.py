import sys
sys.path.append("./tests")  # Test scripts use modules too (run from toplevel tho)

import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
from modules import PDFViewer
import SLMResponse
from SLMResponse import Chatting, StartChatting

root = tk.Tk()
root.title("FOCUS")
root.geometry('800x600')

## Declare functions
# Function to send message
def send_message(message, visible=True):
    StartChatting()
    if message.strip():  # Only send if the message is not empty
        # Enable chat_area to insert message
        chat_area.config(state=tk.NORMAL)
        
        if visible:
            chat_area.insert(tk.END, "You: " + message + "\n\n", "right_align")  # Use the right_align tag for user messages
            #insert_separator_line()
        
        # Call the Chatting function to get the AI response
        response = Chatting(message)  # Assuming Chatting() handles user input and gives a response
        
        # Display AI response in chat_area
        chat_area.insert(tk.END, "AI: " + response + "\n\n")  # AI messages will stay left-aligned

        # Insert a dynamically sized horizontal line
        #insert_separator_line()

        chat_area.config(state=tk.DISABLED)  # Make chat_area read-only again
        message_input.delete(0, tk.END)  # Clear the input field

        print(f"Message Sent: {message}")
        print(f"AI Response: {response}")

# Configure the 'right_align' tag for right-aligned text
chat_area.tag_configure("right_align", justify="right")

# Function to insert a dynamically sized separator line based on the width of the chat area
def insert_separator_line():
    # Get the width of the chat_area in pixels
    width = chat_area.winfo_width()
    
    # Estimate how many characters should fit in the given width.
    # We'll use the width of a single character in the current font
    font_size = int(chat_area.cget("font").split()[1])  # Extract font size
    character_width = font_size * 0.5  # Approximate pixel width of one character

    # Calculate number of characters that can fit in the width of the chat area
    num_chars = int(width // character_width)  # We use floor division to avoid partial characters

    # Insert a line of dashes that fit the width of the chat area
    chat_area.insert(tk.END, "-" * num_chars + "\n")

# Bind the Enter key to send the message
message_input.bind('<Return>', lambda event: send_message(message_input.get()))


# Start the chat by selecting the model
def start_chat():
    """Initiates the chat session and loads the available models."""
    models = SLMResponse.StartChatting()  # Fetch the available models from the container
    model_num = tk.simpledialog.askstring("Model Selection", f"Select a model: {models}")
    SLMResponse.StartChatting(model_num)  # Set the selected model


# Making the frames
Side1 = tk.Frame(root, width=400, height=400, bg="skyblue", relief='ridge', borderwidth=5)
Side1Label = tk.Label(Side1, text="Side1Label", bg="skyblue")

# Side2 Frame (Chat Window)
Side2 = tk.Frame(root, width=400, height=400, bg="skyblue", relief='ridge', borderwidth=5)
Side2Label = tk.Label(Side2, text="Chat Window", bg="skyblue")

# Chat components inside Side2
chat_area = tk.Text(Side2, wrap="word", height=15, width=40, bg="white", fg="black", state=tk.DISABLED, font=("Arial", 16, "bold"))
chat_area.grid(row=0, columnspan=2, sticky="news")

message_input = tk.Entry(Side2, width=40, bg="lightgray", font=("Arial", 16, "bold"))
message_input.grid(row=1, padx=5, pady=5, column=0, sticky="news")

# Using right arrow Unicode for the "Send" button
send_button = tk.Button(Side2, text="-->", width=5, font=("Arial", 16, "bold"), command=lambda: send_message(message_input.get()))
send_button.grid(row=1, column=1, padx=5, pady=5, sticky="news")

# Big Image frame
BigImg = tk.Frame(root, width=800, height=800, bg="grey", relief='ridge', borderwidth=5)
BigImgLabel = tk.Label(BigImg, text="BigImgLabel", bg="grey")

## Grid placement
# Root Grid
root.columnconfigure(0, weight=2)
root.rowconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

# BigImg
BigImg.grid(column=0, row=0, columnspan=1, rowspan=2, sticky='news')
BigImg.columnconfigure(0, weight=2)
BigImg.rowconfigure(0, weight=2)
BigImgLabel.grid(column=0, row=0)

# PDFViewer
pdf_viewer = PDFViewer.PDFViewer(BigImg)
pdf_viewer.grid(column=0, row=0, sticky='news')

# Side1
Side1.grid(column=1, row=0, sticky='news')
Side1.columnconfigure(0, weight=1)
Side1.rowconfigure(0, weight=1)

Side1Label.grid(column=0, row=0)

# Action Buttons
AB = ActionButtons.ActionButtons(Side1)

# Side2 (Chat Window)
Side2.grid(column=1, row=1, sticky='news')
Side2.columnconfigure(0, weight=1)
Side2.rowconfigure(0, weight=1)

Side2Label.grid(column=0, row=0)

# Run the app
start_chat()  # Initiate chat session on startup
chat_area.config(state=tk.NORMAL)
chat_area.insert(tk.END, "AI: I'm a helpful AI assistant tool and I'm here to assist you with whatever you need." + "\n\n")

root.mainloop()
