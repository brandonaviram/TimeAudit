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
        self.root.geometry("300x100")
        self.is_running = True

        self.label = tk.Label(root, text="TimeAudit is running...", font=("Helvetica", 12))
        self.label.pack(pady=20)

        self.quit_button = tk.Button(root, text="Quit", command=self.quit_app)
        self.quit_button.pack()

        self.logs_directory = os.path.join(os.path.expanduser("~"), 'Desktop', 'TimeAudit')
        self.log_file = os.path.join(self.logs_directory, 'logs.md')
        self.create_logs_directory()

        self.prompt_thread = threading.Thread(target=self.start_prompt_timer)
        self.prompt_thread.daemon = True
        self.prompt_thread.start()

    def create_logs_directory(self):
        if not os.path.exists(self.logs_directory):
            os.makedirs(self.logs_directory)

    def start_prompt_timer(self):
        self.prompt_user()  # Prompt immediately on startup
        while self.is_running:
            time.sleep(25 * 60)  # 25 minutes
            self.prompt_user()

    def prompt_user(self):
        if not self.is_running:
            return
        self.root.after(0, self.show_prompt)

    def show_prompt(self):
        response = simpledialog.askstring("TimeAudit", "What are you working on?")
        if response is not None:
            self.log_response(response)

    def log_response(self, response):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"### {timestamp}\n- {response}\n\n"
        with open(self.log_file, 'a') as file:
            file.write(log_entry)

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
