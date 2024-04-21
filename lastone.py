import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from random import choice

tasks = []
label_colors = {}


def calc_time(date, time):
    time = time.split(":")
    calculated_time = datetime.strptime(date, "%Y-%m-%d")
    calculated_time = calculated_time + timedelta(hours=int(time[0]), minutes=int(time[1]))
    return calculated_time


def calc_reminder_date(deadline_date, deadline_time, days_before):
    deadline_datetime = calc_time(deadline_date, deadline_time)
    current_datetime = datetime.now()
    if deadline_datetime < current_datetime:
        return None
    reminder_datetime = deadline_datetime - timedelta(days=days_before)
    return reminder_datetime


def show_error_message(message):
    messagebox.showerror("Error", message)


def add_task():
    task_name = task_entry.get()
    deadline_date = deadline_date_entry.get()
    deadline_time = deadline_time_entry.get()
    days_before = int(days_before_entry.get())
    label = label_entry.get()

    if label not in label_colors:
        label_colors[label] = generate_color()

    reminder_datetime = calc_reminder_date(deadline_date, deadline_time, days_before)

    if reminder_datetime is None:
        show_error_message("This deadline has already passed !!")
        return

    tasks.append({"task": task_name, "completed": False, "deadline": calc_time(deadline_date, deadline_time),
                  "reminder_datetime": reminder_datetime, "label": label, "color": label_colors[label]})

    update_task_list()
    clear_entry_fields()


def is_deadline_approaching(reminder_datetime):
    if reminder_datetime and reminder_datetime < datetime.now():
        return True
    else:
        return False


def remove_task():
    selected_task_index = task_list.curselection()
    if selected_task_index:
        tasks.pop(selected_task_index[0])
        update_task_list()


def mark_completed():
    selected_task_index = task_list.curselection()
    if selected_task_index:
        tasks[selected_task_index[0]]["completed"] = True
        update_task_list()


def clear_completed_tasks():
    global tasks
    tasks = [task for task in tasks if not task["completed"]]
    update_task_list()


def export_tasks():  # User should enter the name of the file
    with open("tasks_output.txt", "w") as file:
        for task in tasks:
            status = "Completed" if task["completed"] else "Pending"
            file.write(f"{task['task']} - {status} - Deadline: {task['deadline']} - Label: {task['label']}\n")


def load_tasks():  # User should enter the name of the file
    global tasks, label_colors
    tasks = []
    label_colors = {}
    try:
        with open("tasks_output.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                task_info = parse_task_text(line)
                if task_info["label"] not in label_colors:
                    label_colors[task_info["label"]] = generate_color()
                task_info["color"] = label_colors[task_info["label"]]
                tasks.append(task_info)
    except FileNotFoundError:
        show_error_message("File is not found !!")
    update_task_list()


def parse_task_text(task_text):
    # Split the task text into components using the '-' separator
    components = [part.strip() for part in task_text.split('-')]

    # Extracting individual components
    task_name = components[0]
    status = components[1]
    deadline_info = components[2].split(': ')[1].split(' -')
    deadline_date = deadline_info[0]
    deadline_time = deadline_info[1]
    label_info = components[3].split(': ')[1]

    # Create a dictionary with the extracted data
    task_dict = {
        "task": task_name,
        "completed": status,
        "deadline": calc_time(deadline_date, deadline_time),
        "label": label_info
    }

    return task_dict


def update_task_list():
    task_list.delete(0, tk.END)

    for task in tasks:
        status = "Completed" if task["completed"] else "Pending"
        task_text = f"{task['task']} - {status} - Deadline: {task['deadline']} - Label: {task['label']}  "

        if is_deadline_approaching(task["reminder_datetime"]):
            task_text += "  Deadline is Approaching !!"
            messagebox.showwarning("Approaching Deadline", f"The deadline for '{task['task']}' is approaching !!")

        task_list.insert(tk.END, task_text)
        task_list.itemconfig(tk.END, {'bg': task['color']})


def clear_entry_fields():
    task_entry.delete(0, tk.END)
    deadline_date_entry.delete(0, tk.END)
    deadline_time_entry.delete(0, tk.END)
    days_before_entry.delete(0, tk.END)
    label_entry.delete(0, tk.END)


def generate_color():
    return f"#{''.join([choice('0123456789ABCDEF') for _ in range(6)])}"


# GUI setup
root = tk.Tk()
root.title("To-Do List")
root.geometry("700x400")
# Task Entry
tk.Label(root, text="Task:").grid(row=0, column=0, sticky=tk.E)
task_entry = tk.Entry(root)
task_entry.grid(row=0, column=1, columnspan=2, sticky=tk.W)

# Deadline Entry
tk.Label(root, text="Deadline date(yyyy-mm-dd):").grid(row=1, column=0, sticky=tk.E)
deadline_date_entry = tk.Entry(root)
deadline_date_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W)

tk.Label(root, text="Deadline time(HH-MM):").grid(row=2, column=0, sticky=tk.E)
deadline_time_entry = tk.Entry(root)
deadline_time_entry.grid(row=2, column=1, columnspan=2, sticky=tk.W)

# Days Before Entry
tk.Label(root, text="Days Before:").grid(row=3, column=0, sticky=tk.E)
days_before_entry = tk.Entry(root)
days_before_entry.grid(row=3, column=1, columnspan=2, sticky=tk.W)

# Label Entry
tk.Label(root, text="Label:").grid(row=4, column=0, sticky=tk.E)
label_entry = tk.Entry(root)
label_entry.grid(row=4, column=1, columnspan=2, sticky=tk.W)

# Add Task Button
add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.grid(row=5, column=0, columnspan=2)

# Remove Task Button
remove_button = tk.Button(root, text="Remove Task", command=remove_task)
remove_button.grid(row=5, column=2)

# Mark Completed Button
mark_completed_button = tk.Button(root, text="Mark as Complete", command=mark_completed)
mark_completed_button.grid(row=5, column=3)

# Clear Completed Tasks Button
clear_completed_button = tk.Button(root, text="Clear Completed Tasks", command=clear_completed_tasks)
clear_completed_button.grid(row=5, column=4)

# Export Tasks Button
export_button = tk.Button(root, text="Export Tasks", command=export_tasks)
export_button.grid(row=5, column=5)

# Load Tasks Button
load_button = tk.Button(root, text="Load Tasks", command=load_tasks)
load_button.grid(row=5, column=6)

# Task List
task_list = tk.Listbox(root, height=15, width=90, selectbackground='lightblue')
task_list.grid(row=6, column=0, columnspan=7)

# Start GUI main loop
root.mainloop()