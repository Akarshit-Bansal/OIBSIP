import json
import socket
import threading
from datetime import datetime

from database import (
    authenticate_user,
    get_message_history,
    get_rooms,
    register_user,
    save_message,
)


HOST = "127.0.0.1"
PORT = 5050

BUFFER_SIZE = 4096

server_running = True

clients = {}
clients_lock = threading.Lock()


# ============================================================
# MESSAGE HELPERS
# ============================================================

def send_json(client_socket, data):
    """
    Send a JSON message followed by a newline.
    """

    payload = json.dumps(
        data,
        ensure_ascii=False,
    ) + "\n"

    client_socket.sendall(
        payload.encode("utf-8")
    )


def receive_json(file_object):
    """
    Receive one newline-delimited JSON message.
    """

    line = file_object.readline()

    if not line:
        return None

    try:
        return json.loads(
            line.decode("utf-8")
        )

    except json.JSONDecodeError:
        return None


def create_response(
    response_type,
    success=True,
    message="",
    **extra,
):
    """
    Create a consistent server response.
    """

    response = {
        "type": response_type,
        "success": success,
        "message": message,
    }

    response.update(extra)

    return response


# ============================================================
# CLIENT MANAGEMENT
# ============================================================

def add_client(
    client_socket,
    username,
    room,
):
    """
    Add a connected client to the active client list.
    """

    with clients_lock:

        clients[client_socket] = {
            "username": username,
            "room": room,
        }


def remove_client(client_socket):
    """
    Remove a disconnected client.
    """

    with clients_lock:

        return clients.pop(
            client_socket,
            None,
        )


def broadcast_to_room(
    room,
    data,
    exclude_socket=None,
):
    """
    Send a message to all clients currently
    connected to the specified room.
    """

    disconnected = []

    with clients_lock:

        active_clients = list(
            clients.items()
        )

    for client_socket, client_data in active_clients:

        if client_socket == exclude_socket:
            continue

        if client_data["room"] != room:
            continue

        try:

            send_json(
                client_socket,
                data,
            )

        except (ConnectionError, OSError):

            disconnected.append(
                client_socket
            )

    for client_socket in disconnected:

        remove_client(
            client_socket
        )

        try:
            client_socket.close()
        except OSError:
            pass


def broadcast_system_message(
    room,
    message,
):
    """
    Send a system notification to everyone in a room.
    """

    broadcast_to_room(
        room,
        {
            "type": "system",
            "message": message,
            "timestamp": current_timestamp(),
        },
    )


# ============================================================
# TIMESTAMP
# ============================================================

def current_timestamp():
    """
    Return a readable local timestamp.
    """

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# ============================================================
# AUTHENTICATION
# ============================================================

def handle_register(
    client_socket,
    request,
):
    """
    Register a new user.
    """

    username = request.get(
        "username",
        "",
    )

    password = request.get(
        "password",
        "",
    )

    success, message = register_user(
        username,
        password,
    )

    send_json(
        client_socket,
        create_response(
            "register_response",
            success,
            message,
        ),
    )


def handle_login(
    client_socket,
    request,
):
    """
    Authenticate a user.
    """

    username = request.get(
        "username",
        "",
    )

    password = request.get(
        "password",
        "",
    )

    authenticated = authenticate_user(
        username,
        password,
    )

    if authenticated:

        send_json(
            client_socket,
            create_response(
                "login_response",
                True,
                "Login successful.",
                username=username,
            ),
        )

    else:

        send_json(
            client_socket,
            create_response(
                "login_response",
                False,
                "Invalid username or password.",
            ),
        )


# ============================================================
# ROOM MANAGEMENT
# ============================================================

def handle_get_rooms(
    client_socket,
):
    """
    Return available chat rooms.
    """

    rooms = get_rooms()

    send_json(
        client_socket,
        {
            "type": "rooms_response",
            "success": True,
            "rooms": rooms,
        },
    )


def handle_create_room(
    client_socket,
    request,
):
    """
    Create a new chat room.
    """

    from database import create_room

    room_name = request.get(
        "room",
        "",
    )

    success, message = create_room(
        room_name
    )

    send_json(
        client_socket,
        create_response(
            "create_room_response",
            success,
            message,
        ),
    )


# ============================================================
# ROOM JOIN
# ============================================================

def handle_join_room(
    client_socket,
    username,
    request,
):
    """
    Move a client into another room and send
    the room's message history.
    """

    room = request.get(
        "room",
        "",
    ).strip()

    if not room:

        send_json(
            client_socket,
            create_response(
                "join_room_response",
                False,
                "Room name is required.",
            ),
        )

        return None

    from database import get_room_by_name

    room_data = get_room_by_name(
        room
    )

    if room_data is None:

        send_json(
            client_socket,
            create_response(
                "join_room_response",
                False,
                "Room does not exist.",
            ),
        )

        return None

    with clients_lock:

        if client_socket in clients:

            clients[
                client_socket
            ]["room"] = room

    history = get_message_history(
        room,
        limit=100,
    )

    send_json(
        client_socket,
        {
            "type": "join_room_response",
            "success": True,
            "message": f"Joined room: {room}",
            "room": room,
            "history": history,
        },
    )

    broadcast_system_message(
        room,
        f"{username} joined the room.",
    )

    return room


# ============================================================
# CHAT MESSAGE
# ============================================================

def handle_chat_message(
    client_socket,
    username,
    request,
):
    """
    Save and broadcast a chat message.
    """

    message = request.get(
        "message",
        "",
    ).strip()

    if not message:

        send_json(
            client_socket,
            create_response(
                "error",
                False,
                "Message cannot be empty.",
            ),
        )

        return

    with clients_lock:

        client_data = clients.get(
            client_socket
        )

    if client_data is None:

        return

    room = client_data["room"]

    timestamp = current_timestamp()

    saved = save_message(
        room,
        username,
        message,
    )

    if not saved:

        send_json(
            client_socket,
            create_response(
                "error",
                False,
                "Unable to save message.",
            ),
        )

        return

    chat_data = {
        "type": "chat",
        "username": username,
        "message": message,
        "room": room,
        "timestamp": timestamp,
    }

    broadcast_to_room(
        room,
        chat_data,
    )


# ============================================================
# CLIENT HANDLER
# ============================================================

def handle_client(
    client_socket,
    address,
):
    """
    Handle one connected client.
    """

    username = None
    current_room = "General"

    print(
        f"[CONNECT] Client connected: {address}"
    )

    try:

        client_file = client_socket.makefile(
            "rb"
        )

        while server_running:

            request = receive_json(
                client_file
            )

            if request is None:

                break

            request_type = request.get(
                "type"
            )

            # ------------------------------------------------
            # REGISTER
            # ------------------------------------------------

            if request_type == "register":

                handle_register(
                    client_socket,
                    request,
                )

            # ------------------------------------------------
            # LOGIN
            # ------------------------------------------------

            elif request_type == "login":

                handle_login(
                    client_socket,
                    request,
                )

            # ------------------------------------------------
            # GET ROOMS
            # ------------------------------------------------

            elif request_type == "get_rooms":

                handle_get_rooms(
                    client_socket
                )

            # ------------------------------------------------
            # CREATE ROOM
            # ------------------------------------------------

            elif request_type == "create_room":

                handle_create_room(
                    client_socket,
                    request,
                )

            # ------------------------------------------------
            # JOIN ROOM
            # ------------------------------------------------

            elif request_type == "join_room":

                if not username:

                    send_json(
                        client_socket,
                        create_response(
                            "error",
                            False,
                            "Please login first.",
                        ),
                    )

                    continue

                new_room = handle_join_room(
                    client_socket,
                    username,
                    request,
                )

                if new_room:

                    current_room = new_room

            # ------------------------------------------------
            # CHAT
            # ------------------------------------------------

            elif request_type == "chat":

                if not username:

                    send_json(
                        client_socket,
                        create_response(
                            "error",
                            False,
                            "Please login first.",
                        ),
                    )

                    continue

                handle_chat_message(
                    client_socket,
                    username,
                    request,
                )

            # ------------------------------------------------
            # LOGIN SESSION
            # ------------------------------------------------

            elif request_type == "set_username":

                username = request.get(
                    "username"
                )

                add_client(
                    client_socket,
                    username,
                    current_room,
                )

                send_json(
                    client_socket,
                    create_response(
                        "session",
                        True,
                        "Session started.",
                        username=username,
                        room=current_room,
                    ),
                )

            # ------------------------------------------------
            # PING
            # ------------------------------------------------

            elif request_type == "ping":

                send_json(
                    client_socket,
                    {
                        "type": "pong",
                        "timestamp": current_timestamp(),
                    },
                )

            # ------------------------------------------------
            # UNKNOWN REQUEST
            # ------------------------------------------------

            else:

                send_json(
                    client_socket,
                    create_response(
                        "error",
                        False,
                        "Unknown request type.",
                    ),
                )

    except (
        ConnectionResetError,
        BrokenPipeError,
        ConnectionAbortedError,
        OSError,
    ):

        pass

    finally:

        client_data = remove_client(
            client_socket
        )

        if client_data:

            username = client_data[
                "username"
            ]

            room = client_data[
                "room"
            ]

            broadcast_system_message(
                room,
                f"{username} disconnected.",
            )

        try:
            client_file.close()
        except Exception:
            pass

        try:
            client_socket.close()
        except OSError:
            pass

        print(
            f"[DISCONNECT] Client disconnected: {address}"
        )


# ============================================================
# SERVER
# ============================================================

def start_server():
    """
    Start the TCP chat server.
    """

    global server_running

    server_running = True

    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )

    server_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1,
    )

    server_socket.bind(
        (
            HOST,
            PORT,
        )
    )

    server_socket.listen(
        10
    )

    print("=" * 60)
    print("OIBSIP CHAT SERVER")
    print("=" * 60)
    print(
        f"Server listening on {HOST}:{PORT}"
    )
    print(
        "Waiting for clients..."
    )
    print(
        "Press CTRL+C to stop."
    )
    print("=" * 60)

    try:

        while server_running:

            client_socket, address = (
                server_socket.accept()
            )

            client_thread = threading.Thread(
                target=handle_client,
                args=(
                    client_socket,
                    address,
                ),
                daemon=True,
            )

            client_thread.start()

    except KeyboardInterrupt:

        print(
            "\n[SERVER] Shutting down..."
        )

    finally:

        server_running = False

        with clients_lock:

            active_clients = list(
                clients.keys()
            )

            clients.clear()

        for client_socket in active_clients:

            try:
                client_socket.close()
            except OSError:
                pass

        server_socket.close()

        print(
            "[SERVER] Server stopped."
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    start_server()