import tkinter as tk
from tkinter import messagebox, simpledialog
import calendar
from datetime import datetime

class CalendarReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monthly Calendar with Reminders")
        self.root.geometry("500x500")
        
        # Dictionary to store reminders in format  }
        self.reminders = {}

        # Start with the current month and year
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        # Header to show the current month and year
        self.header = tk.Label(self.root, text=" ", font=("Times Now", 20))
        self.header.pack(pady=10)
        
        # Navigation buttons to change month
        nav_frame = tk.Frame(self.root)
        nav_frame.pack()
        tk.Button(nav_frame, text="<", command=self.prev_month).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text=">", command=self.next_month).pack(side=tk.RIGHT, padx=5)

        # Frame to hold the calendar
        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack(pady=5)

        # Display the calendar for the current month and year
        self.display_calendar(self.current_year, self.current_month)

    def display_calendar(self, year, month):
        # Clear the previous calendar display
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Update the header
        self.header.config(text=f"{calendar.month_name[month]} {year}")

        # Display the weekday headers
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, width=5, font=("Arial", 10, "bold")).grid(row=0, column=i)

        # Get the calendar matrix (weeks and days)
        month_calendar = calendar.monthcalendar(year, month)

        # Display the calendar days
        for row_num, week in enumerate(month_calendar, start=1):
            for col_num, day in enumerate(week):
                if day != 0:  # Ignore empty cells
                    date_str = f"{year}-{month:02d}-{day:02d}"
                    # Create a button for each valid day
                    btn = tk.Button(
                        self.calendar_frame,
                        text=str(day),
                        width=5,
                        command=lambda d=date_str: self.manage_reminders(d)
                    )
                    # Highlight dates with reminders
                    if date_str in self.reminders:
                        btn.config(bg="lightgreen")
                    btn.grid(row=row_num, column=col_num)
    def manage_reminders(self, date_str):
        # Ask the user what they want to do
        choice = simpledialog.askstring(
            "Reminder Options",
            f"What do you want to do for {date_str}? (add/view/delete):"
        )

        if not choice:
            return  # Cancelled input

        choice = choice.lower()

        # Add a reminder
        if choice == "add":
            reminder = simpledialog.askstring("Add Reminder", "Enter your reminder:")
            if reminder:
                self.reminders.setdefault(date_str, []).append(reminder)
                messagebox.showinfo("Success", "Reminder added!")

        # View reminders
        elif choice == "view":
            items = self.reminders.get(date_str, ["No reminders"])
            messagebox.showinfo(f"Reminders for {date_str}", "\n".join(items))

        # Delete reminders
        elif choice == "delete":
            if date_str in self.reminders:
                del self.reminders[date_str]
                messagebox.showinfo("Deleted", "All reminders deleted for this date.")
            else:
                messagebox.showinfo("Info", "No reminders to delete.")

        else:
            messagebox.showinfo("Invalid Option", "Please enter add, view, or delete.")

        # Refresh the calendar view
        self.display_calendar(self.current_year, self.current_month)
        
    def prev_month(self):
        # Go to previous month
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.display_calendar(self.current_year, self.current_month)

    def next_month(self):
        # Go to next month
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.display_calendar(self.current_year, self.current_month)

# Start the app
if __name__ == '__main__':
    root = tk.Tk()
    app = CalendarReminderApp(root)
    root.mainloop()
