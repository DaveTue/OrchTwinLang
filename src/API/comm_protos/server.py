from TCP import TCPServer
from TCP import TCPClient

# ports = list(map(int, input("Enter the ports (comma-separated): ").split(',')))
# print(ports)
ports =[55001, 55000, 50000]
server = TCPServer(ports)
server.start_server()

# Keep the server running
# input("Press Enter to stop the server...\n")


server_ip = "127.0.0.1"
send_port = 55000
receive_ports = [55001,50000]

client = TCPClient(server_ip, send_port, receive_ports)
client.connect()

while True:
    message = input("Enter a message to send (or 'exit' to quit): ")
    if message.lower() == 'exit':
        break
    client.send_message(message)

client.close()

# port_pairs = [(55000,55001)]

# server = TCPServer(port_pairs)
# server.start_server()

# # # Keep the server running
# input("Press Enter to stop the server...\n")


# if __name__ == "__main__":
#     num_channels = 2
#     base_port = 55000
#     server = TCPServer(num_channels, base_port)
#     server.run()

#     # Keep the server running
#     input("Press Enter to stop the server...\n")
