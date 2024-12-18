from datetime import datetime, timedelta

class RoomManager:
    def __init__(self):
        self.rooms = {}  # Estrutura: {room_name: {users: set(), messages: list(), last_active: datetime}}

    def create_room(self, room_name):
        if room_name in self.rooms:
            return False, "Sala já existe."
        self.rooms[room_name] = {"users": set(), "messages": [], "last_active": datetime.now()}
        return True, f"Sala '{room_name}' criada com sucesso."

    def join_room(self, username, room_name):
        if room_name not in self.rooms:
            return False, "Sala não existe."
        self.rooms[room_name]["users"].add(username)
        self.rooms[room_name]["last_active"] = datetime.now()
        return True, f"Usuário '{username}' entrou na sala '{room_name}'."

    def list_users(self, room_name):
        if room_name not in self.rooms:
            return False, "Sala não existe."
        return True, list(self.rooms[room_name]["users"])

    def clean_inactive_rooms(self, timeout_minutes=5):
        current_time = datetime.now()
        inactive_rooms = [room for room, data in self.rooms.items()
                          if not data["users"] and current_time - data["last_active"] > timedelta(minutes=timeout_minutes)]
        for room in inactive_rooms:
            del self.rooms[room]

    def get_room_names(self):
        return list(self.rooms.keys())
