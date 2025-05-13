
import telebot
from telebot import types
from lists_petr1 import bio_sections
bot = telebot.TeleBot('7861387718:AAHB5vmw90lDXi5v4hbyjSWcu1zjkonn-Xg')
from telebot import types

messages = {}
pages = {}

def get_biography_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_overview = types.InlineKeyboardButton("Общий обзор", callback_data="overview")
    btn_childhood = types.InlineKeyboardButton("Детство и юность", callback_data="childhood")
    btn_reforms = types.InlineKeyboardButton("Реформы", callback_data="reforms")
    btn_military = types.InlineKeyboardButton("Военные кампании", callback_data="military")
    # btn_cultural = types.InlineKeyboardButton("Культура", callback_data="cultural")
    # btn_legacy = types.InlineKeyboardButton("Наследие", callback_data="legacy")
    markup.add(btn_overview, btn_childhood, btn_reforms, btn_military)
    return markup

def get_back_button():
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton("Назад в меню", callback_data="back_to_menu")
    markup.add(btn_back)
    return markup


def create_navigation_buttons(current_page, total_pages, section):
    markup = types.InlineKeyboardMarkup()
    if current_page > 0:
        btn_prev = types.InlineKeyboardButton("Предыдущая страница", callback_data=f"previous_{section}_{current_page}")
        markup.add(btn_prev)
    if current_page < total_pages - 1:
        btn_next = types.InlineKeyboardButton("Следущая страница", callback_data=f"next_{section}_{current_page}")
        markup.add(btn_next)
    btn_back = types.InlineKeyboardButton("Вернуться в меню", callback_data="back_to_menu")
    markup.add(btn_back)
    return markup

@bot.message_handler(commands=["start"])
def start_command(message):
    text = (
        "Привет! Я бот, который расскажет тебе подробную биографию Петра I.\n\n"
        "Выбери интересующий раздел, нажав одну из кнопок ниже."
    )
    msg = bot.send_message(message.chat.id, text, reply_markup=get_biography_menu())
    messages[message.chat.id] = [msg]

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    chat_id = call.message.chat.id

    if call.data in bio_sections:
        for mas in messages.get(chat_id, []):
            try:
                bot.delete_message(chat_id, mas.id)
            except Exception as e:
                print(f"Не удалось удалить сообщение: {e}")

        messages[chat_id] = []
        text = bio_sections[call.data]
        pages[chat_id] = text.split('\n\n')
        current_page = 0
        total_pages = len(pages[chat_id])

        msg_text = pages[chat_id][current_page]
        msg = bot.send_message(chat_id, msg_text, reply_markup=create_navigation_buttons(current_page, total_pages, call.data))
        messages[chat_id].append(msg)

    elif call.data.startswith('next_') or call.data.startswith('previous_'):
        _, section, current_page = call.data.split('_')
        current_page = int(current_page)

        if call.data.startswith('next_'):
            current_page += 1
        else:
            current_page -= 1

        for msg in messages.get(chat_id, []):
            try:
                bot.delete_message(chat_id, msg.id)
            except Exception as e:
                print(f"Не удалось удалить сообщение: {e}")

        messages[chat_id] = []

        msg_text = pages[chat_id][current_page]
        total_pages = len(pages[chat_id])
        msg = bot.send_message(chat_id, msg_text, reply_markup=create_navigation_buttons(current_page, total_pages, section))
        messages[chat_id].append(msg)

    elif call.data == "back_to_menu":
        for mas in messages.get(chat_id, []):
            try:
                bot.delete_message(chat_id, mas.id)
            except Exception as e:
                print(f"Не удалось удалить сообщение: {e}")

        messages[chat_id] = []
        mas = bot.send_message(chat_id, "Возвращаемся в главное меню...")
        messages[chat_id].append(mas)

        mas = bot.send_message(chat_id, "Выбери интересующий раздел, нажав одну из кнопок ниже.",
                               reply_markup=get_biography_menu())
        messages[chat_id].append(mas)
if __name__ == '__main__':
    bot.polling(none_stop=True)
