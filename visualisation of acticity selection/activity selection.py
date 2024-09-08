import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
def get_user_input():
 root = tk.Tk()
 root.title("Activity Input")
 num_activities = tk.IntVar()
 start_time_vars = []
 end_time_vars = []
 activities = []
 def submit():
 activities.clear()
 for i in range(num_activities.get()):
 start_time = int(start_time_vars[i].get())
end_time = int(end_time_vars[i].get())
 if start_time < 0:
 messagebox.showerror("Input Error", f"Activity {i + 1}: Start time cannot be negative.")
 break
 if start_time >= end_time:
 messagebox.showerror("Input Error", f"Activity {i + 1}: Start time cannot be greater than or equal 
to end time.")
 break
 activities.append((start_time, end_time, i + 1))
 root.quit()
 def create_activity_entries():
 for widget in root.pack_slaves():
 widget.destroy()
 for i in range(num_activities.get()):
 activity_frame = ttk.Frame(root)
 activity_frame.pack(padx=10, pady=5)
 ttk.Label(activity_frame, text=f"Activity {i + 1}:\t", font=('calibri', 15, 'bold')).pack(side='left', pady=0)
 ttk.Label(activity_frame, text=f"Start Time", font=('Helvetica', 10)).pack(side='left', pady=0)
 start_time_var = tk.StringVar()
 ttk.Entry(activity_frame, textvariable=start_time_var, width=8).pack(side='left', pady=0)
 ttk.Label(activity_frame, text="\tEnd Time", font=('Helvetica', 10)).pack(side='left', pady=0)
 end_time_var = tk.StringVar()
 ttk.Entry(activity_frame, textvariable=end_time_var, width=8).pack(side='left', pady=0)
 start_time_vars.append(start_time_var)
 end_time_vars.append(end_time_var)
 submit_button = ttk.Button(root, text="Submit", command=submit)
 submit_button.pack(pady=5)
 root.bind("<Return>", lambda event: submit())
 input_frame = ttk.Frame(root)
 input_frame.pack(padx=20, pady=10)
 ttk.Label(input_frame, text="Enter the number of activities: ", font=('Helvetica', 12, 
'bold')).pack(side='left', pady=0)
 num_activities_entry = ttk.Entry(input_frame, textvariable=num_activities, width=10, font=('Helvetica', 
10, 'bold'))
 num_activities_entry.pack(pady=0)
 
 create_activities_button = ttk.Button(root, text="Create Activity Entries", 
command=create_activity_entries,)
create_activities_button.pack(pady=10)
 num_activities_entry.bind("<Return>", lambda event: create_activity_entries())
 root.mainloop()
 return activities, num_activities.get()
def activity_selection(activities):
 n = 0
 activities.sort(key=lambda x: (x[1], x[0]))
 selected_activities = []
 last_end_time = float('-inf')
 for activity in activities:
 start_time, end_time, activity_num = activity
 if start_time >= last_end_time:
 selected_activities.append(activity)
 n = n+1
 last_end_time = end_time
 return selected_activities, activities, n
def plot_all_activities(ax, displayed_activities, selected_activities, n):
 bar_height = 0.3
 for index, activity in enumerate(displayed_activities):
 start, end, num = activity
 color = 'red'
 t = f'✘'
 if activity in selected_activities:
 color = 'green'
 t = f'✔'
 rect = mpatches.Rectangle((start, index), end - start, bar_height, color=color, alpha=0.5)
 ax.add_patch(rect)
 ax.text(start + (end - start) / 2, index + bar_height / 2, f'Activity{num}',
 color='white' if color == 'red' else 'red', ha='center', va='center', fontsize=(35 / n))
 ax.text(end+0.05, index + 0.05, f'{t}', color='black' if color == 'red' else 'black', fontsize=(80/n))
def sort_and_unsorted_activities(ax, displayed_activities, n, color):
 bar_height = 0.3
 for index, activity in enumerate(displayed_activities):
 start, end, num = activity
 rect = mpatches.Rectangle((start, index), end - start, bar_height, color=color, alpha=0.5)
 ax.add_patch(rect)
 ax.text(start + (end - start) / 2, index + bar_height / 2, f'Activity{num}',
color='white', ha='center', va='center', fontsize=(37 / n))
def main():
 activities, num_activities = get_user_input()
 min_start_time = min(activities, key=lambda x: x[0])[0]
 max_end_time = max(activities, key=lambda x: x[1])[1]
 fig, ax = plt.subplots(figsize=(12, 6))
 plot_unsort_sort(activities, ax, min_start_time, max_end_time, num_activities, "UNSORTED ACTIVITY", 
'red')
 selected_activities, sorted_activity, n = activity_selection(activities)
 plot_unsort_sort(activities, ax, min_start_time, max_end_time, num_activities, "SORTED ACTIVITY", 
'blue')
 plot_bar(activities, ax, min_start_time, max_end_time, selected_activities, num_activities)
 plot_unsort_sort(selected_activities, ax, min_start_time, max_end_time, num_activities, "SELECTED 
ACTIVITY", 'purple')
 plt.close(fig)
def plot_bar(activities, ax, min_start_time, max_end_time, selected_activities, num_activities):
 ax.set_xlim(min_start_time - 1, max_end_time + 5)
 ax.set_ylim(-0.5, len(activities) - 0.5)
 ax.set_yticks(range(len(activities)))
 ax.set_yticklabels([f'{i + 1}' for i in range(len(activities))])
 ax.set_xlabel('Time')
 ax.set_xticks(range(min_start_time - 1, max_end_time + 6))
 ax.set_xticklabels(range(min_start_time - 1, max_end_time + 6))
 ax.grid(True, axis='x', linestyle='--', alpha=0.5)
 index = 0
 displayed_activities = []
 while index < len(activities):
 displayed_activities.append(activities[index])
 ax.clear()
 ax.set_xlim(min_start_time - 1, max_end_time + 2)
 ax.set_ylim(-0.5, len(activities) - 0.5)
 ax.set_yticks(range(len(activities)))
 ax.set_yticklabels([f'{i + 1}' for i in range(len(activities))])
 ax.set_ylabel('Activities→', fontsize=20)
 ax.set_xlabel('Time→', fontsize=20)
 ax.set_xticks(range(min_start_time - 1, max_end_time + 2))
 ax.set_xticklabels(range(min_start_time - 1, max_end_time + 2))
 ax.grid(True, axis='x', linestyle='--', alpha=0.5)
 plot_all_activities(ax, displayed_activities, selected_activities, num_activities)
 ax.set_title('ACTIVITY SELECTION')
plt.draw()
 plt.waitforbuttonpress()
 index += 1
 return
def plot_unsort_sort(activities, ax, min_start_time, max_end_time, num_activities, text, color):
 ax.set_xlim(min_start_time - 1, max_end_time + 5)
 ax.set_ylim(-0.5, len(activities) - 0.5)
 ax.set_yticks(range(len(activities)))
 ax.set_yticklabels([f'{i + 1}' for i in range(len(activities))])
 ax.set_xlabel('Time')
 ax.set_xticks(range(min_start_time - 1, max_end_time + 6))
 ax.set_xticklabels(range(min_start_time - 1, max_end_time + 6))
 ax.grid(True, axis='x', linestyle='--', alpha=0.5)
 index = 0
 displayed_activities = []
 while index < len(activities):
 displayed_activities.append(activities[index])
 ax.clear()
 ax.set_xlim(min_start_time - 1, max_end_time + 2)
 ax.set_ylim(-0.5, len(activities) - 0.5)
 ax.set_yticks(range(len(activities)))
 ax.set_yticklabels([f'{i + 1}' for i in range(len(activities))])
 ax.set_ylabel('Activities→', fontsize=20)
 ax.set_xlabel('Time→', fontsize=20)
 ax.set_xticks(range(min_start_time - 1, max_end_time + 2))
 ax.set_xticklabels(range(min_start_time - 1, max_end_time + 2))
 ax.grid(True, axis='x', linestyle='--', alpha=0.5)
 sort_and_unsorted_activities(ax, displayed_activities, num_activities, color)
 ax.set_title(f'{text}')
 plt.draw()
 index += 1
 plt.waitforbuttonpress()
 return
main()