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
import math
import gspread

gc = gspread.service_account(filename='credentials.json')
to_do_sh = gc.open("to do")
to_do_worksheet = to_do_sh.worksheet("Sheet1")

activity_history = []
history_to_print = []

def draw_red_circle():
    circle = canvas.create_oval(5, 10, 25, 30, fill="red")

def draw_unfilled_circle():
    circle = canvas.create_oval(5, 10, 25, 30, fill="white")

window_on_top = tk.Tk()
window_on_top.title("Productivity!")
window_on_top.geometry("111x200")
window_on_top.attributes("-topmost", True)  # Set window_on_top to always on top
window_on_top.configure(background='white')

window_list_of_tasks = tk.Toplevel(window_on_top)
window_list_of_tasks.title("List of Tasks!")
window_list_of_tasks.geometry("200x1600+111+0")
window_list_of_tasks.configure(background='white')

# Create text field for text entry
activity_name_field = tk.Entry(window_on_top, width=13, font=("Cormorant", 11), highlightthickness=0, relief='ridge')
activity_name_field.grid(row=3, column=0, sticky=tk.NSEW, padx=(0, 1), pady=(0, 1))

# Create text field for number entry
minutes_field = tk.Entry(window_on_top, width=3, font=("Cormorant", 12), highlightthickness=0, relief='ridge')
minutes_field.grid(row=3, column=1, sticky=tk.W, padx=(0, 1), pady=(0, 1))

# Create text field for result display
current_activity_field = tk.Text(window_on_top, width=13, height=2.5, font=("Cormorant", 12), highlightthickness=0, relief='ridge')
current_activity_field.grid(row=0, column=0, rowspan=2, columnspan=2, padx=0, pady=0)
current_activity_field.config(state=tk.DISABLED)

# Create canvas for red circle
canvas = tk.Canvas(window_on_top, width=40, height=40, highlightthickness=0, relief='ridge')
canvas.grid(row=2, column=1, sticky=tk.NW, padx=0, pady=0)
canvas.configure(background='white')

class Activity():
    def __init__(self, activity_name=None, minutes=None):
        if activity_name is None:
            print(f'{activity_name_field.get()=}')
            self.activity_name = activity_name_field.get()
        else:
            self.activity_name = activity_name
        if minutes is None:
            print(f'{minutes_field.get()=}')
            self.minutes = int(minutes_field.get())
        else:
            self.minutes = minutes
        print(f'{self.activity_name=} {self.minutes=}')
        #self.activity_name = activity_name
        #self.minutes = minutes
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
            window_on_top.update()
            time.sleep(1)

    def add_activity_to_current(self):
        #clear red circle
        canvas.delete("all")
        draw_unfilled_circle()

        current_activity_field.config(state=tk.NORMAL)
        current_activity_field.delete("1.0", tk.END)
        current_activity_field.insert(tk.END, f"{self.activity_name} {self.minutes} min.\nStart {self.formatted_start_time}. \nEnd {self.formatted_anticipated_time_end}")
        current_activity_field.config(state=tk.DISABLED)

        self.counters()

        activity_name_field.delete(0, tk.END)
        minutes_field.delete(0, tk.END)
        activity_name_field.focus_set()

def history_field_clicked(event):
    index = history_field.index("@%s,%s" % (event.x, event.y))
    line_num = int(index.split(".")[0])
    print(f"{index=} You clicked on line {line_num}")
    index_in_history_list = -math.ceil(line_num/4) - 1
    print(f'{index_in_history_list=}')
    activity = activity_history[index_in_history_list]
    Activity(activity_name = activity.activity_name, minutes = activity.minutes)
    print(f'{activity.activity_name=} {activity.minutes=}')

    activity_name_field.delete(0,tk.END)
    print("Activity name deleted")  # Debug print
    activity_name_field.insert(0,activity.activity_name)
    print("Activity name inserted")  # Debug print

    minutes_field.delete(0,tk.END)
    minutes_field.insert(0,activity.minutes)

    # Update the fields immediately
    activity_name_field.update()
    minutes_field.update()


# Create history field
history_field = tk.Text(window_on_top, width=20, height=15, font=("Cormorant", 11), highlightthickness=0, relief='ridge')
history_field.grid(row=4, column=0, columnspan=2, rowspan=2, padx=0, pady=0)
history_field.config(state=tk.NORMAL)
history_field.bind("<Button-1>", history_field_clicked)


activity_name_field.focus_set()

# Bind Enter key press to the newActivity function
window_on_top.bind('<Return>', lambda event: Activity())

# Create timer label for countdown and countup
timer_field = tk.Label(window_on_top, text="", font=("Cormorant", 15))
timer_field.grid(row=2, column=0, sticky=tk.NW, padx=0, pady=0)
timer_field.configure(background='white')


# Fetch tasks from the Google Spreadsheet
tasks = to_do_worksheet.get_all_values()

# Create a list of tasks in window_list_of_tasks
def create_task_buttons():
    global tasks
    global estimated_time_fields

    # Clear the list of Entry fields
    estimated_time_fields.clear()

    for i, task in enumerate(tasks[1:]):
        print(task)
        task_name = task[2]
        label = task[1]

        # Create an Entry field for the estimated time
        estimated_time_field = tk.Entry(window_list_of_tasks, width=3)
        estimated_time_field.grid(row=i, column=0, sticky=tk.W)
        estimated_time_fields.append(estimated_time_field)  # Add the Entry field to the list

        task_button = tk.Button(window_list_of_tasks, text=label + " " + task_name, background='white')
        task_button.grid(row=i, column=1, sticky=tk.W)  # Change the column to 1 to place the button next to the Entry field

        # Bind a click event to the task button
        task_button.bind('<Button-1>', lambda event, task_name=task_name, i=i: create_activity_from_task(task_name, estimated_time_fields[i].get()))

def refresh_data():
    global tasks

    to_do_sh = gc.open("to do")
    to_do_worksheet = to_do_sh.worksheet("Sheet1")
    tasks = to_do_worksheet.get_all_values()

    # Delete all existing buttons and Entry fields
    for widget in window_list_of_tasks.winfo_children():
        widget.destroy()

    # Create new buttons and Entry fields
    create_task_buttons()

    window_on_top.after(60000, refresh_data)  # Schedule the next refresh

# Initialize an empty list to store the Entry fields
estimated_time_fields = []

# Call the function once to start the refresh cycle
refresh_data()
    
def create_activity_from_task(task_name, estimated_time):
    if estimated_time == '':
        estimated_time = '1' 
    estimated_time = int(estimated_time)
    # Create a new Activity with the task's name and estimated time
    Activity(activity_name=task_name, minutes=estimated_time)

def bring_to_front(event):
    window_list_of_tasks.lift()

window_on_top.bind('<FocusIn>', bring_to_front)


window_on_top.mainloop()
