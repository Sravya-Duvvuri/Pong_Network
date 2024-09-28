import socket
import threading
import subprocess
import os

# Define a Player class
class Player:
    def __init__(self, username, connection):
        self.username = username
        self.connection = connection

# Define a GameSession class
class GameSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def broadcast_message(self, message):
        for player in self.players:
            player.connection.send(message.encode())

# Main Server Class
class GameChatServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.connected_players = []  # List to track connected players
        self.game_sessions = []       # List to manage game sessions
        self.server_socket = None

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")

        # Print the server's IP address
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        print(f"Connect to this IP address: {ip_address}")

        # Accept player connections
        while True:
            connection, address = self.server_socket.accept()
            print(f"Player connected: {address}")
            threading.Thread(target=self.handle_player, args=(connection,)).start()

    def handle_player(self, connection):
        username = connection.recv(1024).decode()  # Get username from player
        player = Player(username, connection)
        self.connected_players.append(player)

        # Logic for starting the game (modify as needed)
        if len(self.connected_players) == 2:  # Example: Start game when 2 players are connected
            self.start_game()

        # Handle messages in a loop
        while True:
            try:
                message = connection.recv(1024).decode()
                if message:
                    print(f"Received message from {username}: {message}")
                    # Logic for handling game or chat messages goes here
            except Exception as e:
                print(f"Error: {e}")
                break

        # Cleanup
        connection.close()
        self.connected_players.remove(player)

    def start_game(self):
        try:
            # Path to your Java bin directory
            java_bin_directory = os.path.join(os.getcwd(), 'pong-network-java', 'bin')
            # Command to start the Java game
            subprocess.Popen(['java', '-cp', java_bin_directory, 'Test'], shell=False)
            print("Game started successfully.")
        except Exception as e:
            print(f"Failed to start the game: {e}")

# Running the server
if __name__ == "__main__":
    server = GameChatServer()
    server.start_server()
