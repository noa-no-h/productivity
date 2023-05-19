import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

activity_history = []

def newActivity():
    #clear red circle
    canvas.delete("all")
    text_value = text_field.get()
    minutes = int(number_field.get())

    formatted_time_start = datetime.now().strftime("%H:%M")
    time_end = datetime.now() + timedelta(minutes=minutes)
    formatted_time_end = time_end.strftime("%H:%M")

    result_field.config(state=tk.NORMAL)
    result_field.delete("1.0", tk.END)
    result_field.insert(tk.END, f"{text_value} {minutes} minutes.\nStarted {formatted_time_start}. Ends {formatted_time_end}")
    result_field.config(state=tk.DISABLED)

    #add_previous_to_history_list()

    counters(minutes)

    text_field.delete(0, tk.END)
    number_field.delete(0, tk.END)
    text_field.focus_set()

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

"""def add_previous_to_history_list():
    text_value = text_field.get()
    minutes = int(number_field.get())
    formatted_time_now = datetime.now().strftime("%H:%M")
    actual_time_taken = formatted_time_start - 
    to_add_to_activity_history = f"{text_value} {minutes} minutes. \nStarted {formatted_time_start}. Ended {formatted_time_now} \n\n"
    activity_history.append(to_add_to_activity_history)
    history_field.config(state=tk.NORMAL)
    history_field.delete("1.0", tk.END)
    for entry in activity_history:
        history_field.insert(tk.END, entry)
    history_field.config(state=tk.DISABLED)"""

def draw_red_circle():
    circle = canvas.create_oval(15, 10, 35, 30, fill="red")

window = tk.Tk()
window.title("Productivity!")
window.geometry("400x300")
window.attributes("-topmost", True)  # Set window to always on top

# Create text field for text entry
text_field = tk.Entry(window, width=15, font=("Garamond", 14))
text_field.grid(row=3, column=0, padx=10, pady=1)

# Create text field for number entry
number_field = tk.Entry(window, width=7, font=("Garamond", 14))
number_field.grid(row=3, column=1, padx=10, pady=1)

# Create text field for result display
result_field = tk.Text(window, width=23, height=3, font=("Garamond", 14))
result_field.grid(row=1, column=0, columnspan=2, padx=10, pady=1)
result_field.config(state=tk.DISABLED)

# Create timer label for countdown and countup
timer_field = tk.Label(window, text="", font=("Garamond", 14, "bold"))
timer_field.grid(row=2, column=0, padx=10, pady=1)

# Create canvas for red circle
canvas = tk.Canvas(window, width=40, height=40)
canvas.grid(row=2, column=1, padx=1, pady=1)


# Create history field
history_field = tk.Text(window, width=40, height=15, font=("Garamond", 12))
history_field.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
history_field.config(state=tk.DISABLED)

text_field.focus_set()

# Bind Enter key press to the newActivity function
window.bind('<Return>', lambda event: newActivity())

style = ttk.Style()
style.configure("TButton", font=("Cormorant", 18, "bold"))

window.mainloop()
