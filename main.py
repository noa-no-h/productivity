import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

activity_history = []
history_to_print = []

class Activity():
    def __init__(self):
        self.activity_name = activity_name_field.get()
        self.minutes = int(minutes_field.get())
        self.start_time = datetime.now().strftime("%H:%M")
        unformatted_anticipated_time_end = datetime.now() + timedelta(minutes=self.minutes)
        self.anticipated_time_end = unformatted_anticipated_time_end.strftime("%H:%M")
        self.real_end_time = 0
        
        if activity_history:
            activity_history[-1].add_previous_to_history_list()

        activity_history.append(self)
        self.add_activity_to_current()

    def add_previous_to_history_list(self):
        self.real_end_time = datetime.now().strftime("%H:%M")
        start_datetime = datetime.strptime(self.start_time, "%H:%M")
        end_datetime = datetime.strptime(self.real_end_time, "%H:%M")
        self.actual_minutes = int((end_datetime - start_datetime).total_seconds() / 60.0)

        activity_history_to_print = f"{self.activity_name} {self.minutes} minutes. Actual: {self.actual_minutes}. \nStarted {self.start_time}. Ended {self.real_end_time}"
        history_to_print.append(activity_history_to_print)
        history_field.config(state=tk.NORMAL)
        history_field.delete("1.0", tk.END)
        print(history_to_print)
        for entry in history_to_print:
            history_field.insert(tk.END, entry + "\n \n")
        history_field.config(state=tk.DISABLED)

    def add_activity_to_current(self):
        #clear red circle
        canvas.delete("all")

        current_activity_field.config(state=tk.NORMAL)
        current_activity_field.delete("1.0", tk.END)
        current_activity_field.insert(tk.END, f"{self.activity_name} {self.minutes} minutes.\nStarted {self.start_time}. Ends {self.anticipated_time_end}")
        current_activity_field.config(state=tk.DISABLED)

        counters(self.minutes)

        activity_name_field.delete(0, tk.END)
        minutes_field.delete(0, tk.END)
        activity_name_field.focus_set()

def draw_red_circle():
    circle = canvas.create_oval(5, 10, 25, 30, fill="red")

window = tk.Tk()
window.title("Productivity!")
window.geometry("160x300")
window.attributes("-topmost", True)  # Set window to always on top

# Create text field for text entry
activity_name_field = tk.Entry(window, width=13, font=("Cormorant", 12))
activity_name_field.grid(row=3, column=0, padx=1, pady=(0, 1))

# Create text field for number entry
minutes_field = tk.Entry(window, width=3, font=("Cormorant", 12))
minutes_field.grid(row=3, column=1, padx=(0, 1), pady=(0, 1))

# Create text field for result display
current_activity_field = tk.Text(window, width=20, height=3, font=("Cormorant", 12))
current_activity_field.grid(row=1, column=0, columnspan=2, padx=(0, 1), pady=(0, 1))
current_activity_field.config(state=tk.DISABLED)

# Create canvas for red circle
canvas = tk.Canvas(window, width=40, height=40)
canvas.grid(row=2, column=1, padx=1, pady=(0, 1))

# Create history field
history_field = tk.Text(window, width=25, height=15, font=("Cormorant", 12))
history_field.grid(row=4, column=0, columnspan=2, padx=1, pady=(0, 1))
history_field.config(state=tk.DISABLED)

activity_name_field.focus_set()

# Bind Enter key press to the newActivity function
window.bind('<Return>', lambda event: Activity())

style = ttk.Style()
style.configure("TButton", font=("Cormorant", 18))

# Create timer label for countdown and countup
timer_field = tk.Label(window, text="", font=("Cormorant", 15))
timer_field.grid(row=2, column=0, padx=1, pady=(0, 1))

def counters(minutes):
    countdown_seconds = 0
    countup_seconds = 0
    countdown_minutes = minutes
    countup_minutes = 0
    while countdown_minutes >= 0:
        timer_field.config(text=f"{countdown_minutes:02d}:{countdown_seconds:02d} {countup_minutes:02d}:{countup_seconds:02d}")
        window.update()
        if countup_seconds == 0:
            if countdown_minutes != 0:
                countdown_minutes -= 1
                countdown_seconds = 59
        else:
            countdown_seconds -= 1
        if countup_seconds == 59:
            countup_minutes += 1
            countup_seconds = 0
        else:
            countup_seconds += 1
        if countdown_minutes == 0 and countdown_seconds == 0:
            draw_red_circle()
        window.after(1000)
        
window.mainloop()
