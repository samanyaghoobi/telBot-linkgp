from app.telegram.bot_instance import bot

@bot.message_handler(commands=["panel"], is_admin=True)
def admin_panel(message):
    bot.reply_to(message, "Welcome, admin!")

@bot.message_handler(commands=["panel"])
def admin_panel(message):
    bot.reply_to(message, "Welcome, user!")
