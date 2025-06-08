from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery
from app.messages.fa import PLANS, RULES_TEXT
from app.telegram.bot_instance import bot
from app.telegram.exception_handler import catch_errors
from app.utils.message import get_message

def getRulesMarkup(explain_rules:bool=True):
    markup = InlineKeyboardMarkup()
    if explain_rules:
        markup.add(InlineKeyboardButton(get_message("rules.explain.rules"), callback_data=get_message("rules.explain.rules")))
    else:
        markup.add(InlineKeyboardButton(get_message("rules.explain.plans"), callback_data=get_message("rules.explain.plans")))
    markup.add(InlineKeyboardButton(get_message("rules.acc"), callback_data=get_message("rules.acc")))
    return markup

@bot.message_handler(func=lambda m: m.text == get_message("btn.user.rules"))
@catch_errors(bot)
def show_rules(msg: Message):
    markup=getRulesMarkup(explain_rules=False)
    bot.send_message(
        chat_id=msg.chat.id,
        text=RULES_TEXT,
        parse_mode="HTML",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda c: c.data == get_message("rules.explain.rules"))
@catch_errors(bot)
def rules(call:CallbackQuery):
    markup=getRulesMarkup(explain_rules=False)
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=RULES_TEXT,parse_mode="HTML",reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == get_message("rules.explain.plans"))
@catch_errors(bot)
def rules(call:CallbackQuery):
    markup=getRulesMarkup(explain_rules=True)
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=PLANS,parse_mode="HTML",reply_markup=markup)


@bot.callback_query_handler(func=lambda c: c.data == get_message("rules.acc"))
@catch_errors(bot)
def acknowledge_rules(call:CallbackQuery):
    bot.answer_callback_query(call.id, "ممنون که قوانین را مطالعه کردید ✅")
    bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.id)
    

