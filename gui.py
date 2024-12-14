import tkinter as tk
from tkinter import messagebox
import csv
from reference import grading_sy

class GradingSys:
    def __init__(self, frame):
        self.frame = frame
        self.frame.title('Grade Calculator')
        self.frame.geometry('500x500')
        self.frame.resizable(False, False)

        #create frames
        self.page1 = tk.Frame(self.frame)
        self.page2 = tk.Frame(self.frame)
        self.page3 = tk.Frame(self.frame)
        self.page4 = tk.Frame(self.frame)
        self.page5 = tk.Frame(self.frame)

        #default scores
        self.num_students = 0
        self.student_data = []
        self.current_student_index = 0

        self.build_page1()
        self.build_page2()
        self.build_page3()
        self.build_page4()
        self.build_page5()

        #start push
        self.show_page(self.page1)

    def show_page(self, page):
        #one page at a time sorted
        for frame in (self.page1, self.page2, self.page3, self.page4, self.page5):
            frame.pack_forget()
        page.pack(fill=tk.BOTH, expand=True, pady=20)

    def build_page1(self):
        #page one ask for total of students
        tk.Label(self.page1, text='Total number of students:').pack(pady=10)
        self.num_students_box = tk.Entry(self.page1, width=10)
        self.num_students_box.pack(pady=10)
        tk.Button(self.page1, text='Submit', command=self.input_num_students).pack(pady=20)

    def build_page2(self):
        #page 2 name and attemps
        self.student_details_frame = tk.Frame(self.page2)
        self.student_details_frame.pack(pady=10)
        self.next_student_button = tk.Button(self.page2, text='Next', command=self.proceed_to_student_scores)
        self.next_student_button.pack(pady=20)

    def build_page3(self):
        #focus on each student score
        self.student_scores_frame = tk.Frame(self.page3)
        self.student_scores_frame.pack(pady=10)
        self.submit_scores_button = tk.Button(self.page3, text='Submit Scores', command=self.save_student_scores)
        self.submit_scores_button.pack(pady=20)

    def build_page4(self):
        #page for the result
        self.student_results_frame = tk.Frame(self.page4)
        self.student_results_frame.pack(pady=10)
        self.next_result_button = tk.Button(self.page4, text='Next Student', command=self.next_student)
        self.next_result_button.pack(pady=20)

    def build_page5(self):
        #restart or view final score which is a cvs file saver
        self.final_summary_frame = tk.Frame(self.page5)
        self.final_summary_frame.pack(pady=10)
        tk.Button(self.page5, text='Restart', command=self.restart).pack(side=tk.LEFT, padx=20)
        tk.Button(self.page5, text='View Results', command=self.view_all_results).pack(side=tk.RIGHT, padx=20)

    def input_num_students(self):
        try:
            #no negative or 0
            self.num_students = int(self.num_students_box.get())
            if self.num_students <= 0:
                raise ValueError
            for widget in self.student_details_frame.winfo_children():
                widget.destroy()
            #store
            tk.Label(self.student_details_frame, text='Enter student details:').pack(pady=10)
            self.student_name_entries = []
            self.student_attempts_entries = []

            for i in range(self.num_students):
                frame = tk.Frame(self.student_details_frame)
                frame.pack(pady=5)
                tk.Label(frame, text=f'Student {i + 1} Name:').pack(side=tk.LEFT, padx=5)
                name_entry = tk.Entry(frame, width=15)
                name_entry.pack(side=tk.LEFT, padx=5)
                tk.Label(frame, text='Attempts:').pack(side=tk.LEFT, padx=5)
                attempts_entry = tk.Entry(frame, width=5)
                attempts_entry.pack(side=tk.LEFT, padx=5)
                self.student_name_entries.append(name_entry)
                self.student_attempts_entries.append(attempts_entry)

            self.show_page(self.page2)
        except ValueError:
            messagebox.showerror('Input Error', 'enter a valid integer.')

    def proceed_to_student_scores(self):
        try:
            #save data
            self.student_data.clear()
            self.current_student_index = 0
            for i in range(self.num_students):
                name = self.student_name_entries[i].get().strip()
                attempts = int(self.student_attempts_entries[i].get())
                if not name:
                    raise ValueError(f'Name for Student {i + 1} can not be empty.')
                if not (1 <= attempts <= 4):
                    raise ValueError(f'Attempts for Student {i + 1} must be between 1 to 4.')
                self.student_data.append({
                    'name': name,
                    'attempts': attempts,
                    'scores': []
                })
                #for the csv file
            self.prepare_student_scores()
            self.show_page(self.page3)
        except ValueError as e:
            messagebox.showerror('Input Error', str(e))

    def prepare_student_scores(self):
        #clear data for the "next" button
        for widget in self.student_scores_frame.winfo_children():
            widget.destroy()
        #prompt
        current_student = self.student_data[self.current_student_index]
        name = current_student['name']
        attempts = current_student['attempts']
        tk.Label(self.student_scores_frame,
                 text=f'Enter scores for {name} (Attempts: {attempts})',
                 font=('Arial', 12)).pack(pady=10)

        self.score_entries = []
        for i in range(attempts):
            frame = tk.Frame(self.student_scores_frame)
            frame.pack(pady=5)
            tk.Label(frame, text=f'Attempt {i + 1}:').pack(side=tk.LEFT, padx=5)
            entry = tk.Entry(frame, width=10)
            entry.pack(side=tk.LEFT, padx=5)
            self.score_entries.append(entry)

    def save_student_scores(self):
        try:
            scores = [int(entry.get()) for entry in self.score_entries]
            if not all(0 <= score <= 100 for score in scores):
                raise ValueError('Scores must be between 0 and 100.')
            self.student_data[self.current_student_index]['scores'] = scores
            self.display_student_results()
            self.show_page(self.page4)
        except ValueError as f:
            messagebox.showerror('Input Error', str(f))

    def display_student_results(self):
        #clear
        for widget in self.student_results_frame.winfo_children():
            widget.destroy()
        student = self.student_data[self.current_student_index]
        name = student['name']
        scores = student['scores']
        total_score = sum(scores)
        highest_score = max([sum(s['scores']) for s in self.student_data])
        letter_grade = grading_sy(total_score, highest_score)
        #color
        if letter_grade in ['D', 'F']:
            grade_color = 'red'
        elif letter_grade == 'C':
            grade_color = 'orange'
        else:
            grade_color = 'green'

        #result
        tk.Label(self.student_results_frame, text=f'Results for {name}').pack(pady=10)
        tk.Label(self.student_results_frame, text=f"Scores: {', '.join(map(str, scores))}").pack()
        tk.Label(self.student_results_frame, text=f"Total Score: {total_score}", fg="green").pack()
        tk.Label(self.student_results_frame, text=f"Grade: {letter_grade}", fg=grade_color,
                 font=('Arial', 14, 'bold')).pack()

        if self.current_student_index < self.num_students - 1:
            self.next_result_button.config(text='Next Student', state=tk.NORMAL)
        else:
            self.next_result_button.config(text='Finish', state=tk.NORMAL)

    def next_student(self):
        self.current_student_index += 1
        if self.current_student_index < self.num_students:
            #multiple students, go to scores page
            self.prepare_student_scores()
            self.show_page(self.page3)
        else:
            #go to final page
            self.write_csv()
            self.show_page(self.page5)

    def view_all_results(self):
        #cvs file create
        self.write_csv()
        messagebox.showinfo('Results', 'Results have been saved to students.csv')
    def write_csv(self):
        with open('students.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Attempts', 'Scores', 'Total Score', 'Grade'])
            for student in self.student_data:
                name = student['name']
                attempts = student['attempts']
                scores = student['scores']
                total_score = sum(scores)
                highest_score = max([sum(s['scores']) for s in self.student_data])
                letter_grade = grading_sy(total_score, highest_score)
                writer.writerow([name, attempts, scores, total_score, letter_grade])

    def restart(self):
        self.num_students = 0
        self.student_data.clear()
        self.current_student_index = 0
        self.num_students_box.delete(0, tk.END)
        for frame in (self.student_details_frame, self.student_scores_frame,
                      self.student_results_frame, self.final_summary_frame):
            for widget in frame.winfo_children():
                widget.destroy()

        self.show_page(self.page1)

if __name__ == '__main__':
    frame = tk.Tk()
    app = GradingSys(frame)
    frame.mainloop()