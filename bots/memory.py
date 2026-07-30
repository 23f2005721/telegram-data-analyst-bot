"""
Conversation memory for multi-turn chats.
"""

conversation_memory = {}

# Stores current dataframe for each chat
dataframe_memory = {}

# Stores last downloaded file path
file_memory = {}

# Stores last parsed task (optional)
task_memory = {}


# ----------------------------
# Conversation History
# ----------------------------

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


# ----------------------------
# DataFrame Memory
# ----------------------------

def save_dataframe(chat_id: int, df):
    dataframe_memory[chat_id] = df


def get_dataframe(chat_id: int):
    return dataframe_memory.get(chat_id)


def clear_dataframe(chat_id: int):
    dataframe_memory.pop(chat_id, None)


# ----------------------------
# File Memory
# ----------------------------

def save_file(chat_id: int, filepath: str):
    file_memory[chat_id] = filepath


def get_file(chat_id: int):
    return file_memory.get(chat_id)


def clear_file(chat_id: int):
    file_memory.pop(chat_id, None)


# ----------------------------
# Task Memory (Optional)
# ----------------------------

def save_task(chat_id: int, task):
    task_memory[chat_id] = task


def get_task(chat_id: int):
    return task_memory.get(chat_id)


def clear_task(chat_id: int):
    task_memory.pop(chat_id, None)


# ----------------------------
# Clear Everything
# ----------------------------

def clear_chat(chat_id: int):
    clear_history(chat_id)
    clear_dataframe(chat_id)
    clear_file(chat_id)
    clear_task(chat_id)
