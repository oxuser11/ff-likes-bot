import os
import json
import time
import threading
import requests
import telebot
from telebot import types
from flask import Flask

# 1. 24/7 Web Server for Render
app = Flask(__name__)

@app.route('/')
def home():
    return "FREE FIRE MULTI-TOOL BOT IS 24/7 ONLINE"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# 2. Configurations
BOT_TOKEN = "8708303127:AAHE2yb5TU9jfeFrtx3RaDhY5oS97DoDOF0"
ADMIN_ID = 8671410379
ADMIN_USERNAME = "OxRehann"

TG_CHANNEL_ID = "@OxRehanCyber"
TG_CHANNEL_LINK = "https://t.me/OxRehanCyber"
INSTA_LINK = "https://instagram.com/ox.mods"

KV_URL = "https://api.keyval.org/ox_ff_likes_vault_2026"
DB_FILE = "ff_likes_db.json"

bot = telebot.TeleBot(BOT_TOKEN)
user_states = {}
active_reports = {}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# 3. Database Engine
def load_db():
    try:
        res = requests.get(KV_URL, timeout=5)
        if res.status_code == 200 and res.text:
            data = res.json()
            if isinstance(data, dict):
                if "users" not in data:
                    data = {"users": data, "gift_codes": {}}
                return data
    except Exception:
        pass
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                data = json.load(f)
                if "users" not in data:
                    data = {"users": data, "gift_codes": {}}
                return data
        except Exception:
            return {"users": {}, "gift_codes": {}}
    return {"users": {}, "gift_codes": {}}

def save_db(data):
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(data, f)
    except Exception:
        pass
    try:
        requests.post(KV_URL, json=data, timeout=5)
    except Exception:
        pass

db = load_db()

def get_user(uid):
    s = str(uid)
    if s not in db["users"]:
        db["users"][s] = {"credits": 2, "referrals": 0, "likes_sent": 0}
        save_db(db)
    return db["users"][s]

def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(TG_CHANNEL_ID, user_id).status
        if status in ['member', 'administrator', 'creator']:
            return True
    except Exception:
        return True
    return False

# 4. Keyboards
def force_join_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton("📢 𝗝𝗢𝗜𝗡 𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗠 𝗖𝗛𝗔𝗡𝗡𝗘𝗟", url=TG_CHANNEL_LINK)
    b2 = types.InlineKeyboardButton("📸 𝗙𝗢𝗟𝗟𝗢𝗪 𝗜𝗡𝗦𝗧𝗔𝗚𝗥𝗔𝗠 (@ox.mods)", url=INSTA_LINK)
    b3 = types.InlineKeyboardButton("⚡ 𝗩𝗘𝗥𝗜𝗙𝗬 & 𝗨𝗡𝗟𝗢𝗖𝗞 ⚡", callback_data="check_joined")
    markup.add(b1, b2, b3)
    return markup

def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    b1 = types.KeyboardButton("❤️‍🔥 FREE LIKES (50 LIKES)")
    b2 = types.KeyboardButton("📊 PLAYER STATS CARD")
    b3 = types.KeyboardButton("🚨 AUTO REPORT PLAYER")
    b4 = types.KeyboardButton("💎 MY BALANCE")
    b5 = types.KeyboardButton("👥 REFER & EARN")
    b6 = types.KeyboardButton("🎁 REDEEM GIFT CODE")
    b7 = types.KeyboardButton("🛍️ BUY LIKES PACK")
    markup.add(b1, b2)
    markup.add(b3, b4)
    markup.add(b5, b6)
    markup.add(b7)
    return markup

# 5. Handlers
@bot.message_handler(commands=['start'])
def start_cmd(message):
    uid = message.from_user.id
    s = str(uid)
    text = message.text.split()

    if s not in db["users"]:
        ref_id = text[1] if len(text) > 1 and text[1].isdigit() and text[1] != s else None
        if ref_id and ref_id in db["users"]:
            db["users"][ref_id]["credits"] += 5
            db["users"][ref_id]["referrals"] += 1
            try:
                bot.send_message(
                    int(ref_id),
                    "🎉 *New Referral Joined!*\n💎 *+5 Credits* aapke account me add ho gaye!",
                    parse_mode='Markdown'
                )
            except Exception:
                pass
        db["users"][s] = {"credits": 2, "referrals": 0, "likes_sent": 0}
        save_db(db)

    if not is_subscribed(uid):
        msg = (
            f"👋 *Welcome {message.from_user.first_name}!* 🎮\n\n"
            "⚠️ Bot ke saare tools unlock karne ke liye pehle official channels ko join & follow karein:\n\n"
            "1️⃣ *Telegram Channel Join Karein*\n"
            "2️⃣ *Instagram Follow Karein*\n\n"
            "Dono complete karne ke baad **⚡ VERIFY & UNLOCK ⚡** button dabayein!"
        )
        bot.reply_to(message, msg, parse_mode='Markdown', reply_markup=force_join_keyboard())
        return

    bot.reply_to(
        message,
        f"🔥 *FREE FIRE AUTO TOOL & LIKES BOT* 🔥\n\n"
        f"👋 Namaste, *{message.from_user.first_name}*!\n"
        "🎁 *Signup Bonus:* `+2 Credits` Free Mil Gaye!\n\n"
        "👇 Neeche keyboard menu se feature select karein:",
        parse_mode='Markdown',
        reply_markup=main_keyboard()
    )

@bot.callback_query_handler(func=lambda call: call.data == "check_joined")
def verify_join(call):
    uid = call.from_user.id
    if is_subscribed(uid):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(
            call.message.chat.id,
            "✅ *Channel Verified Successfully!*\n\nNeeche keyboard menu se feature select karein:",
            parse_mode='Markdown',
            reply_markup=main_keyboard()
        )
    else:
        bot.answer_callback_query(call.id, "❌ Verification failed! Pehle dono channels join karein.", show_alert=True)

@bot.message_handler(func=lambda m: m.text == "💎 MY BALANCE")
def check_balance(m):
    u = get_user(m.from_user.id)
    text = (
        "╔════════════════════╗\n"
        "       📊  *PLAYER WALLET*  📊\n"
        "╚════════════════════╝\n\n"
        f"👤 *Player:* {m.from_user.first_name}\n"
        f"🆔 *User ID:* `{m.from_user.id}`\n\n"
        f"💎 *Available Credits:* `{u['credits']}`\n"
        f"👥 *Total Referrals:* `{u['referrals']}`\n"
        f"❤️ *Likes Delivered:* `{u['likes_sent']}`\n\n"
        "📌 *Rule:* `10 Credits = 50 Free Fire Likes`"
    )
    bot.reply_to(m, text, parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "👥 REFER & EARN")
def refer_system(m):
    uid = m.from_user.id
    bot_user = bot.get_me().username
    text = (
        "🔥 *REFER & EARN UNLIMITED LIKES* 🔥\n\n"
        "💎 *Per Referral:* 5 Credits\n"
        "🎯 *Target:* Sirf 2 Referrals = 50 Free Likes Direct Profile Par!\n\n"
        "🔗 *Aapka Personal Invite Link:*\n"
        f"`https://t.me/{bot_user}?start={uid}`\n\n"
        "*(Link copy karke Free Fire groups me share karein)*"
    )
    bot.reply_to(m, text, parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "🛍️ BUY LIKES PACK")
def buy_packs(m):
    text = (
        "🛍️ *INSTANT FREE FIRE LIKES PRICING* 🛍️\n\n"
        "❤️ 50 Likes (10 Credits)   = ₹15\n"
        "❤️ 100 Likes (20 Credits)  = ₹25\n"
        "❤️ 300 Likes (50 Credits)  = ₹60\n"
        "👑 1,000 Bulk Likes Pack   = ₹150\n\n"
        f"Instant purchase ke liye direct admin ko contact karein:\n"
        f"👉 @{ADMIN_USERNAME}"
    )
    bot.reply_to(m, text, parse_mode='Markdown')

# --- LIKES INITIATION ---
@bot.message_handler(func=lambda m: m.text == "❤️‍🔥 FREE LIKES (50 LIKES)")
def request_likes(m):
    u = get_user(m.from_user.id)
    if u["credits"] < 10:
        bot.reply_to(
            m,
            f"⚠️ *Insufficient Credits!*\n\n"
            f"Aapke paas sirf `{u['credits']}` Credits hain.\n"
            "50 Likes bhejne ke liye **10 Credits** chahiye hote hain.\n\n"
            "👉 **👥 REFER & EARN** button se doston ko share karein (Har refer par 5 Credits milenge)!",
            parse_mode='Markdown'
        )
        return

    user_states[m.from_user.id] = "waiting_likes_uid"
    bot.reply_to(m, "🔢 Apni Free Fire ki **Numeric UID** yahan bhejein (Jaise: `1583920194`):\n\n_(Cancel ke liye /cancel likhein)_")

# --- STATS INITIATION ---
@bot.message_handler(func=lambda m: m.text == "📊 PLAYER STATS CARD")
def request_stats(m):
    user_states[m.from_user.id] = "waiting_stats_uid"
    bot.reply_to(m, "🔍 Jis player ka profile check karna hai, uski **Numeric UID** bhejein:\n\n_(Cancel ke liye /cancel likhein)_")

# --- REPORT INITIATION ---
@bot.message_handler(func=lambda m: m.text == "🚨 AUTO REPORT PLAYER")
def start_report_flow(m):
    user_states[m.from_user.id] = "waiting_report_uid"
    bot.reply_to(
        m,
        "🚨 *FREE FIRE AUTO REPORT TOOL*\n\n"
        "Jis player ko mass report karna hai, uski **Numeric UID** bhejein:\n\n"
        "_(Cancel ke liye /cancel likhein)_",
        parse_mode='Markdown'
    )

# --- GIFT CODE INITIATION ---
@bot.message_handler(func=lambda m: m.text == "🎁 REDEEM GIFT CODE")
def request_gift(m):
    user_states[m.from_user.id] = "waiting_gift_code"
    bot.reply_to(m, "🎁 Apna **Gift Code** yahan enter karein:\n\n_(Cancel ke liye /cancel likhein)_")

@bot.message_handler(commands=['cancel'])
def cancel_state(m):
    user_states.pop(m.from_user.id, None)
    bot.reply_to(m, "❌ Action cancel ho gaya.", reply_markup=main_keyboard())

# --- TEXT HANDLER FOR ACTIVE STATES ---
@bot.message_handler(func=lambda m: m.from_user.id in user_states)
def handle_text_states(m):
    uid = m.from_user.id
    state = user_states.pop(uid, None)

    # 1. Delivery Logic
    if state == "waiting_likes_uid":
        ff_uid = m.text.strip()
        if not ff_uid.isdigit() or len(ff_uid) < 7:
            bot.reply_to(m, "❌ Invalid UID! Valid numeric UID daalein.")
            return

        u = get_user(uid)
        if u["credits"] < 10:
            bot.reply_to(m, "⚠️ Balance low ho gaya.")
            return

        bot.reply_to(m, f"⏳ *UID `{ff_uid}` par 50 Likes process ho rahe hain...*", parse_mode='Markdown')

        api_url = f"https://like-api-freefire.vercel.app/api?uid={ff_uid}&server_name=ind"

        try:
            requests.get(api_url, headers=HEADERS, timeout=15)
        except Exception:
            pass

        u["credits"] -= 10
        u["likes_sent"] += 50
        save_db(db)

        bot.reply_to(
            m,
            f"🎉 *50 LIKES SENT SUCCESSFULLY!* ❤️‍🔥\n\n"
            f"🎯 *Player UID:* `{ff_uid}`\n"
            f"💎 *Remaining Credits:* `{u['credits']}`\n\n"
            "Likes 2–5 minutes me profile me reflect ho jayenge. Game refresh karke check karein!",
            parse_mode='Markdown',
            reply_markup=main_keyboard()
        )

    # 2. Player Stats Card
    elif state == "waiting_stats_uid":
        ff_uid = m.text.strip()
        if not ff_uid.isdigit() or len(ff_uid) < 7:
            bot.reply_to(m, "❌ Invalid format! Free Fire numeric UID daalein.")
            return

        bot.reply_to(m, f"🔍 UID `{ff_uid}` ki details fetch ho rahi hain...", parse_mode='Markdown')
        info = None

        try:
            r1 = requests.get(f"https://www.freefireapi.me/api/info?uid={ff_uid}", headers=HEADERS, timeout=8).json()
            if r1 and (r1.get("AccountInfo") or r1.get("basicInfo") or r1.get("nickname")):
                info = r1.get("AccountInfo") or r1.get("basicInfo") or r1
        except Exception:
            pass

        if not info:
            try:
                r2 = requests.get(f"https://freefire-api-six.vercel.app/get_player_personal_show?server=ind&uid={ff_uid}", headers=HEADERS, timeout=8).json()
                if r2 and ("basic_info" in r2 or "AccountInfo" in r2 or "nickname" in r2):
                    info = r2.get("basic_info") or r2.get("AccountInfo") or r2
            except Exception:
                pass

        if not info:
            try:
                r3 = requests.get(f"https://freefire-virusteam.vercel.app/info?uid={ff_uid}&region=ind", headers=HEADERS, timeout=8).json()
                if r3 and (r3.get("AccountInfo") or r3.get("basicInfo")):
                    info = r3.get("AccountInfo") or r3.get("basicInfo")
            except Exception:
                pass

        if info:
            name = info.get("nickname") or info.get("AccountName") or info.get("name") or "Free Fire Player"
            lvl = info.get("level") or info.get("AccountLevel") or "N/A"
            likes = info.get("likes") or info.get("AccountLikes") or "N/A"
            region = info.get("region") or info.get("AccountRegion") or "IND"
            bio = info.get("signature") or info.get("AccountSignature") or "None"

            card = (
                "╔════════════════════╗\n"
                "    🎮  *FREE FIRE PROFILE CARD*  🎮\n"
                "╚════════════════════╝\n\n"
                f"👤 *IGN:* `{name}`\n"
                f"🆔 *UID:* `{ff_uid}`\n"
                f"⭐ *Level:* `{lvl}`\n"
                f"❤️ *Current Likes:* `{likes}`\n"
                f"🌍 *Server:* `{region}`\n"
                f"📝 *Signature / Bio:* `{bio}`\n\n"
                "⚡ _Verified Profile Data_"
            )
            bot.reply_to(m, card, parse_mode='Markdown', reply_markup=main_keyboard())
        else:
            bot.reply_to(
                m,
                f"⚠️ UID `{ff_uid}` ka real-time data fetch nahi ho paya. Server busy hai ya UID galat hai.",
                parse_mode='Markdown',
                reply_markup=main_keyboard()
            )

    # 3. Report Target Lookup
    elif state == "waiting_report_uid":
        ff_uid = m.text.strip()
        if not ff_uid.isdigit() or len(ff_uid) < 7:
            bot.reply_to(m, "❌ Invalid UID! Valid numeric UID enter karein.")
            return

        bot.reply_to(m, f"🔍 Target UID `{ff_uid}` verify ho rahi hai...", parse_mode='Markdown')
        name = "Free Fire Player"
        lvl = "N/A"
        try:
            r = requests.get(f"https://www.freefireapi.me/api/info?uid={ff_uid}", headers=HEADERS, timeout=6).json()
            if r:
                info = r.get("AccountInfo") or r.get("basicInfo") or r
                name = info.get("nickname") or info.get("AccountName") or name
                lvl = info.get("level") or info.get("AccountLevel") or lvl
        except Exception:
            pass

        markup = types.InlineKeyboardMarkup()
        b_start = types.InlineKeyboardButton("⚠️ START MASS REPORT", callback_data=f"rep_start_{ff_uid}")
        b_cancel = types.InlineKeyboardButton("❌ CANCEL", callback_data="rep_cancel")
        markup.add(b_start)
        markup.add(b_cancel)

        text = (
            "⚠️ *TARGET VERIFIED FOR REPORT*\n\n"
            f"👤 *IGN:* `{name}`\n"
            f"🆔 *UID:* `{ff_uid}`\n"
            f"⭐ *Level:* `{lvl}`\n\n"
            "Kya aap is profile par automated reports trigger karna chahte hain?"
        )
        bot.reply_to(m, text, parse_mode='Markdown', reply_markup=markup)

    # 4. Gift Code Redeem
    elif state == "waiting_gift_code":
        code = m.text.strip().upper()
        s = str(uid)
        codes = db.get("gift_codes", {})

        if code not in codes:
            bot.reply_to(m, "❌ Invalid Gift Code! Code galat hai ya expire ho chuka hai.", reply_markup=main_keyboard())
            return

        gdata = codes[code]
        if s in gdata["users"]:
            bot.reply_to(m, "⚠️ Aap yeh gift code pehle hi claim kar chuke hain!", reply_markup=main_keyboard())
            return

        if len(gdata["users"]) >= gdata["max_claims"]:
            bot.reply_to(m, "⚠️ Yeh code limit poori hone ki wajah se expire ho chuka hai!", reply_markup=main_keyboard())
            return

        creds = gdata["credits"]
        u = get_user(uid)
        u["credits"] += creds
        gdata["users"].append(s)
        save_db(db)

        bot.reply_to(
            m,
            f"🎉 *Gift Code Redeemed!*\n\n"
            f"💎 *+{creds} Credits* add ho gaye hain!\n"
            f"💰 *New Balance:* `{u['credits']}` Credits",
            parse_mode='Markdown',
            reply_markup=main_keyboard()
        )

# --- REPORT BACKGROUND WORKER & CALLBACKS ---
def background_reporter(chat_id, message_id, user_id, target_uid):
    active_reports[user_id] = True
    stop_markup = types.InlineKeyboardMarkup()
    stop_markup.add(types.InlineKeyboardButton("🛑 STOP REPORT", callback_data=f"rep_stop_{user_id}"))

    for count in range(1, 26):
        if not active_reports.get(user_id, False):
            break

        try:
            requests.get(f"https://like-api-freefire.vercel.app/api?uid={target_uid}&server_name=ind", headers=HEADERS, timeout=5)
        except Exception:
            pass

        try:
            bot.edit_message_text(
                f"🚨 *REPORTING IN PROGRESS...*\n\n"
                f"🎯 *Target UID:* `{target_uid}`\n"
                f"📊 *Reports Sent:* `{count}/25`\n"
                f"⚡ *Status:* Dispatching server flags...\n\n"
                "Rukne ke liye neeche button dabayein 👇",
                chat_id=chat_id,
                message_id=message_id,
                parse_mode='Markdown',
                reply_markup=stop_markup
            )
        except Exception:
            pass

        time.sleep(2)

    was_running = active_reports.pop(user_id, False)
    final_text = (
        f"🛑 *REPORT PROCESS STOPPED*\n\n"
        f"🎯 Target UID `{target_uid}` par reporting process complete/stopped."
    ) if was_running else f"✅ Reporting finished for UID `{target_uid}`."

    try:
        bot.edit_message_text(final_text, chat_id=chat_id, message_id=message_id, parse_mode='Markdown')
    except Exception:
        pass

@bot.callback_query_handler(func=lambda call: call.data.startswith("rep_"))
def handle_report_callbacks(call):
    uid = call.from_user.id

    if call.data.startswith("rep_start_"):
        target_uid = call.data.split("_")[2]
        bot.answer_callback_query(call.id, "🚨 Report process started!")
        threading.Thread(
            target=background_reporter,
            args=(call.message.chat.id, call.message.message_id, uid, target_uid)
        ).start()

    elif call.data.startswith("rep_stop_"):
        active_reports[uid] = False
        bot.answer_callback_query(call.id, "🛑 Stopping reports...", show_alert=True)

    elif call.data == "rep_cancel":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "❌ Action cancel kar diya gaya.")

# --- ADMIN COMMANDS ---
@bot.message_handler(commands=['all'])
def admin_broadcast(m):
    if m.from_user.id != ADMIN_ID:
        return

    text_parts = m.text.split(maxsplit=1)
    if len(text_parts) < 2:
        bot.reply_to(m, "⚠️ Format: `/all <Aapka Message>`", parse_mode='Markdown')
        return

    broadcast_msg = text_parts[1]
    all_users = list(db.get("users", {}).keys())

    bot.reply_to(m, f"📢 Broadcast shuru ho gaya. Total {len(all_users)} users ko bhej rahe hain...")

    success = 0
    failed = 0

    for user_id in all_users:
        try:
            bot.send_message(
                int(user_id),
                f"📢 *OFFICIAL NOTIFICATION*\n\n{broadcast_msg}",
                parse_mode='Markdown'
            )
            success += 1
            time.sleep(0.05)
        except Exception:
            failed += 1

    bot.send_message(
        m.chat.id,
        f"✅ *Broadcast Complete!*\n\n✔️ Sent: `{success}` users\n❌ Blocked/Failed: `{failed}` users",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['gen'])
def admin_gen_code(m):
    if m.from_user.id != ADMIN_ID:
        return
    p = m.text.split()
    if len(p) != 4:
        bot.reply_to(m, "Usage: `/gen <CODE> <CREDITS> <MAX_USERS>`\nExample: `/gen FFLIKE 10 100`", parse_mode='Markdown')
        return

    code_name = p[1].upper()
    credits = int(p[2])
    max_claims = int(p[3])

    if "gift_codes" not in db:
        db["gift_codes"] = {}

    db["gift_codes"][code_name] = {
        "credits": credits,
        "max_claims": max_claims,
        "users": []
    }
    save_db(db)

bot.reply_to(
        m,
        f"✅ *Gift Code Created!*\n\n🎁 Code: `{code_name}`\n💎 Credits: `{credits}`\n👥 Limit: `{max_claims}`",
        parse_mode='Markdown'
    )

if __name__ == '__main__':
    threading.Thread(target=run_web).start()
    bot.infinity_polling()
