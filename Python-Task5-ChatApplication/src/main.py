import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

from client import ChatClient
from chat_utils import (
    convert_shortcodes,
    format_chat_message,
    validate_room_name,
    validate_username,
)


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

APP_TITLE = "OIBSIP Chat Application"

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700


# ============================================================
# MAIN APPLICATION
# ============================================================

class ChatApplication:

    def __init__(self, root):

        self.root = root

        self.root.title(
            APP_TITLE
        )

        self.root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        )

        self.root.minsize(
            900,
            600
        )

        self.client = ChatClient()

        self.username = None
        self.current_room = "General"

        self.logged_in = False

        self.rooms = []

        self.login_frame = None
        self.chat_frame = None

        self.username_entry = None
        self.password_entry = None

        self.chat_display = None
        self.message_entry = None

        self.room_listbox = None
        self.room_label = None

        self.status_label = None

        self.original_title = APP_TITLE

        # ----------------------------------------------------
        # CALLBACKS
        # ----------------------------------------------------

        self.client.set_message_callback(
            self.handle_server_message
        )

        self.client.set_connection_callback(
            self.handle_connection
        )

        # ----------------------------------------------------
        # WINDOW EVENTS
        # ----------------------------------------------------

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_application
        )

        self.show_login_screen()

    # ========================================================
    # CONNECTION
    # ========================================================

    def connect_to_server(self):

        if self.client.running:
            return True

        return self.client.connect()

    # ========================================================
    # LOGIN SCREEN
    # ========================================================

    def show_login_screen(self):

        if self.chat_frame:

            self.chat_frame.destroy()

            self.chat_frame = None

        if self.login_frame:

            self.login_frame.destroy()

        self.root.title(
            f"{APP_TITLE} - Login"
        )

        self.login_frame = tk.Frame(
            self.root,
            bg="#0f172a"
        )

        self.login_frame.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # CENTER CARD
        # ----------------------------------------------------

        card = tk.Frame(
            self.login_frame,
            bg="#1e293b",
            padx=45,
            pady=40
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        title = tk.Label(
            card,
            text="OIBSIP Chat",
            font=("Segoe UI", 28, "bold"),
            bg="#1e293b",
            fg="white"
        )

        title.pack(
            pady=(0, 8)
        )

        subtitle = tk.Label(
            card,
            text="Real-Time Python Chat Application",
            font=("Segoe UI", 11),
            bg="#1e293b",
            fg="#94a3b8"
        )

        subtitle.pack(
            pady=(0, 30)
        )

        # ----------------------------------------------------
        # USERNAME
        # ----------------------------------------------------

        tk.Label(
            card,
            text="Username",
            font=("Segoe UI", 10, "bold"),
            bg="#1e293b",
            fg="white"
        ).pack(
            anchor="w"
        )

        self.username_entry = tk.Entry(
            card,
            width=32,
            font=("Segoe UI", 11),
            bg="#334155",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        self.username_entry.pack(
            pady=(5, 18),
            ipady=8
        )

        # ----------------------------------------------------
        # PASSWORD
        # ----------------------------------------------------

        tk.Label(
            card,
            text="Password",
            font=("Segoe UI", 10, "bold"),
            bg="#1e293b",
            fg="white"
        ).pack(
            anchor="w"
        )

        self.password_entry = tk.Entry(
            card,
            width=32,
            font=("Segoe UI", 11),
            bg="#334155",
            fg="white",
            insertbackground="white",
            show="*",
            relief="flat"
        )

        self.password_entry.pack(
            pady=(5, 25),
            ipady=8
        )

        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        button_frame = tk.Frame(
            card,
            bg="#1e293b"
        )

        button_frame.pack(
            fill="x"
        )

        login_button = tk.Button(
            button_frame,
            text="Login",
            command=self.login_user,
            font=("Segoe UI", 11, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10
        )

        login_button.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(0, 6)
        )

        register_button = tk.Button(
            button_frame,
            text="Register",
            command=self.register_user,
            font=("Segoe UI", 11, "bold"),
            bg="#475569",
            fg="white",
            activebackground="#334155",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10
        )

        register_button.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(6, 0)
        )

        self.username_entry.focus_set()

        self.password_entry.bind(
            "<Return>",
            lambda event: self.login_user()
        )

    # ========================================================
    # REGISTER
    # ========================================================

    def register_user(self):

        username = self.username_entry.get().strip()

        password = self.password_entry.get()

        valid, error = validate_username(
            username
        )

        if not valid:

            messagebox.showerror(
                "Invalid Username",
                error
            )

            return

        if len(password) < 6:

            messagebox.showerror(
                "Invalid Password",
                "Password must contain at least 6 characters."
            )

            return

        if not self.connect_to_server():

            messagebox.showerror(
                "Connection Error",
                "Could not connect to the chat server."
            )

            return

        # Temporarily listen for the registration response.
        self.client.register(
            username,
            password
        )

        self.pending_action = "register"

        self.username = username

        self._wait_for_auth_response(
            "register_response"
        )

    # ========================================================
    # LOGIN
    # ========================================================

    def login_user(self):

        username = self.username_entry.get().strip()

        password = self.password_entry.get()

        valid, error = validate_username(
            username
        )

        if not valid:

            messagebox.showerror(
                "Invalid Username",
                error
            )

            return

        if not password:

            messagebox.showerror(
                "Invalid Password",
                "Please enter your password."
            )

            return

        if not self.connect_to_server():

            messagebox.showerror(
                "Connection Error",
                "Could not connect to the chat server."
            )

            return

        self.pending_action = "login"

        self.client.login(
            username,
            password
        )

    # ========================================================
    # SERVER MESSAGE HANDLER
    # ========================================================

    def handle_server_message(
        self,
        message
    ):

        # Tkinter must be updated from its main thread.
        self.root.after(
            0,
            lambda: self.process_server_message(
                message
            )
        )

    # ========================================================
    # PROCESS SERVER MESSAGE
    # ========================================================

    def process_server_message(
        self,
        message
    ):

        message_type = message.get(
            "type"
        )

        # ----------------------------------------------------
        # LOGIN
        # ----------------------------------------------------

        if message_type == "login_response":

            if message.get("success"):

                self.username = message.get(
                    "username",
                    self.username
                )

                self.logged_in = True

                self.client.start_session(
                    self.username
                )

                self.show_chat_screen()

                return

            messagebox.showerror(
                "Login Failed",
                message.get(
                    "message",
                    "Invalid username or password."
                )
            )

        # ----------------------------------------------------
        # REGISTER
        # ----------------------------------------------------

        elif message_type == "register_response":

            if message.get("success"):

                messagebox.showinfo(
                    "Registration Successful",
                    "Account created successfully.\n\n"
                    "You can now login."
                )

                self.password_entry.delete(
                    0,
                    tk.END
                )

            else:

                messagebox.showerror(
                    "Registration Failed",
                    message.get(
                        "message",
                        "Registration failed."
                    )
                )

        # ----------------------------------------------------
        # ROOMS
        # ----------------------------------------------------

        elif message_type == "rooms_response":

            if message.get("success"):

                self.rooms = message.get(
                    "rooms",
                    []
                )

                self.update_room_list()

        # ----------------------------------------------------
        # CREATE ROOM
        # ----------------------------------------------------

        elif message_type == "create_room_response":

            if message.get("success"):

                self.client.get_rooms()

                messagebox.showinfo(
                    "Room Created",
                    message.get(
                        "message",
                        "Room created."
                    )
                )

            else:

                messagebox.showerror(
                    "Create Room",
                    message.get(
                        "message",
                        "Unable to create room."
                    )
                )

        # ----------------------------------------------------
        # JOIN ROOM
        # ----------------------------------------------------

        elif message_type == "join_room_response":

            if message.get("success"):

                self.current_room = message.get(
                    "room",
                    self.current_room
                )

                self.room_label.config(
                    text=f"Room: #{self.current_room}"
                )

                self.clear_chat()

                history = message.get(
                    "history",
                    []
                )

                for item in history:

                    self.display_message(
                        item.get(
                            "username",
                            "Unknown"
                        ),
                        item.get(
                            "message",
                            ""
                        ),
                        item.get(
                            "created_at",
                            ""
                        )
                    )

                self.display_system_message(
                    f"Joined #{self.current_room}"
                )

            else:

                messagebox.showerror(
                    "Join Room",
                    message.get(
                        "message",
                        "Unable to join room."
                    )
                )

        # ----------------------------------------------------
        # CHAT
        # ----------------------------------------------------

        elif message_type == "chat":

            self.display_message(
                message.get(
                    "username",
                    "Unknown"
                ),
                message.get(
                    "message",
                    ""
                ),
                message.get(
                    "timestamp",
                    ""
                )
            )

            # Notify when application isn't focused.
            if not self.window_is_focused():

                self.show_background_notification(
                    message.get(
                        "username",
                        "New message"
                    ),
                    message.get(
                        "message",
                        ""
                    )
                )

        # ----------------------------------------------------
        # SYSTEM
        # ----------------------------------------------------

        elif message_type == "system":

            self.display_system_message(
                message.get(
                    "message",
                    ""
                )
            )

        # ----------------------------------------------------
        # ERROR
        # ----------------------------------------------------

        elif message_type == "error":

            messagebox.showerror(
                "Chat Error",
                message.get(
                    "message",
                    "An unknown error occurred."
                )
            )

    # ========================================================
    # AUTH RESPONSE FALLBACK
    # ========================================================

    def _wait_for_auth_response(
        self,
        response_type
    ):
        """
        Kept for registration flow compatibility.

        Server callbacks are handled centrally through
        process_server_message().
        """

        return

    # ========================================================
    # CONNECTION CALLBACK
    # ========================================================

    def handle_connection(
        self,
        connected,
        message
    ):

        self.root.after(
            0,
            lambda: self.process_connection(
                connected,
                message
            )
        )

    def process_connection(
        self,
        connected,
        message
    ):

        if self.status_label:

            self.status_label.config(
                text=(
                    "● Connected"
                    if connected
                    else "● Disconnected"
                ),
                fg=(
                    "#22c55e"
                    if connected
                    else "#ef4444"
                )
            )

    # ========================================================
    # CHAT SCREEN
    # ========================================================

    def show_chat_screen(self):

        if self.login_frame:

            self.login_frame.destroy()

            self.login_frame = None

        if self.chat_frame:

            self.chat_frame.destroy()

        self.root.title(
            f"{APP_TITLE} - {self.username}"
        )

        self.chat_frame = tk.Frame(
            self.root,
            bg="#0f172a"
        )

        self.chat_frame.pack(
            fill="both",
            expand=True
        )

        # ====================================================
        # HEADER
        # ====================================================

        header = tk.Frame(
            self.chat_frame,
            bg="#1e293b",
            height=65
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )

        tk.Label(
            header,
            text="OIBSIP Chat",
            font=("Segoe UI", 18, "bold"),
            bg="#1e293b",
            fg="white"
        ).pack(
            side="left",
            padx=20
        )

        self.status_label = tk.Label(
            header,
            text="● Connected",
            font=("Segoe UI", 10, "bold"),
            bg="#1e293b",
            fg="#22c55e"
        )

        self.status_label.pack(
            side="left"
        )

        tk.Label(
            header,
            text=f"Logged in as: {self.username}",
            font=("Segoe UI", 10),
            bg="#1e293b",
            fg="#94a3b8"
        ).pack(
            side="right",
            padx=20
        )

        # ====================================================
        # BODY
        # ====================================================

        body = tk.Frame(
            self.chat_frame,
            bg="#0f172a"
        )

        body.pack(
            fill="both",
            expand=True
        )

        # ====================================================
        # SIDEBAR
        # ====================================================

        sidebar = tk.Frame(
            body,
            width=230,
            bg="#111827"
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(
            False
        )

        tk.Label(
            sidebar,
            text="CHAT ROOMS",
            font=("Segoe UI", 10, "bold"),
            bg="#111827",
            fg="#94a3b8"
        ).pack(
            anchor="w",
            padx=15,
            pady=(20, 10)
        )

        self.room_listbox = tk.Listbox(
            sidebar,
            bg="#1f2937",
            fg="white",
            selectbackground="#2563eb",
            selectforeground="white",
            activestyle="none",
            borderwidth=0,
            highlightthickness=0,
            font=("Segoe UI", 10)
        )

        self.room_listbox.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        self.room_listbox.bind(
            "<Double-Button-1>",
            self.join_selected_room
        )

        create_room_button = tk.Button(
            sidebar,
            text="+ Create Room",
            command=self.create_new_room,
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            pady=9
        )

        create_room_button.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        refresh_button = tk.Button(
            sidebar,
            text="↻ Refresh Rooms",
            command=self.client.get_rooms,
            font=("Segoe UI", 10),
            bg="#374151",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            pady=8
        )

        refresh_button.pack(
            fill="x",
            padx=10,
            pady=(0, 15)
        )

        # ====================================================
        # CHAT AREA
        # ====================================================

        chat_area = tk.Frame(
            body,
            bg="#0f172a"
        )

        chat_area.pack(
            side="left",
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.room_label = tk.Label(
            chat_area,
            text="Room: #General",
            font=("Segoe UI", 15, "bold"),
            bg="#0f172a",
            fg="white"
        )

        self.room_label.pack(
            anchor="w",
            pady=(0, 10)
        )

        # ----------------------------------------------------
        # CHAT DISPLAY
        # ----------------------------------------------------

        display_frame = tk.Frame(
            chat_area,
            bg="#1e293b"
        )

        display_frame.pack(
            fill="both",
            expand=True
        )

        self.chat_display = tk.Text(
            display_frame,
            bg="#1e293b",
            fg="#e2e8f0",
            insertbackground="white",
            font=("Consolas", 10),
            wrap="word",
            state="disabled",
            borderwidth=0,
            padx=15,
            pady=15
        )

        self.chat_display.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            display_frame,
            orient="vertical",
            command=self.chat_display.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.chat_display.config(
            yscrollcommand=scrollbar.set
        )

        # ----------------------------------------------------
        # MESSAGE INPUT
        # ----------------------------------------------------

        input_frame = tk.Frame(
            chat_area,
            bg="#0f172a"
        )

        input_frame.pack(
            fill="x",
            pady=(12, 0)
        )

        self.message_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 11),
            bg="#334155",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        self.message_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=10
        )

        self.message_entry.bind(
            "<Return>",
            lambda event: self.send_message()
        )

        send_button = tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=25,
            pady=9
        )

        send_button.pack(
            side="right",
            padx=(8, 0)
        )

        # ----------------------------------------------------
        # EMOJI HELP
        # ----------------------------------------------------

        emoji_help = tk.Label(
            chat_area,
            text=(
                "Emoji shortcuts: "
                ":smile:  :heart:  :laugh:  :thumbsup:  "
                ":fire:  :rocket:  :python:"
            ),
            font=("Segoe UI", 8),
            bg="#0f172a",
            fg="#64748b"
        )

        emoji_help.pack(
            anchor="w",
            pady=(6, 0)
        )

        # ----------------------------------------------------
        # INITIAL DATA
        # ----------------------------------------------------

        self.client.get_rooms()

        self.client.join_room(
            "General"
        )

        self.message_entry.focus_set()

    # ========================================================
    # ROOM LIST
    # ========================================================

    def update_room_list(self):

        if not self.room_listbox:
            return

        self.room_listbox.delete(
            0,
            tk.END
        )

        for room in self.rooms:

            self.room_listbox.insert(
                tk.END,
                room.get(
                    "name",
                    ""
                )
            )

        for index, room in enumerate(
            self.rooms
        ):

            if room.get(
                "name"
            ) == self.current_room:

                self.room_listbox.selection_set(
                    index
                )

                self.room_listbox.see(
                    index
                )

                break

    # ========================================================
    # CREATE ROOM
    # ========================================================

    def create_new_room(self):

        room_name = simpledialog.askstring(
            "Create Room",
            "Enter a new room name:",
            parent=self.root
        )

        if room_name is None:
            return

        room_name = room_name.strip()

        valid, error = validate_room_name(
            room_name
        )

        if not valid:

            messagebox.showerror(
                "Invalid Room",
                error
            )

            return

        self.client.create_room(
            room_name
        )

    # ========================================================
    # JOIN SELECTED ROOM
    # ========================================================

    def join_selected_room(
        self,
        event=None
    ):

        selection = self.room_listbox.curselection()

        if not selection:
            return

        room_name = self.room_listbox.get(
            selection[0]
        )

        if room_name == self.current_room:
            return

        self.client.join_room(
            room_name
        )

    # ========================================================
    # SEND MESSAGE
    # ========================================================

    def send_message(self):

        if not self.logged_in:
            return

        message = self.message_entry.get().strip()

        if not message:
            return

        # Convert emoji shortcodes before sending.
        message = convert_shortcodes(
            message
        )

        success = self.client.send_message(
            message
        )

        if success:

            self.message_entry.delete(
                0,
                tk.END
            )

    # ========================================================
    # DISPLAY CHAT MESSAGE
    # ========================================================

    def display_message(
        self,
        username,
        message,
        timestamp
    ):

        formatted = format_chat_message(
            username,
            message,
            timestamp
        )

        self.chat_display.config(
            state="normal"
        )

        self.chat_display.insert(
            tk.END,
            formatted + "\n"
        )

        self.chat_display.config(
            state="disabled"
        )

        self.chat_display.see(
            tk.END
        )

    # ========================================================
    # DISPLAY SYSTEM MESSAGE
    # ========================================================

    def display_system_message(
        self,
        message
    ):

        self.chat_display.config(
            state="normal"
        )

        self.chat_display.insert(
            tk.END,
            f"--- {message} ---\n"
        )

        self.chat_display.config(
            state="disabled"
        )

        self.chat_display.see(
            tk.END
        )

    # ========================================================
    # CLEAR CHAT
    # ========================================================

    def clear_chat(self):

        if not self.chat_display:
            return

        self.chat_display.config(
            state="normal"
        )

        self.chat_display.delete(
            "1.0",
            tk.END
        )

        self.chat_display.config(
            state="disabled"
        )

    # ========================================================
    # WINDOW FOCUS
    # ========================================================

    def window_is_focused(self):

        try:

            return self.root.focus_displayof() is not None

        except tk.TclError:

            return False

    # ========================================================
    # BACKGROUND NOTIFICATION
    # ========================================================

    def show_background_notification(
        self,
        username,
        message
    ):

        # In-app desktop-style notification.
        self.root.bell()

        self.root.title(
            f"🔔 New message from {username}"
        )

        # Restore normal title after 3 seconds.
        self.root.after(
            3000,
            lambda: self.root.title(
                self.original_title
                + f" - {self.username}"
            )
        )

    # ========================================================
    # CLOSE APPLICATION
    # ========================================================

    def close_application(self):

        if self.client:

            self.client.disconnect()

        self.root.destroy()


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

def main():

    root = tk.Tk()

    application = ChatApplication(
        root
    )

    root.mainloop()


if __name__ == "__main__":
    main()