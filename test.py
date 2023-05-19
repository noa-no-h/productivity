import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import threading

def newActivity():
    text_value = text_field.get()
    minutes = int(number_field.get())

    formatted_time_start = datetime.now().strftime("%H:%M")
    time_end = datetime.now() + timedelta(minutes=minutes)
    formatted_time_end = time_end.strftime("%H:%M")

    result_field.config(state=tk.NORMAL)
    result_field.delete("1.0", tk.END)
    result_field.insert(tk.END, f"{text_value} {minutes} minutes.\nStarted {formatted_time_start}. Ends {formatted_time_end}")
    result_field.config(state=tk.DISABLED)

    # Create and start the countdown and countup threads. threads run these simultaneously
    countdown_thread = threading.Thread(target=countdown, args=(minutes,))
    countup_thread = threading.Thread(target=countup)
    countdown_thread.start()
    countup_thread.start()

    text_field.delete(0, tk.END)
    number_field.delete(0, tk.END)
    text_field.focus_set()

def countdown(minutes):
    seconds = 0
    timer_field.config(text=f"{minutes:02d}:{seconds:02d}")  # Set initial value
    while minutes >= 0:
        timer_field.config(text=f"{minutes:02d}:{seconds:02d}")
        window.update()
        if seconds == 0:
            if minutes == 0:
                break
            minutes -= 1
            seconds = 59
        else:
            seconds -= 1
        window.after(1000)

def task_done():
    pass


def countup():
    minutes = 0
    seconds = 0
    print(f'{minutes} {seconds}')
    while True:
        countup_field.config(text=f"{minutes:02d}:{seconds:02d}")
        window.update()
        if seconds == 59:
            minutes += 1
            seconds = 0
        else:
            seconds += 1
        window.after(1000)


window = tk.Tk()
window.title("Productivity!")
window.geometry("400x300")
window.attributes("-topmost", True)  # Set window to always on top

# Create text field for text entry
text_field = tk.Entry(window, width=15, font=("Garamond", 14))
text_field.grid(row=2, column=0, padx=10, pady=10)

# Create text field for number entry
number_field = tk.Entry(window, width=7, font=("Garamond", 14))
number_field.grid(row=2, column=1, padx=10, pady=10)

# Create text field for result display
result_field = tk.Text(window, width=23, height=3, font=("Garamond", 14))
result_field.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
result_field.config(state=tk.DISABLED)

# Create timer label for countdown
timer_field = tk.Label(window, text="", font=("Garamond", 14, "bold"))
timer_field.grid(row=3, column=0, padx=10, pady=10)

# Create timer label for countup
countup_field = tk.Label(window, text="", font=("Garamond", 14, "bold"))
countup_field.grid(row=3, column=1, padx=10, pady=10)

text_field.focus_set()

# Bind Enter key press to the newActivity function
window.bind('<Return>', lambda event: newActivity())

style = ttk.Style()
style.configure("TButton", font=("Cormorant", 18, "bold"))

window.mainloop()
