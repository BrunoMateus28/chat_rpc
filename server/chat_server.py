import xmlrpc.server
import threading
from datetime import datetime
import xmlrpc.client

class ChatServer:
    def __init__(self, binder_host="localhost", binder_port=5000):
        self.users = set()
        self.rooms = {}
        self.binder = xmlrpc.client.ServerProxy(f"http://{binder_host}:{binder_port}")
        self.server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 9000),allow_none=True)
        
        # Registro de métodos no Binder
        self.register_procedures()

        print("Servidor de chat iniciado em localhost:9000")

    def register_user(self, username):
        """
        Registra um novo usuário. Se o username já estiver em uso, lança uma exceção.
        """
        if username in self.users:
            raise Exception("O nome de usuário já está em uso. Escolha outro.")
        else:
            self.users.add(username)  # Adiciona o usuário ao conjunto
            return "Usuário registrado com sucesso."

    def unregister_user(self, username):
        """
        Remove um usuário do sistema. Retorna mensagem de sucesso ou erro.
        """
        if username in self.users:
            self.users.remove(username)  # Remove o usuário do conjunto
            for room in self.rooms.values():
                if username in room["users"]:
                    room["users"].remove(username)
            return "Usuário desconectado com sucesso."
        else:
            return "Usuário não encontrado. Nenhuma ação realizada."


    def register_procedures(self):
        """Registra os métodos do servidor no Binder."""
        procedures = ["create_room", "join_room", "send_message", 
                      "receive_messages", "list_rooms", "list_users",
                      "register_user", "unregister_user"]
        for proc in procedures:
            self.binder.register_procedure(proc, "localhost", 9000)
            self.server.register_function(getattr(self, proc), proc)

    def create_room(self, room_name):
        """
        Cria uma nova sala de chat com o nome especificado.
        Retorna uma mensagem de sucesso ou erro caso a sala já exista.
        """
        if room_name in self.rooms:
            return "Sala já existe."
        self.rooms[room_name] = {"users": [], "messages": []}
        return f"Sala '{room_name}' criada."                   

    def join_room(self, username, room_name):
        if username in self.users:
            if room_name in self.rooms:
                for room in self.rooms.values():
                    if username in room["users"]:
                        room["users"].remove(username)
                self.rooms[room_name]["users"].append(username)
                return {
                    "users": self.rooms[room_name]["users"],
                    "messages": self.rooms[room_name]["messages"][-50:]
                }
            else:
                return "Sala não existe."
        else:
            return "Usuário não registrado."

    def send_message(self, username, room_name, message, recipient=None):
        if room_name not in self.rooms:
            return "Sala não existe."
        if username not in self.rooms[room_name]["users"]:
            return "Usuário não está na sala."
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg_type = "unicast" if recipient else "broadcast"
        message_data = {
            "type": msg_type,
            "origin": username,
            "destination": recipient,
            "content": message,
            "timestamp": timestamp
        }
        self.rooms[room_name]["messages"].append(message_data)
        return "Mensagem enviada."


    def receive_messages(self, username, room_name):
        if room_name not in self.rooms:
            return []
        return [
            msg for msg in self.rooms[room_name]["messages"]
            if msg["type"] == "broadcast" or msg["destination"] == username
        ]

    def list_rooms(self):
        return list(self.rooms.keys())
    
    def list_users(self, room_name):
        """
        Lista os usuários de uma sala específica. Retorna uma mensagem apropriada
        se a sala não existir ou se nenhuma sala foi criada.
        """
        if not self.rooms:  # Verifica se o dicionário de salas está vazio
            return "Nenhuma sala criada ainda."
        
        if room_name in self.rooms:
            return self.rooms[room_name]["users"]  # Retorna a lista de usuários da sala
        
        return "Sala não encontrada."


    def run(self):
        self.server.serve_forever()

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.run()
