import os
import json
import logging
import sys
from telegram import Update,ReplyKeyboardMarkup,InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,filters, MessageHandler,CallbackQueryHandler
import requests
from urllib.parse import quote
#from telegram import ParseMode
from telegram import Bot
#from telegram import ChatAction
logging.basicConfig(level=logging.INFO)
all_string={
"add_money":{"title":"𝗕𝘂𝘆 𝗽𝗿𝗲𝗺𝗶𝘂𝗺","msg":""},
"send_sms":{"title":"𝗦𝗘𝗡𝗗 𝗦𝗠𝗦","msg":""},
"send_sms_to_user":{"title":"Send Message to User 📤","msg":""},
"redeem":{"title":"Redeem","msg":""},
"redeem_code":{"title":"Redeem code♻️","msg":""},
"support":{"title":"☎️ Support","msg":""},
"my_account":{"title":"𝗠𝗬 𝗜𝗡𝗙𝗢","msg":""},
"back":{"title":"𝗕𝗔𝗖𝗞","msg":""},
"send_balance":{"title":"𝗔𝗱𝗱 𝘂𝘀𝗲𝗿 𝗕𝗮𝗹𝗮𝗻𝗰𝗲","msg":""},
"statistics":{"title":"📊 Statistics","msg":""},
"add_admin":{"title":"➕ Add Admin","msg":""},
}
all_message={
"not_admin":"𒊹︎︎︎➪𝙁𝙪𝙘𝙠 𝙔𝙤𝙪! 𝙔𝙤𝙪𝙧 𝙉𝙤𝙩 𝘼𝙩 𝘼𝙙𝙢𝙞𝙣",
"0balance":"",
"number":">𒊹︎︎︎➪ 𝙀𝙣𝙩𝙚𝙧 𝙔𝙤𝙪𝙧 𝙍𝙤𝙗𝙞 / 𝘼𝙞𝙧𝙩𝙚𝙡 𝙉𝙪𝙢𝙗𝙚𝙧 "}

add_balance=all_string["add_money"]["title"]
send_sms=all_string["send_sms"]["title"]
send_stu=all_string["send_sms_to_user"]["title"]
redeem=all_string["redeem"]["title"]
redeem_codes=all_string["redeem_code"]["title"]
support=all_string["support"]["title"]
my_account=all_string["my_account"]["title"]
back_btn=all_string["back"]["title"]
statistics=all_string["statistics"]["title"]
add_admin=all_string["add_admin"]["title"]
send_balance=all_string["send_balance"]["title"]

DB_FILE = "bot.json"

def load_data_from_file(files):
    try:
        with open(DB_FILE, 'r') as file:
            return json.load(file).get(files, [])
    except FileNotFoundError:
        logging.info(f"File '{DB_FILE}' not found. Creating a new one.")
        return []
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON in file '{DB_FILE}'. Initializing with an empty list.")
        return []
channel_id =-1002124153192

adminid=load_data_from_file("admin")
redeem_code=load_data_from_file("redeem")
data=load_data_from_file("data")

def save_data_to_file(data, files):
    try:
        with open(DB_FILE, 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        logging.info(f"File '{DB_FILE}' not found. Creating a new one.")
        existing_data = {}

    existing_data[files] = data

    try:
        with open(DB_FILE, 'w') as file:
            json.dump(existing_data, file, indent=2)
    except IOError as e:
        logging.error(f"Error saving data to file '{DB_FILE}': {e}")

def get_user_by_id(user_id):
    for user_data in data:
        if user_data["user_id"] == user_id:
            return user_data

def updatee(user_id,key,val ):
    for i, user_data in enumerate(data):
        if user_data["user_id"] == user_id:
            data[i][key]=str(val)
            save_data(data)
def update_plus(user_id, key, val):
    for i, user_data in enumerate(data):
        if user_data["user_id"] == user_id:
            current_value = int(user_data[key])
            data[i][key] = str(current_value + int(val))
            save_data(data)
def update_min(user_id,key,val):
    for i, user_data in enumerate(data):
        if user_data["user_id"] == user_id:
            current_value = int(user_data[key])
            data[i][key] = str(current_value - int(val))
            save_data(data)

def save_data(data):
    save_data_to_file(data, "data")
def save_redeem(data):
    save_data_to_file(data, "redeem")
def save_admin(data):
    save_data_to_file(data, "admin")
def user_exists(user_id):
    return any(user_data["user_id"] == user_id for user_data in data)


def add_adminid(adminn):
    adminid=load_data_from_file("admin")
    adminid.append(adminn)
    save_admin(adminid)


async def add_user(new_user_data, context):
    user_id = new_user_data["user_id"]
    
    if not user_exists(user_id):
        chat_id = new_user_data["referral_user"]
        message=f"🧐 New User 🙂\n\n🆔 Id : `{new_user_data['user_id']}`\n✅ Name : {new_user_data['name']}\n🔶 Uname: {new_user_data['username']}\n💰 balance: {new_user_data['balance']}"

        await context.bot.send_message(chat_id="5644179586", text=message, )
        data.append(new_user_data)
        save_data(data)
        update_plus(user_id,"balance","10")  # Pass data to the function
        if chat_id is not None:
            if not chat_id == user_id:
                update_plus(chat_id,"referral_count","1")
                update_plus(chat_id,"balance","2")
                update_plus(user_id,"balance","1")
        logging.info(f"User with ID {user_id} added successfully.")
    else:
        logging.info(f"User with ID {user_id} already exists.")
        #message=f"🧐 User start the bot 🙂\n\n🆔 Id : `{new_user_data['user_id']}`\n✅ Name : {new_user_data['name']}\n🔶 Uname: {new_user_data['username']}\n💰 balance: {new_user_data['balance']}"
        #await context.bot.send_message(chat_id="5891721724", text=message)
    



async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id =str(update.effective_user.id)
    user = update.effective_user
    def check_admin():
        update.message.reply_markdown(
        fr'{all_message["not_admin"]}'
        )
    if update.message.text == send_sms:
        if 0 < int(get_user_by_id(id)['balance']):
            message="𒊹︎︎︎=> 𝙀𝙣𝙩𝙚𝙧 𝙔𝙤𝙪𝙧 𝙣𝙪𝙢𝙗𝙚𝙧 ➪"
            await update.message.reply_text(message)
            context.user_data['send_sms'] = True
        else:
            #await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
            message=f"𝙃𝙚𝙮 {update.effective_user.full_name} 𝘼𝙥𝙣𝙧 𝘽𝙖𝙡𝙖𝙣𝙘𝙚 0 𝙨𝙢𝙨 𝙠𝙤𝙧𝙩𝙚 𝙥𝙧𝙚𝙢𝙞𝙪𝙢 𝙠𝙞𝙣𝙪𝙣 "
            await update.message.reply_markdown(message)
    elif 'send_sms' in context.user_data and context.user_data['send_sms']:
        if (update.message.text.isdigit() and len(update.message.text) == 11):
            context.user_data['send_smsnum'] = update.message.text
            del context.user_data['send_sms']
            sent_message = await update.message.reply_text(
            fr'𝗛𝗲𝘆! 𝗔𝗽𝗻𝗶 𝗷𝗲 𝘀𝗺𝘀 𝘀𝗲𝗻𝗱 𝗸𝗿𝘁𝗲 𝗰𝗵𝗮𝗻 𝗔𝗶 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝘁𝗶 𝗿𝗲𝗽𝗹𝘆 𝗱𝗶𝘆𝗲 𝗟𝗶𝗸𝗵𝘂𝗻...'
            )
            context.user_data['initial_message_id'] = sent_message.message_id
        else:
            message="𝘃𝗵𝘂𝗹 𝗡𝘂𝗺𝗯𝗲𝗿 𝗗𝗶𝘆𝗲𝗰𝗵𝗲𝗻"
            await update.message.reply_text(message)
            del context.user_data['send_sms']
            await cancel(update,context)
    elif 'send_smsnum' in context.user_data and context.user_data['send_smsnum']:
        if update.message.reply_to_message:
            if 'initial_message_id' in context.user_data and context.user_data['initial_message_id'] == update.message.reply_to_message.message_id:
                message =update.message.text
                #gali=open("Gali.txt","r",encoding="utf-8").read()
                #check= message.split()
                #new_user_data=get_user_by_id(id)
                """for i in check:
                    if i.lower() in gali:
                        await update.message.reply_text(f"Chi Tumi Gali Dew Chi Chi Chi 🧐")
                        message=f"🙂 User gali dice 🙂\n\n🆔 Id : {new_user_data['user_id']}\n✅ Name : {new_user_data['name']}\n🔶 Uname: {new_user_data['username']}\n💰 balance: {new_user_data['balance']}"
                        await context.bot.send_message(chat_id="5891721724", text=message)
    
                        return """
                #await update.message.reply_text(context.user_data)
                number=context.user_data['send_smsnum']
                url = "https://alternativezonebd.xyz/customsms/sms.php"
                
                encoded_message = quote(message)
                complete_url = f"{url}?number={number}&msg={encoded_message}"
                response = requests.get(complete_url).json()
                if response["Response"]["success"] == "success":
                    await update.message.reply_text(f'𝗦𝗠𝗦 𝗦𝗲𝗻𝗱 𝗦𝘂𝗰𝗰𝘀𝘀𝗲𝘀𝗳𝘂𝗹𝗹𝘆 𝘁𝗼 𝘀𝗲𝗻𝗱 {number} 𝗧𝗵𝗶𝘀 𝗡𝘂𝗺𝗯𝗲𝗿. 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 ➪ {response["Response"]["message"]}')
                    update_min(id,"balance","1")
            else:
                await update.message.reply_text(f'𝗙𝗮𝗶𝗹𝗱: 𝗦𝗠𝗦 𝗡𝗢𝗧 𝗦𝗲𝗻𝗱 𝗧𝗵𝗶𝘀 𝗡𝘂𝗺𝗯𝗲𝗿. 𝗿𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {response["Response"]["message"]} Contact To The Developer')
            del context.user_data['send_smsnum']
            del context.user_data['initial_message_id']
            await cancel1(update,context)
        else:
            await update.message.reply_text("𝙥𝙠𝙚𝙖𝙨𝙚 𝙏𝙤 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙩𝙤 /cancel 𝙩𝙤 𝙀𝙣𝙙 𝙔𝙤𝙪𝙧 𝘾𝙤𝙢𝙢𝙖𝙣𝙙!")
        await cancel1(update,context)
    elif update.message.text == my_account:
        my_account_message=(
        f"""\n𝙐𝙎𝙀𝙍𝙄𝘿 <=> {id}
𝙐𝙎𝙀𝙍𝙉𝘼𝙈𝙀 <=> {user.username}
𝘽𝘼𝙇𝘼𝙉𝘾𝙀 <=> {get_user_by_id(id)['balance']}
𝙏𝙊𝙏𝘼𝙇 𝙍𝙀𝙁𝙁𝙀𝙍 <=> {get_user_by_id(id)['referral_count']}"""
        )
        keyboard = [[add_balance, support], [back_btn]]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            fr"Hi {update.effective_user.first_name+update.effective_user.last_name} {my_account_message}",
            reply_markup=markup,
            )
    elif update.message.text == "𝙍𝙀𝙁𝙁𝙀𝙍":
        keyboard = [
            [InlineKeyboardButton("Invite Friends", url=f"https://t.me/share/url?url={get_user_by_id(id)['referral_link']}")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(f"𝘼𝙥𝙣𝙧 𝙍𝙚𝙛𝙛𝙚𝙧 𝙇𝙞𝙣𝙠=>{get_user_by_id(id)['referral_link']}\n 𝙥𝙧𝙤𝙩𝙞 𝙍𝙚𝙛𝙛𝙚𝙧 𝙖 𝘼𝙥𝙣𝙠 1 𝙘𝙧𝙚𝙙𝙞𝙩 𝙙𝙚𝙮𝙖 𝙝𝙗𝙚. 𝘼𝙣𝙙 𝘼𝙥𝙣𝙞 𝙟𝙖𝙠𝙚 𝙞𝙣𝙫𝙞𝙩𝙚 𝙠𝙧𝙚𝙘𝙚𝙣 𝙎𝙝𝙚 2 𝙘𝙧𝙚𝙙𝙞𝙩 𝙥𝙖𝙗𝙚..", reply_markup=reply_markup)
    elif update.message.text == redeem:
        await update.message.reply_markdown(
        fr'HEY {user.mention_markdown()}  ENTER CODE YOU WANT TO REDEEM\!'
        )
        context.user_data["redeem"]=True
    elif 'redeem' in context.user_data and context.user_data['redeem']:
        code = update.message.text
        msg=""
        for j, rcode in enumerate(redeem_code):
            if code == rcode["code"]:
                if int(rcode["balance"]) == 0:
                    await update.message.reply_text("This code has already been redeemed")
                    msg="ok"
                else:
                    update_plus(id, "balance", int(rcode["balance"]))
                    redeem_code[j]["user"] = id  # Use square brackets for dictionary access
                    redeem_code[j]["balance"] = "0"  # Use square brackets for dictionary access
                    save_redeem(redeem_code)
                    await update.message.reply_markdown(
                    fr'HEY {user.mention_markdown()} You Have Successfully Redeemed the Code {code}. Your Account New {get_user_by_id(id)["balance"]} Credit balance.'
                    )
                    msg="ok"
                    break
        if not msg=="ok":
            await update.message.reply_text("Invalid code")
        del context.user_data["redeem"]
        await cancel1(update,context)
    elif update.message.text == add_balance:
        message = (
            "⭓━━━━━━━━━━━━━━━━⪦\n"
            "⭓━━━━━━━━━━━━━━━━━⪦\n"
            " 𒊹︎︎︎➪   100 𝗦𝗠𝗦 30 𝗕𝗗𝗧\n"
            " 𒊹︎︎︎➪    200 𝗦𝗠𝗦 55 𝗕𝗗𝗧\n"
            " 𒊹︎︎︎➪    500 𝗦𝗠𝗦 150 𝗕𝗗𝗧\n"
            " 𒊹︎︎︎➪    1000 𝗦𝗠𝗦  300 𝗕𝗗𝗧\n"
            "⭓━━━━━━━━━━━━━━━━⪦\n"
            " 𒊹︎︎︎➪ 𝗧𝗢 𝗕𝗨𝗬 𝗦𝗠𝗦 𝗶𝗻𝗯𝗼𝘅 : @STDNX ✅\n"
            "⭓━━━━━━━━━━━━━━━━━⪦\n")
        await update.message.reply_text(message)
    elif update.message.text == statistics:
        message=f'📊 𝗧𝗼𝘁𝗮𝗹 𝗨𝘀𝗲𝗿 𝗢𝗻 𝗕𝗼𝘁  : {len(data)} Users \n\n BoT DEVELOPER : @STDNXR \n\n Any Query? @STDNXR'
        await context.bot.send_message(chat_id=id, text=message,parse_mode="Markdown")
##__________________________________________________________________________________________________________________________________________________________________________________________________________________##
    elif update.message.text == back_btn:
        await start(update, context)  # Call the start function to go back to the start menu
        return

    elif update.message.text == support:
        # First message
        await update.message.reply_markdown(
            fr'Enter your message'
        )
        
        # Set a flag in context to indicate waiting for the second message
        context.user_data['waiting_for_second_message'] = True
    elif 'waiting_for_second_message' in context.user_data and context.user_data['waiting_for_second_message']:
        # Second message
        messages = (
        "User Support Message\n"
        f"Userid: ` {id} `\n"
        f"message: `{update.message.text}`"
        )
        for aid in adminid:
            await context.bot.send_message(chat_id=aid, text=messages,parse_mode="Markdown")
        await update.message.reply_markdown(
            fr'Your Message Send In All Admin'
        )
        
        # Reset the flag
        del context.user_data['waiting_for_second_message']
        await cancel1(update,context)
    elif update.message.text == send_stu:
        if id in adminid:
            await update.message.reply_markdown(
            fr'Enter User Id You Want To Send message')
            context.user_data['send_stu'] = True
        else: await check_admin()
    
    elif 'send_stu' in context.user_data and context.user_data['send_stu']:
        if id in adminid:
            userid=update.message.text
            info=get_user_by_id(userid)
            message=(
            "Enter message you want to send\n"
            "to this user\n"
            f"Username: {info['username']}\n"
            f"name: {info['name']}\n"
            f"balance: {info['balance']}\n")
            await update.message.reply_text(message)
            context.user_data['send_stuid'] = userid
            del context.user_data['send_stu']
    elif 'send_stuid' in context.user_data and context.user_data['send_stuid']:
        if id in adminid:
            userid= context.user_data['send_stuid']
            await context.bot.send_message(chat_id=userid, text=update.message.text, parse_mode="Markdown")
            del context.user_data['send_stuid']
            await cancel1(update,context)
    














    elif update.message.text == "remove_balance":
        if id in adminid:
            await update.message.reply_markdown(
            fr'Enter User Id You Want To remove Balance')
            context.user_data['remove_money'] = True
        else: await check_admin()
    elif 'remove_money' in context.user_data and context.user_data['remove_money']:
        if id in adminid:
            userid=update.message.text
            info=get_user_by_id(userid)
            message=(
            "Enter Amount you want to remove 💴\n"
            "to this user\n"
            f"Username: {info['username']}\n"
            f"name: {info['name']}\n"
            f"old balance: {info['balance']}\n")
            await update.message.reply_text(
            fr'{message}')
            context.user_data['remove_moneyid'] = userid
            del context.user_data['remove_money']
    elif 'remove_moneyid' in context.user_data and context.user_data['remove_moneyid']:
        if id in adminid:
            userid= context.user_data['remove_moneyid']
            amount=update.message.text
            updatee(userid,"balance",amount)
            await update.message.reply_text(
            fr'Balance revome success to user id {userid} 💴')
            del context.user_data['remove_moneyid']
            await cancel1(update,context)
    elif update.message.text == redeem_codes:
        if id in adminid:
            await update.message.reply_text(
            fr'Enter Code You Want To Add')
            context.user_data['redeem_code1'] = True
        else: await check_admin()
    elif 'redeem_code1' in context.user_data and context.user_data['redeem_code1']:
        if id in adminid:
            code = update.message.text
            await update.message.reply_text(
            fr'Enter Balance ')
            context.user_data['redeem_codeb'] = code
            del context.user_data['redeem_code1']
    elif 'redeem_codeb' in context.user_data and context.user_data['redeem_codeb']:
        if id in adminid:
            codes=context.user_data['redeem_codeb']
            balance = update.message.text
            new_c = {
                "code":codes,
                "balance":balance,
                "user":""}
            redeem_code.append(new_c)
            save_redeem(redeem_code)
            await update.message.reply_text(
                fr'Successfully Added New key {codes}')
            del context.user_data['redeem_codeb']
            
    elif update.message.text == add_admin:
         if id in adminid:
            await update.message.reply_markdown(
                fr'Enter admin id'
            )
        
            context.user_data['admin_id'] = True
         else: await check_admin()
    elif 'admin_id' in context.user_data and context.user_data['admin_id']:
        admi=update.message.text
        add_adminid(admi)
        globals()["adminid"] = load_data_from_file("admin")
    elif update.message.text == send_balance:
        if id in adminid:
            await update.message.reply_markdown(
            fr'Enter User Id You Want To Send 💴')
            context.user_data['send_money'] = True
        else: await check_admin()
    elif 'send_money' in context.user_data and context.user_data['send_money']:
        if id in adminid:
            userid=update.message.text
            info=get_user_by_id(userid)
            message=(
            "Enter Amount you want to send 💴\n"
            "to this user\n"
            f"Username: {info['username']}\n"
            f"name: {info['name']}\n"
            f"old balance: {info['balance']}\n")
            await update.message.reply_text(
            fr'{message}')
            context.user_data['send_moneyid'] = userid
            del context.user_data['send_money']
    elif 'send_moneyid' in context.user_data and context.user_data['send_moneyid']:
        if id in adminid:
            userid= context.user_data['send_moneyid']
            amount=update.message.text
            update_plus(userid,"balance",amount)
            await update.message.reply_text(
            fr'Balance send success to user id {userid} 💴')
            del context.user_data['send_moneyid']
            await cancel1(update,context)
    elif update.message.text == "UNLOCK 🔓":
        chat_member = await context.bot.get_chat_member(channel_id, id)
        if not chat_member.status in ['member','creator','administrator']:
            keyboard = [[InlineKeyboardButton("Join Channel", url=f'https://t.me/BD_Api_Zone')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            magi ="𝙃𝙞 𝙨𝙞𝙧 !"+update.effective_user.full_name+"\n\n 𒊹︎︎︎➪ 𝘾𝙝𝙚𝙣𝙚𝙡 𝙖 𝙟𝙤𝙞𝙣 𝙠𝙤𝙧𝙪𝙣 𝙣𝙖 𝙝𝙮 𝘽𝙤𝙩 𝘼𝙘𝙘𝙚𝙨𝙨 𝙠𝙧𝙩𝙚 𝙥𝙖𝙧𝙗𝙚𝙣 𝙣𝙖!"
            await update.message.reply_photo(photo="http://alternativezonebd.xyz/images.jpeg",caption=magi,parse_mode="Markdown",
            reply_markup=reply_markup
            )
        else: await start(update,context)
    elif update.message.text == "anusc":
        if id in adminid:
            #await update.message.reply_text('Enter Video Link')
            #context.user_data['video_link']= True
            #magi =" * Hello * 👋..."+update.effective_user.full_name+"*\n\n💡 Now Bot Upgrade Successful Added New Future /video You Can See Video How To Use And Some Function Improve To Use Experience Better "
            #magi = "<b> 🔊  Announcement 🥳 </b> \n\n <b>Hello</b> 👋..." + update.effective_user.full_name + "<b>\n\nNow Bot Upgrade Successful Added New Future /video You Can See Video How To Use And Some Function Improve To Use Experience Better</b>"
            #await update.message.reply_photo(photo="https://teamdccs.xyz/tb.png",caption=magi,parse_mode="HTML")
            for user in data:
                magi = "<b> 🔊  Announcement 🥳 </b> \n\n <b>Hello</b> 👋..." + user["name"] + "<b>\n\nNow Bot Upgrade Successful Added New Future /video You Can See Video How To Use And Some Function Improve To Use Experience Better</b>"
                try:
                    await context.bot.send_photo(chat_id=user["user_id"],photo="http://alternativezonebd.xyz/images.jpeg")
                except:
                    await context.bot.send_photo(chat_id=user["user_id"],photo="http://alternativezonebd.xyz/images.jpeg")
                 
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    
    
    
    if not any(user_data["user_id"] == str(user.id) for user_data in data):
        chat_id = context.args[0] if context.args else None
        referral_link = f"https://t.me/Api_Zone_csms_bot?start={user.id}"
        user_data = {
            "user_id": str(update.effective_user.id),
            "username": update.effective_user.username,
            "name": update.effective_user.full_name,
            "balance": "0",
            "referral_user":chat_id,
            "referral_link":referral_link,
            "referral_count":0,}
        await add_user(user_data, context)
    chat_member = await context.bot.get_chat_member(channel_id, str(user.id))
    if not chat_member.status in ['member','creator','administrator']:
        keyboard = [[InlineKeyboardButton("Join Channel", url=f'https://t.me/BD_Api_Zone')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        magi ="𝙃𝙞 𝙨𝙞𝙧 !"+update.effective_user.full_name+"\n\n 𒊹︎︎︎➪ 𝘾𝙝𝙚𝙣𝙚𝙡 𝙖 𝙟𝙤𝙞𝙣 𝙠𝙤𝙧𝙪𝙣 𝙣𝙖 𝙝𝙮 𝘽𝙤𝙩 𝘼𝙘𝙘𝙚𝙨𝙨 𝙠𝙧𝙩𝙚 𝙥𝙖𝙧𝙗𝙚𝙣 𝙣𝙖!"
        await update.message.reply_photo(photo="http://alternativezonebd.xyz/images.jpeg",
        reply_markup=reply_markup
        )
        #await context.bot.send_message(chat_id=update.effective_chat.id, text=f"You must join the channel to access this {chat_member.status}")
        await update.message.reply_text(
        fr"𒊹︎︎︎➪ 𝘼𝙨𝙨𝙖𝙇𝙖𝙢𝙪-𝘼𝙖𝙇𝙖𝙞𝙠𝙪𝙢 {update.effective_user.full_name}! 𝙬𝙚𝙇𝙘𝙤𝙢𝙚 𝙎𝙞𝙧! 𝙃𝙖𝙥𝙥𝙮 𝙉𝙚𝙬 𝙔𝙚𝙖𝙧! 💝",
        reply_markup=ReplyKeyboardMarkup(
            [[" "], [" ", " "],["UNLOCK 🔓"],[' '," "]],
            resize_keyboard=True
        
            )
        )
    else:
        message=f"🧐 User start the bot 🙂\n\n🆔 Id : `{update.effective_user.id}`\n✅ Name : {update.effective_user.full_name}\n🔶 Uname: {update.effective_user.username}"
        await context.bot.send_message(chat_id="5644179586", text=message)
        await update.message.reply_text(
        fr"𒊹︎︎︎➪ 𝘼𝙨𝙨𝙖𝙇𝙖𝙢𝙪-𝘼𝙖𝙇𝙖𝙞𝙠𝙪𝙢 {update.effective_user.full_name} ! 𝙬𝙚𝙇𝙘𝙤𝙢𝙚 𝙎𝙞𝙧!  𝙃𝙖𝙥𝙥𝙮 𝙉𝙚𝙬 𝙔𝙚𝙖𝙧! 💝",
        reply_markup=ReplyKeyboardMarkup(
            [[send_sms], [add_balance, my_account],["𝙍𝙀𝙁𝙁𝙀𝙍"]],
            resize_keyboard=True,
            one_time_keyboard=False
        
            )
        )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Handle user cancellation
    context.user_data.clear()
    await update.message.reply_text("cancelled!")
async def cancel1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Handle user cancellation
    context.user_data.clear()
async def adminxx(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    #adminid=["5891721724"]
    if str(user.id) in adminid:
        keyboard = [[send_stu],
        [send_balance, my_account],
        [add_admin,"remove_balance"],
        ["Redeem code♻️","📊 Statistics"]
        ]
        #[[], [, ],[]],
        await update.message.reply_text(
        fr'Hi Admin {update.effective_user.full_name}\!',
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        ))
    else:
        await update.message.reply_text(
        fr'Hey {update.effective_user.full_name}\! \n Your Not a Admin Bro {str(user.id)}',)
async def video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    id = str(update.effective_user.id)
    await update.message.reply_text('Please Wait Video Sending...')
    await context.bot.send_video(chat_id=id, video=open('v.mp4', 'rb'),  caption="This Is A Video Tutorial How To Use 🙂👍",supports_streaming=True)




app = ApplicationBuilder().token("6532294820:AAEKefdzGx9I4M-Nxg1naCTdKKK6tp7MXkk").build()

# Add command handler for /start command
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("STDNXR", adminxx))
app.add_handler(CommandHandler("cancel", cancel))
app.add_handler(CommandHandler("cancel1", cancel))
app.add_handler(CommandHandler("video", video))
# Add message handler to handle regular messages
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

# Run the bot
app.run_polling()


""" 
#save_data_to_file(new_admin_data, "admin")
#save_data_to_file(new_redeem_data, "redeem")

#print(load_data_from_file("data"))
adminid=load_data_from_file("admin")
redeem_code=load_data_from_file("redeem")
data=load_data_from_file("data")
adminid.append("123")
adminid.append("1234")
save_data_to_file(adminid, "admin")         
id="5439903101"
key="username"
val="saimun"
update(id,key,val)
"""
#print(load_data_from_file("data")6

