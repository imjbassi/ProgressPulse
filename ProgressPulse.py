"""ProgressPulse - a lightweight desktop fitness tracker.

Tkinter GUI backed by a MySQL database. Lets a user log workouts,
nutrition entries, and goals, and view a simple progress dashboard.

Configuration is read from environment variables (see .env.example)
so credentials never need to be hardcoded in source.
"""

import os
import sys
import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

import mysql.connector
from mysql.connector import Error as MySQLError

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

DB_CONFIG = {
    "host": os.environ.get("PP_DB_HOST", "localhost"),
    "user": os.environ.get("PP_DB_USER", "root"),
    "password": os.environ.get("PP_DB_PASSWORD", ""),
    "database": os.environ.get("PP_DB_NAME", "progresspulsedb"),
}


def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except MySQLError as exc:
        messagebox.showerror(
            "Database connection failed",
            f"Could not connect to MySQL:\n{exc}\n\n"
            "Check your .env settings and that the MySQL server is running.",
        )
        sys.exit(1)


class ProgressPulseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ProgressPulse")
        self.root.geometry("640x520")
        self.root.minsize(560, 460)

        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        self.current_user_id = tk.StringVar()

        self._build_user_bar()

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.workouts_tab = WorkoutsTab(notebook, self)
        self.nutrition_tab = NutritionTab(notebook, self)
        self.goals_tab = GoalsTab(notebook, self)
        self.dashboard_tab = DashboardTab(notebook, self)

        notebook.add(self.workouts_tab, text="Workouts")
        notebook.add(self.nutrition_tab, text="Nutrition")
        notebook.add(self.goals_tab, text="Goals")
        notebook.add(self.dashboard_tab, text="Dashboard")

        notebook.bind("<<NotebookTabChanged>>", lambda e: self.refresh_all())

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _build_user_bar(self):
        bar = ttk.Frame(self.root)
        bar.pack(fill="x", padx=10, pady=(10, 0))

        ttk.Label(bar, text="User ID:").pack(side="left")
        entry = ttk.Entry(bar, textvariable=self.current_user_id, width=8)
        entry.pack(side="left", padx=(4, 10))
        ttk.Button(bar, text="Refresh", command=self.refresh_all).pack(side="left")
        ttk.Label(
            bar,
            text="Enter a User ID from the Users table to view/manage their data.",
            foreground="gray",
        ).pack(side="left", padx=10)

    def refresh_all(self):
        for tab in (self.workouts_tab, self.nutrition_tab, self.goals_tab, self.dashboard_tab):
            tab.refresh()

    def get_user_id(self):
        uid = self.current_user_id.get().strip()
        if not uid.isdigit():
            messagebox.showwarning("Missing User ID", "Enter a numeric User ID first.")
            return None
        return int(uid)

    def on_close(self):
        try:
            self.cursor.close()
            self.conn.close()
        finally:
            self.root.destroy()


class BaseTab(ttk.Frame):
    """Shared scaffolding for a form + list + delete tab."""

    columns = ()
    table = ""
    id_column = ""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._build_form()
        self._build_list()

    def _build_form(self):
        raise NotImplementedError

    def _build_list(self):
        list_frame = ttk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=8, pady=(4, 8))

        self.tree = ttk.Treeview(list_frame, columns=self.columns, show="headings", height=8)
        for col in self.columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        ttk.Button(self, text="Delete Selected", command=self.delete_selected).pack(
            anchor="e", padx=8, pady=(0, 8)
        )

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        uid = self.app.current_user_id.get().strip()
        if not uid.isdigit():
            return

        try:
            self.app.cursor.execute(
                f"SELECT {', '.join(self.columns)} FROM {self.table} WHERE user_id = %s "
                f"ORDER BY {self.id_column} DESC",
                (int(uid),),
            )
            for row in self.app.cursor.fetchall():
                self.tree.insert("", "end", values=row)
        except MySQLError as exc:
            messagebox.showerror("Query failed", str(exc))

    def delete_selected(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("Nothing selected", "Select a row to delete.")
            return
        values = self.tree.item(selection[0], "values")
        record_id = values[0]
        if not messagebox.askyesno("Confirm delete", f"Delete record {record_id}?"):
            return
        try:
            self.app.cursor.execute(
                f"DELETE FROM {self.table} WHERE {self.id_column} = %s", (record_id,)
            )
            self.app.conn.commit()
            self.refresh()
        except MySQLError as exc:
            messagebox.showerror("Delete failed", str(exc))


class WorkoutsTab(BaseTab):
    columns = ("workout_id", "date", "workout_type", "duration")
    table = "Workouts"
    id_column = "workout_id"

    def _build_form(self):
        form = ttk.LabelFrame(self, text="Log a Workout")
        form.pack(fill="x", padx=8, pady=8)

        self.date_var = tk.StringVar(value=date.today().isoformat())
        self.type_var = tk.StringVar()
        self.duration_var = tk.StringVar()

        ttk.Label(form, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.date_var).grid(row=0, column=1, padx=4, pady=4)

        ttk.Label(form, text="Workout Type:").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.type_var).grid(row=1, column=1, padx=4, pady=4)

        ttk.Label(form, text="Duration (min):").grid(row=2, column=0, sticky="w", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.duration_var).grid(row=2, column=1, padx=4, pady=4)

        ttk.Button(form, text="Add Workout", command=self.add_workout).grid(
            row=3, column=0, columnspan=2, pady=8
        )

    def add_workout(self):
        uid = self.app.get_user_id()
        if uid is None:
            return
        duration = self.duration_var.get().strip()
        if not duration.isdigit():
            messagebox.showwarning("Invalid duration", "Duration must be a whole number of minutes.")
            return
        try:
            self.app.cursor.execute(
                "INSERT INTO Workouts (user_id, date, workout_type, duration) VALUES (%s, %s, %s, %s)",
                (uid, self.date_var.get().strip(), self.type_var.get().strip(), int(duration)),
            )
            self.app.conn.commit()
            messagebox.showinfo("Success", "Workout added.")
            self.type_var.set("")
            self.duration_var.set("")
            self.refresh()
        except MySQLError as exc:
            messagebox.showerror("Insert failed", str(exc))


class NutritionTab(BaseTab):
    columns = ("nutrition_id", "date", "meal_type", "calories")
    table = "Nutrition"
    id_column = "nutrition_id"

    def _build_form(self):
        form = ttk.LabelFrame(self, text="Log Nutrition")
        form.pack(fill="x", padx=8, pady=8)

        self.date_var = tk.StringVar(value=date.today().isoformat())
        self.meal_var = tk.StringVar()
        self.calories_var = tk.StringVar()

        ttk.Label(form, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.date_var).grid(row=0, column=1, padx=4, pady=4)

        ttk.Label(form, text="Meal Type:").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.meal_var).grid(row=1, column=1, padx=4, pady=4)

        ttk.Label(form, text="Calories:").grid(row=2, column=0, sticky="w", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.calories_var).grid(row=2, column=1, padx=4, pady=4)

        ttk.Button(form, text="Add Entry", command=self.add_entry).grid(
            row=3, column=0, columnspan=2, pady=8
        )

    def add_entry(self):
        uid = self.app.get_user_id()
        if uid is None:
            return
        calories = self.calories_var.get().strip()
        if not calories.isdigit():
            messagebox.showwarning("Invalid calories", "Calories must be a whole number.")
            return
        try:
            self.app.cursor.execute(
                "INSERT INTO Nutrition (user_id, date, meal_type, calories) VALUES (%s, %s, %s, %s)",
                (uid, self.date_var.get().strip(), self.meal_var.get().strip(), int(calories)),
            )
            self.app.conn.commit()
            messagebox.showinfo("Success", "Nutrition entry added.")
            self.meal_var.set("")
            self.calories_var.set("")
            self.refresh()
        except MySQLError as exc:
            messagebox.showerror("Insert failed", str(exc))


class GoalsTab(BaseTab):
    columns = ("goal_id", "goal_type", "target_value", "target_date")
    table = "Goals"
    id_column = "goal_id"

    def _build_form(self):
        form = ttk.LabelFrame(self, text="Set a Goal")
        form.pack(fill="x", padx=8, pady=8)

        self.goal_type_var = tk.StringVar()
        self.target_value_var = tk.StringVar()
        self.target_date_var = tk.StringVar(value=date.today().isoformat())

        ttk.Label(form, text="Goal Type:").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.goal_type_var).grid(row=0, column=1, padx=4, pady=4)

        ttk.Label(form, text="Target Value:").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.target_value_var).grid(row=1, column=1, padx=4, pady=4)

        ttk.Label(form, text="Target Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="w", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.target_date_var).grid(row=2, column=1, padx=4, pady=4)

        ttk.Button(form, text="Add Goal", command=self.add_goal).grid(
            row=3, column=0, columnspan=2, pady=8
        )

    def add_goal(self):
        uid = self.app.get_user_id()
        if uid is None:
            return
        target_value = self.target_value_var.get().strip()
        if not target_value.isdigit():
            messagebox.showwarning("Invalid target", "Target value must be a whole number.")
            return
        try:
            self.app.cursor.execute(
                "INSERT INTO Goals (user_id, goal_type, target_value, target_date) VALUES (%s, %s, %s, %s)",
                (uid, self.goal_type_var.get().strip(), int(target_value), self.target_date_var.get().strip()),
            )
            self.app.conn.commit()
            messagebox.showinfo("Success", "Goal added.")
            self.goal_type_var.set("")
            self.target_value_var.set("")
            self.refresh()
        except MySQLError as exc:
            messagebox.showerror("Insert failed", str(exc))


class DashboardTab(ttk.Frame):
    """Read-only summary of a user's activity."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.summary_labels = {}
        stats = ttk.LabelFrame(self, text="Summary")
        stats.pack(fill="x", padx=8, pady=8)

        for i, key in enumerate(("Total Workouts", "Total Minutes", "Total Calories Logged", "Active Goals")):
            ttk.Label(stats, text=f"{key}:").grid(row=i, column=0, sticky="w", padx=8, pady=4)
            value_label = ttk.Label(stats, text="-", font=("TkDefaultFont", 10, "bold"))
            value_label.grid(row=i, column=1, sticky="w", padx=8, pady=4)
            self.summary_labels[key] = value_label

    def refresh(self):
        uid = self.app.current_user_id.get().strip()
        if not uid.isdigit():
            for label in self.summary_labels.values():
                label.config(text="-")
            return

        uid = int(uid)
        cursor = self.app.cursor
        try:
            cursor.execute("SELECT COUNT(*), COALESCE(SUM(duration), 0) FROM Workouts WHERE user_id = %s", (uid,))
            workout_count, total_minutes = cursor.fetchone()

            cursor.execute("SELECT COALESCE(SUM(calories), 0) FROM Nutrition WHERE user_id = %s", (uid,))
            (total_calories,) = cursor.fetchone()

            cursor.execute("SELECT COUNT(*) FROM Goals WHERE user_id = %s", (uid,))
            (goal_count,) = cursor.fetchone()

            self.summary_labels["Total Workouts"].config(text=str(workout_count))
            self.summary_labels["Total Minutes"].config(text=str(total_minutes))
            self.summary_labels["Total Calories Logged"].config(text=str(total_calories))
            self.summary_labels["Active Goals"].config(text=str(goal_count))
        except MySQLError as exc:
            messagebox.showerror("Query failed", str(exc))


def main():
    root = tk.Tk()
    ProgressPulseApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
