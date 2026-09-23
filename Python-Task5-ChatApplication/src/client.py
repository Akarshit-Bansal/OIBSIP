import json
import socket
import threading


HOST = "127.0.0.1"
PORT = 5050


class ChatClient:

    def __init__(
        self,
        host=HOST,
        port=PORT,
    ):
        self.host = host
        self.port = port

        self.socket = None
        self.receive_thread = None

        self.running = False

        self.username = None
        self.current_room = "General"

        self.message_callback = None
        self.connection_callback = None

        self.send_lock = threading.Lock()

    # ========================================================
    # CONNECTION
    # ========================================================

    def connect(self):

        if self.running:
            return True

        try:

            self.socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM,
            )

            self.socket.connect(
                (
                    self.host,
                    self.port,
                )
            )

            self.running = True

            self.receive_thread = threading.Thread(
                target=self._receive_loop,
                daemon=True,
            )

            self.receive_thread.start()

            self._notify_connection(
                True,
                "Connected to chat server."
            )

            return True

        except OSError as error:

            self.running = False

            self._notify_connection(
                False,
                f"Unable to connect: {error}"
            )

            return False

    # ========================================================
    # DISCONNECT
    # ========================================================

    def disconnect(self):

        self.running = False

        if self.socket:

            try:
                self.socket.shutdown(
                    socket.SHUT_RDWR
                )
            except OSError:
                pass

            try:
                self.socket.close()
            except OSError:
                pass

        self.socket = None

        self._notify_connection(
            False,
            "Disconnected from chat server."
        )

    # ========================================================
    # SEND JSON
    # ========================================================

    def send(self, data):

        if not self.running:
            return False

        try:

            payload = (
                json.dumps(
                    data,
                    ensure_ascii=False,
                )
                + "\n"
            )

            encoded = payload.encode(
                "utf-8"
            )

            with self.send_lock:

                self.socket.sendall(
                    encoded
                )

            return True

        except (
            BrokenPipeError,
            ConnectionResetError,
            ConnectionAbortedError,
            OSError,
        ):

            self.disconnect()

            return False

    # ========================================================
    # REGISTER
    # ========================================================

    def register(
        self,
        username,
        password,
    ):

        return self.send(
            {
                "type": "register",
                "username": username,
                "password": password,
            }
        )

    # ========================================================
    # LOGIN
    # ========================================================

    def login(
        self,
        username,
        password,
    ):

        self.username = username

        return self.send(
            {
                "type": "login",
                "username": username,
                "password": password,
            }
        )

    # ========================================================
    # START SESSION
    # ========================================================

    def start_session(
        self,
        username,
    ):

        self.username = username

        return self.send(
            {
                "type": "set_username",
                "username": username,
            }
        )

    # ========================================================
    # GET ROOMS
    # ========================================================

    def get_rooms(self):

        return self.send(
            {
                "type": "get_rooms"
            }
        )

    # ========================================================
    # CREATE ROOM
    # ========================================================

    def create_room(
        self,
        room_name,
    ):

        return self.send(
            {
                "type": "create_room",
                "room": room_name,
            }
        )

    # ========================================================
    # JOIN ROOM
    # ========================================================

    def join_room(
        self,
        room_name,
    ):

        self.current_room = room_name

        return self.send(
            {
                "type": "join_room",
                "room": room_name,
            }
        )

    # ========================================================
    # SEND CHAT MESSAGE
    # ========================================================

    def send_message(
        self,
        message,
    ):

        return self.send(
            {
                "type": "chat",
                "message": message,
            }
        )

    # ========================================================
    # RECEIVE LOOP
    # ========================================================

    def _receive_loop(self):

        buffer = ""

        try:

            while self.running:

                data = self.socket.recv(
                    4096
                )

                if not data:
                    break

                buffer += data.decode(
                    "utf-8"
                )

                while "\n" in buffer:

                    line, buffer = buffer.split(
                        "\n",
                        1
                    )

                    line = line.strip()

                    if not line:
                        continue

                    try:

                        message = json.loads(
                            line
                        )

                        self._handle_message(
                            message
                        )

                    except json.JSONDecodeError:

                        self._notify_message(
                            {
                                "type": "error",
                                "message": "Invalid server response."
                            }
                        )

        except (
            ConnectionResetError,
            ConnectionAbortedError,
            OSError,
        ):

            pass

        finally:

            was_running = self.running

            self.running = False

            if was_running:

                self._notify_connection(
                    False,
                    "Connection to server lost."
                )

    # ========================================================
    # HANDLE SERVER MESSAGE
    # ========================================================

    def _handle_message(
        self,
        message,
    ):

        message_type = message.get(
            "type"
        )

        if message_type == "login_response":

            if message.get("success"):

                self.username = message.get(
                    "username",
                    self.username
                )

        elif message_type == "join_room_response":

            if message.get("success"):

                self.current_room = message.get(
                    "room",
                    self.current_room
                )

        self._notify_message(
            message
        )

    # ========================================================
    # CALLBACKS
    # ========================================================

    def set_message_callback(
        self,
        callback,
    ):

        self.message_callback = callback

    def set_connection_callback(
        self,
        callback,
    ):

        self.connection_callback = callback

    def _notify_message(
        self,
        message,
    ):

        if self.message_callback:

            try:

                self.message_callback(
                    message
                )

            except Exception as error:

                print(
                    f"[CLIENT CALLBACK ERROR] {error}"
                )

    def _notify_connection(
        self,
        connected,
        message,
    ):

        if self.connection_callback:

            try:

                self.connection_callback(
                    connected,
                    message,
                )

            except Exception as error:

                print(
                    f"[CONNECTION CALLBACK ERROR] {error}"
                )