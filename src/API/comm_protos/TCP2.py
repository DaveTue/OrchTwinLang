import socket
import threading

class TCPServer:
    def __init__(self, ports):
        """
        Initialize the server with multiple ports.
        :param ports: List of ports to listen on.
        """
        self.ports = ports
        self.sockets = {}
        self.clients = {}
        self.running = True

    def start(self):
        """
        Start the server to listen on all specified ports.
        """
        for port in self.ports:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(("0.0.0.0", port))
            server_socket.listen(5)
            self.sockets[port] = server_socket
            threading.Thread(target=self._accept_clients, args=(server_socket, port), daemon=True).start()
            print(f"Server listening on port {port}.")

    def _accept_clients(self, server_socket, port):
        """
        Accept clients and handle communication.
        :param server_socket: The server socket.
        :param port: The port associated with the socket.
        """
        while self.running:
            client_socket, client_address = server_socket.accept()
            print(f"Client {client_address} connected on port {port}.")
            self.clients[client_socket] = port
            threading.Thread(target=self._handle_client, args=(client_socket, port), daemon=True).start()

    def _handle_client(self, client_socket, port):
        """
        Handle communication with a single client.
        :param client_socket: The client socket.
        :param port: The port on which the client connected.
        """
        try:
            while self.running:
                message = client_socket.recv(1024).decode()
                if message:
                    print(f"Message received on port {port} from client: {message}")
                    self._broadcast(message, port, client_socket)
        except Exception as e:
            print(f"Error handling client on port {port}: {e}")
        finally:
            client_socket.close()
            del self.clients[client_socket]

    def _broadcast(self, message, port, sender_socket):
        """
        Broadcast a message to all clients except the sender.
        :param message: The message to broadcast.
        :param port: The port on which the message was received.
        :param sender_socket: The socket of the client that sent the message.
        """
        for client_socket, client_port in self.clients.items():
            if client_port == port and client_socket != sender_socket:
                try:
                    client_socket.send(message.encode())
                except Exception as e:
                    print(f"Error broadcasting to client on port {port}: {e}")

    def stop(self):
        """
        Stop the server and close all sockets.
        """
        self.running = False
        for server_socket in self.sockets.values():
            server_socket.close()
        print("Server stopped.")

class TCPClient:
    def __init__(self, server_ip, send_ports, receive_ports):
        """
        Initialize the client with multiple sending ports and multiple receiving ports.
        :param server_ip: IP address of the server.
        :param send_ports: List of ports used for sending messages.
        :param receive_ports: List of ports used for receiving messages.
        """
        self.server_ip = server_ip
        self.send_ports = send_ports
        self.receive_ports = receive_ports

        self.send_sockets = {}
        self.receive_sockets = {}

        self.message_sent = {port: "" for port in send_ports}
        self.sent_history = {port: [] for port in send_ports}
        self.message_received = {port: "" for port in receive_ports}
        self.received_history = {port: [] for port in receive_ports}

    def connect(self):
        """
        Connect to the server on all sending ports and all receiving ports.
        """
        try:
            for port in self.send_ports:
                send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                send_socket.connect((self.server_ip, port))
                self.send_sockets[port] = send_socket
                print(f"Connected to server on send port {port}.")

            for port in self.receive_ports:
                recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                recv_socket.connect((self.server_ip, port))
                self.receive_sockets[port] = recv_socket
                threading.Thread(target=self._receive_messages, args=(recv_socket, port), daemon=True).start()
                print(f"Connected to server on receive port {port}.")
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def send_message(self, port, message):
        """
        Send a message to the server via a specific sending port.
        :param port: The port to use for sending the message.
        :param message: The message to send.
        """
        # print(message)
        # print(type(message))
        try:
            if port in self.send_sockets:
                self.send_sockets[port].send(message.encode())
                self.message_sent[port] = message
                self.sent_history[port].append(message)
                print(f"Message sent on port {port}: {message}")
            else:
                print(f"Port {port} is not a valid sending port.")
        except Exception as e:
            print(f"Error sending message on port {port}: {e}")

    def _receive_messages(self, recv_socket, port):
        """
        Receive messages from the server on a specific port.
        :param recv_socket: The socket connected to the receiving port.
        :param port: The receiving port.
        """
        try:
            while True:
                message = recv_socket.recv(1024).decode()
                if message:
                    self.message_received[port] = message
                    self.received_history[port].append(message)
                    print(f"Message received on port {port}: {message}")
        except Exception as e:
            print(f"Error receiving message on port {port}: {e}")
        finally:
            recv_socket.close()

    def close(self):
        """
        Close all connections.
        """
        try:
            for port, send_socket in self.send_sockets.items():
                send_socket.close()
            for port, recv_socket in self.receive_sockets.items():
                recv_socket.close()
            print("All connections closed.")
        except Exception as e:
            print(f"Error closing connections: {e}")


