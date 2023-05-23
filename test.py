# TO DO
# package as easy-to-launch app
# offer items from todo list to click on and do
# save history in a new google spreadsheet
# beautiful graphic design https://github.com/ParthJadhav/Tkinter-Designer https://www.youtube.com/watch?v=Qf5cnJDSolE&t=342s
#white on black switch to black on white when red circle

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import time

activity_history = []
history_to_print = []

def draw_red_circle():
    circle = canvas.create_oval(5, 10, 25, 30, fill="red")

class Activity():
    def __init__(self):
        self.activity_name = activity_name_field.get()
        self.minutes = int(minutes_field.get())
        self.start_time = datetime.now()
        self.formatted_start_time = datetime.now().strftime("%H:%M")
        self.anticipated_time_end = datetime.now() + timedelta(minutes=self.minutes)
        self.formatted_anticipated_time_end = self.anticipated_time_end.strftime("%H:%M")
        self.real_end_time = None
        self.stop_timer = False
        
        if activity_history:
            activity_history[-1].stop_timer = True
            activity_history[-1].add_previous_to_history_list()

        activity_history.append(self)
        self.add_activity_to_current()

    def add_previous_to_history_list(self):
        self.real_end_time = datetime.now()
        self.formatted_real_end_time = self.real_end_time.strftime("%H:%M")
        self.actual_minutes = int((self.real_end_time - self.start_time).total_seconds() / 60.0)

        activity_history_to_print = f"{self.activity_name} {self.minutes} minutes. \nActual: {self.actual_minutes}. \nStart {self.formatted_start_time}. End {self.formatted_real_end_time}"
        history_to_print.append(activity_history_to_print)
        history_field.config(state=tk.NORMAL)
        history_field.delete("1.0", tk.END)
        print(history_to_print)
        for entry in reversed(history_to_print):
            history_field.insert(tk.END, entry + "\n \n")
        history_field.config(state=tk.DISABLED)
    
    def counters(self):
        while True:
            if self.stop_timer is True:
                break

            now = datetime.now()

            time_difference_since = now - self.start_time
            minutes_since = int(time_difference_since.total_seconds() // 60)
            seconds_since = int(time_difference_since.total_seconds() % 60)

            time_difference_till = self.anticipated_time_end - now
            minutes_till = int(time_difference_till.total_seconds() // 60)
            seconds_till = int(time_difference_till.total_seconds() % 60)

            if minutes_till == 0 and seconds_till == 0:
                draw_red_circle()

            timer_field.config(text=f"{minutes_till:02d}:{seconds_till:02d} {minutes_since:02d}:{seconds_since:02d}")
            window.update()
            time.sleep(1)

    def add_activity_to_current(self):
        #clear red circle
        canvas.delete("all")

        current_activity_field.config(state=tk.NORMAL)
        current_activity_field.delete("1.0", tk.END)
        current_activity_field.insert(tk.END, f"{self.activity_name} {self.minutes} min.\nStart {self.formatted_start_time}. End {self.formatted_anticipated_time_end}")
        current_activity_field.config(state=tk.DISABLED)

        self.counters()

        activity_name_field.delete(0, tk.END)
        minutes_field.delete(0, tk.END)
        activity_name_field.focus_set()



window = tk.Tk()
window.title("Productivity!")
window.geometry("160x300")
window.attributes("-topmost", True)  # Set window to always on top
window.configure(background='white')

# Create text field for text entry
activity_name_field = tk.Entry(window, width=13, font=("Cormorant", 12), highlightthickness=0, relief='ridge')
activity_name_field.grid(row=2, column=0, padx=(0, 1), pady=(0, 1))

# Create text field for number entry
minutes_field = tk.Entry(window, width=3, font=("Cormorant", 12), highlightthickness=0, relief='ridge')
minutes_field.grid(row=2, column=1, padx=(0, 1), pady=(0, 1))

# Create text field for result display
current_activity_field = tk.Text(window, width=20, height=2, font=("Cormorant", 12), highlightthickness=0, relief='ridge')
current_activity_field.grid(row=0, column=0, padx=0, pady=0)
current_activity_field.config(state=tk.DISABLED)

# Create canvas for red circle
canvas = tk.Canvas(window, width=40, height=40, highlightthickness=0, relief='ridge')
canvas.grid(row=1, column=1, padx=0, pady=0)
canvas.configure(background='white')

# Create history field
history_field = tk.Text(window, width=25, height=15, font=("Cormorant", 12), highlightthickness=0, relief='ridge')
history_field.grid(row=3, column=0, columnspan=2, padx=0, pady=0)
history_field.config(state=tk.DISABLED)

activity_name_field.focus_set()

# Bind Enter key press to the newActivity function
window.bind('<Return>', lambda event: Activity())

# Create timer label for countdown and countup
timer_field = tk.Label(window, text="", font=("Cormorant", 15))
timer_field.grid(row=1, column=0, padx=0, pady=0)
timer_field.configure(background='white')

window.mainloop()
