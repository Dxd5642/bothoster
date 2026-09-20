import secrets

async def generate_session():
    return secrets.token_urlsafe(32)