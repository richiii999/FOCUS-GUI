import tkinter as tk
from tkinter import messagebox
import re

class QuizWindow(tk.Toplevel):
    def __init__(self, master, quiz_text):
        super().__init__(master)
        self.title("Algebra Quiz")
        self.geometry("400x400")
        
        # Parse the quiz text into questions and answers
        self.questions_and_answers = self.parse_quiz_text(quiz_text)
        self.current_question_index = 0
        self.selected_answer = None

        # Display the first question and answers
        self.display_question()

        # Submit button to check the answer
        self.submit_button = tk.Button(self, text="Submit", font=("Arial", 14), command=self.check_answer)
        self.submit_button.pack(pady=20)

        self.result_label = tk.Label(self, text="", font=("Arial", 14), fg="red")
        self.result_label.pack(pady=10)

    def parse_quiz_text(self, quiz_text):
        """Parse the quiz text into questions and answers."""
        questions_and_answers = []
        # Split the quiz into questions by matching question format
        question_blocks = re.findall(r"(\d+\..+?)(a\..+?d\..+?)(Correct Answer: .+?)", quiz_text, re.DOTALL)

        for question_block in question_blocks:
            question = question_block[0].strip()
            answers = question_block[1].strip().splitlines()
            correct_answer = question_block[2].strip().split(":")[1].strip()

            options = [answers[0], answers[1], answers[2], answers[3]]
            questions_and_answers.append({
                "question": question,
                "options": options,
                "correct_answer": correct_answer
            })

        return questions_and_answers

    def display_question(self):
        """Display the current question with its answers."""
        question_data = self.questions_and_answers[self.current_question_index]
        question_text = question_data["question"]
        options = question_data["options"]

        # Clear any previous question or options
        for widget in self.winfo_children():
            widget.destroy()

        # Display the question
        question_label = tk.Label(self, text=question_text, font=("Arial", 14))
        question_label.pack(pady=10)

        # Create buttons for each of the options (a, b, c, d)
        self.answer_buttons = []
        for option in options:
            button = tk.Button(self, text=option, width=20, height=2, font=("Arial", 12), command=lambda opt=option: self.select_answer(opt))
            button.pack(pady=5)
            self.answer_buttons.append(button)

        # Submit button to check the answer
        self.submit_button = tk.Button(self, text="Submit", font=("Arial", 14), command=self.check_answer)
        self.submit_button.pack(pady=20)

    def select_answer(self, answer):
        """Store the selected answer."""
        self.selected_answer = answer

    def check_answer(self):
        """Check if the selected answer is correct."""
        if not self.selected_answer:
            messagebox.showwarning("No Answer", "Please select an answer before submitting.")
            return

        correct_answer = self.questions_and_answers[self.current_question_index]["correct_answer"]

        if self.selected_answer == correct_answer:
            self.result_label.config(text="Correct!", fg="green")
        else:
            self.result_label.config(text=f"Wrong! Correct answer: {correct_answer}", fg="red")

        # Wait a moment before moving to the next question
        self.after(1000, self.next_question)

    def next_question(self):
        """Move to the next question."""
        self.result_label.config(text="")  # Clear previous result
        self.current_question_index += 1

        if self.current_question_index < len(self.questions_and_answers):
            self.display_question()
        else:
            self.finish_quiz()

    def finish_quiz(self):
        """Finish the quiz and show a final message."""
        messagebox.showinfo("Quiz Finished", "You've completed the quiz!")
        self.destroy()  # Close the quiz window


class ChatWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.chat_area = tk.Text(master, wrap="word", height=20, width=60, bg="black", fg="lime", state=tk.DISABLED, font=("Consolas", 14))
        self.chat_area.grid(row=0, columnspan=2, sticky="news", padx=5, pady=5)
        self.chat_area.tag_configure("center", justify="center")
        self.chat_area.tag_configure("right_align", justify="right")

        self.message_input = tk.Entry(master, width=40, bg="gray20", fg="white", font=("Arial", 14))
        self.message_input.grid(row=1, padx=5, pady=5, column=0, sticky="news")
        self.message_input.bind('<Return>', lambda e: self.send_message(self.message_input.get()))

        self.send_button = tk.Button(master, text="-->", width=5, font=("Arial", 14), command=lambda: self.send_message(self.message_input.get()))
        self.send_button.grid(row=1, column=1, padx=5, pady=5, sticky="news")

        self.grid(column=0, row=0, sticky='news')

        self.start_chat()

    def send_message(self, message, visible=True):
        if message.strip():
            self.chat_area.config(state=tk.NORMAL)
            self.chat_area.insert(tk.END, f"You: {message}\n\n", "right_align")
            self.chat_area.config(state=tk.DISABLED)
            self.chat_area.see(tk.END)

            # Trigger quiz if the user asks for it
            if "quiz" in message.lower():
                self.start_quiz()

    def start_chat(self):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, "AI: I'm a helpful assistant! Type 'quiz' to start an algebra quiz.\n\n")
        self.chat_area.config(state=tk.DISABLED)

    def start_quiz(self):
        """Starts the quiz in a new window with dynamically generated questions."""
        # Here you simulate the Llama generating a quiz text
        generated_quiz_text = """
        1. What is 2 + 2?
        a. 3
        b. 4
        c. 5
        d. 6
        Correct Answer: b

        2. What is 3 * 3?
        a. 6
        b. 7
        c. 9
        d. 12
        Correct Answer: c

        3. What is 5 - 3?
        a. 1
        b. 2
        c. 3
        d. 4
        Correct Answer: b

        4. What is 6 / 2?
        a. 2
        b. 3
        c. 4
        d. 5
        Correct Answer: b

        5. What is 10 + 5?
        a. 12
        b. 13
        c. 14
        d. 15
        Correct Answer: d
        """

        # Open the quiz window with the generated quiz
        QuizWindow(self, generated_quiz_text)