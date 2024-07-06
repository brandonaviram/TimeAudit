import os
import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
import time
from datetime import datetime

class TimeAuditApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TimeAudit")
        self.root.geometry("300x200")  # Adjusted window size for more options and made it taller
        self.is_running = True

        self.label = tk.Label(root, text="TimeAudit is running...", font=("Helvetica", 12))
        self.label.pack(pady=10)

        self.quit_button = tk.Button(root, text="Quit", command=self.quit_app)
        self.quit_button.pack(pady=5)

        self.add_activity_button = tk.Button(root, text="Add Activity", command=self.show_prompt)
        self.add_activity_button.pack(pady=5)

        self.show_timelog_button = tk.Button(root, text="Show TimeLog", command=self.show_timelog)
        self.show_timelog_button.pack(pady=5)

        self.countdown_label = tk.Label(root, text="", font=("Helvetica", 10))
        self.countdown_label.pack(pady=5)

        self.logs_directory = os.path.join(os.path.expanduser("~"), 'Desktop', 'TimeAudit')
        self.log_file = os.path.join(self.logs_directory, 'TimeLog.md')
        self.create_logs_directory()

        self.prompt_thread = threading.Thread(target=self.start_prompt_timer)
        self.prompt_thread.daemon = True
        self.prompt_thread.start()
        print("Prompt thread started")  # Debug print

    def create_logs_directory(self):
        if not os.path.exists(self.logs_directory):
            os.makedirs(self.logs_directory)

    def start_prompt_timer(self):
        self.prompt_user()  # Prompt immediately on startup
        print("Initial prompt done")  # Debug print
        self.update_countdown(900)  # 15 minutes for actual use, change as needed

    def update_countdown(self, remaining_seconds):
        print(f"Updating countdown: {remaining_seconds} seconds remaining")  # Debug print
        if remaining_seconds > 0 and self.is_running:
            mins, secs = divmod(remaining_seconds, 60)
            time_format = f"Next prompt in: {mins:02}:{secs:02}"
            self.countdown_label.config(text=time_format)
            self.root.after(1000, self.update_countdown, remaining_seconds - 1)
        elif self.is_running:
            self.prompt_user()
            self.update_countdown(900)  # Reset countdown after prompt

    def prompt_user(self):
        if not self.is_running:
            return
        self.root.after(0, self.show_prompt)

    def show_prompt(self):
        prompt_window = tk.Toplevel(self.root)
        prompt_window.withdraw()  # Hide the window to calculate its size

        response = simpledialog.askstring("TimeAudit", "What are you working on?", parent=prompt_window)
        if response is None:
            prompt_window.destroy()
            return

        category = simpledialog.askstring("TimeAudit", "Category (e.g., Work, Personal)?", parent=prompt_window)
        if category is None:
            prompt_window.destroy()
            return

        priority = simpledialog.askstring("TimeAudit", "Priority (High, Medium, Low)?", parent=prompt_window)
        if priority is None:
            prompt_window.destroy()
            return

        energy = simpledialog.askstring("TimeAudit", "Energy Level (High, Medium, Low)?", parent=prompt_window)
        if energy is None:
            prompt_window.destroy()
            return

        mood = simpledialog.askstring("TimeAudit", "Mood (e.g., Happy, Stressed)?", parent=prompt_window)
        if mood is None:
            prompt_window.destroy()
            return

        location = simpledialog.askstring("TimeAudit", "Location (e.g., Home, Office)?", parent=prompt_window)
        if location is None:
            prompt_window.destroy()
            return

        prompt_window.update_idletasks()  # Update "requested size" from geometry manager
        width = prompt_window.winfo_reqwidth()
        height = prompt_window.winfo_reqheight()
        x = (prompt_window.winfo_screenwidth() // 2) - (width // 2)
        y = (prompt_window.winfo_screenheight() // 2) - (height // 2)
        prompt_window.geometry(f'{width}x{height}+{x}+{y}')
        prompt_window.deiconify()  # Show the window again

        self.log_response(response, category, priority, energy, mood, location)
        prompt_window.destroy()  # Destroy the prompt window after use

    def log_response(self, response, category, priority, energy, mood, location):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = (f"### {timestamp}\n"
                     f"- Activity: {response}\n"
                     f"- Category: {category}\n"
                     f"- Priority: {priority}\n"
                     f"- Energy Level: {energy}\n"
                     f"- Mood: {mood}\n"
                     f"- Location: {location}\n\n")
        with open(self.log_file, 'a') as file:
            file.write(log_entry)

    def show_timelog(self):
        if os.path.exists(self.logs_directory):
            if os.name == 'nt':  # For Windows
                os.startfile(self.logs_directory)
            elif os.name == 'posix':  # For macOS and Linux
                os.system(f'open "{self.logs_directory}"')
            else:
                messagebox.showerror("TimeAudit", "Unsupported OS.")
        else:
            messagebox.showerror("TimeAudit", "Log directory does not exist.")

    def quit_app(self):
        self.is_running = False
        messagebox.showinfo("TimeAudit", "TimeAudit is shutting down.")
        self.root.destroy()

def main():
    root = tk.Tk()
    app = TimeAuditApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
