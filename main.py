import os
import json
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

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
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

# 4. Colorful Keyboards
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
    b3 = types.KeyboardButton("🎯 HEADSHOT SENSITIVITY")
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
            db["users"][ref_id]["credits"] += 1
            db["users"][ref_id]["referrals"] += 1
            try:
                bot.send_message(int(ref_id), "🎉 *New Referral!* +1 Credit add ho gaya!", parse_mode='Markdown')
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
        "💎 *Per Referral:* 1 Credit\n"
        "🎯 *Milestone:* Har 10 Referrals par direct 50 Likes!\n\n"
        "🔗 *Aapka Personal Invite Link:*\n"
        f"`https://t.me/{bot_user}?start={uid}`\n\n"
        "*(Link par tap karke copy karein aur Free Fire groups me share karein)*"
    )
    bot.reply_to(m, text, parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "🎯 HEADSHOT SENSITIVITY")
def headshot_settings(m):
    text = (
        "⚡ *PRO HEADSHOT SENSITIVITY GUIDE* ⚡\n\n"
        "🔘 *General:* 98 - 100\n"
        "🔴 *Red Dot:* 95\n"
        "🎯 *2x Scope:* 90\n"
        "🔭 *4x Scope:* 86\n"
        "🦅 *Sniper Scope:* 58\n"
        "👀 *Free Look:* 72\n\n"
        "⚙️ *Pro Tip:* Apne mobile settings me DPI ko default se +50 increase karein fast drag ke liye."
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
        f"Instant pack purchase ke liye direct admin ko message karein:\n"
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
            "50 Likes deliver karne ke liye **10 Credits** chahiye hote hain.\n\n"
            "👉 **👥 REFER & EARN** button se doston ko share karein ya **🛍️ BUY LIKES PACK** se buy karein!",
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

        bot.reply_to(m, f"⏳ *UID `{ff_uid}` par 50 Likes order process ho raha hai...*", parse_mode='Markdown')

        # Public Free Fire Token Like Dispatcher
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
        if not ff_uid.isdigit():
            bot.reply_to(m, "❌ Invalid format.")
            return

        bot.reply_to(m, f"🔍 UID `{ff_uid}` ka data fetch ho raha hai...", parse_mode='Markdown')
        info_api = f"https://ff-api-stats.vercel.app/api/info?uid={ff_uid}&region=ind"

        try:
            res = requests.get(info_api, headers=HEADERS, timeout=10).json()
            name = res.get("AccountName", "FreeFire Player")
            lvl = res.get("AccountLevel", "N/A")
            likes = res.get("AccountLikes", "N/A")
            region = res.get("AccountRegion", "IND")
            bio = res.get("AccountSignature", "None")

            card = (
                "╔════════════════════╗\n"
                "    🎮  *FREE FIRE PROFILE CARD*  🎮\n"
                "╚════════════════════╝\n\n"
                f"👤 *IGN:* `{name}`\n"
                f"🆔 *UID:* `{ff_uid}`\n"
                f"⭐ *Level:* `{lvl}`\n"
                f"❤️ *Likes:* `{likes}`\n"
                f"🌍 *Region:* `{region}`\n"
                f"📝 *Signature:* `{bio}`"
            )
            bot.reply_to(m, card, parse_mode='Markdown', reply_markup=main_keyboard())
        except Exception:
            bot.reply_to(
                m,
                f"👤 *UID:* `{ff_uid}`\n⚠️ Profile stats service abhi busy hai. Thodi der baad try karein.",
                parse_mode='Markdown',
                reply_markup=main_keyboard()
            )

    # 3. Gift Code Redeem
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

# --- ADMIN COMMANDS ---
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
        f"✅ *Gift Code Created!*\n\n"
        f"🎁 Code: `{code_name}`\n"
        f"💎 Credits: `{credits}`\n"
        f"👥 Limit: `{max_claims}`\n\n"
        f"📢 Channel me post kar sakte hain!",
        parse_mode='Markdown'
    )

if __name__ == '__main__':
    threading.Thread(target=run_web).start()
    bot.infinity_polling()
  
