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
        
        # New regex pattern to match questions and answers
        question_blocks = re.findall(r"(\d+\. [^\n]+)\n(a\..+)\n(b\..+)\n(c\..+)\n(d\..+)\nCorrect Answer: ([a-d])", quiz_text)

        print("Found question blocks:", question_blocks)  # Debugging print

        for question_block in question_blocks:
            question = question_block[0].strip()  # Question text
            answers = [question_block[1].strip(), question_block[2].strip(), question_block[3].strip(), question_block[4].strip()]  # Answer options
            correct_answer = question_block[5].strip()  # Correct answer (a, b, c, or d)

            questions_and_answers.append({
                "question": question,
                "options": answers,
                "correct_answer": correct_answer
            })
        
        print(quiz_text)
        print("Question and Answers: ")
        print(questions_and_answers)
        return questions_and_answers

    def display_question(self):
        if not self.questions_and_answers:
            print("No questions available to display!")
            return

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

        # Display the current question number
        question_counter_label = tk.Label(self, text=f"Question {self.current_question_index + 1} of {len(self.questions_and_answers)}", font=("Arial", 10))
        question_counter_label.pack(pady=5)

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


