import socket
import threading
import time
import json

HEADER = 256
PORT = 7000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DICONNECT_MESSAGE = "DISCONNECT"

threads = []
stop_event = threading.Event()

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.\n")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DICONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")

    conn.close()

def broadcast_ip(port, broadcast_ip="255.255.255.255"):
    """Broadcasts the server's IP to the network."""
    # Set up the broadcast socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Enable broadcasting

        message = json.dumps({
            "SERVER": SERVER,
            "PORT": PORT,
        })

        while not stop_event.is_set():  # Stop broadcasting when stop_event is set
            # Send the message to the broadcast address
            s.sendto(message.encode(), (broadcast_ip, port))
            print(f"Broadcasting message: {message} to {broadcast_ip}:{port}")
            time.sleep(2)

def calculate_broadcast(ip):
    """Calculates the broadcast address for the given IP with a standard subnet mask 255.255.255.0."""
    ip_parts = ip.split('.')
    ip_parts[-1] = '255'  # Set the last part of the IP to 255 to get the broadcast address
    broadcast_address = '.'.join(ip_parts)
    return broadcast_address
should_run = True
def nuke_server():
    """Forcefully stops all server activities, including broadcast and active client threads."""
    print("[NUKE] Stopping all server activities...")
    should_run = False

    # Signal threads to stop
    stop_event.set()

    # Close the server socket to stop accepting new connections
    try:
        server.close()
        print("[NUKE] Server socket closed.")
    except Exception as e:
        print(f"[NUKE] Error while closing server socket: {e}")

    # Terminate all threads, including broadcast and client threads
    for thread in threads:
        if thread.is_alive():
            print(f"[NUKE] Terminating thread {thread.name}")
            thread.join(timeout=0.1)  # Give each thread a short time to clean up

    print("[NUKE] All server threads terminated.")

def start_server():

    """Starts the server, broadcasting, and handling client connections."""
    # Start broadcasting in a separate thread
    ip_address_broadcast = calculate_broadcast(SERVER)
    broadcast_thread = threading.Thread(target=broadcast_ip, args=(PORT, ip_address_broadcast))
    broadcast_thread.daemon = False # Daemon thread will exit when the program stops
    broadcast_thread.start()
    threads.append(broadcast_thread)

    server.listen(5)
    print("[SERVER] Listening for incoming connections...")

    while should_run:
        try:
            conn, addr = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
            threads.append(client_thread)
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        except Exception as e:
            if stop_event.is_set():
                break  # Stop loop if nuke_server was triggered
            print(f"Error while accepting connections: {e}")
            break

    print("[SERVER] Server stopped listening for connections.")



if __name__ == "__main__":
    pass
