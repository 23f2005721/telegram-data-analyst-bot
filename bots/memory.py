"""
Conversation memory for multi-turn chats.
"""

conversation_memory = {}


def get_history(chat_id: int):
    return conversation_memory.get(chat_id, [])


def add_message(chat_id: int, role: str, content: str):
    conversation_memory.setdefault(chat_id, []).append(
        {
            "role": role,
            "content": content
        }
    )


def clear_history(chat_id: int):
    conversation_memory.pop(chat_id, None)
