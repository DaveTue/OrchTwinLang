import socket
import threading

class TCPServer:
    def __init__(self, ports,printFlag = False):
        """
        Initialize the server with specified ports.
        :param ports: List of ports to handle.
        """
        self.ports = ports
        self.clients = {port: [] for port in ports}  # Dictionary to store clients per port
        self.lock = threading.Lock()
        self.printFlag = printFlag

    def start_server(self):
        """
        Start the server for all specified ports.
        """
        for port in self.ports:
            threading.Thread(target=self._listen, args=(port,), daemon=True).start()
            print(f"Server is running on port {port}.")

    def _listen(self, port):
        """
        Listen for incoming client connections on the specified port.
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("0.0.0.0", port))
        server_socket.listen(5)
        print(f"Listening on port {port}...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address} on port {port}")
            with self.lock:
                self.clients[port].append(client_socket)
            threading.Thread(target=self._handle_client, args=(client_socket, port), daemon=True).start()

    def _handle_client(self, client_socket, port):
        """
        Handle communication for a single client connected to a specific port.
        """
        try:
            while True:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                if self.printFlag == True:
                    print(f"Received on port {port}: {message}")
                self._route_message(client_socket, port, message)
        except ConnectionResetError:
            print(f"Client disconnected from port {port}.")
        finally:
            with self.lock:
                self.clients[port].remove(client_socket)
            client_socket.close()

    def _route_message(self, sender_socket, port, message):
        """
        Route the message from the sender to all other clients connected to the same port.
        """
        with self.lock:
            for client_socket in self.clients[port]:
                if client_socket != sender_socket:
                    try:
                        client_socket.send(message.encode())
                        if self.printFlag == True:
                            print(f"Message routed on port {port}.")
                    except Exception as e:
                        print(f"Error routing message on port {port}: {e}")




class TCPClient:
    def __init__(self, server_ip, send_port, receive_ports, printFlag = False):
        """
        Initialize the client with a sending port and multiple receiving ports.
        :param server_ip: IP address of the server.
        :param send_port: Port used for sending messages.
        :param receive_ports: List of ports used for receiving messages.
        """
        self.server_ip = server_ip
        self.send_port = send_port
        self.receive_ports = receive_ports

        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive_sockets = {}

        self.printFlag = printFlag
        
        self.message_sent = ""
        self.sent_history = []
        self.message_received = {}
        self.received_history = {port: [] for port in receive_ports}

    def connect(self):
        """
        Connect to the server on the sending port and all receiving ports.
        """
        try:
            self.send_socket.connect((self.server_ip, self.send_port))
            print(f"Connected to server on send port {self.send_port}.")

            for port in self.receive_ports:
                recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                recv_socket.connect((self.server_ip, port))
                self.receive_sockets[port] = recv_socket
                self.message_received[port] = ""
                threading.Thread(target=self._receive_messages, args=(recv_socket, port), daemon=True).start()
                print(f"Connected to server on receive port {port}.")
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def send_message(self, message):
        """
        Send a message to the server via the sending port.
        :param message: The message to send.
        """
        # print(message)
        # print(type(message))
        try:
            self.send_socket.send(message.encode())
            self.message_sent = message
            self.sent_history.append(message)
            print(f"Message sent: {message}")
        except Exception as e:
            print(f"Error sending message: {e}")

    def _receive_messages(self, recv_socket, port):
        """
        Receive messages from the server on a specific port.
        :param recv_socket: The socket connected to the receiving port.
        :param port: The receiving port.
        """
        try:
            while True:
                message = recv_socket.recv(1024).decode()
                # print(message)
                if message:
                    self.message_received[port] = message
                    # print(self.message_received[port])
                    self.received_history[port].append(message)
                    if self.printFlag == True:
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
            self.send_socket.close()
            for port, recv_socket in self.receive_sockets.items():
                recv_socket.close()
            print("All connections closed.")
        except Exception as e:
            print(f"Error closing connections: {e}")

