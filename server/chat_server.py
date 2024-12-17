from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
from datetime import datetime

from message_manager import MessageManager
from room_manager import RoomManager

class ChatServer:
    def __init__(self, binder_address, server_port):
        self.rooms = {}  # {room_name: {users: [], messages: []}}
        self.usernames = set()
        self.binder = xmlrpc.client.ServerProxy(binder_address)
        self.server_port = server_port
        self.room_manager = RoomManager() 
        self.message_manager = MessageManager()

    def register_on_binder(self):
        self.binder.register_procedure("create_room", "localhost", self.server_port)
        self.binder.register_procedure("join_room", "localhost", self.server_port)
        self.binder.register_procedure("list_rooms", "localhost", self.server_port)
        self.binder.register_procedure("list_users", "localhost", self.server_port)
        self.binder.register_procedure("receive_messages", "localhost", self.server_port)


    def create_room(self, room_name):
        return self.room_manager.create_room(room_name)[1]

    def join_room(self, username, room_name):
        return self.room_manager.join_room(username,room_name)

    def send_message(self, username, room_name, message, recipient=None):
        return self.message_manager.add_message(self, room_name, username, message, recipient)

    # Método para listar todas as salas disponíveis
    def list_rooms(self):
        """
        Retorna a lista de todas as salas disponíveis no servidor.
        """
        return self.room_manager.get_room_names()

    # Método para listar todos os usuários conectados em uma sala específica
    def list_users(self, room_name):
        """
        Retorna a lista de usuários conectados em uma sala específica.

        Args:
            room_name (str): Nome da sala.

        Returns:
            list: Lista de usernames conectados na sala.
        """
        if room_name not in self.room_manager.rooms:
            return f"Erro: A sala '{room_name}' não existe."
        return self.room_manager.list_users(room_name)

    # Método para receber mensagens de uma sala
    def receive_messages(self, username, room_name):
        """
        Retorna as mensagens pendentes para um usuário na sala especificada.

        Args:
            username (str): Nome do usuário.
            room_name (str): Nome da sala.

        Returns:
            list: Lista de mensagens públicas e privadas para o usuário.
        """
        if room_name not in self.room_manager.rooms:
            return f"Erro: A sala '{room_name}' não existe."
        
        if username not in self.room_manager.rooms[room_name]['users']:
            return f"Erro: O usuário '{username}' não está conectado na sala '{room_name}'."
        
        # Retorna mensagens públicas e privadas destinadas ao usuário
        return self.message_manager.get_messages_for_user(
            self.room_manager.rooms[room_name], username
        )


def main():
    binder_address = "http://localhost:5000"
    server_port = 8000
    server = SimpleXMLRPCServer(("localhost", server_port))
    chat_server = ChatServer(binder_address, server_port)

    chat_server.register_on_binder()
    server.register_instance(chat_server)
    print(f"Chat server running on port {server_port}...")
    server.serve_forever()

if __name__ == "__main__":
    main()
