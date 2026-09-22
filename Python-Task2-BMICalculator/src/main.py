import tkinter as tk
from tkinter import ttk, messagebox

from src.bmi import calculate_bmi, get_bmi_category, get_category_color
from src.database import (
    initialize_database,
    save_bmi_record,
    get_user_history,
    get_all_users,
)


class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator")
        self.root.geometry("760x650")
        self.root.minsize(700, 600)

        self.root.configure(bg="#f4f6f8")

        initialize_database()

        self.create_styles()
        self.create_widgets()

    def create_styles(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 24, "bold"),
            background="#f4f6f8",
            foreground="#1f2937",
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 11),
            background="#f4f6f8",
            foreground="#6b7280",
        )

        style.configure(
            "Card.TFrame",
            background="white",
        )

        style.configure(
            "Field.TLabel",
            font=("Segoe UI", 11, "bold"),
            background="white",
            foreground="#374151",
        )

        style.configure(
            "Action.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=10,
        )

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=30, pady=25)

        # Header
        ttk.Label(
            main_frame,
            text="Advanced BMI Calculator",
            style="Title.TLabel",
        ).pack(anchor="center")

        ttk.Label(
            main_frame,
            text="Calculate, save, and track BMI history for multiple users",
            style="Subtitle.TLabel",
        ).pack(anchor="center", pady=(5, 20))

        # Input card
        input_card = ttk.Frame(
            main_frame,
            style="Card.TFrame",
            padding=25,
        )
        input_card.pack(fill="x")

        ttk.Label(
            input_card,
            text="User Name",
            style="Field.TLabel",
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.user_entry = ttk.Entry(
            input_card,
            width=35,
            font=("Segoe UI", 11),
        )
        self.user_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(
            input_card,
            text="Weight (kg)",
            style="Field.TLabel",
        ).grid(row=1, column=0, sticky="w", padx=10, pady=10)

        self.weight_entry = ttk.Entry(
            input_card,
            width=35,
            font=("Segoe UI", 11),
        )
        self.weight_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(
            input_card,
            text="Height (cm)",
            style="Field.TLabel",
        ).grid(row=2, column=0, sticky="w", padx=10, pady=10)

        self.height_entry = ttk.Entry(
            input_card,
            width=35,
            font=("Segoe UI", 11),
        )
        self.height_entry.grid(row=2, column=1, padx=10, pady=10)

        # Buttons
        button_frame = ttk.Frame(input_card)
        button_frame.grid(
            row=3,
            column=0,
            columnspan=2,
            pady=(15, 5),
        )

        ttk.Button(
            button_frame,
            text="Calculate BMI",
            style="Action.TButton",
            command=self.calculate_and_save,
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="View History",
            style="Action.TButton",
            command=self.show_history,
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="View Trend",
            style="Action.TButton",
            command=self.show_trend,
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Clear",
            style="Action.TButton",
            command=self.clear_fields,
        ).pack(side="left", padx=5)

        # Result card
        result_card = tk.Frame(
            main_frame,
            bg="white",
            bd=0,
            highlightthickness=1,
            highlightbackground="#e5e7eb",
        )
        result_card.pack(fill="x", pady=20)

        tk.Label(
            result_card,
            text="BMI RESULT",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#6b7280",
        ).pack(pady=(20, 5))

        self.bmi_label = tk.Label(
            result_card,
            text="--",
            font=("Segoe UI", 38, "bold"),
            bg="white",
            fg="#374151",
        )
        self.bmi_label.pack()

        self.category_label = tk.Label(
            result_card,
            text="Enter your details and calculate BMI",
            font=("Segoe UI", 15, "bold"),
            bg="white",
            fg="#6b7280",
        )
        self.category_label.pack(pady=(5, 20))

        # User selector
        user_frame = ttk.Frame(main_frame)
        user_frame.pack(fill="x", pady=5)

        ttk.Label(
            user_frame,
            text="Saved Users:",
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=(0, 10))

        self.user_combo = ttk.Combobox(
            user_frame,
            state="readonly",
            width=30,
        )
        self.user_combo.pack(side="left")

        ttk.Button(
            user_frame,
            text="Refresh Users",
            command=self.refresh_users,
        ).pack(side="left", padx=10)

        self.refresh_users()

    def calculate_and_save(self):
        user_name = self.user_entry.get().strip()
        weight_text = self.weight_entry.get().strip()
        height_text = self.height_entry.get().strip()

        if not user_name:
            messagebox.showwarning(
                "Missing Information",
                "Please enter a user name.",
            )
            return

        if not weight_text or not height_text:
            messagebox.showwarning(
                "Missing Information",
                "Please enter both weight and height.",
            )
            return

        try:
            weight = float(weight_text)
            height = float(height_text)

            bmi = calculate_bmi(weight, height)
            category = get_bmi_category(bmi)

            save_bmi_record(
                user_name,
                weight,
                height,
                bmi,
                category,
            )

            self.bmi_label.config(
                text=f"{bmi:.2f}",
                fg=get_category_color(category),
            )

            self.category_label.config(
                text=category,
                fg=get_category_color(category),
            )

            self.refresh_users()

            messagebox.showinfo(
                "BMI Saved",
                f"BMI for {user_name} has been saved successfully.",
            )

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Weight and height must be valid positive numbers.",
            )

        except RuntimeError as error:
            messagebox.showerror(
                "Database Error",
                str(error),
            )

    def show_history(self):
        user_name = self.user_entry.get().strip()

        if not user_name:
            user_name = self.user_combo.get().strip()

        if not user_name:
            messagebox.showwarning(
                "User Required",
                "Please enter or select a user.",
            )
            return

        try:
            records = get_user_history(user_name)

            if not records:
                messagebox.showinfo(
                    "No History",
                    f"No BMI records found for {user_name}.",
                )
                return

            history_window = tk.Toplevel(self.root)
            history_window.title(
                f"BMI History - {user_name}"
            )
            history_window.geometry("800x450")

            columns = (
                "date",
                "weight",
                "height",
                "bmi",
                "category",
            )

            tree = ttk.Treeview(
                history_window,
                columns=columns,
                show="headings",
            )

            tree.heading("date", text="Date")
            tree.heading("weight", text="Weight (kg)")
            tree.heading("height", text="Height (cm)")
            tree.heading("bmi", text="BMI")
            tree.heading("category", text="Category")

            tree.column("date", width=180)
            tree.column("weight", width=120)
            tree.column("height", width=120)
            tree.column("bmi", width=100)
            tree.column("category", width=150)

            for record in records:
                tree.insert(
                    "",
                    "end",
                    values=(
                        record["recorded_at"],
                        record["weight"],
                        record["height"],
                        record["bmi"],
                        record["category"],
                    ),
                )

            tree.pack(
                fill="both",
                expand=True,
                padx=20,
                pady=20,
            )

        except RuntimeError as error:
            messagebox.showerror(
                "Database Error",
                str(error),
            )

    def show_trend(self):
        user_name = self.user_entry.get().strip()

        if not user_name:
            user_name = self.user_combo.get().strip()

        if not user_name:
            messagebox.showwarning(
                "User Required",
                "Please enter or select a user.",
            )
            return

        try:
            records = get_user_history(user_name)

            if len(records) < 2:
                messagebox.showinfo(
                    "Not Enough Data",
                    "At least two BMI records are required "
                    "to display a trend.",
                )
                return

            import matplotlib.pyplot as plt

            dates = [
                record["recorded_at"]
                for record in records
            ]

            bmi_values = [
                record["bmi"]
                for record in records
            ]

            plt.figure(
                figsize=(10, 5)
            )

            plt.plot(
                dates,
                bmi_values,
                marker="o",
                linewidth=2,
            )

            plt.axhline(
                y=18.5,
                linestyle="--",
                label="Underweight Limit",
            )

            plt.axhline(
                y=25,
                linestyle="--",
                label="Normal Limit",
            )

            plt.axhline(
                y=30,
                linestyle="--",
                label="Obese Limit",
            )

            plt.title(
                f"BMI Trend - {user_name}",
                fontsize=16,
                fontweight="bold",
            )

            plt.xlabel("Date")
            plt.ylabel("BMI")

            plt.xticks(
                rotation=45,
                ha="right",
            )

            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.tight_layout()
            plt.show()

        except RuntimeError as error:
            messagebox.showerror(
                "Database Error",
                str(error),
            )

        except Exception as error:
            messagebox.showerror(
                "Chart Error",
                f"Unable to display BMI trend:\n{error}",
            )

    def refresh_users(self):
        try:
            users = get_all_users()

            self.user_combo["values"] = users

        except RuntimeError as error:
            messagebox.showerror(
                "Database Error",
                str(error),
            )

    def clear_fields(self):
        self.user_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)

        self.bmi_label.config(
            text="--",
            fg="#374151",
        )

        self.category_label.config(
            text="Enter your details and calculate BMI",
            fg="#6b7280",
        )


def main():
    root = tk.Tk()
    BMICalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()