import tkinter as tk

name = None
selected_time = None
feedback_result = None

def submit_name():
    global name
    name = name_entry.get()
    name_window.destroy()

def submit_time(choice):
    global selected_time
    selected_time = choice
    time_window.destroy()

def submit_feedback(feedback):
    global feedback_result
    feedback_result = feedback
    feedback_window.destroy()

def show_name_window():
    global name_entry, name_window
    name_window = tk.Tk()
    name_window.title("Enter Your Name")
    
    label = tk.Label(name_window, text="Please enter your name:")
    label.pack(pady=10)
    
    name_entry = tk.Entry(name_window)
    name_entry.pack(pady=5)
    
    submit_button = tk.Button(name_window, text="Submit", command=submit_name)
    submit_button.pack(pady=10)
    
    name_window.mainloop()
    return name  # 창이 닫힌 후 name 반환

def show_time_window():
    global time_window
    time_window = tk.Tk()
    time_window.title("Select Time Interval")
    
    label = tk.Label(time_window, text="Select the time interval (seconds):")
    label.pack(pady=10)
    
    button_1 = tk.Button(time_window, text="20 seconds", width=20, command=lambda: submit_time(19))
    button_1.pack(pady=5)
    
    button_2 = tk.Button(time_window, text="40 seconds", width=20, command=lambda: submit_time(39))
    button_2.pack(pady=5)
    
    button_3 = tk.Button(time_window, text="60 seconds", width=20, command=lambda: submit_time(59))
    button_3.pack(pady=5)
    
    time_window.mainloop()
    return selected_time  # 창이 닫힌 후 selected_time 반환

def show_feedback_window():
    global feedback_window
    feedback_window = tk.Tk()
    feedback_window.title("Feedback")
    
    label = tk.Label(feedback_window, text="Please provide your feedback on the system's performance:")
    label.pack(pady=10)
    
    buttons = ["Cold", "Cool", "Neutral", "Warm", "Hot"]
    
    for b in buttons:
        button = tk.Button(feedback_window, text=b, width=20, command=lambda b=b: submit_feedback(b))
        button.pack(pady=5)
    
    feedback_window.mainloop()
    return feedback_result  # 창이 닫힌 후 feedback_result 반환
