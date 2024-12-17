import xmlrpc.client
import time

class ChatClient:
    def __init__(self, binder_address):
        self.binder = xmlrpc.client.ServerProxy(binder_address)
        self.server = None
        self.username = None

    def discover_server(self, method_name):
        address = self.binder.lookup_procedure(method_name)
        if address:
            self.server = xmlrpc.client.ServerProxy(f"http://{address[0]}:{address[1]}")
        else:
            print("Method not found.")

    def register_user(self, username):
        self.username = username
        print(f"Registered as '{username}'.")

    def interact(self):
        self.discover_server("create_room")
        while True:
            cmd = input("Enter command (create, join, send, list, exit): ").lower()
            if cmd == "create":
                room_name = input("Room name: ")
                print(self.server.create_room(room_name))
            elif cmd == "send":
                room = input("Room name: ")
                msg = input("Message: ")
                self.server.send_message(self.username, room, msg)
            elif cmd == "list":
                print(self.server.list_rooms())
            elif cmd == "exit":
                break

def main():
    binder_address = "http://localhost:5000"
    client = ChatClient(binder_address)
    username = input("Enter your username: ")
    client.register_user(username)
    client.interact()

if __name__ == "__main__":
    main()
