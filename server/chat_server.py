import time
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
        try:
            if username in self.users:
                raise Exception("O nome de usuário já está em uso. Escolha outro.")
            else:
                self.users.add(username)
                return "Usuário registrado com sucesso."
        except Exception as e:
            print(f"Erro ao registrar usuário: {e}")
            return f"Erro ao registrar usuário: {e}"

    def unregister_user(self, username):
        try:
            if username in self.users:
                self.users.remove(username)
                for room in self.rooms.values():
                    if username in room["users"]:
                        room["users"].remove(username)
                        # Atualiza o timestamp da última interação
                        room["last_interaction"] = datetime.now()
                return "Usuário desconectado com sucesso."
            else:
                return "Usuário não encontrado."
        except Exception as e:
            print(f"Erro ao tentar desconectar o usuário: {e}")
            return f"Erro ao tentar desconectar o usuário: {e}"


    def register_procedures(self):
        try:
            """Registra os métodos do servidor no Binder."""
            procedures = ["create_room", "join_room", "send_message", 
                        "receive_messages", "receive_new_messages", "list_rooms", "list_users",
                        "register_user", "unregister_user"]
            for proc in procedures:
                self.binder.register_procedure(proc, "localhost", 9000)  # Registra o procedimento no Binder
                self.server.register_function(getattr(self, proc), proc)  # Registra o procedimento no servidor local
        except Exception as e:
            print(f"Erro ao registrar procedimentos: {e}")

    def create_room(self, room_name):
        if room_name in self.rooms:
            return "Sala já existe."
        
        # Adiciona o timestamp da última interação
        self.rooms[room_name] = {
            "users": [],
            "messages": [],
            "last_interaction": datetime.now()  # Adiciona a data de criação
        }
        return f"Sala '{room_name}' criada."

    def check_empty_rooms(self):
        while True:
            try:
                current_time = datetime.now()
                for room_name, room_data in list(self.rooms.items()):
                    if not room_data["users"] and (current_time - room_data["last_interaction"]).total_seconds() > 300:
                        del self.rooms[room_name]  # Remove a sala
                        print(f"Sala '{room_name}' removida por inatividade.")
            except Exception as e:
                print(f"Erro ao verificar salas vazias: {e}")
            time.sleep(60)  # Verifica a cada 60 segundos


    def join_room(self, username, room_name):
        try:
            if username in self.users:
                if room_name in self.rooms:
                    # Atualiza a lista de usuários na sala
                    for room in self.rooms.values():
                        if username in room["users"]:
                            room["users"].remove(username)
                    self.rooms[room_name]["users"].append(username)
                    
                    # Atualiza o timestamp da última interação
                    self.rooms[room_name]["last_interaction"] = datetime.now()
                    
                    return {
                        "users": self.rooms[room_name]["users"],
                        "messages": self.rooms[room_name]["messages"][-50:]  # Últimas 50 mensagens
                    }
                else:
                    return "Sala não existe."
            else:
                return "Usuário não registrado."
        except Exception as e:
            print(f"Erro ao tentar entrar na sala: {e}")
            return f"Erro ao tentar entrar na sala: {e}"


    def send_message(self, username, room_name, message, recipient=None):
        try:
            """Envio de mensagem"""
            if room_name not in self.rooms:
                return "Sala não existe."
            if username not in self.rooms[room_name]["users"]:
                return "Usuário não está na sala."
            if len(self.rooms[room_name]['users']) <= 1:
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
            if(recipient==None or recipient=="" or recipient in self.rooms[room_name]['users']):
                self.rooms[room_name]["messages"].append(message_data)
            else:
                return(f"Usuario {recipient} não encontrado")
            # Envia a mensagem para os outros usuários na sala, dependendo do tipo de mensagem
            if msg_type == "broadcast":
                for user in self.rooms[room_name]["users"]:
                    if user != username:  # Não envia a mensagem para o próprio usuário
                        print(f"Nova mensagem para {user}: {message}")
            elif msg_type == "unicast" and recipient:
                # Envia a mensagem somente para o destinatário
                print(f"Nova mensagem privada para {recipient}: {message}")
            
            return "Mensagem enviada."
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            return f"Erro ao enviar mensagem: {e}"

    def receive_messages(self, username, room_name):
        try:
            if room_name not in self.rooms:
                return []
            return [
                msg for msg in self.rooms[room_name]["messages"]
                if msg["type"] == "broadcast" or msg["destination"] == username
            ]
        except Exception as e:
            print(f"Erro ao receber mensagens: {e}")
            return f"Erro ao receber mensagens: {e}"

    def receive_new_messages(self, username, room_name, last_timestamp):
        try:
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
        except Exception as e:
            print(f"Erro ao receber novas mensagens: {e}")
            return f"Erro ao receber novas mensagens: {e}"

    def list_rooms(self):
        try:
            return list(self.rooms.keys())
        except Exception as e:
            print(f"Erro ao listar salas: {e}")
            return f"Erro ao listar salas: {e}"

    def list_users(self, room_name):
        try:
            if not self.rooms:
                return "Nenhuma sala criada ainda."
            
            if room_name in self.rooms:
                return self.rooms[room_name]["users"]
            
            return "Sala não encontrada."
        except Exception as e:
            print(f"Erro ao listar usuários: {e}")
            return f"Erro ao listar usuários: {e}"

    def run(self):
        try:
            # Inicia a thread para verificar salas vazias
            threading.Thread(target=self.check_empty_rooms, daemon=True).start()

            # Inicia o servidor principal
            self.server.serve_forever()
        except Exception as e:
            print(f"Erro inesperado no servidor: {e}. O servidor continuará tentando.")

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.run()