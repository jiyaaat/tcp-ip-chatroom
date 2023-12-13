import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser, QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt

# Define a dictionary to map usernames to colors
user_colors = {}

name = None  # Initialize the name variable to None

# Caesar cipher functions
def encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            offset = ord('a') if char.islower() else ord('A')
            encrypted_text += chr((ord(char) - offset + shift) % 26 + offset)
        else:
            encrypted_text += char
    return encrypted_text

def decrypt(text, shift):
    return encrypt(text, -shift)

def send_message():
    message = input_field.text()
    encrypted_message = encrypt(f"{name}: {message}", shift=3)  # You can change the shift value
    client.send(encrypted_message.encode())
    chat_box.append(f"<font size='4' color='{user_colors.get(name, '#000000')}'>{name}: {message}</font>")  # Add this line
    input_field.clear()


def receive_messages():
    while True:
        try:
            encrypted_message = client.recv(1024).decode()
            decrypted_message = decrypt(encrypted_message, shift=3)  # You should use the same shift value as in send_message

            username, text = decrypted_message.split(": ", 1)

            # Set the color for the user (assign a color if it's a new user)
            if username not in user_colors:
                user_colors[username] = f"#{hash(username) % 0xffffff:06x}"  # Assign a color based on the username

            # Format the message with the user's color
            formatted_message = f"<font size='4' color='{user_colors[username]}'>{decrypted_message}</font>"
            chat_box.append(formatted_message)

        except Exception as e:
            print("Error:", str(e))
            break


# Create a socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 1234
client.connect((host, port))

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Professional Chat Application")
window.setGeometry(100, 100, 600, 400)

central_widget = QWidget()
window.setCentralWidget(central_widget)

layout = QVBoxLayout()

chat_box = QTextBrowser()
chat_box.setOpenExternalLinks(True)
layout.addWidget(chat_box)

status_label = QLabel()
layout.addWidget(status_label)

if name is None:
    name_label = QLabel("Enter your name:")
    layout.addWidget(name_label)

    name_input = QLineEdit()
    name_input.setPlaceholderText("Your Name")
    layout.addWidget(name_input)

    def set_name():
        global name
        name = name_input.text()
        name_label.setText(f"Name: {name}")
        name_input.setDisabled(True)
        name_input.setPlaceholderText("Name set")
        name_button.setDisabled(True)
        send_button.setDisabled(False)
        input_field.setDisabled(False)  # Enable the input field after setting the name
        status_label.setText("Name set successfully.")

    name_button = QPushButton("Set Name")
    name_button.clicked.connect(set_name)
    layout.addWidget(name_button)
else:
    name_label = QLabel(f"Name: {name}")
    layout.addWidget(name_label)

input_field = QLineEdit()
input_field.setPlaceholderText("Type your message here")
layout.addWidget(input_field)

# Connect Enter key press to send_message
input_field.returnPressed.connect(send_message)

def enable_input():
    input_field.setPlaceholderText("Type your message here")
    input_field.setDisabled(False)
    send_button.setDisabled(False)

send_button = QPushButton("Send")
send_button.clicked.connect(send_message)
send_button.setDisabled(True)
layout.addWidget(send_button)

central_widget.setLayout(layout)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

window.show()
sys.exit(app.exec_())

