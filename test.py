
from database.db_setting import db_botSetting_insert, db_botSetting_updateValue, db_botSetting_getValue

defult =db_botSetting_getValue(name="bot_is_enable")
print(f"def value ={defult}")

bot_is_enable =db_botSetting_getValue(name="bot_is_enable")
print(f"before: {bot_is_enable}")
db_botSetting_updateValue(name="bot_is_enable",newValue="1")
bot_is_enable =db_botSetting_getValue(name="bot_is_enable")
print(f"after: {bot_is_enable}")