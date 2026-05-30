
# қарапайым memory (in-memory storage)
user_memory = {}

def add_message(user_id: int, role: str, text: str):

    if user_id not in user_memory:
        user_memory[user_id] = []

    user_memory[user_id].append({
        "role": role,
        "content": text
    })

    # memory limit (соңғы 10 message ғана)
    if len(user_memory[user_id]) > 10:
        user_memory[user_id] = user_memory[user_id][-10:]


def get_memory(user_id: int):

    return user_memory.get(user_id, [])

