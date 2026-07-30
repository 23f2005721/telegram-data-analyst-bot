"""
memory.py

In-memory storage for multi-turn conversations.

Stores:
- Conversation history
- Current dataframe
- Last downloaded file
- Last parsed task

NOTE:
This is in-memory only. Data will be lost when the bot restarts.
"""

from typing import Any, Dict, List, Optional

# ==========================================================
# Internal Storage
# ==========================================================

conversation_memory: Dict[int, List[dict]] = {}

dataframe_memory: Dict[int, Any] = {}

file_memory: Dict[int, str] = {}

task_memory: Dict[int, Any] = {}

# ==========================================================
# Conversation History
# ==========================================================


def get_history(chat_id: int) -> List[dict]:
    return conversation_memory.get(chat_id, [])


def add_message(chat_id: int, role: str, content: str) -> None:
    conversation_memory.setdefault(chat_id, []).append(
        {
            "role": role,
            "content": content
        }
    )


def clear_history(chat_id: int) -> None:
    conversation_memory.pop(chat_id, None)

# ==========================================================
# DataFrame Memory
# ==========================================================


def save_dataframe(chat_id: int, dataframe) -> None:
    dataframe_memory[chat_id] = dataframe


def get_dataframe(chat_id: int):
    return dataframe_memory.get(chat_id)


def has_dataframe(chat_id: int) -> bool:
    return chat_id in dataframe_memory


def clear_dataframe(chat_id: int) -> None:
    dataframe_memory.pop(chat_id, None)

# ==========================================================
# File Memory
# ==========================================================


def save_file(chat_id: int, filepath: str) -> None:
    file_memory[chat_id] = filepath


def get_file(chat_id: int) -> Optional[str]:
    return file_memory.get(chat_id)


def has_file(chat_id: int) -> bool:
    return chat_id in file_memory


def clear_file(chat_id: int) -> None:
    file_memory.pop(chat_id, None)

# ==========================================================
# Task Memory
# ==========================================================


def save_task(chat_id: int, task) -> None:
    task_memory[chat_id] = task


def get_task(chat_id: int):
    return task_memory.get(chat_id)


def has_task(chat_id: int) -> bool:
    return chat_id in task_memory


def clear_task(chat_id: int) -> None:
    task_memory.pop(chat_id, None)

# ==========================================================
# Utility Functions
# ==========================================================


def clear_chat(chat_id: int) -> None:
    """
    Remove all memory associated with a chat.
    """

    clear_history(chat_id)
    clear_dataframe(chat_id)
    clear_file(chat_id)
    clear_task(chat_id)


def clear_all() -> None:
    """
    Clears every stored conversation.
    Useful during testing.
    """

    conversation_memory.clear()
    dataframe_memory.clear()
    file_memory.clear()
    task_memory.clear()
