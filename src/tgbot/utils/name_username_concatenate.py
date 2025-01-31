from src.db.users.schemas import User


def name_username_concatenate(user: User) -> str:
    return f"{user.name} ({user.username})"
