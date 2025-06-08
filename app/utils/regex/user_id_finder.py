import re
from telebot.types import Message

# Function to extract user ID from a formatted message like:
# "👤 نام کاربری : Samanyaghoobi
# 🆔 شناسه کاربری :5416152450
# 💵 موجودی : 5465480 هزار تومان
# 💯 امتیاز شما: 0"
def extract_user_id(text: str) -> int:
    # Regular expression to match the user ID pattern
    match = re.search(r"🆔 شناسه کاربری :\s*(\d+)", text)
    if match:
        return int(match.group(1))  # Extract user ID as integer
    return None

