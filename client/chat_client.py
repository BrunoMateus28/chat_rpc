import xmlrpc.client

class ChatClient:
    def __init__(self, binder_host="localhost", binder_port=5000):
        self.username = None
        self.binder = xmlrpc.client.ServerProxy(f"http://{binder_host}:{binder_port}")
        self.server = None
        self.connected_room = None
        self.discover_server()
        self.register_user()

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

    def interact(self):
        while True:
            cmd = input("Enter command (create, join, send, list, users, exit): ").lower()
            if cmd == "create":
                room_name = input("Room name: ")
                print(self.server.create_room(room_name))
            elif cmd == "join":
                room_name = input("Room name: ")
                response = self.server.join_room(self.username, room_name)
                if "users" in response:
                    self.connected_room = room_name
                    print(f"You have joined the room '{room_name}'.")
                else:
                    print(response)
            elif cmd == "send":
                if self.connected_room is None:
                    print("You are not connected to any room.")
                    continue
                msg = input("Message: ")
                print(self.server.send_message(self.username, self.connected_room, msg))
            elif cmd == "list":
                print("Available rooms:")
                print(self.server.list_rooms())
            elif cmd == "users":
                if self.connected_room is None:
                    print("You are not connected to any room.")
                    continue
                print(f"Users in the room '{self.connected_room}':")
                print(self.server.list_users(self.connected_room))
            elif cmd == "exit":
                print("Exiting the client...")
                self.server.unregister_user(self.username)
                break
            else:
                print("Unknown command. Please enter one of the following: create, join, send, list, users, exit.")

if __name__ == "__main__":
    client = ChatClient()
    client.interact()
