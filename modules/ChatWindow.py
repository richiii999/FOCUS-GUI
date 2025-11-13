import tkinter as tk
from tkinter import simpledialog
import SLMResponse

class ChatWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Chat area (where we’ll also display the timer)
        self.chat_area = tk.Text(master, wrap="word", height=20, width=50,
                                 bg="black", fg="lime", state=tk.DISABLED,
                                 font=("Consolas", 18, "bold"))
        self.chat_area.grid(row=0, columnspan=2, sticky="news")
        self.chat_area.tag_configure("center", justify="center")
        self.chat_area.tag_configure("right_align", justify="right")

        # Input box
        self.message_input = tk.Entry(master, width=40, bg="gray20",
                                      fg="white", font=("Arial", 16, "bold"))
        self.message_input.grid(row=1, padx=5, pady=5, column=0, sticky="news")
        self.message_input.bind('<Return>', lambda event: self.send_message(self.message_input.get()))

        # Send button
        self.send_button = tk.Button(master, text="-->", width=5,
                                     font=("Arial", 16, "bold"),
                                     command=lambda: self.send_message(self.message_input.get()))
        self.send_button.grid(row=1, column=1, padx=5, pady=5, sticky="news")

        # Grid placement
        self.grid(column=0, row=0, sticky='news')

        # Start chat session
        self.start_chat()
        self._insert_ai("I'm a helpful AI assistant tool and I'm here to assist you with whatever you need.")

        # Timer setup
        self.timer_running = False
        self.time_left = 300  # 5 minutes in seconds
        self.total_time = 300

    def _insert_ai(self, text):
        """Helper to insert AI text in chat."""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"AI: {text}\n\n")
        self.chat_area.config(state=tk.DISABLED)

    def _insert_user(self, text):
        """Helper to insert user text right-aligned."""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"You: {text}\n\n", "right_align")
        self.chat_area.config(state=tk.DISABLED)

    # ---------------- TIMER ----------------
    def start_timer(self):
        """Starts the timer display in the chat window."""
        if not self.timer_running:
            self.timer_running = True
            self._show_timer()

    def _show_timer(self):
        """Updates the chat window with countdown and progress bar."""
        if self.timer_running and self.time_left > 0:
            mins, secs = divmod(self.time_left, 60)
            time_str = f"{mins:02}:{secs:02}"

            # Calculate progress bar width
            bar_length = 30  # characters wide
            filled = int(bar_length * (self.time_left / self.total_time))
            bar = "█" * filled + "░" * (bar_length - filled)

            # Update chat area
            self.chat_area.config(state=tk.NORMAL)
            self.chat_area.delete("1.0", tk.END)  # Clear chat area
            self.chat_area.insert(tk.END, f"\n\n\n⏰  {time_str}\n", "center")
            self.chat_area.insert(tk.END, f"{bar}\n\n", "center")
            self.chat_area.insert(tk.END, "Take a deep breath — your break timer is running...\n", "center")
            self.chat_area.config(state=tk.DISABLED)

            # Countdown
            self.time_left -= 1
            self.after(1000, self._show_timer)
        else:
            self.timer_running = False
            self.chat_area.config(state=tk.NORMAL)
            self.chat_area.delete("1.0", tk.END)
            self.chat_area.insert(tk.END, "\n\n\n🕒 Time’s up! Break finished.\n", "center")
            self.chat_area.config(state=tk.DISABLED)
    # ---------------- END TIMER ----------------

    def send_message(self, message, visible=True):
        SLMResponse.StartChatting()
        if message.strip():
            if visible:
                self._insert_user(message)

            response = SLMResponse.Chatting(message)
            self._insert_ai(response)
            self.message_input.delete(0, tk.END)

    def start_chat(self):
        models = SLMResponse.StartChatting()
        model_num = tk.simpledialog.askstring("Model Selection", f"Select a model: {models}")
        SLMResponse.StartChatting(model_num)

    def start_break(self, event=None):
        """Starts a 5-minute break timer and replaces chat with countdown."""
        self._insert_user("Give me a 5 minute break")
        self.start_timer()
