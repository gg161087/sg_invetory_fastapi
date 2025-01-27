from src.core.security import bcrypt_context

USERS = [
    {
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "admin",
        "last_name": "admin",
        "password": bcrypt_context.hash('admin'),
        "role": "admin"
    },
    {
        "username": "user",
        "email": "user@example.com",
        "first_name": "user",
        "last_name": "user",
        "password": bcrypt_context.hash('user'),
        "role": "user"
    }
]