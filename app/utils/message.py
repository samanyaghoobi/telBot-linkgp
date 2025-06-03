from app.messages import fa as lang

def get_message(key: str, **kwargs):
    """
    Return a formatted message string by key.
    You can pass placeholders as keyword arguments.
    """

    raw = lang.MESSAGES.get(key, f"[Missing message: {key}]")
    return raw.format(**kwargs)
