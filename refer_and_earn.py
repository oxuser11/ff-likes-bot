import os
import json
import time
import threading
import requests
import telebot
from telebot import types
from flask import Flask

# 1. Web Server for Render 24/7
app = Flask(__name__)

@app.route('/')
def home():
    return "REFER & EARN BOT IS ACTIVE 24/7"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# 2. Configurations & Bot Token
BOT_TOKEN = "8600453122:AAHplw4g0dNZ8Es_6oXRX6LdPv6I_aQqIV4"
ADMIN_ID = 8671410379
ADMIN_USER = "OxRehann"

CH1_ID = "@OxRehanCyber"
CH1_LINK = "https://t.me/OxRehanCyber"
CH2_LINK = "https://t.me/+852hkOgj0UNlZGU9"
INSTA_LINK = "https://instagram.com/ox.mods"

KV_URL = "https://api.keyval.org/ox_refer_earn_cash_2026"
DB_FILE = "refer_earn_db.json"

bot = telebot.TeleBot(BOT_TOKEN)
user_states = {}

# 3. Database Engine
def load_db():
    try:
        r = requests.get(KV_URL, timeout=4).json()
        if isinstance(r, dict) and "users" in r:
            return r
    except:
        pass
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"users": {}, "gift_codes": {}}

def save_db(data):
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(data, f)
    except:
        pass
    try:
        requests.post(KV_URL, json=data, timeout=4)
    except:
        pass

db = load_db()

def get_user(uid):
    s = str(uid)
    if s not in db["users"]:
        db["users"][s] = {
            "balance": 0.0,
            "referrals": 0,
            "total_withdrawn": 0.0,
            "joined": True
        }
        save_db(db)
    return db["users"][s]

def is_subscribed(uid):
    try:
        status = bot.get_chat_member(CH1_ID, uid).status
        return status in ['member', 'administrator', 'creator']
    except:
        return True

# 4. Keyboards
def verify_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton("📢 𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 𝟭", url=CH1_LINK)
    b2 = types.InlineKeyboardButton("📢 𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 𝟮", url=CH2_LINK)
    b3 = types.InlineKeyboardButton("📸 𝗙𝗢𝗟𝗟𝗢𝗪 𝗜𝗡𝗦𝗧𝗔𝗚𝗥𝗔𝗠", url=INSTA_LINK)
    b4 = types.InlineKeyboardButton("⚡ 𝗩𝗘𝗥𝗜𝗙𝗬 & 𝗨𝗡𝗟𝗢𝗖𝗞 ⚡", callback_data="check_joined")
    kb.add(b1, b2, b3, b4)
    return kb

def main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    b1 = types.KeyboardButton("💰 MY WALLET")
    b2 = types.KeyboardButton("👥 REFER & EARN (₹3/REF)")
    b3 = types.KeyboardButton("💳 WITHDRAW MONEY")
    b4 = types.KeyboardButton("🎁 REDEEM CODE")
    b5 = types.KeyboardButton("📊 LIVE STATISTICS")
    b6 = types.KeyboardButton("📞 24/7 SUPPORT")
    kb.add(b1, b2)
    kb.add(b3, b4)
    kb.add(b5, b6)
    return kb

def withdraw_choice_kb():
    kb = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton("📱 UPI ID", callback_data="wth_upi")
    b2 = types.InlineKeyboardButton("📞 PhonePe / Paytm", callback_data="wth_num")
    b3 = types.InlineKeyboardButton("🖼️ Upload QR Code", callback_data="wth_qr")
    b4 = types.InlineKeyboardButton("❌ Cancel", callback_data="wth_cancel")
    kb.add(b1, b2)
    kb.add(b3)
    kb.add(b4)
    return kb

# 5. Handlers
@bot.message_handler(commands=['start'])
def start_cmd(m):
    uid = m.from_user.id
    s = str(uid)
    text = m.text.split()

    if s not in db["users"]:
        ref_id = text[1] if len(text) > 1 and text[1].isdigit() and text[1] != s else None
        if ref_id and ref_id in db["users"]:
            db["users"][ref_id]["balance"] += 3.0
            db["users"][ref_id]["referrals"] += 1
            try:
                bot.send_message(
                    int(ref_id),
                    f"🎉 *New Referral Joined!*\n\n"
                    f"👤 Member: `{m.from_user.first_name}`\n"
                    f"💵 *+₹3.0 Cash* aapke wallet me add ho gaya!",
                    parse_mode='Markdown'
                )
            except:
                pass
        db["users"][s] = {"balance": 0.0, "referrals": 0, "total_withdrawn": 0.0, "joined": True}
        save_db(db)

    if not is_subscribed(uid):
        msg = (
            f"👋 *Welcome {m.from_user.first_name}!* 🎮\n\n"
            "⚠️ Bot ko unlock karke paise kamane ke liye dono channel join aur Instagram follow karein:\n\n"
            "1️⃣ *Telegram Channel 1*\n"
            "2️⃣ *Telegram Channel 2*\n"
            "3️⃣ *Instagram Handle (@ox.mods)*\n\n"
            "Sabhi tasks poore karke **⚡ VERIFY & UNLOCK ⚡** par tap karein!"
        )
        bot.reply_to(m, msg, parse_mode='Markdown', reply_markup=verify_keyboard())
        return

    bot.reply_to(
        m,
        f"🔥 *WELCOME TO REFER & EARN CASH BOT* 🔥\n\n"
        f"👋 Namaste, *{m.from_user.first_name}*!\n"
        f"💸 *Per Refer:* `₹3.0 Real Cash`\n"
        f"🎯 *Minimum Withdraw:* `₹100`\n\n"
        "Neeche menu se explore karein 👇",
        parse_mode='Markdown',
        reply_markup=main_keyboard()
    )

@bot.callback_query_handler(func=lambda c: c.data == "check_joined")
def check_join_callback(c):
    if is_subscribed(c.from_user.id):
        bot.delete_message(c.message.chat.id, c.message.message_id)
        bot.send_message(
            c.message.chat.id,
            "✅ *Verification Successful!*\n\nAapka dashboard active ho chuka hai. Menu se option select karein:",
            parse_mode='Markdown',
            reply_markup=main_keyboard()
        )
    else:
        bot.answer_callback_query(c.id, "❌ Aapne abhi tak channels join nahi kiye! Pehle join karein.", show_alert=True)

@bot.message_handler(func=lambda m: m.text == "💰 MY WALLET")
def wallet_cmd(m):
    u = get_user(m.from_user.id)
    text = (
        "╔════════════════════╗\n"
        "       💼  *USER WALLET*  💼\n"
        "╚════════════════════╝\n\n"
        f"👤 *Account:* {m.from_user.first_name}\n"
        f"🆔 *User ID:* `{m.from_user.id}`\n\n"
        f"💰 *Available Balance:* `₹{u['balance']:.2f}`\n"
        f"👥 *Total Referrals:* `{u['referrals']}`\n"
        f"💳 *Total Withdrawn:* `₹{u['total_withdrawn']:.2f}`\n\n"
        "📌 *Withdraw Limit:* `₹100.00`"
    )
    bot.reply_to(m, text, parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "👥 REFER & EARN (₹3/REF)")
def refer_cmd(m):
    uid = m.from_user.id
    bot_user = bot.get_me().username
    text = (
        "🚀 *REFER & EARN UNLIMITED CASH* 🚀\n\n"
        "💵 *Reward:* ₹3.0 har valid invite par!\n"
        "🎯 *Daily Goal:* 34 referrals = ₹100 Instant Cash!\n\n"
        "🔗 *Aapka Personal Invite Link:*\n"
        f"`https://t.me/{bot_user}?start={uid}`\n\n"
        "📌 *Is link ko doston aur groups me share karein!*"
    )
    bot.reply_to(m, text, parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "💳 WITHDRAW MONEY")
def withdraw_prompt(m):
    u = get_user(m.from_user.id)
    if u["balance"] < 100.0:
        bot.reply_to(
            m,
            f"⚠️ *Insufficient Balance!*\n\n"
            f"Aapka balance sirf `₹{u['balance']:.2f}` hai.\n"
            f"Withdraw lagane ke liye kam se kam **₹100** hona zaroori hai.\n\n"
            f"👉 Aur `₹{100.0 - u['balance']:.2f}` earn karne ke liye link share karein!",
            parse_mode='Markdown'
        )
        return

    bot.reply_to(
        m,
        f"✅ *Eligible for Withdrawal!*\n\n"
        f"💰 Available Balance: `₹{u['balance']:.2f}`\n\n"
        "Payment receive karne ka method select karein:",
        parse_mode='Markdown',
        reply_markup=withdraw_choice_kb()
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("wth_"))
def handle_withdraw_choice(c):
    action = c.data
    uid = c.from_user.id

    if action == "wth_cancel":
        bot.delete_message(c.message.chat.id, c.message.message_id)
        bot.send_message(c.message.chat.id, "❌ Withdrawal canceled.", reply_markup=main_keyboard())
        return

    user_states[uid] = action
    bot.delete_message(c.message.chat.id, c.message.message_id)

    if action == "wth_upi":
        bot.send_message(c.message.chat.id, "📱 Apni valid **UPI ID** bhejein (Jaise: `user@upi` ya `user@axl`):")
    elif action == "wth_num":
        bot.send_message(c.message.chat.id, "📞 Apna **Paytm / PhonePe Registered Mobile Number** bhejein:")
    elif action == "wth_qr":
        bot.send_message(c.message.chat.id, "🖼️ Apna Payment **QR Code Photo** yahan send karein:")

@bot.message_handler(content_types=['photo'], func=lambda m: user_states.get(m.from_user.id) == "wth_qr")
def handle_qr_upload(m):
    uid = m.from_user.id
    user_states.pop(uid, None)
    u = get_user(uid)

    if u["balance"] < 100.0:
        bot.reply_to(m, "⚠️ Balance insufficient hai.")
        return

    amount = u["balance"]
    u["balance"] = 0.0
    u["total_withdrawn"] += amount
    save_db(db)

    photo_id = m.photo[-1].file_id

    admin_kb = types.InlineKeyboardMarkup()
    admin_kb.add(
        types.InlineKeyboardButton("✅ APPROVE", callback_data=f"adm_ok_{uid}_{amount}"),
        types.InlineKeyboardButton("❌ REJECT & REFUND", callback_data=f"adm_no_{uid}_{amount}")
    )

    bot.send_photo(
        ADMIN_ID,
        photo_id,
        caption=(
            "🚨 *NEW WITHDRAW REQUEST (QR CODE)* 🚨\n\n"
            f"👤 User: {m.from_user.first_name} (`{uid}`)\n"
            f"💵 Amount: `₹{amount:.2f}`\n"
            f"Method: QR Code Scan"
        ),
        parse_mode='Markdown',
        reply_markup=admin_kb
    )

    bot.reply_to(
        m,
        f"✅ *Withdrawal Request Submitted!*\n\n"
        f"💵 Amount: `₹{amount:.2f}`\n"
        "Admin verify karke 1–2 hours me payment send kar denge.",
        parse_mode='Markdown',
        reply_markup=main_keyboard()
    )

@bot.message_handler(func=lambda m: m.text == "🎁 REDEEM CODE")
def redeem_prompt(m):
    user_states[m.from_user.id] = "redeem_code"
    bot.reply_to(m, "🎁 Apna **Redeem Code** enter karein:\n\n_(Cancel: /cancel)_")

@bot.message_handler(func=lambda m: m.text == "📊 LIVE STATISTICS")
def stats_view(m):
    total_users = len(db.get("users", {}))
    bot.reply_to(
        m,
        "📊 *BOT LIVE STATISTICS* 📊\n\n"
        f"👥 Total Members: `{total_users}`\n"
        "⚡ Payout: UPI / Number / QR Code\n"
        "🔒 Cloud Sync: Active 24/7",
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda m: m.text == "📞 24/7 SUPPORT")
def support_view(m):
    bot.reply_to(
        m,
        f"📞 *OFFICIAL SUPPORT*\n\n"
        f"Kisi bhi query ke liye admin ko message karein:\n"
        f"👉 @{ADMIN_USER}",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['cancel'])
def cancel_cmd(m):
    user_states.pop(m.from_user.id, None)
    bot.reply_to(m, "❌ Canceled.", reply_markup=main_keyboard())

# 6. User Inputs (UPI, Number, Code)
@bot.message_handler(func=lambda m: m.from_user.id in user_states)
def process_user_inputs(m):
    uid = m.from_user.id
    st = user_states.pop(uid, None)
    u = get_user(uid)

    if st in ["wth_upi", "wth_num"]:
        pay_info = m.text.strip()
        if u["balance"] < 100.0:
            bot.reply_to(m, "⚠️ Balance insufficient hai.")
            return

        amount = u["balance"]
        u["balance"] = 0.0
        u["total_withdrawn"] += amount
        save_db(db)

        admin_kb = types.InlineKeyboardMarkup()
        admin_kb.add(
            types.InlineKeyboardButton("✅ APPROVE", callback_data=f"adm_ok_{uid}_{amount}"),
            types.InlineKeyboardButton("❌ REJECT & REFUND", callback_data=f"adm_no_{uid}_{amount}")
        )

        bot.send_message(
            ADMIN_ID,
            f"🚨 *NEW WITHDRAW REQUEST* 🚨\n\n"
            f"👤 User: {m.from_user.first_name} (`{uid}`)\n"
            f"💵 Amount: `₹{amount:.2f}`\n"
            f"📌 Details: `{pay_info}`",
            parse_mode='Markdown',
            reply_markup=admin_kb
        )

        bot.reply_to(
            m,
            f"✅ *Withdrawal Request Submitted!*\n\n"
            f"💵 Amount: `₹{amount:.2f}`\n"
            f"📌 Detail: `{pay_info}`\n\n"
            "Admin check karke payment dispatch kar denge!",
            parse_mode='Markdown',
            reply_markup=main_keyboard()
        )

    elif st == "redeem_code":
        code = m.text.strip().upper()
        s = str(uid)
        codes = db.get("gift_codes", {})

        if code not in codes:
            bot.reply_to(m, "❌ Invalid ya Expired Code!", reply_markup=main_keyboard())
            return

        gdata = codes[code]
        if s in gdata["users"]:
            bot.reply_to(m, "⚠️ Yeh code aap pehle claim kar chuke hain!", reply_markup=main_keyboard())
            return

        if len(gdata["users"]) >= gdata["max_claims"]:
            bot.reply_to(m, "⚠️ Code limit full ho gayi!", reply_markup=main_keyboard())
            return

        amt = float(gdata["amount"])
        u["balance"] += amt
        gdata["users"].append(s)
        save_db(db)

        bot.reply_to(
            m,
            f"🎉 *Code Redeemed Successfully!*\n\n"
            f"💵 *+₹{amt:.2f} Cash* wallet me add ho gaya!\n"
            f"💰 Balance: `₹{u['balance']:.2f}`",
            parse_mode='Markdown',
            reply_markup=main_keyboard()
        )

# 7. Admin Callback & Commands
@bot.callback_query_handler(func=lambda c: c.data.startswith("adm_"))
def admin_approval_callback(c):
    if c.from_user.id != ADMIN_ID:
        return
    
    parts = c.data.split("_")
    action = parts[1]
    target_uid = int(parts[2])
    amt = float(parts[3])

    if action == "ok":
        bot.answer_callback_query(c.id, "Payment Approved!")
        bot.edit_message_caption(c.message.caption + "\n\n✅ *STATUS: PAID & APPROVED*", chat_id=c.message.chat.id, message_id=c.message.message_id, parse_mode='Markdown') if c.message.caption else bot.edit_message_text(c.message.text + "\n\n✅ *STATUS: PAID & APPROVED*", chat_id=c.message.chat.id, message_id=c.message.message_id, parse_mode='Markdown')
        try:
            bot.send_message(target_uid, f"🎉 *WITHDRAWAL SUCCESSFUL!*\n\nAapki `₹{amt:.2f}` ki payment complete kar di gayi hai!", parse_mode='Markdown')
        except:
            pass

    elif action == "no":
        target_s = str(target_uid)
        if target_s in db["users"]:
            db["users"][target_s]["balance"] += amt
            db["users"][target_s]["total_withdrawn"] -= amt
            save_db(db)
        bot.answer_callback_query(c.id, "Payment Rejected & Refunded!")
        bot.edit_message_caption(c.message.caption + "\n\n❌ *STATUS: REJECTED & REFUNDED*", chat_id=c.message.chat.id, message_id=c.message.message_id, parse_mode='Markdown') if c.message.caption else bot.edit_message_text(c.message.text + "\n\n❌ *STATUS: REJECTED & REFUNDED*", chat_id=c.message.chat.id, message_id=c.message.message_id, parse_mode='Markdown')
        try:
            bot.send_message(target_uid, f"⚠️ *WITHDRAWAL REJECTED*\n\nAapki `₹{amt:.2f}` ki request reject ho gayi hai aur paise wapas refund kar diye gaye hain.", parse_mode='Markdown')
        except:
            pass

@bot.message_handler(commands=['gen'])
def admin_generate_code(m):
    if m.from_user.id != ADMIN_ID:
        return
    parts = m.text.split()
    if len(parts) != 4:
        bot.reply_to(m, "Format: `/gen <CODE> <AMOUNT_INR> <MAX_USERS>`\nExample: `/gen CASH20 20 50`", parse_mode='Markdown')
        return

    code = parts[1].upper()
    amount = float(parts[2])
    max_c = int(parts[3])

    if "gift_codes" not in db:
        db["gift_codes"] = {}

    db["gift_codes"][code] = {
        "amount": amount,
        "max_claims": max_c,
        "users": []
    }
    save_db(db)

    bot.reply_to(
        m,
        f"✅ *Gift Code Created!*\n\n"
        f"🎁 Code: `{code}`\n"
        f"💵 Amount: `₹{amount:.2f}`\n"
        f"👥 Max Users: `{max_c}`",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['all'])
def admin_broadcast(m):
    if m.from_user.id != ADMIN_ID:
        return
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(m, "Format: `/all <Aapka Message>`", parse_mode='Markdown')
        return

    msg = parts[1]
    all_users = list(db.get("users", {}).keys())
    bot.reply_to(m, f"📢 Broadcast shuru: {len(all_users)} users ko bhej rahe hain...")

    success, failed = 0, 0
    for u in all_users:
        try:
            bot.send_message(int(u), f"📢 *OFFICIAL BROADCAST*\n\n{msg}", parse_mode='Markdown')
            success += 1
            time.sleep(0.04)
        except:
            failed += 1

    bot.send_message(m.chat.id, f"✅ Broadcast Complete!\nSent: `{success}`\nFailed: `{failed}`", parse_mode='Markdown')

if __name__ == '__main__':
    threading.Thread(target=run_web).start()
    bot.infinity_polling()
  
