import socket
import subprocess
import os

def launch_game():
    try:
        # Path to the Java bin directory
        java_bin_directory = r'C:\Users\Sravya Duvvuri\PongAttemptJava2\pong-network-java\bin'
        
        # Change to the Java bin directory
        os.chdir(java_bin_directory)
        
        # Launch the Java game using the Test class
        process = subprocess.Popen(['java', '-cp', java_bin_directory, 'Test'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Continuously print the output from the game as it runs
        while True:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                print(output.strip().decode())
        
        print("Game launched successfully.")
        
    except Exception as e:
        print(f"Failed to launch the game: {e}")

def start_client(server_ip, username):
    # Implement your client connection logic here
    try:
        # Create a socket connection to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_ip, 12345))  # Replace 12345 with your server port
            
            # Send the username to the server
            client_socket.sendall(username.encode('utf-8'))
            print("Connected to server successfully.")
            
            # Optionally receive messages from the server here
            # while True:
            #     message = client_socket.recv(1024).decode('utf-8')
            #     print(f"Message from server: {message}")
            
            # Launch the game after connecting
            launch_game()

    except Exception as e:
        print(f"Error in client: {e}")

if __name__ == "__main__":
    # Input server IP and username
    server_ip = input("Enter the server IP address: ")
    username = input("Enter your username: ")

    # Start the client
    start_client(server_ip, username)
