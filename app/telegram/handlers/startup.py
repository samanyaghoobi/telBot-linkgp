from config import ADMINS

def startup_message(bot):
    for admin in ADMINS:
        print (admin)
        bot.send_message(
            admin,  
            "🤖 ربات با موفقیت راه‌اندازی شد و به کار افتاد!"
        )