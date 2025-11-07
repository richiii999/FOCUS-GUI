import tkinter as tk
from tkinter import simpledialog

import SLMResponse

class ChatWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master) # required idk

        # Chat area
        self.chat_area = tk.Text(master, wrap="word", height=15, width=40, bg="white", fg="black", state=tk.DISABLED, font=("Arial", 16, "bold"))
        self.chat_area.grid(row=0, columnspan=2, sticky="news")
        self.chat_area.tag_configure("right_align", justify="right")

        # Input box
        self.message_input = tk.Entry(master, width=40, bg="lightgray", font=("Arial", 16, "bold"))
        self.message_input.grid(row=1, padx=5, pady=5, column=0, sticky="news")
        self.message_input.bind('<Return>', lambda event: self.send_message(self.message_input.get()))

        # Send button
        self.send_button = tk.Button(master, text="-->", width=5, font=("Arial", 16, "bold"), command=lambda: self.send_message(self.message_input.get()))
        self.send_button.grid(row=1, column=1, padx=5, pady=5, sticky="news")
        
        # Place self within parent
        self.grid(column=0, row=0, sticky='news')

        # Initilize chat session on startup
        self.start_chat() 
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, "AI: I'm a helpful AI assistant tool and I'm here to assist you with whatever you need." + "\n\n")

    # User input
    def send_message(self, message, visible=True):
        SLMResponse.StartChatting()
        if message.strip(): # Only send if the message is not empty
            self.chat_area.config(state=tk.NORMAL) # Enable chat_area to insert message
            
            if visible: self.chat_area.insert(tk.END, "You: " + message + "\n\n", "right_align")
            
            response = SLMResponse.Chatting(message)
            
            self.chat_area.insert(tk.END, "AI: " + response + "\n\n") # Display AI response in chat_area

            self.chat_area.config(state=tk.DISABLED)  # Make chat_area read-only again
            self.message_input.delete(0, tk.END)  # Clear the input field

            print(f"Message Sent: {message}")
            print(f"AI Response: {response}")

    def start_chat(self):
        """Initiates the chat session and loads the available models."""
        models = SLMResponse.StartChatting()  # Fetch the available models from the container
        model_num = tk.simpledialog.askstring("Model Selection", f"Select a model: {models}")
        SLMResponse.StartChatting(model_num)  # Set the selected model

    # Display "Hello" for 3 seconds
    def Hello(self):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, "Hello\n")
        self.chat_area.config(state=tk.DISABLED)
        master.after(3000, clear_message)

    # Function to clear the message after 3 seconds
    def clear_message(self):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete("end-1c linestart", "end-1c lineend")  # Deletes the last line (the "Hello" message)
        self.chat_area.config(state=tk.DISABLED)

