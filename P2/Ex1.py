from Client0 import Client

PRACTICE = 2
EXERCISE = 1

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

SERVER_IP = "localhost"
SERVER_PORT = 8081

c = Client(SERVER_IP, SERVER_PORT)

c.ping()

print(f"Server's address: ({c.server_ip}:{c.server_port})")