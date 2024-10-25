from flask import Flask
from flask_socketio import SocketIO, emit

class Agent:
    def __init__(self, host="0.0.0.0", port=5001, cors_allowed_origins="*"):
        """Initialize the Flask app and SocketIO"""
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins=cors_allowed_origins)
        self.host = host
        self.port = port
        self.message_handler = None  # Placeholder for user-defined message handler

        # Register event handler for user messages
        self.socketio.on_event('user_message', self._handle_user_message)

    def on_message(self, handler):
        """Set the function that handles user messages"""
        self.message_handler = handler

    def _handle_user_message(self, message):
        """Internal method to handle incoming messages"""
        print(f"Received message: {message}")
        
        # Check if a user-defined message handler is set
        if self.message_handler:
            self.message_handler(message)  # Delegate the message handling to the user-defined function
        else:
            print("No message handler defined!")

    def send_message(self, message):
        """Send a message to the client"""
        emit('bot_response', message)

    def start_typing(self):
        """Emit typing start event to the client"""
        emit('agent_typing')

    def stop_typing(self):
        """Emit typing stop event to the client"""
        emit('agent_stop_typing')

    def run(self, debug=True):
        """Start the SocketIO server with hot-reloading support"""
        # Flask-SocketIO automatically manages threading and reloading when debug=True
        self.socketio.run(self.app, host=self.host, port=self.port, use_reloader=debug)

