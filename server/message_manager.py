from datetime import datetime

class MessageManager:
    def __init__(self):
        self.MAX_MESSAGES = 50  # Limite do histórico de mensagens públicas

    def add_message(self, room_data, username, content, recipient=None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg_type = "unicast" if recipient else "broadcast"
        message = {"type": msg_type, "origin": username, "recipient": recipient, "content": content, "timestamp": timestamp}

        room_data["messages"].append(message)
        if len(room_data["messages"]) > self.MAX_MESSAGES:
            room_data["messages"].pop(0)

        return f"Mensagem enviada às {timestamp}."

    def get_messages_for_user(self, room_data, username):
        return [msg for msg in room_data["messages"] if msg["type"] == "broadcast" or msg["recipient"] == username]
