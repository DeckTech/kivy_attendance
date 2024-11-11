import socket
import threading
import json
import time

HEADER = 256
FORMAT = 'utf-8'
PORT = 7000
DISCONNECT_MESSAGE = "DISCONNECT"
listen_stop_event = threading.Event()
active_connections = []
threads = []  # List to track all threads
servers_found = []  # List to store details of discovered servers


def listen_to_all_servers(port):
    """
    Listens for broadcast messages from servers on the specified port.
    Each discovered server IP and port are stored in servers_found.
    """
    def listen():
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.bind(("", port))

            while not listen_stop_event.is_set():
                try:
                    message, addr = s.recvfrom(HEADER)
                    server_info = json.loads(message.decode(FORMAT))
                    if "SERVER" in server_info and "PORT" in server_info:
                        server_address = (server_info["SERVER"], server_info["PORT"])
                        if server_address not in servers_found:
                            servers_found.append(server_address)
                            print(f"Discovered server: {server_address}")
                except Exception as e:
                    if listen_stop_event.is_set():
                        break
                    print(f"Error receiving broadcast: {e}")
        print("Stopped listening for broadcasts.")

    # Start the listener in a separate thread
    listener_thread = threading.Thread(target=listen)
    listener_thread.daemon = True  # Stops with the program
    listener_thread.start()
    threads.append(listener_thread)  # Track the thread
    return listener_thread


def connect(server_ip, server_port):
    """
    Connects to a server at the given IP and port.
    Returns the connection object if successful.
    """
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((server_ip, server_port))
        active_connections.append(conn)
        print(f"Connected to server {server_ip}:{server_port}")

        # Start a thread to listen for server messages
        client_thread = threading.Thread(target=handle_server_messages, args=(conn,))
        client_thread.daemon = True
        client_thread.start()
        threads.append(client_thread)  # Track the thread

        return conn
    except Exception as e:
        print(f"Failed to connect to {server_ip}:{server_port} - {e}")
        return None


def handle_server_messages(conn):
    """
    Handles incoming messages from a connected server.
    """
    try:
        while not listen_stop_event.is_set():
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                print(f"[SERVER MESSAGE] {msg}")
    except Exception as e:
        print(f"Error receiving message from server: {e}")
    finally:
        if conn in active_connections:
            active_connections.remove(conn)
        conn.close()
        print("Connection closed.")


def disconnect(conn):
    """
    Disconnects from the server.
    """
    try:
        conn.send(DISCONNECT_MESSAGE.encode(FORMAT))
        conn.close()
        if conn in active_connections:
            active_connections.remove(conn)
        print(f"Disconnected from server.")
    except Exception as e:
        print(f"Failed to disconnect: {e}")
    finally:
        stop_listening()  # Ensures all threads stop


def stop_listening():
    """
    Stops listening for broadcast messages from servers
    and terminates all active threads.
    """
    listen_stop_event.set()  # Signal all threads to stop

    # Close any active connections
    for conn in active_connections:
        try:
            conn.send(DISCONNECT_MESSAGE.encode(FORMAT))
            conn.close()
        except Exception as e:
            print(f"Failed to disconnect connection: {e}")

    # Wait for all threads to finish
    for thread in threads:
        if thread.is_alive():
            thread.join()
    print("All threads terminated, listener stopped.")


# Example usage:
if __name__ == "__main__":
    pass
