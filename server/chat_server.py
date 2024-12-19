import xmlrpc.server
import threading
from datetime import datetime
import xmlrpc.client

class ChatServer:
    def __init__(self, binder_host="localhost", binder_port=5000):
        self.users = set()
        self.rooms = {}
        self.binder = xmlrpc.client.ServerProxy(f"http://{binder_host}:{binder_port}")
        self.server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 9000), allow_none=True)
        self.lock = threading.Lock()  # Lock para proteger as requisições
        
        # Registro de métodos no Binder
        self.register_procedures()

        print("Servidor de chat iniciado em localhost:9000")

    def register_user(self, username):
        if username in self.users:
            raise Exception("O nome de usuário já está em uso. Escolha outro.")
        else:
            self.users.add(username)
            return "Usuário registrado com sucesso."

    def unregister_user(self, username):
        if username in self.users:
            self.users.remove(username)
            for room in self.rooms.values():
                if username in room["users"]:
                    room["users"].remove(username)
            return "Usuário desconectado com sucesso."
        else:
            return "Usuário não encontrado."

    def register_procedures(self):
        """Registra os métodos do servidor no Binder."""
        procedures = ["create_room", "join_room", "send_message", 
                    "receive_messages", "receive_new_messages", "list_rooms", "list_users",
                    "register_user", "unregister_user"]
        for proc in procedures:
            self.binder.register_procedure(proc, "localhost", 9000)  # Registra o procedimento no Binder
            self.server.register_function(getattr(self, proc), proc)  # Registra o procedimento no servidor local


    def create_room(self, room_name):
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
                    "messages": self.rooms[room_name]["messages"][-50:]  # Últimas 50 mensagens
                }
            else:
                return "Sala não existe."
        else:
            return "Usuário não registrado."

    def send_message(self, username, room_name, message, recipient=None):
        """Envio de mensagem"""
        if room_name not in self.rooms:
            return "Sala não existe."
        if username not in self.rooms[room_name]["users"]:
            return "Usuário não está na sala."
        if len(self.rooms[room_name]['users'])<=1:
            return "Você está sozinho na sala"
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
        
        # Envia a mensagem para todos os outros usuários na sala, exceto o que enviou
        for user in self.rooms[room_name]["users"]:
            if user != username:  # Não envia a mensagem para o próprio usuário
                print(f"Nova mensagem para {user}: {message}")
        
        return "Mensagem enviada."



    def receive_messages(self, username, room_name):
        if room_name not in self.rooms:
            return []
        return [
            msg for msg in self.rooms[room_name]["messages"]
            if msg["type"] == "broadcast" or msg["destination"] == username
        ]

    from datetime import datetime

    def receive_new_messages(self, username, room_name, last_timestamp):
        """
        Retorna apenas as mensagens enviadas após o último timestamp.
        """
        if room_name not in self.rooms:
            return []

        # Se last_timestamp é uma string, converta para datetime
        if isinstance(last_timestamp, str):
            last_timestamp = datetime.strptime(last_timestamp, "%Y-%m-%d %H:%M:%S")

        # Filtra as mensagens que têm timestamp maior que o last_timestamp
        new_messages = [
            msg for msg in self.rooms[room_name]["messages"]
            if datetime.strptime(msg["timestamp"], "%Y-%m-%d %H:%M:%S") > last_timestamp and (
                msg["type"] == "broadcast" or msg["destination"] == username
            )
        ]
        return new_messages


    def list_rooms(self):
        return list(self.rooms.keys())
    
    def list_users(self, room_name):
        if not self.rooms:
            return "Nenhuma sala criada ainda."
        
        if room_name in self.rooms:
            return self.rooms[room_name]["users"]
        
        return "Sala não encontrada."

    def run(self):
        self.server.serve_forever()

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.run()
