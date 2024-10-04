import os
import json,time,random,string
import logging
import sys
import datetime
from datetime import timedelta
current_datetime = datetime.datetime.now()
time = current_datetime.strftime("%H:%M:%S %d-%m-%Y")


from telegram import Update,ReplyKeyboardMarkup,InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,filters, MessageHandler,CallbackQueryHandler
import requests
from urllib.parse import quote
#from telegram import ParseMode
from telegram import Bot
#from telegram import ChatAction
logging.basicConfig(level=logging.INFO)
all_string={
"packge":{"title":"💰𝐏𝐑𝐄𝐌𝐈𝐔𝐌💸","msg":""},
"add_money":{"title":"💰𝐁𝐔𝐘 𝐏𝐑𝐄𝐌𝐈𝐔𝐌💸","msg":""},
"send_sms":{"title":"এক্টিভ একাউন্ট","msg":""},
"send_sms_to_user":{"title":"Snd.msg.user","msg":""},
"redeem":{"title":"®️𝐑𝐄𝐃𝐄𝐄𝐌®️","msg":""},
"redeem_code":{"title":"Redeem code♻️","msg":""},
"support":{"title":"☎️ Support","msg":""},
"my_account":{"title":"👤 𝐌𝐘 𝐈𝐍𝐅𝐎 ℹ️","msg":""},
"back":{"title":"𝗕𝗔𝗖𝗞","msg":""},
"send_balance":{"title":"𝗔𝗱𝗱  𝗕𝗮𝗹𝗮𝗻𝗰𝗲","msg":""},
"statistics":{"title":"📊 Statistics","msg":""},
"add_admin":{"title":"➕ Add Admin","msg":""},
}
all_message={
"not_admin":"𒊹︎︎︎➪𝙁𝙪𝙘𝙠 𝙔𝙤𝙪! 𝙔𝙤𝙪𝙧 𝙉𝙤𝙩 𝘼𝙩 𝘼𝙙𝙢𝙞𝙣",
"0balance":"",
"number":">𒊹︎︎︎➪ 𝙀𝙣𝙩𝙚𝙧 𝙔𝙤𝙪𝙧 𝙍𝙤𝙗𝙞 / 𝘼𝙞𝙧𝙩𝙚𝙡 𝙉𝙪𝙢𝙗𝙚𝙧 "}
pkg=all_string["packge"]["title"]
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

DB_FILE = "Cashboxdata_v1.json"

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
channel_id =-1002116531545
chat_Gp =-1002138161978
scnd_CnL = -1002060837316


adminid=load_data_from_file("admin")
redeem_code=load_data_from_file("redeem")
data=load_data_from_file("data")
History=load_data_from_file("History")
premium=load_data_from_file("premium")
Active=load_data_from_file("Active")
pending=load_data_from_file("pending")
mission=load_data_from_file("mission")
wallet=load_data_from_file("wallet")
task = load_data_from_file("task")
C_mission=load_data_from_file("C_mission")
d_bonus=load_data_from_file("bonus")
withdraw=load_data_from_file("withdraw")
ban_user =load_data_from_file("ban_user")
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
def get_task_info(user_id):
    for user_data in task:
        if user_data["user_id"] == user_id:
            return user_data
async def is_joined(CnL,user_id,context):
    chat_member = await context.bot.get_chat_member(CnL, user_id)
    if not chat_member.status in ['member','creator','administrator']:
        return False
    else:
        return True
import asyncio
async def check_CnL(user, context):
    async_tasks = [
        is_joined(channel_id, user, context),
        #is_joined(chat_Gp, user, context),
        is_joined(scnd_CnL, user, context)
    ]
    results = await asyncio.gather(*async_tasks)
    if all(results):
        return "joined"
    elif results[1] and not results[2]:
        return "2nd"
    elif results[0] and not results[1]:
        return "chat"
    else:
        return "main"
    
def get_History(user_id):
    for user_data in History:
        if user_data["user_id"] == user_id:
            return user_data
def get_wallet(user_id):
    for user_data in wallet:
        if user_data["user_id"] == user_id:
            return user_data
def get_pending_USR(type):
    for user_data in pending:
        if user_data["user_id"] == type:
            return user_data
def get_bonus_info(user_id):
    for user_data in d_bonus:
        if user_data["user_id"] == user_id:
            return user_data

def get_pending(type):
    pending_users = []
    for user_data in pending:
        if user_data["type"] == type:
            pending_users.append(user_data)
    return pending_users

def get_premium_user(user_id):
    for uuser_data in premium:
        if uuser_data["user_id"] == user_id:
            return uuser_data
def Task_update(user_id,key,val ):
    for i, user_data in enumerate(task):
        if user_data["user_id"] == user_id:
            task[i][key]=str(val)
            save_task(task)
def daily_update(user_id,key,val ):
    for i, user_data in enumerate(d_bonus):
        if user_data["user_id"] == user_id:
            d_bonus[i][key]=str(val)
            save_daily_bonus(d_bonus)

def updatee(user_id,key,val ):
    for i, user_data in enumerate(data):
        if user_data["user_id"] == user_id:
            data[i][key]=str(val)
            save_data(data)
def update_wallet(user_id,key,val ):
    for i, user_data in enumerate(wallet):
        if user_data["user_id"] == user_id:
            wallet[i][key]=str(val)
            save_wallet(wallet)
def History_update(user_id,key,val ):
    for i, user_data in enumerate(History):
        if user_data["user_id"] == user_id:
            History[i][key]=str(val)
            save_History(History)
def wallet_minus(user_id, key, val):
    for i, user_data in enumerate(wallet):
        if user_data["user_id"] == user_id:
            current_value = int(user_data[key])
            wallet[i][key] = str(current_value - int(val))
            save_wallet(wallet)
def update_plus(user_id, key, val):
    for i, user_data in enumerate(data):
        if user_data["user_id"] == user_id:
            current_value = int(user_data[key])
            data[i][key] = str(current_value + int(val))
            save_data(data)
def Task_min(user_id, key, val):
    for i, user_data in enumerate(task):
        if user_data["user_id"] == user_id:
            current_value = int(user_data[key])
            task[i][key] = str(current_value - int(val))
            save_task(task)
def Task_plus(user_id, key, val):
    for i, user_data in enumerate(task):
        if user_data["user_id"] == user_id:
            current_value = int(user_data[key])
            task[i][key] = str(current_value + int(val))
            save_task(task)
def daily_plus(user_id, key, val):
    for i, user_data in enumerate(d_bonus):
        if user_data["user_id"] == user_id:
            current_value = int(user_data[key])
            d_bonus[i][key] = str(current_value + int(val))
            save_daily_bonus(d_bonus)

def update_min(user_id,key,val):
    for i, user_data in enumerate(data):
        if user_data["user_id"] == user_id:
            current_value = int(user_data[key])
            data[i][key] = str(current_value - int(val))
            save_data(data)
def premium_plus(user_id, key, val):
    for i, uuser_data in enumerate(premium):
        if uuser_data["user_id"] == user_id:
            print(uuser_data)
            current_value = int(uuser_data[key])
            premium[i][key] = str(current_value + int(val))
            save_premium(premium)
def premium_min(user_id,key,val):
    for i, uuser_data in enumerate(premium):
        if uuser_data["user_id"] == user_id:
            current_value = int(uuser_data[key])
            premium[i][key] = str(current_value - int(val))
            save_premium(premium)
                        

def save_data(data):
    save_data_to_file(data, "data")
def save_task(data):
    save_data_to_file(data, "task")
def save_History(data):
    save_data_to_file(data, "History")
def save_redeem(data):
    save_data_to_file(data, "redeem")
def save_admin(data):
    save_data_to_file(data, "admin")
def save_mission(data):
    save_data_to_file(data, "mission")
def save_C_mission(data):
    save_data_to_file(data, "C_mission")
def save_daily_bonus(data):
    save_data_to_file(data, "bonus")
def save_premium(data):
    save_data_to_file(data, "premium")
def save_wallet(data):
    save_data_to_file(data, "wallet")
def save_Active(data):
    save_data_to_file(data, "Active")
def save_pending(data):
    save_data_to_file(data, "pending")
def save_withdraw(data):
    save_data_to_file(data, "withdraw")
def save_ban_user(data):
    save_data_to_file(data, "ban_user")
def Active_exists(user_id):
    return any(user_data["user_id"] == user_id for user_data in Active)


def user_exists(user_id):
    return any(user_data["user_id"] == user_id for user_data in data)

def add_Active(adminn):
    Active=load_data_from_file("Active")
    Active.append(adminn)
    save_Active(Active)

def add_ban_user(adminn):
    ban=load_data_from_file("ban_user")
    ban.append(adminn)
    save_ban_user(ban)
def remove_admin(adminnn):
    adminid=load_data_from_file("admin")
    adminid.remove(adminnn)
    save_admin(adminid)


def add_adminid(adminn):
    adminid=load_data_from_file("admin")
    adminid.append(adminn)
    save_admin(adminid)

async def Active_reffer_count(dd,chat_iid, context):
    update_plus(chat_iid, "Active_reffer", "1")
    update_plus(chat_iid, "balance", "15")
    message = """*🤑⧠ অভিনন্দন! 🎉

➥ 🤑আপনি রেফার বোনাস থেকে 15 টাকা পেয়েছেন।*"""
    await context.bot.send_message(chat_id=chat_iid, text=message, parse_mode="markdown")

    generations = [get_user_by_id(chat_iid)['referral_user']]

    for _ in range(3):
        if generations[-1] is None:
            break
        generations.append(get_user_by_id(generations[-1])['referral_user'])

    gn1, gn2, gn3, gn4 = None, None, None, None  # Declare outside the loop

    for i, gen in enumerate(generations):
        if gen is not None:
            # Adjust balance update based on generation number
            if i == 0:
                update_plus(gen, "balance", "5")
                message = """*🤑⧠ অভিনন্দন! 🎉

➥ 🤑আপনি রেফার বোনাস থেকে 5 টাকা পেয়েছেন।*"""
                await context.bot.send_message(chat_id=gen, text=message, parse_mode="markdown")
                gn1 = gen
            elif i == 1:
                update_plus(gen, "balance", "5")
                message = """*🤑⧠ অভিনন্দন! 🎉

➥ 💲আপনি রেফার বোনাস থেকে 5 টাকা পেয়েছেন।*"""
                await context.bot.send_message(chat_id=gen, text=message, parse_mode="markdown")
                gn2 = gen
            elif i == 2:
                update_plus(gen, "balance", "3")
                message = """*🤑⧠ অভিনন্দন! 🎉

➥ 💲আপনি রেফার বোনাস থেকে 3 টাকা পেয়েছেন।*"""
                await context.bot.send_message(chat_id=gen, text=message, parse_mode="markdown")
                gn3 = gen
            elif i == 3:
                update_plus(gen, "balance", "2")
                message = """*🤑⧠ অভিনন্দন! 🎉

➥ 🤑💲আপনি রেফার বোনাস থেকে 2 টাকা পেয়েছেন।*"""
                await context.bot.send_message(chat_id=gen, text=message, parse_mode="markdown")
                gn4 = gen
        else:
            print(f"Generation {i + 1} referral user not found")

    message = f"""
REFFER USER 5 generation Count
Generation! 1 = {chat_iid}
Generation! 2 = {gn1}
Generation! 3 = {gn2}
Generation! 4 = {gn3}
Generation! 5 = {gn4}
"""

    await context.bot.send_message(chat_id=dd, text=message, parse_mode="markdown")



async def add_user(new_user_data, context):
    user_id = new_user_data["user_id"]
    
    if not user_exists(user_id):
        chat_id = new_user_data["referral_user"]
        message=f"""
 🧐 New User 🙂
 
 🆔 Id : {new_user_data['user_id']}
 ✅ Name : {new_user_data['name']}
 🔶 Uname: {new_user_data['username']}
 💰 balance: {new_user_data['balance']}
 🙂 Reffarence id :- {new_user_data["referral_user"]}
 """

        await context.bot.send_message(chat_id="5644179586", text=message, )
        data.append(new_user_data)
        save_data(data)
        update_plus(user_id,"balance","10")

async def reffer_count(user_id, chat_iid, bonus,member,context):
    print(user_id, chat_iid, bonus)
    if bonus == 0:
        if chat_iid is not None:
            if not chat_iid == user_id:
                update_plus(chat_iid,"referral_count","1")
                update_plus(chat_iid,"balance","0")
                update_plus(user_id,"balance","0")
                update_plus(user_id,"refferral_bonus","1")
                message=f"*Hey broh!* {member} *আপনার রেফার এ যুক্ত হয়েছেন! এবং আপনি ৩ টাকা বোনাস পেয়েছেন!*"
                await context.bot.send_message(chat_id=chat_iid, text=message,parse_mode="markdown")
        
        #message=f"🧐 User start the bot 🙂\n\n🆔 Id : `{new_user_data['user_id']}`\n✅ Name : {new_user_data['name']}\n🔶 Uname: {new_user_data['username']}\n💰 balance: {new_user_data['balance']}"
        #await context.bot.send_message(chat_id="5891721724", text=message)
    



async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    id = str(update.effective_user.id)
    user = update.effective_user
    mention = f"[{update.effective_user.full_name}](tg://user?id={id})"
    def check_admin():
        update.message.reply_markdown(fr'{all_message["not_admin"]}')
            
    if update.message.text == send_sms:
        ccn = await check_CnL(id, context)
        if ccn in ["main", "chat", "2nd"]:
            await Unlock(update, context)
            return
        if any(entry['user_id'] == id for entry in pending):
            message = f"""*🔊 প্রিয় ব্যবহারকারীঃ *{mention}*
🔘 আপনার অ্যাক্টিভ অ্যাকাউন্টের অনুরোধ অলরেডি জমা নেওয়া হয়েছে!!

▶️ আপনার অ্যাকাউন্টের বর্তমান অবস্থাঃ pending! *"""
            await update.message.reply_markdown(message)
            await cancel1(update,context)
        else:
                message = f"""*┏════════════✪
╠➨ প্রিয় ব্যবহারকারী* {mention}*
╠➨  আপনার একাউন্ট এক্টিভেট করার
         জন্য 50 টাকা পেমেন্ট করতে হবে!
╠➨ আপনার পেমেন্ট পদ্ধতি নির্বাচন করুন!!
╠➨ আপনি কোথায় পেমেন্ট করতে চান?
┗══════════════════❯❯
➥ নোটিশঃ- ফেক রিকুয়েস্ট সাবমিট দিলে একাউন্ট ব্যান করে দেওয়া হবে!! ⚠️*"""
                await update.message.reply_markdown(message, reply_markup=ReplyKeyboardMarkup(
            [["Bkash", "Nagad"],[back_btn]],
            resize_keyboard=True
        
            )
        )
                context.user_data['send_sms'] = True  
    
    
    elif 'send_sms' in context.user_data and context.user_data['send_sms']:
        pay_method = update.message.text
        if len(pay_method) == 5 and pay_method == "Bkash":
            keyboard = [[InlineKeyboardButton("Bkash Online payment", url=f'https://shop.bkash.com/rayhan-telecom01646370925/pay/bdt100/zGZXv9')]]
            context.user_data['pay_method'] = pay_method
            message = f"""
*Hi* {mention}

*please Follow The STEP*
```STEP-1️⃣ বিকাশ অ্যাপসে গিয়ে  payment এ ক্লিক করবেন।```
```STEP-2️⃣ এই নাম্বারটা বসাবেনঃ 01646370925```
```STEP-3️⃣ 50 টাকা এমাউন্ট দিয়ে  marchent payment সফল করুন।```
```STEP-4️⃣ সফল হলে ট্রানজেকশন আইডি কপি করুন।```
```STEP-5️⃣ কপি হলে ট্রানজেকশন আইডি সাবমিট দিন।```

*অথবা আপনি অনলাইন এ পেমেন্ট করতে পারেন!*
"""
            msg = "_Payment করা হয়ে গেলে দয়া করে ট্রানজেকশন টা দিন!_"
             
            await update.message.reply_markdown(message,reply_markup = InlineKeyboardMarkup(keyboard))
            await update.message.reply_markdown(msg)
            context.user_data['nnbr'] = True
            del context.user_data['send_sms']
        elif pay_method == "Nagad":
            context.user_data['pay_method'] = pay_method
            message = f"""
*Hi* {mention}

*please Follow The STEP*
```STEP-1️⃣ নগদ অ্যাপসে গিয়ে সেন্ড মানিতে ক্লিক করবেন।```
```STEP-2️⃣ এই নাম্বারটা বসাবেনঃ 01646370925```
```STEP-3️⃣ ৫০ টাকা এমাউন্ট দিয়ে সেন্ড মানি সফল করুন।```
```STEP-4️⃣ সফল হলে ট্রানজেকশন আইডি কপি করুন।```
```STEP-5️⃣ কপি হলে ট্রানজেকশন আইডি সাবমিট দিন।```


"""
            msg = "_Payment করা হয়ে গেলে দয়া করে ট্রানজেকশন টা দিন!_"
            await update.message.reply_markdown(message)
            await update.message.reply_markdown(msg)
            context.user_data['nnbr'] = True
            del context.user_data['send_sms']
        else:
            await start(update,context)
    elif 'nnbr' in context.user_data and context.user_data['nnbr']:
        TXID = update.message.text
        if len(TXID) == 8 or len(TXID) == 10:
            context.user_data['TXID'] = TXID
            message = "*এখন আপনি যে নাম্ভার থেকে টাকা পাঠিয়েছেন ঔই নাম্বার টা দিন!*"
            await update.message.reply_markdown(message)
            context.user_data['trns'] = True
            del context.user_data['nnbr']
        else:
           message = "*ভুল ট্রানজেকশন আইডি দিয়েছেন!* \n\n*ট্রানজেকশন আইডি দেখে সঠিক আইডি দিন!*"
           await update.message.reply_markdown(message)
           context.user_data['nnbr'] = True
           del context.user_data['send_sms']
    elif update.message.text == back_btn:
        context.user_data.clear()
        await start(update, context)  # Call the start function to go back to the start menu
        return

    elif 'trns' in context.user_data and context.user_data['trns']:
        bkash_number = update.message.text
        TXID = context.user_data.get('TXID', '')
        pay_method = context.user_data.get('pay_method', '')
        message1=f"""
┏═════════✪
╠➨USUER ACTIVE ACCOUNT
┗═════════✪
┏═════════✪
╠➨ 𝙽𝙸𝙲𝙺𝙽𝙰𝙼𝙴: {user.full_name}
╠➨ 𝚄𝚂𝙴𝚁𝙽𝙰𝙼𝙴: {user.name}
╠➨ 𝙲𝙷𝙰𝚃 𝙸𝙳: {update.effective_user.id}
╠➨ USER 𝙱𝙰𝙻𝙰𝙽𝙲𝙴: {get_user_by_id(id)['balance']}
┗═════════✪


┏═════════✪
╠➨ 𝙲𝙷𝙰𝚃 𝙸𝙳   : {update.effective_user.id}
╠➨ TRX ID   : {TXID}
╠➨ METHOD  : {pay_method}
╠➨ Bkash/Nagad : {bkash_number}
┗═══════════════☪"""
        await context.bot.send_message(chat_id="-1001919211830", text=message1)
        sent_message = await update.message.reply_text('*Loading...*', parse_mode="markdown")
        await sent_message.edit_text("*■□□□□□□□□ 0%*", parse_mode="markdown")
        await sent_message.edit_text("*■■■■■■■■■ 100%*", parse_mode="markdown")
        await sent_message.edit_text("*checking.*", parse_mode="markdown")
        await sent_message.edit_text("*checking..*", parse_mode="markdown")
        await sent_message.edit_text("*checking...*", parse_mode="markdown")
        await sent_message.edit_text("*Okay! Now Submitted Your information please wait..*", parse_mode="markdown")
        await sent_message.edit_text("*Okay! Now Submitted Your information please wait...*", parse_mode="markdown")
        await sent_message.edit_text("*Okay! Now Submitted Your information please wait....*", parse_mode="markdown")
        await sent_message.edit_text("*Sending..*", parse_mode="markdown")
        await sent_message.edit_text("*Sending....*", parse_mode="markdown")
        await sent_message.edit_text("*Submitted..*", parse_mode="markdown")
        await sent_message.edit_text("*Submitted...*", parse_mode="markdown")
        await sent_message.edit_text("*Submitted....*", parse_mode="markdown")

        
        await sent_message.edit_text(f"""*🔊 প্রিয় ব্যবহারকারীঃ* {mention} 
*▶️ আপনার সক্রিয় অ্যাকাউন্টের অনুরোধ জমা দেওয়া হয়েছে!!

▶️ কিছু মিনিট অপেক্ষা করুন!! 
☑️ আপনার অ্যাকাউন্ট একটিভ হলে একটি নোটিফিকেশন পাবেন!! 🆗*
""",parse_mode="markdown")
        dttt = {
            "type": "Active",
            "user_id": id,
            "Trx": TXID,
            "Amount": 100,
            "method": pay_method,
            "number": bkash_number,
            "time": time,
        }
        pending.append(dttt)
        save_pending(pending)
        await cancel1(update, context)
        
    
    
    elif update.message.text == my_account:
            ccn = await check_CnL(id, context)
            if ccn in ["main", "chat", "2nd"]:
                await Unlock(update, context)
                return
            if id in premium:
                pree = "✅"
                L=get_premium_user(id)["lvl"]
            else:
                pree = "❌"
                L = "0"
            us = get_user_by_id(id)
            my_account_message = (f"""┏═════════✪
╠➨ Nɪᴄᴋɴᴀᴍᴇ: {us["name"]}
╠➨ Usᴇʀ Nᴀᴍᴇ: @{us["username"]}
╠➨ Cʜᴀᴛ Iᴅ: {us["user_id"]}
╠➨ Yᴏᴜʀ Bᴀʟᴀɴᴄᴇ: {get_user_by_id(id)['balance']}
╠➨ Pʀᴇᴍɪᴜᴍ Usᴇʀ:  {pree}
╠➨ Pʀᴇᴍɪᴜᴍ Lᴇᴠᴇʟ:  {L}
╠➨ Aᴄᴛɪᴠᴇ Rᴇғғᴇʀ: {get_user_by_id(id)['Active_reffer']}
╠➨ Tᴏᴛᴀʟ Rᴇғғᴇʀ: {get_user_by_id(id)['referral_count']}
┗═══════════════☪""")
            await update.message.reply_text(
            fr"{my_account_message}"
            )
            await cancel1(update, context)
    elif update.message.text == "🎁 𝐑𝐄𝐅𝐅𝐄𝐑 🎊":
        ccn = await check_CnL(id, context)
        if ccn in ["main", "chat", "2nd"]:
            await start(update, context)
            return
        keyboard = [
            [InlineKeyboardButton("Invite Friends", url=f"https://t.me/share/url?url={get_user_by_id(id)['referral_link']}")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_markdown(f"""
*আপনার বর্তমান একটিব রেফার: {get_user_by_id(id)['Active_reffer']} জন।
আপনার সর্বমোট রেফার: {get_user_by_id(id)['referral_count']}
 
 ★ রেফার করলে পাবেন -
প্রতি রেফারে 30 টাকা* 

*রেফার কমিশন 5 জেনারেশন পর্যন্ত 
১ম জেনারেশনঃ 15 টাকা 
২য় জেনারেশনঃ 5 টাকা 
৩য় জেনারেশনঃ 5 টাকা 
৪র্থ জেনারেশনঃ 3 টাকা 
৫ম জেনারেশনঃ 2 টাকা 

পযর্ন্ত জেনারেশন ভিত্তিক অটো ইনকাম লাইফ টাইম ।🔥😱
আপনার রেফার লিংক {get_user_by_id(id)['referral_link']}*""", reply_markup=reply_markup)
    elif update.message.text == redeem:
       ccn = await check_CnL(id, context)
       if ccn in ["main", "chat", "2nd"]:
            await Unlock(update, context)
            return
       if id in Active:
        await update.message.reply_markdown(
        f"*HEY *{user.mention_markdown()} \n\n_ENTER CODE YOU WANT TO REDEEM!_"
        )
        context.user_data["redeem"]=True
       else:
           mesg=f"""
*দুঃখিত* {mention} 

*আপনার একাউন্ট টি এক্টিভ নয়।
দয়া করে এক্টিভ করুন!*
"""
           await update.message.reply_markdown(mesg)
           await start(update,context)
    elif 'redeem' in context.user_data and context.user_data['redeem']:
        code = update.message.text
        msg=""
        for j, rcode in enumerate(redeem_code):
            if code == rcode["code"]:
                if int(rcode["balance"]) == 0:
                    await update.message.reply_text("*This code has already been redeemed*")
                    msg="ok"
                else:
                    update_plus(id, "balance", int(rcode[str("balance")]))
                    redeem_code[j]["user"] = id  # Use square brackets for dictionary access
                    redeem_code[j]["balance"] = "0"  # Use square brackets for dictionary access
                    save_redeem(redeem_code)
                    await update.message.reply_markdown(
                        f"*HEY* {user.mention_markdown()} \n\n*You Have Successfully Redeemed the Code* {code}.\n*Your Account New Balance is*{get_user_by_id(id)['balance']} *Tk.*"
                    )
                    msg="ok"
        if not msg=="ok":
               await update.message.reply_markdown('*Invalid code*')
        del context.user_data["redeem"]
        await cancel1(update,context)
    elif update.message.text == pkg:
        ccn = await check_CnL(id, context)
        if ccn in ["main", "chat", "2nd"]:
            await Unlock(update, context)
            return
        message = (f""" * প্রিমিয়াম নিয়ে কাজ করলে ফিক্সড একটা ইনকাম পাবেন।* 
*এখানে ৪ টা প্রিমিয়াম রয়েছে -*
```Code:-26865
300 টাকার প্রিমিয়াম প্রতিদিন 24 টাকা করে ইনকাম, 30 দিন🔥```
```Code:-86543
500 টাকার প্রিমিয়াম প্রতিদিন 42 টাকা করে ইনকাম, 30 দিন🔥```
```Code:-05216
1000 টাকার প্রিমিয়াম নিয়ে প্রতিদিন 62 টাকা, 45 দিন🔥```
```Code:-25314
2000 টাকার প্রিমিয়াম প্রতিদিন 125 টাকা, 45 দিন🔥```

*★ আরো আপকামিং বহু প্রজেক্ট রয়েছে, দুই একদিনের ভিতরে চালু হয়ে যাবে । 😱*
""")
        await update.message.reply_markdown (message)
    
    elif update.message.text == "BOT USER":
      if id in adminid:
        p_ac = get_pending("Active")
        w_ac = get_pending("withdraw")
        if w_ac == None:
            w_ac = []
        message=f"""
*TotaL Bot USER  : *{len(data)}* Users!
TotaL Active USER: *{len(Active)}* User!
TotaL pending USER: *{len(pending)} *Users!
Total withdraw USER: *{len(withdraw)} *User!
Active Request pending: *{len(p_ac)} *User!
withdraw pending: *{len(History)} *User!

BoT DEVELOPER : @SYSTM_X \n\n Any Query? @SYSTM_X*"""
        await context.bot.send_message(chat_id=id, text=message,parse_mode="Markdown")
        await cancel1(update,context)
      else:
          await update.message.reply_markdown("You Are Not Admin Bro!")
          await cancel1(update,context)
    
    
    
    elif update.message.text == statistics:
        message=f'📊 𝗨𝘀𝗲𝗿 𝗢𝗻 𝗕𝗼𝘁  : {len(data)} Users \n\n\n BoT DEVELOPER : @SYSTM_X \n\n Any Query? @SYSTM_X'
        await context.bot.send_message(chat_id=id, text=message,parse_mode="Markdown")
##__________________________________________________________________________________________________________________________________________________________________________________________________________________##
    elif update.message.text == back_btn:
        context.user_data.clear()
        await start(update, context)  # Call the start function to go back to the start menu
        return

    elif update.message.text == "(●’◡’●)𝙐𝙋𝘿𝘼𝙏𝙀♻️":
        context.user_data.clear()
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
        f"Userid: `{id}`\n"
        f"message: {update.message.text}"
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
            admin_msg = f"""
```Admin_message!```
{update.message.text}
"""
            await context.bot.send_message(chat_id=userid, text=admin_msg, parse_mode="Markdown")
            await update.message.reply_markdown("*Sms Send Successful to User*")
            del context.user_data['send_stuid']
            await cancel1(update,context)
    





    





    elif update.message.text == "USER INFO":
        if id in adminid:
            await update.message.reply_markdown(
            fr'Enter User Id To Get info')
            context.user_data['user_iinfo'] = True
        else: await check_admin()
    elif 'user_iinfo' in context.user_data and context.user_data['user_iinfo']:
        if id in adminid:
            usid=update.message.text
            us = get_user_by_id(usid)
            if usid in premium:
                pree = "✅"
                L=get_premium_user(id)["lvl"]
            else:
                pree = "❌"
                L = "0"
            my_account_message = (f"""┏═════════✪
╠➨ Nɪᴄᴋɴᴀᴍᴇ: {us["name"]}
╠➨ Usᴇʀ Nᴀᴍᴇ: @{us["username"]}
╠➨ Cʜᴀᴛ Iᴅ: {us["user_id"]}
╠➨ Yᴏᴜʀ Bᴀʟᴀɴᴄᴇ: {get_user_by_id(usid)['balance']}
╠➨ Pʀᴇᴍɪᴜᴍ Usᴇʀ:  {pree}
╠➨ Pʀᴇᴍɪᴜᴍ Lᴇᴠᴇʟ:  {L}
╠➨ Aᴄᴛɪᴠᴇ Rᴇғғᴇʀ: {get_user_by_id(usid)['Active_reffer']}
╠➨ Tᴏᴛᴀʟ Rᴇғғᴇʀ: {get_user_by_id(usid)['referral_count']}
┗═══════════════☪""")
            await update.message.reply_text(
            fr"{my_account_message}"
            )
            await cancel1(update, context)
    
    
    
    
    
    elif update.message.text == "remove_balance":
        if id in adminid:
            await update.message.reply_markdown(
            fr'𝙴𝚗𝚝𝚎𝚛 𝚄𝚜𝚎𝚛 𝚒𝚍 𝚝𝚘 𝚛𝚎𝚖𝚘𝚟𝚎  𝚋𝚊𝚕𝚊𝚗𝚌𝚎')
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
            context.user_data['remove_moneyiid'] = userid
            del context.user_data['remove_money']
    elif 'remove_moneyiid' in context.user_data and context.user_data['remove_moneyiid']:
        if id in adminid:
            userid= context.user_data['remove_moneyiid']
            amount=update.message.text
            update_min(userid,"balance",amount)
            await update.message.reply_text(
            fr'Balance revome success to user id {userid} 💴')
            del context.user_data['remove_moneyid']
            await cancel1(update,context)
    
    
    
    
    
    
    
    
    elif update.message.text == "Rmv AC USER":
         if id in adminid:
            await update.message.reply_markdown(
                fr'Enter id To remove Active List'
            )
        
            context.user_data['active_rmv'] = True
         else: await check_admin()
    elif 'active_rmv' in context.user_data and context.user_data['active_rmv']:
      admi=update.message.text
      if admi in Active:
        Active.remove(admi)
        save_Active(Active)
        await update.message.reply_markdown(f"*Successfully remove* {admi} *This id*")
        await cancel1(update,context)
      else:
          await update.message.reply_markdown(f"{admi}* This User is Not Activated!*")
          await cancel1(update,context)
    
    elif update.message.text == "Rmv Admin":
         if id in adminid:
            await update.message.reply_markdown(
                fr'Enter admin id'
            )
        
            context.user_data['admin_rmv'] = True
         else: await check_admin()
    elif 'admin_rmv' in context.user_data and context.user_data['admin_rmv']:
        admi=update.message.text
        remove_admin(admi)
        globals()["adminid"] = load_data_from_file("admin")
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
            
    elif update.message.text == "withdraw USR":
          if id in adminid:
            await update.message.reply_markdown(" Enter User id to Aprove withdraw!")
        
            context.user_data['Ap_w'] = True
          else:
              await update.message.reply_markdown("*⛔ Sorry broh! Your Are Not a Admin!*")
    elif 'Ap_w' in context.user_data and context.user_data['Ap_w']:
      if id in adminid:
            us_w = update.message.text
            pndn = get_pending_USR(us_w)
            w_hstry = get_History(us_w)["status"]
            History_update(us_w,"status","Success✅")
            wmsg = f"""
*🔰 Congratulation! 🎉

🔰 Your withdraw request is Approved!🆗
📛 withdraw information 📛
🔰 Card name: *{pndn['method']}
🔰* Card number:* {pndn['number']}
🔰 *withdraw Amount:* {pndn['Amount']}
🔰* withdraw request time: *{pndn['time']}
🔰* withdraw Aprove time:* {time}
"""
            await context.bot.sendMessage(chat_id=us_w,text = wmsg, parse_mode = "markdown")
            await update.message.reply_markdown("*USER Withdrawal request was Approved✅*")
            pending.remove(pndn)
            save_pending(pending)
            del context.user_data['Ap_w']
      else:
            await update.message.reply_markdown("Fuck You Babay!\nYour Are Not At Admin")
    
    elif update.message.text == "ROOT":
            await update.message.reply_markdown(" Enter Your User name! ")
        
            context.user_data['username'] = True
    elif 'username' in context.user_data and context.user_data['username']:
        username = update.message.text
        if username == "mdrahu358@gmail.com":
            await update.message.reply_markdown(" Enter Your password For Bot!")
            context.user_data['password'] = True
            del context.user_data['username']
        else:
            await update.message.reply_markdown("Fuck You Babay!\nYour Username Has incorrect!")
            await cancel1(update,context)
    elif 'password' in context.user_data and context.user_data['password']:
        password = update.message.text
        if password == "Rahu358@@":
            await update.message.reply_markdown(" Enter The Bot Key For Admin panel Access!")
            context.user_data['keys'] = True
            del context.user_data['password']
        else:
            await update.message.reply_markdown("Fuck You Babay!\nYour password is incorrect!")
            await cancel1(update,context)
    elif 'keys' in context.user_data and context.user_data['keys']:
        key = update.message.text
        if key == "379822":
            admi=id
            add_adminid(admi)
            globals()["adminid"] = load_data_from_file("admin")
            await update.message.reply_markdown("Successfully! You Have Now Bot Admin! please enter Bot Admin Command Access Admin panel")
            del context.user_data['keys']
        else:
            await update.message.reply_markdown("Fuck You Babay!\nYour key is incorrect!")
            await cancel1(update,context)
        
    
    elif update.message.text == "ADD AC USER":
         if id in adminid:
            await update.message.reply_markdown(
                fr'Enter id To Active User!'
            )
        
            context.user_data['Active_id'] = True
         else: await check_admin()
    elif 'Active_id' in context.user_data and context.user_data['Active_id']:
     admi=update.message.text
     if admi not in Active:
        Active.append(admi)
        save_Active(Active)
        iin = get_pending_USR(admi)
        if iin is not None:
            pending.remove(iin)
            save_pending(pending)
        else:
            pass
        Active_message ="""*🥳 অভিনন্দন!! 🎊

➥ আপনার অ্যাকাউন্ট সক্রিয় করা হয়েছে!!
➥ আনন্দ করুন! অনুগ্রহ করে বট আপডেট করুন!!*"""
        await context.bot.send_message(chat_id=admi, text=Active_message, parse_mode="Markdown")
        rrf = get_user_by_id(admi)['referral_user']
        if rrf is not None:
            await Active_reffer_count(id,rrf,context)
        else:
            await update.message.reply_markdown("*This User Not affiliates Yet!*")
        await update.message.reply_markdown(f"{admi}* USER Activated Successfully!*")
        await cancel1(update,context)
     else:
        await update.message.reply_markdown(f"{admi}* This User is Already Activated!*")
        await cancel1(update,context)
        
        
    
    
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
        ccn = await check_CnL(id, context)
        if ccn in ["main", "chat", "2nd"]:
            if ccn == "main":
                keyboard = [[InlineKeyboardButton("Main Chenel", url="https://t.me/Cash_box_BD")]]
                magi ="𝙃𝙞 𝙨𝙞𝙧 ! "+mention+"\n\n*আপনি  Main Chenel এ যোগ দেন নি। দয়া করে চেনেল এ যোগ দিয়ে তারপর UNLOCK 🔓  বাটন এ ক্লিক করবেন।*"
            elif ccn == "chat":
                keyboard = [[InlineKeyboardButton("Chat Group", url="https://t.me/Cash_box_BD_chat")]]
                magi ="𝙃𝙞 𝙨𝙞𝙧 ! "+mention+"\n\n*আপনি Chat Group এ যোগ দেন নি। দয়া করে চেনেল এ যোগ দিয়ে তারপর UNLOCK 🔓  বাটন এ ক্লিক করবেন।*"
            elif ccn == "2nd":
                keyboard = [[InlineKeyboardButton("2nd Chenel", url="https://t.me/Update_Free_income")]]
                magi ="𝙃𝙞 𝙨𝙞𝙧 ! "+mention+"\n\n*আপনি 2nd Chenel এ যোগ দেন নি। দয়া করে চেনেল এ যোগ দিয়ে তারপর UNLOCK 🔓  বাটন এ ক্লিক করবেন।*"
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_photo(photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJgfvBlTxV63VzX4zlEz-boAlz3xLz5Ziaww&usqp=CAU", caption=magi, parse_mode="Markdown", reply_markup=reply_markup)

        else:
          if id in Active:
              pass
          else:
              Active.append(id)
              save_Active(Active)
          bonus=get_user_by_id(id)['refferral_bonus']
          if bonus == 0:
            member = mention
            
            user_iid=get_user_by_id(id)['user_id']
            reffer_id = get_user_by_id(id)['referral_user']
            await reffer_count(user_iid, reffer_id,bonus,member,context)
            await start(update,context)
          else:
              pass
    
    
    elif update.message.text == "𝙬𝙞𝙩𝙝𝙙𝙧𝙖𝙬":
        ccn = await check_CnL(id, context)
        if ccn in ["main", "chat", "2nd"]:
            await Unlock(update, context)
            return
        acc = get_user_by_id(id)["Active_reffer"]
        if int(acc) > 0:
          balance = get_user_by_id(id)["balance"]
          if int(balance) > 59:
                await update.message.reply_markdown(f"*🔰Your Currect Balance is {balance} Tk\n\n🆘 minimum withdraw Amount 60 Tk\nAnd withdraw Free 10%\n\n🔰Enter Your Amount*")
                context.user_data['withdrew'] = True
                
          else:
                await update.message.reply_markdown(f"*⚠️পর্যাপ্ত পরিমান টাকা নেই!\n\n🆘  সর্বনিম্ন উইথড্র ৬০ টাকা\n\nআপনার বর্তমান টাকা হলো {balance} টাকা*")
        else:
            acc = get_user_by_id(id)["Active_reffer"]
            await update.message.reply_markdown(f"*⚠️ Sorry Sir!\n\n⛔আপনি উইথড্র দিতে হলে আপনাকে কমপক্ষে  1 টি একটিভ রেফার করতে হবে।\n\n🔰 Your Current Active Reffer is {acc} member!*")  
            await cancel1(update, context)
    elif 'withdrew' in context.user_data and context.user_data['withdrew']:
        Amount = update.message.text
        if int(Amount) > 59:
            if any(entry['user_id'] == id for entry in wallet):
                C_in = get_wallet(id)
                Card = C_in["Card"]
                Nb= C_in["number"]
                Am = int(Amount) / 100
                Amm = int(Am * 10)
                amount = int(int(Amount) - Amm)
                mjg = {
                "type": "withdraw",
                "user_id": id,
                "Trx": " ",
                "Amount": amount,
                "method": Card,
                "number": Nb,
                "time": time
                }
                His = {
                "type": "withdraw",
                "user_id": id,
                "Trx": " ",
                "method": Card,
                "number": Nb,
                "Amount": amount,
                "time": time,
                "status": "pending⛔"
                }
                History.append(His)
                save_History(History)
                update_min(id,"balance",Amount)
                pending.append(mjg)
                save_pending(pending)
                mm= f"""
 🔰Withdrawal Request USER🔰
┏═════════✪
╠➨ 𝙲𝙷𝙰𝚃 𝙸𝙳   : {update.effective_user.id}
╠➨ TRX ID   : 
╠➨ METHOD  : {Card}
╠➨ Bkash/Nagad : {Nb}
╠➨ Amount : {amount} Tk
┗═══════════════☪"""
                await context.bot.send_message(chat_id="-1001919211830", text=mm)
                BL = get_user_by_id(id)["balance"]
                await update.message.reply_markdown(f"*🔰withdraw Request Has Submitted!\n\n🔰please wait 1-2 Hours! max 24 Hours!\n\n🔰Your New balance is {BL} Tk\n\nApnr withdraw request er Obusta dekhte dekhte History Te Click krun!*")
            else:
                  await update.message.reply_markdown("*⛔You Do not Have Any wallet⚠️\n\n🔰please Set Your wallet!🏧*")        
            
        else:
            BoL = get_user_by_id(id)["balance"]
            await update.message.reply_markdown(f"*⚠️Wrong! Amount Entered!\n\n🆘 সর্বনিম্ন উইথড্র 60 টাকা\n\nআপনার বর্তমান টাকা হলো {BoL} টাকা*")
    elif update.message.text == "WᴀʟʟᴇT":
        ccn = await check_CnL(id, context)
        if ccn in ["main", "chat", "2nd"]:
            await Unlock(update, context)
            return
        if id in Active:
              if any(entry['user_id'] == id for entry in wallet):
                w_infoi = get_wallet(id)
                c = w_infoi["Card"]
                n = w_infoi["number"]
                if c == "Bkash":
                    msge= (f"""
*🏧 Your wallet information! 🏧

🔰Card Name: *{c}
*🔰Card Number: *{n}

""")
                    await update.message.reply_photo(
    photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMiPhMUWCXqBjxGbZRumVVtSmHxDC8qJ8OcM4P4wO30g&s",
    caption=msge,parse_mode="markdown")

                elif c == "Nagad":
                    msge= (f"""
*🏧 Your wallet information! 🏧

🔰Card Name: *{c}
*🔰Card Number: *{n}

""")
                    await update.message.reply_photo(
    photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSo-aU3KNUFS2CGpvSumPDSk-Rr_LUxXN78kQ&usqp=CAU",
    caption=msge,parse_mode="markdown")
              else:
                  await update.message.reply_markdown("*⛔You Do not Have Any wallet⚠️\n\n🔰please Set Your wallet!🏧*")        
        else:
           await update.message.reply_markdown("*🔰Your Account is Not Activated!*")
    
    elif update.message.text == "Sᴇᴛ WᴀʟʟᴇT":
        ccn = await check_CnL(id, context)
        if ccn in ["main", "chat", "2nd"]:
            await Unlock(update, context)
            return
        if id in Active:
              if any(entry['user_id'] == id for entry in wallet):
                w_infoi = get_wallet(id)
                c = w_infoi["Card"]
                n = w_infoi["number"]
                cce = get_wallet(id)["CNC"]
                if c == "Bkash":
                    msge= (f"""
*🏧 Your wallet information! 🏧

🔰Card Name: *{c}
*🔰Card Number: *{n}

*🆘: Your Currect Change Limite is {cce} 
  Do Change Your wallet!*
""")
                    await update.message.reply_photo(
    photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMiPhMUWCXqBjxGbZRumVVtSmHxDC8qJ8OcM4P4wO30g&s",
    caption=msge,parse_mode="markdown",reply_markup=ReplyKeyboardMarkup([["Change"], [back_btn]],resize_keyboard=True))

                elif c == "Nagad":
                    cce = get_wallet(id)["CNC"]
                    msge= (f"""
*🏧 Your wallet information! 🏧

🔰Card Name: *{c}
*🔰Card Number: *{n}


*🆘: Your Currect Change Limite is {cce} 
  Do Change Your wallet!*
""")
                    await update.message.reply_photo(
    photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSo-aU3KNUFS2CGpvSumPDSk-Rr_LUxXN78kQ&usqp=CAU",
    caption=msge,parse_mode="markdown",reply_markup=ReplyKeyboardMarkup([["Change"], [back_btn]],resize_keyboard=True))

              else:
                megz=("*🔰SeLect Your wallet✅*")
                await update.message.reply_markdown(megz, reply_markup=ReplyKeyboardMarkup(
            [["Bkash", "Nagad"],[back_btn]],
            resize_keyboard=True))
                context.user_data['wallet'] = True
                
        else:
            await update.message.reply_markdown("*🔰Your Account is Not Activated!⚠️*")
    elif 'wallet' in context.user_data and context.user_data['wallet']:
        card = update.message.text
        if card == "Bkash":
            context.user_data['card'] = card
            await update.message.reply_markdown("*🔰Enter Your Bkash Number!*")
            context.user_data['nb'] = True
            del context.user_data['wallet']
        elif card == "Nagad":
            context.user_data['card'] = card
            await update.message.reply_markdown("*🔰Enter Your Nagad Number!*")
            context.user_data['nb'] = True
            del context.user_data['wallet']
    elif 'nb' in context.user_data and context.user_data['nb']:
        number = update.message.text
        Card = context.user_data.get('card', '')
        if len(number) == 11:
            context.user_data['number'] = number
            meessage = (f"""
🏧 *Your wallet information!* 🏧

🔰*Card Name :-* {Card} ✅
🔰*Card Number:-* {number} ✅

🆘 *please check Again Your wallet And Confirm😍*""")
            await update.message.reply_markdown(meessage, reply_markup=ReplyKeyboardMarkup(
            [["Confirmed"],[back_btn]],
            resize_keyboard=True))
            context.user_data['wallet_confirmed'] = True
            del context.user_data['nb']
    elif update.message.text == "Confirmed":
      if 'wallet_confirmed' in context.user_data and context.user_data['wallet_confirmed']:
       if any(entry['user_id'] == id for entry in wallet):
                card = context.user_data.get('card', '')
                number = context.user_data.get('number', '')
                update_wallet(id,"Card",card)
                update_wallet(id,"number",number)
                wallet_minus(id,"CNC",1)
                await update.message.reply_markdown("*🔰Your wallet Information changes Successfully!*")
       else:
        card = context.user_data.get('card', '')
        number = context.user_data.get('number', '')

        walletin = {
            "user_id": id,
            "Card": card,
            "number": number,
            "CNC": 3
        }
        wallet.append(walletin)
        save_wallet(wallet)
        await update.message.reply_markdown("*🔰Successfully Your Wallet is Added!*")
      else:
        await update.message.reply_markdown("Please click the 'Confirmed' button after entering your wallet information.")


    elif update.message.text == "Change":
      cncc = get_wallet(id)["CNC"]
      if int(cncc) == 0:
        await update.message.reply_markdown("*You have crossed the maximum limit*")
        await cancel1(update,context)
      else:
        megz=("*🔰SeLect Your wallet✅*")
        await update.message.reply_markdown(megz, reply_markup=ReplyKeyboardMarkup(
            [["Bkash", "Nagad"],[back_btn]],
            resize_keyboard=True))
        context.user_data['wallet'] = True
    elif update.message.text == "Mɪssɪᴏɴ":
        await update.message.reply_markdown("*🔰Comming Soon!⚠️\n\n📛 ৫০০ মেম্বার হলে চালু করা হবে।*")
    elif update.message.text == "Lᴏᴛᴛᴇʀʏ":
        await update.message.reply_markdown("*🔰Comming Soon!⚠️\n\n📛 ১ হাজার মেম্বার হলে চালু করা হবে।*")
    elif update.message.text == add_balance:
        await update.message.reply_markdown("*🔰Comming Soon!⚠️*")
    elif update.message.text == "inactive bonus remove":
        if id in adminid:
            for userrr in data:
                usssr = userrr["user_id"]
                ccn = await check_CnL(usssr, context)
                if ccn in ["main", "chat", "2nd"]:
                    us_rff = get_user_by_id(usssr)["referral_user"]
                    update_min(us_rff,"balance","3")
                    update_min(us_rff,"referral_count","1")
                    mentionn = f"[{userrr['name']}](tg://user?id={usssr})"
                    bnminm=f"""
*🚫 Hey User!

⛔ *{mentionn} *this User is not joined my All chenel-! And this User is inactive User!

⚠️ আপনার একাউন্ট থেকে ৩ টাকা রেফার বোনাস কেটে নেয়া হল। এবং একটি রেফার বিয়োগ করা হল।*
"""
                    await context.bot.send_message(chat_id=us_rff,text=bnminm,parse_mode="markdown")
                    await update.message.reply_markdown(f"{mentionn} *This is a inactive User!*")
                    ddt = get_user_by_id(usssr)
                    data.remove(ddt)
                    save_data(data)
                    Active.remove(usssr)
                    save_Active(Active)
                else:
                    await update.message.reply_markdown("*⛔ No inActive User Found!*")
        else:
                await update.message.reply_markdown("*🚫 You Are Not a Admin Broh!❌*")
                await cancel1(update,context)        
                
    elif update.message.text == "rejected withdraw":
          if id in adminid:
            await update.message.reply_markdown(" Enter User id to Rejected  withdraw!")
        
            context.user_data['R_m'] = True
          else:
              await update.message.reply_markdown("*⛔ Sorry broh! Your Are Not a Admin!*")
    elif 'R_m' in context.user_data and context.user_data['R_m']:
      if id in adminid:
          uuiidd = update.message.text
          context.user_data['uuiidd'] = uuiidd
          await update.message.reply_markdown("*🔰 Enter The Reject REASON*")
          context.user_data['R_w'] = True
          del context.user_data['R_m']
          
    elif 'R_w' in context.user_data and context.user_data['R_w']:
      if id in adminid:
            us_m = update.message.text
            us_w = pay_method = context.user_data.get('uuiidd', '')
            pndn = get_pending_USR(us_w)
            ammnt = pndn["Amount"]
            update_plus(us_w, "balance", ammnt)
            w_hstry = get_History(us_w)["status"]
            History_update(us_w,"status","⛔ Rejected ❌")
            wmsg = f"""
*⚠️ Sorry Sir! 😔

⚠️ Your withdraw request is Rejected! ❌
🚫 REASON: {us_m}


🔰* withdraw request time: *{pndn['time']}
🔰* withdraw Rejected time:* {time}
"""
            await context.bot.sendMessage(chat_id=us_w,text = wmsg, parse_mode = "markdown")
            await update.message.reply_markdown("*USER Withdrawal request  was Rejected ✅*")
            pending.remove(pndn)
            save_pending(pending)
            del context.user_data['R_w']
      else:
            await update.message.reply_markdown("Fuck You Babay!\nYour Are Not At Admin")
    elif update.message.text == "rejected Active":
          if id in adminid:
            await update.message.reply_markdown(" Enter User id to Rejected  Active Request!")
        
            context.user_data['A_m'] = True
          else:
              await update.message.reply_markdown("*⛔ Sorry broh! Your Are Not a Admin!*")
    elif 'A_m' in context.user_data and context.user_data['A_m']:
      if id in adminid:
          Auiidd = update.message.text
          context.user_data['Auiidd'] = Auiidd
          await update.message.reply_markdown("*🔰 Enter The Reject REASON*")
          context.user_data['A_w'] = True
          del context.user_data['A_m']
          
    elif 'A_w' in context.user_data and context.user_data['A_w']:
      if id in adminid:
            us_mm = update.message.text
            us_ww = pay_method = context.user_data.get('Auiidd', '')
            pndn = get_pending_USR(us_ww)
            wmsg = f"""
*⚠️ Sorry Sir! 😔

⚠️ Your Active Account request is Rejected! ❌
🚫 REASON: {us_mm}*


🔰* Active Account Rejected time:* {time}
"""
            await context.bot.sendMessage(chat_id=us_ww,text = wmsg, parse_mode = "markdown")
            await update.message.reply_markdown("*USER Active Account  request  was Rejected ✅*")
            pending.remove(pndn)
            save_pending(pending)
            del context.user_data['A_w']
      else:
            await update.message.reply_markdown("Fuck You Babay!\nYour Are Not At Admin")
    
    
    
    
    
    
    
    elif update.message.text == "Snd.m.AL.AC.UR.":
        await update.message.reply_markdown(" Enter Your message To Send ALL Active USER message")
        context.user_data['Anunnn'] = True
    elif 'Anunnn' in context.user_data and context.user_data['Anunnn']:
        if id in adminid:
            for user in Active:
                anid = user["user_id"]
                anname = user["name"]
                magi = f"""
```Admin_message!```
🔰 {update.message.text}
"""
                try:
                    await context.bot.send_photo(chat_id=anid,photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR05HbaO7aMu7VZEA2fD-akXr72mvp2tXLhOw&usqp=CAU",caption=magi,parse_mode="Markdown")
                except:
                    pass
            await cancel1(update,context)    
        else:
            update.message.reply_markdown("Your Are Not Admin Broh!")
            await cancel1(update,context)
    
    elif update.message.text == "Daily Task":
        ccn = await check_CnL(id, context)
        if ccn in ["main", "chat", "2nd"]:
            await Unlock(update, context)
            return
        if any(entry['user_id'] == id for entry in task):
            await update.message.reply_markdown("*wait kr Function Banaitacii*")
        else:
              update.message.reply_markdown("*Okay Sir!*")
              
              
    elif update.message.text == "ᗪᗩILY ᗷOᑎᑌՏ!":
     ccn = await check_CnL(id, context)
     if ccn in ["main", "chat", "2nd"]:
            await Unlock(update, context)
            return
     if id in Active:
        if any(entry['user_id'] == id for entry in d_bonus):
            inf = get_bonus_info(id)
            bbt = inf["next"]
            tuiu= datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")
            time1 = datetime.datetime.strptime(bbt, "%H:%M:%S %d-%m-%Y")
            time2 = datetime.datetime.strptime(tuiu, "%H:%M:%S %d-%m-%Y")
            if time2 > time1:
                bonuss = random.randint(5, 7)
                bbns = 4
                update_plus(id, "balance", bbns)
                #iuo = datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")
                next_bonus = datetime.datetime.now() + timedelta(hours=24)
                next_bonus_time=next_bonus.strftime("%H:%M:%S %d-%m-%Y")
                daily_update(id, "next", next_bonus_time)
                daily_plus(id,"claimed",1)
                await update.message.reply_markdown(f"*🔰You Have Received {bbns} Tk\n\n🔰Successfully Claimed Daily Bonus🥳*")
            else:
                await update.message.reply_markdown("*⚠️You Have Already Claimed Daily Bonus✅\n\n⛔Try Again Tomorrow! Daily Bonus Claim!🆗*")
        else:
            bonuss = random.randint(5, 7)
            bbns = 3
            update_plus(id, "balance", bbns)
            next_bonus_time = datetime.datetime.now() + timedelta(hours=24)
            uui = next_bonus_time.strftime("%H:%M:%S %d-%m-%Y")
            fff = {
                "user_id": id,
                "bonus": bonuss,
                "claimed": 1,
                "next": uui,
            }
            d_bonus.append(fff)
            save_daily_bonus(d_bonus)
            await update.message.reply_markdown(f"*🔰You Have Received {bbns} Tk\n\n🔰Successfully Claimed Daily Bonus🥳*")
     else:
        await update.message.reply_markdown("*Sorry! Bro\n\nYour Account is Not Activated!*")


    elif update.message.text == "♻️HisTory♻️":
      ccn = await check_CnL(id, context)
      if ccn in ["main", "chat", "2nd"]:
            await Unlock(update, context)
            return
      if id in Active:
        if any(entry['user_id'] == id for entry in History):
            for user_entry in History:
                if user_entry['user_id'] == id:
                    message = f"""                   🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰
🔰 *Type:* {user_entry['type']}
🔰 *USER:* {user_entry['user_id']}
🔰 *Method:* {user_entry['method']}
🔰 *Number:* {user_entry['number']}
🔰 *Amount:* {user_entry['Amount']} Tk
🔰* STATUS: *{user_entry['status']} 
🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰"""
                    await update.message.reply_markdown(message)
        else:
                 await update.message.reply_markdown("*🔰You Do Not Have Any History! \n\n⛔please make a withdraw!*")
                    
      else:
            await update.message.reply_markdown("*🔰 Your Account is Not Activated!*")
    elif update.message.text == "pending USR":
      if id in adminid:
        if pending:  # Check if there are any pending users
            for user in pending:
                message21 = f"""
🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰
🔰 *Type:  *{user['type']}*
🔰 USER: *{user['user_id']}
🔰 *Trxid:* {user['Trx']}
🔰 *Method:* {user['method']}
🔰 *Number:* {user['number']}
🔰 *Amount: * {user['Amount']} Tk
🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰
"""
                await update.message.reply_markdown(message21)
        else:
            await update.message.reply_markdown("*No Pending Users Found Boss!*")
      else:
        await update.message.reply_markdown("*You Are Not Admin Broh!*")

    
    elif update.message.text == "Help":
        await update.message.reply_markdown(
    f"""
*আসসালামু আলাইকুম! *{mention}*

⭕ WeeLcome! To the CashBox BD bot
🔰 বট এ কিভাবে টাকা ইনকাম করবেন 🔰

⭕ বট এ থাকছে ডেইলি বোনাস! ৪ টাকা!
⭕ বট এ আছে রেফার বোনাস সিস্টেম। আপনার রেফার এ যদি কেউ একাউন্ট এক্টিভেট করে তাহলে আপনি পাবেন ২০ টাকা। আরেকজনকে একাউন্ট এক্টিভেট করালে আপনি রেফার জেনারেশন লেবেল ২ এর ১০ টাকা বোনাস পাবেন। এইভাবে লেবেল ৫ পর্যন্ত বোনাস পাবেন। যত বেশি রেফার, তত বেশি ইনকাম।
⭕ বট এ আরো আছে লটারি। লটারি ৫০ টাকা দিয়ে টিকেট কিনলে। যদি লটারি তে আপনার টিকিট আসে তাহলে আপনি পাবেন ১৫০০ টাকা বোনাস। 
⭕ আরও আছে মিশন। মিশন এ আপনাকে কাজ দেয়া হবে। কাজ সম্পুর্ন করলে মিশন বোনাস যত টাকা থাকবে, আপনি তত টাকা পাবেন।*

    """)
    
    elif update.message.text == "Snd.m.AL.UR":
        await update.message.reply_markdown(" Enter Your message To Send ALL USER message")
        context.user_data['Anuunnn'] = True
    elif 'Anuunnn' in context.user_data and context.user_data['Anuunnn']:
        if id in adminid:
            for user in data:
                anid = user["user_id"]
                anname = user["name"]
                magi = f"""
```Admin_message!```
🔰 {update.message.text}
"""
                try:
                    await context.bot.send_photo(chat_id=anid,photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR05HbaO7aMu7VZEA2fD-akXr72mvp2tXLhOw&usqp=CAU",caption=magi,parse_mode="Markdown")
                except:
                    pass
            await cancel1(update,context)
        else:
            update.message.reply_markdown("Your Are Not Admin Broh!")
            await cancel1(update,context)
    
    
    
    elif update.message.text == "Anouncement":
        await update.message.reply_markdown(" Enter Your message To Send Announcement")
        context.user_data['Anun'] = True
    elif 'Anun' in context.user_data and context.user_data['Anun']:
        if id in adminid:
            for user in data:
                anid = user["user_id"]
                anname = user["name"]
                magi = f"""
```Announcement-!```

🔰 {update.message.text}
"""
                try:
                    await context.bot.send_photo(chat_id=anid,photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-5izi_UWJp3xDp-7SSLn5QtNmT-wN8Cy0ig&usqp=CAU",caption=magi,parse_mode="Markdown")
                except:
                    pass
            await cancel1(update,context)
        else:
            update.message.reply_markdown("Your Are Not Admin Broh!")
            await cancel1(update,context)                
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    id = str(update.effective_user.id)
    user = update.effective_user
    mention = f"[{update.effective_user.full_name}](tg://user?id={id})"
    if not any(user_data["user_id"] == str(user.id) for user_data in data):
        chat_id = context.args[0] if context.args else None
        referral_link = f"http://t.me/Cash_Box_BD_bot?start={user.id}"
        user_data = {
            "user_id": str(update.effective_user.id),
            "username": update.effective_user.username,
            "name": update.effective_user.full_name,
            "balance": "0",
            "joined": time,
            "referral_user":chat_id,
            "refferral_bonus":0,
            "Active_reffer":0,
            "referral_link":referral_link,
            "referral_count":0,}
        await add_user(user_data, context)
    ccn = await check_CnL(id, context)
    if ccn in ["main", "chat", "2nd"]:
        keyboard = [[InlineKeyboardButton("Main Chenel", url=f'https://t.me/Cash_box_BD')],[InlineKeyboardButton("Chat Group", url=f'https://t.me/Cash_box_BD_chat'),InlineKeyboardButton("2nd Chenel", url=f'https://t.me/Update_Free_income')],[InlineKeyboardButton("Contact Bot Developer", url=f'https://t.me/SYSTM_X')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        magi ="𝙃𝙞 𝙨𝙞𝙧 ! "+mention+"\n\n 𒊹︎︎︎➪ 𝘾𝙝𝙚𝙣𝙚𝙡 𝙖 𝙟𝙤𝙞𝙣 𝙠𝙤𝙧𝙪𝙣 𝙣𝙖 𝙝𝙮 𝘽𝙤𝙩 𝘼𝙘𝙘𝙚𝙨𝙨 𝙠𝙧𝙩𝙚 𝙥𝙖𝙧𝙗𝙚𝙣 𝙣𝙖!"
        await update.message.reply_photo(photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJgfvBlTxV63VzX4zlEz-boAlz3xLz5Ziaww&usqp=CAU",caption=magi,parse_mode="Markdown",
            reply_markup=reply_markup
            )
        await update.message.reply_markdown("*🔰যোগ দেওয়া হলে UNLOCK 🔓 বাটনে ক্লিক করুন✅*",reply_markup=ReplyKeyboardMarkup(
            [[" "], [" ", " "],["UNLOCK 🔓"],[' '," "]],
            resize_keyboard=True))
    else:
            member = mention
            bonus=get_user_by_id(id)['refferral_bonus']
            user_iid=get_user_by_id(id)['user_id']
            reffer_id = get_user_by_id(id)['referral_user']
            await reffer_count(user_iid, reffer_id,bonus,member,context)
            if id in Active:
               #☑️ আপনি ইতিমধ্যে একটিভ করেছেন।
               await update.message.reply_markdown(f"""*🎉 অভিনন্দনঃ-* {mention}* প্রিয়।

🎇 রেফার করুন, যত রেফার তত লাভ।
▶️ আরো বেশি ইনকাম করতে চাইলে সাপ্তাহিক লটারি কিনুন ৫০ টাকা।*""",
            reply_markup=ReplyKeyboardMarkup(
                [["ᗪᗩILY ᗷOᑎᑌՏ!"],[my_account,pkg,add_balance],["🎁 𝐑𝐄𝐅𝐅𝐄𝐑 🎊","Help", redeem],["Lᴏᴛᴛᴇʀʏ","WᴀʟʟᴇT","𝙬𝙞𝙩𝙝𝙙𝙧𝙖𝙬"],["Daily Task"],["Mɪssɪᴏɴ","♻️HisTory♻️","Sᴇᴛ WᴀʟʟᴇT"],["(●’◡’●)𝙐𝙋𝘿𝘼𝙏𝙀♻️",support]],
                resize_keyboard=True,
                one_time_keyboard=False
        
                )
            )
            else:
                await update.message.reply_markdown(
    f"""
*আসসালামু আলাইকুম! *{mention}*

⭕ WeeLcome! To the CashBox BD bot
🆘 প্রিয় ব্যবহারকারী, আপনি যদি বট ব্যবহার করে টাকা ইনকাম করতে চান তাহলে আপনাকে আগে একাউন্ট এক্টিভেট করতে হবে। একাউন্ট এক্টিভেট করতে আপনাকে 50 টাকা পেমেন্ট করতে হবে। একাউন্ট এক্টিভেট করতে 'একটিভ একাউন্ট' বাটনে ক্লিক করুন!


🔰 বট এ কিভাবে টাকা ইনকাম করবেন 🔰

⭕ বট এ থাকছে ডেইলি বোনাস! ৪ টাকা!
⭕ বট এ আছে রেফার বোনাস সিস্টেম। আপনার রেফার এ যদি কেউ একাউন্ট এক্টিভেট করে তাহলে আপনি পাবেন ২০ টাকা। আরেকজনকে একাউন্ট এক্টিভেট করালে আপনি রেফার জেনারেশন লেবেল ২ এর ১০ টাকা বোনাস পাবেন। এইভাবে লেবেল ৫ পর্যন্ত বোনাস পাবেন। যত বেশি রেফার, তত বেশি ইনকাম।
⭕ বট এ আরো আছে লটারি। লটারি ৫০ টাকা দিয়ে টিকেট কিনলে। যদি লটারি তে আপনার টিকিট আসে তাহলে আপনি পাবেন ১৫০০ টাকা বোনাস। 
⭕ আরও আছে মিশন। মিশন এ আপনাকে কাজ দেয়া হবে। কাজ সম্পুর্ন করলে মিশন বোনাস যত টাকা থাকবে, আপনি তত টাকা পাবেন।*


*আপনার একাউন্ট টি এক্টিভ নয়।*
*দয়া করে এক্টিভ করুন*
    """,
    reply_markup=ReplyKeyboardMarkup(
        [[" "], ["🎁 𝐑𝐄𝐅𝐅𝐄𝐑 🎊",my_account],[" "],[send_sms],['(●’◡’●)𝙐𝙋𝘿𝘼𝙏𝙀♻️',support]],
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
        keyboard = [["Anouncement","Snd.m.AL.AC.UR.","Snd.m.AL.UR"],[send_stu,"USER INFO"],
        [send_balance, "Rmv AC USER"],
        [add_admin,"Rmv Admin","remove_balance"],
        ["Redeem code♻️","📊 Statistics","BOT USER"],
        ["ADD AC USER","pending USR","withdraw USR"],
        ["rejected withdraw","rejected Active"],
        ["inactive bonus remove"],
        ["Add.mission","OFF.mission","On.mission"],
        ["Ck.mission"]
        ]
        #[[], [, ],[]],
        await update.message.reply_text(
        fr'Hi Admin {update.effective_user.full_name}!',
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

async def Unlock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        id = str(update.effective_user.id)
        mention = f"[{update.effective_user.full_name}](tg://user?id={id})"
        msgg = update.message.text
        ccn = await check_CnL(id, context)
        if ccn in ["main", "chat", "2nd"]:
            if ccn == "main":
                keyboard = [[InlineKeyboardButton("Main Chenel", url="https://t.me/Cash_box_BD")]]
                magi ="𝙃𝙞 𝙨𝙞𝙧 ! "+mention+f"\n\n*আপনি  Main Chenel এ যোগ দেন নি। দয়া করে চেনেল এ যোগ দিয়ে তারপর {msgg}  বাটন এ ক্লিক করবেন।*"
            elif ccn == "chat":
                keyboard = [[InlineKeyboardButton("Chat Group", url="https://t.me/Cash_box_BD_chat")]]
                magi ="𝙃𝙞 𝙨𝙞𝙧 ! "+mention+f"\n\n*আপনি Chat Group এ যোগ দেন নি। দয়া করে চেনেল এ যোগ দিয়ে তারপর {msgg}  বাটন এ ক্লিক করবেন।*"
            elif ccn == "2nd":
                keyboard = [[InlineKeyboardButton("2nd Chenel", url="https://t.me/Update_Free_income")]]
                magi ="𝙃𝙞 𝙨𝙞𝙧 ! "+mention+f"\n\n*আপনি 2nd Chenel এ যোগ দেন নি। দয়া করে চেনেল এ যোগ দিয়ে তারপর {msgg} বাটন এ ক্লিক করবেন।*"
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_photo(photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJgfvBlTxV63VzX4zlEz-boAlz3xLz5Ziaww&usqp=CAU", caption=magi, parse_mode="Markdown", reply_markup=reply_markup)



app = ApplicationBuilder().token("6816903297:AAEyJGFYQf4FWcOIOH3owWr1gTTV7lsdU5M").build()

# Add command handler for /start command
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("STDNXR", adminxx))
app.add_handler(CommandHandler("cancel", cancel))
app.add_handler(CommandHandler("Unlock", Unlock))
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

