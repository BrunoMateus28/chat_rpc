from datetime import datetime
import xmlrpc.client
import threading
import time

class ChatClient:
    def __init__(self, binder_host="localhost", binder_port=5000):
        self.username = None
        self.binder = xmlrpc.client.ServerProxy(f"http://{binder_host}:{binder_port}")
        self.server = None
        self.connected_room = None
        self.last_message_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Inicializa com a data e hora atual
        self.discover_server()
        self.discover_server()
        self.register_user()
        self.lock = threading.Lock()  # Lock para proteger as requisições

    def discover_server(self):
        """Descobre métodos registrados no Binder."""
        self.server = xmlrpc.client.ServerProxy(f"http://{self.binder.lookup_procedure('create_room')[0]}:9000")

    def register_user(self):
        """Solicita e registra um nome de usuário válido no servidor."""
        while True:
            try:
                self.username = input("Digite seu username: ")
                response = self.server.register_user(self.username)
                print(response)
                break  # Sai do loop se o registro for bem-sucedido
            except xmlrpc.client.Fault as fault:
                print(f"Erro: {fault.faultString}")
                print("Por favor, escolha outro username.")

    def listen_for_messages(self):
        """Função que roda em uma thread para buscar novas mensagens em tempo real."""
        while True:
            if self.connected_room:
                try:
                    with self.lock:  # Usando o lock para garantir que a leitura e envio sejam síncronos
                        # Pega as últimas mensagens desde o timestamp da última mensagem recebida
                        messages = self.server.receive_new_messages(self.username, self.connected_room, self.last_message_timestamp)

                        if messages:
                            for msg in messages:
                                # Garantir que o timestamp seja tratado como um inteiro
                                msg_timestamp = msg['timestamp']
                                if msg_timestamp > self.last_message_timestamp and msg['origin']!=self.username:  # Comparar corretamente
                                    print(f"\n[{msg_timestamp}] {msg['origin']}: {msg['content']}")
                                    self.last_message_timestamp = msg_timestamp
                except (xmlrpc.client.Fault, ConnectionError) as e:
                    print(f"Erro ao tentar receber mensagens: {e}")
            time.sleep(2)  # Aguarda 2 segundos antes de buscar novas mensagens novamente

    def interact(self):
        # Começa a thread para escutar novas mensagens
        message_thread = threading.Thread(target=self.listen_for_messages)
        message_thread.daemon = True  # Para que a thread seja encerrada quando o programa terminar
        message_thread.start()
        while True:
            with self.lock:
                try:
                    cmd = input("Use um comando (create, join, send, list, users, exit): ").lower()
                    if cmd == "create":
                        room_name = input("Nome da sala: ")
                        print(self.server.create_room(room_name))
                    elif cmd == "join":
                        room_name = input("Nome da sala: ")
                        response = self.server.join_room(self.username, room_name)
                        if "users" in response:
                            self.connected_room = room_name
                            print(f"Voce entrou na sala '{room_name}'.")
                            # Mostra o histórico de mensagens
                            print("Ultimas mensagens:")
                            for msg in response["messages"]:
                                if(msg["destination"]=="" or msg["destination"]==None):
                                    print(f"[{msg['timestamp']}] {msg['origin']} -> {msg['content']}")
                            # Atualiza o timestamp da última mensagem recebida
                            if response["messages"]:
                                self.last_message_timestamp = response["messages"][-1]["timestamp"]
                        else:
                            print(response)
                    elif cmd == "send":
                        if self.connected_room is None:
                            print("Voce nao esta em nenhuma sala.")
                            continue
                        msg = input("Mensagem: ")
                        recipient = input("Usuario(se quiser mensagem privada): ")
                        with self.lock:
                            print(self.server.send_message(self.username, self.connected_room, msg, recipient))
                    elif cmd == "list":
                        print("Salas existentes:")
                        print(self.server.list_rooms())
                    elif cmd == "users":
                        if self.connected_room is None:
                            print("Voce nao esta em nenhuma sala.")
                            continue
                        print(f"Usuarios na sala: '{self.connected_room}':")
                        print(self.server.list_users(self.connected_room))
                    elif cmd == "exit":
                        print("Desconectando o Cliente...")
                        self.server.unregister_user(self.username)
                        break
                    else:
                        print("Comando desconhecido. Use um dos seguintes: create, join, send, list, users, exit.")
                except Exception as e:
                    print(f"Erro inesperado: {e}. O programa continuará a execução.")
                    message_thread = threading.Thread(target=self.listen_for_messages)
                    message_thread.daemon = True  # Para que a thread seja encerrada quando o programa terminar
                    message_thread.start()


if __name__ == "__main__":
    client = ChatClient()
    client.interact()
