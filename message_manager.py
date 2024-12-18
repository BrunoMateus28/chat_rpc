from datetime import datetime

class MessageManager:
    def __init__(self):
        self.MAX_MESSAGES = 50  # Limite do histórico de mensagens públicas

    def send_message(self, username, room_name, message, recipient=None):
        # Retrieve the room's data
        room_data = self.room_manager.rooms.get(room_name)
        if not room_data:
            return f"Erro: A sala '{room_name}' não existe."
        if username not in room_data["users"]:
            return f"Erro: O usuário '{username}' não está conectado na sala '{room_name}'."

        # Call add_message with the correct room data
        return self.message_manager.add_message(room_data, username, message, recipient)


    def get_messages_for_user(self, room_data, username):
        return [msg for msg in room_data["messages"] if msg["type"] == "broadcast" or msg["recipient"] == username]
