import tkinter as tk
from tkinter import simpledialog
import SLMResponse

class ChatWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Chat area (monospace so ASCII art/stickman lines align)
        self.chat_area = tk.Text(master, wrap="word", height=20, width=60,
                                 bg="black", fg="lime", state=tk.DISABLED,
                                 font=("Consolas", 14))
        self.chat_area.grid(row=0, columnspan=2, sticky="news", padx=5, pady=5)
        self.chat_area.tag_configure("center", justify="center")
        self.chat_area.tag_configure("right_align", justify="right")

        # Input box
        self.message_input = tk.Entry(master, width=40, bg="gray20",
                                      fg="white", font=("Arial", 14))
        self.message_input.grid(row=1, padx=5, pady=5, column=0, sticky="news")
        self.message_input.bind('<Return>', lambda e: self.send_message(self.message_input.get()))

        # Send button
        self.send_button = tk.Button(master, text="-->", width=5,
                                     font=("Arial", 14),
                                     command=lambda: self.send_message(self.message_input.get()))
        self.send_button.grid(row=1, column=1, padx=5, pady=5, sticky="news")

        self.grid(column=0, row=0, sticky='news')

        # Start chat session
        self.start_chat()
        self._insert_ai("I'm a helpful AI assistant tool and I'm here to assist you with whatever you need.")

        # Timer-related state
        self.timer_running = False
        self.time_left = 0
        self.total_time = 0
        self._timer_widget = None           # Frame embedded inside Text for timer + stickman
        self._stickman_frame = None
        self._stickman_canvas = None
        self._stickman_anim_id = None
        self._stickman_step = 0

        # Pre-built stickman frames (simple walking animation)
        # Each frame is drawing commands; we'll draw on Canvas instead of ASCII for smoothness.
        # We'll animate by changing x offset of legs/arms to simulate walking.
        # Configurable sizes:
        self.stickman_scale = 1.2
        self.canvas_width = 220
        self.canvas_height = 80

    # ---------- Chat helpers ----------
    def _insert_ai(self, text):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"AI: {text}\n\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def _insert_user(self, text):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"You: {text}\n\n", "right_align")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    # ---------- Break timer and embedded UI ----------
    def start_break(self, event=None, minutes=2):
        """Public trigger: insert timer widget and start countdown (minutes default 2)."""
        if self.timer_running:
            return  # already running

        # Insert user message
        self._insert_user(f"Give me a {minutes} minute break")

        # prepare timer
        self.time_left = int(minutes * 60)
        self.total_time = self.time_left
        self.timer_running = True
        self._stickman_step = 0

        # Build embedded timer frame and add to the chat area (preserves chat history)
        self._create_timer_widget()
        # start the recurring updates
        self._update_timer_tick()

    def _create_timer_widget(self):
        """Create a Frame with labels + canvas and embed it into the Text widget."""
        # If already exists, remove it first
        if self._timer_widget:
            try:
                self.chat_area.config(state=tk.NORMAL)
                self.chat_area.window_create(tk.END, window=tk.Label(self.chat_area, text=""))  # noop to keep index sane
                self.chat_area.config(state=tk.DISABLED)
            except Exception:
                pass

        # Build widget
        timer_frame = tk.Frame(self.chat_area, bg="black")
        # clock label
        clock_lbl = tk.Label(timer_frame, text="", font=("Consolas", 20), fg="white", bg="black")
        clock_lbl.pack(fill="x", pady=(4,0))
        # progress text bar
        bar_lbl = tk.Label(timer_frame, text="", font=("Consolas", 12), fg="white", bg="black")
        bar_lbl.pack(fill="x", pady=(2,4))
        # stickman canvas
        canvas = tk.Canvas(timer_frame, width=self.canvas_width, height=self.canvas_height, bg="black", highlightthickness=0)
        canvas.pack(pady=(2,6))

        # store references
        timer_frame._clock_lbl = clock_lbl
        timer_frame._bar_lbl = bar_lbl
        timer_frame._canvas = canvas

        # Insert a small spacer line then the window
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, "\n")  # spacer
        self.chat_area.window_create(tk.END, window=timer_frame)
        self.chat_area.insert(tk.END, "\n\n")  # spacer after widget
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

        self._timer_widget = timer_frame
        self._stickman_canvas = canvas

    def _update_timer_tick(self):
        """Called every second while timer_running; updates clock, bar and stickman animation."""
        if not self.timer_running:
            return

        if self.time_left <= 0:
            self._finish_timer()
            return

        # Compute mm:ss
        mins, secs = divmod(self.time_left, 60)
        time_str = f"{mins:02}:{secs:02}"

        # Progress bar as blocks
        bar_len = 28
        filled = int(bar_len * (self.time_left / max(1, self.total_time)))
        bar = "█" * filled + "░" * (bar_len - filled)

        # Update UI inside embedded frame
        self._timer_widget._clock_lbl.config(text=f"⏰  {time_str}")
        self._timer_widget._bar_lbl.config(text=bar)

        # Animate stickman on canvas
        self._animate_stickman_frame(self._stickman_step)

        # advance
        self._stickman_step = (self._stickman_step + 1) % 8  # 8-step walking cycle
        self.time_left -= 1

        # schedule next tick
        self._timer_widget.after(1000, self._update_timer_tick)

    def _animate_stickman_frame(self, step):
        """Draw a stickman walking on the canvas. 'step' controls limb offsets."""
        c = self._stickman_canvas
        c.delete("all")
        w = self.canvas_width
        h = self.canvas_height

        # Base coordinates
        cx = 40 + (step % 4) * 6  # make the stickman subtly move horizontally for 'walking'
        cy = h // 2 + 5
        scale = self.stickman_scale

        # limb swing offset based on step to simulate walk
        # values chosen to look like a simple gait
        swing_values = [ -8, -5, 0, 5, 8, 5, 0, -5 ]
        swing = swing_values[step % len(swing_values)]

        head_r = int(8 * scale)

        # head
        c.create_oval(cx - head_r, cy - 45, cx + head_r, cy - 45 + 2*head_r, outline="white", width=2)

        # body
        c.create_line(cx, cy - 45 + 2*head_r, cx, cy - 45 + 2*head_r + 28, fill="white", width=2)

        # arms (swing opposite to legs)
        arm_y = cy - 45 + 2*head_r + 8
        arm_len = int(18 * scale)
        c.create_line(cx, arm_y, cx - arm_len + swing//2, arm_y + 8, fill="white", width=2)  # left arm
        c.create_line(cx, arm_y, cx + arm_len - swing//2, arm_y + 8, fill="white", width=2)  # right arm

        # legs (swing)
        leg_y0 = cy - 45 + 2*head_r + 28
        leg_len = int(24 * scale)
        # left leg
        c.create_line(cx, leg_y0, cx - 8 + swing, leg_y0 + leg_len, fill="white", width=2)
        # right leg
        c.create_line(cx, leg_y0, cx + 8 - swing, leg_y0 + leg_len, fill="white", width=2)

        # shoes / feet small lines
        c.create_line(cx - 12 + swing, leg_y0 + leg_len, cx - 6 + swing, leg_y0 + leg_len - 3, fill="white", width=2)
        c.create_line(cx + 12 - swing, leg_y0 + leg_len, cx + 6 - swing, leg_y0 + leg_len - 3, fill="white", width=2)

        # Optional: small ground line
        c.create_line(10, h-6, w-10, h-6, fill="#222", width=1)

    def _finish_timer(self):
        """Timer done: clear the embedded widget (leaving chat history intact) and notify user."""
        self.timer_running = False
        # update final notification appended to chat
        self.chat_area.config(state=tk.NORMAL)
        # Remove the embedded frame (we find it by destroying widget)
        if self._timer_widget:
            try:
                # To remove the widget from the Text, we can delete the line that contains it.
                # Simpler: destroy the widget and then insert a final message.
                self._timer_widget.destroy()
            except Exception:
                pass
            self._timer_widget = None
            self._stickman_canvas = None

        # Insert final message (keeps prior history)
        self.chat_area.insert(tk.END, "🕒 Time’s up! Break finished.\n\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    # ---------- Chat send ----------
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
