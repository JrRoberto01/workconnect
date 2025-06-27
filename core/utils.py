from .models import ChatRoom

def get_or_create_private_chat(user1, user2):
    rooms = ChatRoom.objects.filter(is_group=False, participants=user1).filter(participants=user2)
    if rooms.exists():
        return rooms.first()
    room = ChatRoom.objects.create(is_group=False)
    room.participants.add(user1, user2)
    return room
