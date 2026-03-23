import threading
from TCP2 import TCPServer
from TCP2 import TCPClient

# if __name__ == "__main__":
# Start the server
server_ports = [5000, 5001, 5002]
server = TCPServer(server_ports)
threading.Thread(target=server.start, daemon=True).start()

# Start client 1
client1 = TCPClient("127.0.0.1", send_ports=[5000], receive_ports=[5001])
threading.Thread(target=client1.connect, daemon=True).start()

# Start client 2
client2 = TCPClient("127.0.0.1", send_ports=[5001], receive_ports=[5000])
threading.Thread(target=client2.connect, daemon=True).start()

# Interactive loop
try:
    while True:
        command = input("Enter 'exit' to stop the server and clients: ").strip().lower()
        if command == 'exit':
            server.stop()
            client1.disconnect()
            client2.disconnect()
            break
except KeyboardInterrupt:
    server.stop()
    client1.disconnect()
    client2.disconnect()


# server_ip = "127.0.0.1"
# send_port = 55000
# receive_ports = [55001,50000]

# client = TCPClient(server_ip, send_port, receive_ports)
# client.connect()

# while True:
#     message = input("Enter a message to send (or 'exit' to quit): ")
#     if message.lower() == 'exit':
#         break
#     client.send_message(message)

# client.close()

