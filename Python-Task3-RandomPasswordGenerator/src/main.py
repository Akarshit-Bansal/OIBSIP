import tkinter as tk
from tkinter import ttk, messagebox

import pyperclip

from password_generator import (
    generate_password,
    calculate_strength,
)


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Random Password Generator")
        self.root.geometry("700x650")
        self.root.resizable(False, False)

        # Store only the last 5 generated passwords for this session.
        self.history = []

        self.setup_variables()
        self.setup_style()
        self.create_widgets()

    def setup_variables(self):
        self.length_var = tk.IntVar(value=16)

        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)

        self.exclude_ambiguous_var = tk.BooleanVar(value=True)

        self.password_var = tk.StringVar()
        self.strength_var = tk.StringVar(value="Strength: —")

    def setup_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 22, "bold"),
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 10),
        )

        style.configure(
            "Section.TLabel",
            font=("Segoe UI", 12, "bold"),
        )

        style.configure(
            "Generate.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=10,
        )

        style.configure(
            "Action.TButton",
            font=("Segoe UI", 10),
            padding=7,
        )

    def create_widgets(self):
        main = ttk.Frame(self.root, padding=25)
        main.pack(fill="both", expand=True)

        # ---------------------------------------------------------
        # Header
        # ---------------------------------------------------------
        ttk.Label(
            main,
            text="Secure Random Password Generator",
            style="Title.TLabel",
        ).pack(pady=(0, 5))

        ttk.Label(
            main,
            text=(
                "Generate strong passwords using Python's "
                "cryptographically secure secrets module."
            ),
            style="Subtitle.TLabel",
        ).pack(pady=(0, 20))

        # ---------------------------------------------------------
        # Password display
        # ---------------------------------------------------------
        password_frame = ttk.LabelFrame(
            main,
            text="Generated Password",
            padding=15,
        )
        password_frame.pack(fill="x", pady=5)

        self.password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            font=("Consolas", 16),
            justify="center",
            state="readonly",
        )
        self.password_entry.pack(
            fill="x",
            ipady=8,
            padx=5,
        )

        strength_frame = ttk.Frame(password_frame)
        strength_frame.pack(fill="x", pady=(12, 0))

        self.strength_label = ttk.Label(
            strength_frame,
            textvariable=self.strength_var,
            font=("Segoe UI", 11, "bold"),
        )
        self.strength_label.pack()

        # ---------------------------------------------------------
        # Password length
        # ---------------------------------------------------------
        settings_frame = ttk.LabelFrame(
            main,
            text="Password Settings",
            padding=15,
        )
        settings_frame.pack(fill="x", pady=10)

        length_row = ttk.Frame(settings_frame)
        length_row.pack(fill="x", pady=(0, 10))

        ttk.Label(
            length_row,
            text="Password Length:",
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left")

        self.length_spinbox = tk.Spinbox(
            length_row,
            from_=8,
            to=128,
            textvariable=self.length_var,
            width=8,
            font=("Segoe UI", 10),
        )
        self.length_spinbox.pack(
            side="left",
            padx=(15, 0),
        )

        # ---------------------------------------------------------
        # Character type checkboxes
        # ---------------------------------------------------------
        ttk.Label(
            settings_frame,
            text="Character Types",
            style="Section.TLabel",
        ).pack(anchor="w", pady=(5, 8))

        types_frame = ttk.Frame(settings_frame)
        types_frame.pack(fill="x")

        ttk.Checkbutton(
            types_frame,
            text="Uppercase (A-Z)",
            variable=self.uppercase_var,
        ).grid(row=0, column=0, sticky="w", padx=5, pady=4)

        ttk.Checkbutton(
            types_frame,
            text="Lowercase (a-z)",
            variable=self.lowercase_var,
        ).grid(row=0, column=1, sticky="w", padx=5, pady=4)

        ttk.Checkbutton(
            types_frame,
            text="Numbers (0-9)",
            variable=self.numbers_var,
        ).grid(row=1, column=0, sticky="w", padx=5, pady=4)

        ttk.Checkbutton(
            types_frame,
            text="Symbols (!@#$...)",
            variable=self.symbols_var,
        ).grid(row=1, column=1, sticky="w", padx=5, pady=4)

        ttk.Checkbutton(
            settings_frame,
            text="Exclude ambiguous characters (0, O, l, 1, I)",
            variable=self.exclude_ambiguous_var,
        ).pack(anchor="w", pady=(10, 0))

        # ---------------------------------------------------------
        # Buttons
        # ---------------------------------------------------------
        button_frame = ttk.Frame(main)
        button_frame.pack(fill="x", pady=10)

        ttk.Button(
            button_frame,
            text="Generate Password",
            command=self.generate,
            style="Generate.TButton",
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=(0, 5),
        )

        ttk.Button(
            button_frame,
            text="Copy to Clipboard",
            command=self.copy_password,
            style="Action.TButton",
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=5,
        )

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_password,
            style="Action.TButton",
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=(5, 0),
        )

        # ---------------------------------------------------------
        # History
        # ---------------------------------------------------------
        history_frame = ttk.LabelFrame(
            main,
            text="Generation History — Last 5",
            padding=10,
        )
        history_frame.pack(fill="both", expand=True, pady=(5, 0))

        self.history_listbox = tk.Listbox(
            history_frame,
            height=5,
            font=("Consolas", 11),
            activestyle="none",
        )
        self.history_listbox.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar = ttk.Scrollbar(
            history_frame,
            orient="vertical",
            command=self.history_listbox.yview,
        )
        scrollbar.pack(side="right", fill="y")

        self.history_listbox.config(
            yscrollcommand=scrollbar.set
        )

        ttk.Label(
            main,
            text="History is session-only and is never saved to disk.",
            font=("Segoe UI", 8),
        ).pack(pady=(8, 0))

    def get_selected_type_count(self):
        return sum(
            [
                self.uppercase_var.get(),
                self.lowercase_var.get(),
                self.numbers_var.get(),
                self.symbols_var.get(),
            ]
        )

    def generate(self):
        try:
            length = int(self.length_var.get())

            if length < 8:
                raise ValueError(
                    "Password length must be at least 8 characters."
                )

            selected_count = self.get_selected_type_count()

            if selected_count < 2:
                raise ValueError(
                    "Please select at least two character types."
                )

            password = generate_password(
                length=length,
                use_uppercase=self.uppercase_var.get(),
                use_lowercase=self.lowercase_var.get(),
                use_numbers=self.numbers_var.get(),
                use_symbols=self.symbols_var.get(),
                exclude_ambiguous=self.exclude_ambiguous_var.get(),
            )

            self.password_var.set(password)

            strength = calculate_strength(
                password,
                selected_count,
            )

            self.strength_var.set(
                f"Strength: {strength}"
            )

            self.update_strength_display(strength)
            self.add_to_history(password)

            # Automatically copy the newly generated password.
            self.copy_to_clipboard(silent=True)

        except ValueError as error:
            messagebox.showerror(
                "Invalid Settings",
                str(error),
            )

        except Exception as error:
            messagebox.showerror(
                "Generation Error",
                f"Unable to generate password:\n\n{error}",
            )

    def update_strength_display(self, strength):
        if strength == "Strong":
            self.strength_label.configure(
                text="Strength: Strong ✓"
            )

        elif strength == "Medium":
            self.strength_label.configure(
                text="Strength: Medium"
            )

        else:
            self.strength_label.configure(
                text="Strength: Weak"
            )

    def add_to_history(self, password):
        self.history.insert(0, password)

        # Keep only the most recent five passwords.
        self.history = self.history[:5]

        self.history_listbox.delete(0, tk.END)

        for item in self.history:
            self.history_listbox.insert(
                tk.END,
                item,
            )

    def copy_to_clipboard(self, silent=False):
        password = self.password_var.get()

        if not password:
            if not silent:
                messagebox.showwarning(
                    "No Password",
                    "Generate a password first.",
                )
            return

        try:
            pyperclip.copy(password)

            if not silent:
                messagebox.showinfo(
                    "Copied",
                    "Password copied to clipboard.",
                )

        except Exception as error:
            if not silent:
                messagebox.showerror(
                    "Clipboard Error",
                    f"Could not copy password:\n\n{error}",
                )

    def copy_password(self):
        self.copy_to_clipboard(silent=False)

    def clear_password(self):
        self.password_var.set("")
        self.strength_var.set("Strength: —")
        self.strength_label.configure(
            text="Strength: —"
        )


def main():
    root = tk.Tk()
    app = PasswordGeneratorApp(root)

    # Generate an initial password when the application starts.
    app.generate()

    root.mainloop()


if __name__ == "__main__":
    main()
