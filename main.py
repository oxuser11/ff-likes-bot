import os, json, time, threading, requests, telebot
from telebot import types
from flask import Flask

# 1. Web Server 24/7
app = Flask(__name__)
@app.route('/')
def home(): return "BOT ONLINE 24/7"
def run_web(): app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# 2. Configs
BOT_TOKEN = "8708303127:AAHE2yb5TU9jfeFrtx3RaDhY5oS97DoDOF0"
ADMIN_ID = 8671410379
ADMIN_USER = "OxRehann"
CH_ID, CH_URL = "@OxRehanCyber", "https://t.me/OxRehanCyber"
IG_URL = "https://instagram.com/ox.mods"
KV_URL = "https://api.keyval.org/ox_ff_likes_vault_2026"
DB_FILE = "ff_likes_db.json"

bot = telebot.TeleBot(BOT_TOKEN)
user_states, active_rep = {}, {}
HDR = {"User-Agent": "Mozilla/5.0"}

# 3. Database
def load_db():
    try:
        r = requests.get(KV_URL, timeout=4).json()
        if isinstance(r, dict) and "users" in r: return r
    except: pass
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f: return json.load(f)
        except: pass
    return {"users": {}, "gift_codes": {}}

def save_db(data):
    try:
        with open(DB_FILE, 'w') as f: json.dump(data, f)
    except: pass
    try: requests.post(KV_URL, json=data, timeout=4)
    except: pass

db = load_db()

def get_user(uid):
    s = str(uid)
    if s not in db["users"]:
        db["users"][s] = {"credits": 2, "referrals": 0, "likes_sent": 0}
        save_db(db)
    return db["users"][s]

def is_sub(uid):
    try: return bot.get_chat_member(CH_ID, uid).status in ['member', 'administrator', 'creator']
    except: return True

# 4. Keyboards
def fjoin_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("📢 JOIN TELEGRAM CHANNEL", url=CH_URL),
        types.InlineKeyboardButton("📸 FOLLOW INSTAGRAM (@ox.mods)", url=IG_URL),
        types.InlineKeyboardButton("⚡ VERIFY & UNLOCK ⚡", callback_data="check_joined")
    )
    return kb

def main_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        types.KeyboardButton("❤️‍🔥 FREE LIKES (50 LIKES)"),
        types.KeyboardButton("📊 PLAYER STATS CARD"),
        types.KeyboardButton("🚨 AUTO REPORT PLAYER"),
        types.KeyboardButton("💎 MY BALANCE"),
        types.KeyboardButton("👥 REFER & EARN"),
        types.KeyboardButton("🎁 REDEEM GIFT CODE"),
        types.KeyboardButton("🛍️ BUY LIKES PACK")
    )
    return kb

# 5. Commands & Buttons
@bot.message_handler(commands=['start'])
def start(m):
    uid, s = m.from_user.id, str(m.from_user.id)
    txt = m.text.split()
    if s not in db["users"]:
        if len(txt) > 1 and txt[1].isdigit() and txt[1] in db["users"] and txt[1] != s:
            db["users"][txt[1]]["credits"] += 5
            db["users"][txt[1]]["referrals"] += 1
            try: bot.send_message(int(txt[1]), "🎉 *New Referral!* +5 Credits add ho gaye!", parse_mode='Markdown')
            except: pass
        db["users"][s] = {"credits": 2, "referrals": 0, "likes_sent": 0}
        save_db(db)
    if not is_sub(uid):
        bot.reply_to(m, f"👋 *Welcome {m.from_user.first_name}!*\n\nPehle dono channel join karein aur verify karein:", parse_mode='Markdown', reply_markup=fjoin_kb())
        return
    bot.reply_to(m, f"🔥 *FREE FIRE TOOL BOT*\n\n👋 Namaste *{m.from_user.first_name}*!\n🎁 +2 Bonus Credits added!", parse_mode='Markdown', reply_markup=main_kb())

@bot.callback_query_handler(func=lambda c: c.data == "check_joined")
def ver_call(c):
    if is_sub(c.from_user.id):
        bot.delete_message(c.message.chat.id, c.message.message_id)
        bot.send_message(c.message.chat.id, "✅ *Verified!* Menu select karein:", parse_mode='Markdown', reply_markup=main_kb())
    else: bot.answer_callback_query(c.id, "❌ Pehle channels join karein!", show_alert=True)

@bot.message_handler(func=lambda m: m.text == "💎 MY BALANCE")
def bal(m):
    u = get_user(m.from_user.id)
    bot.reply_to(m, f"👤 *Player:* {m.from_user.first_name}\n🆔 *ID:* `{m.from_user.id}`\n\n💎 *Credits:* `{u['credits']}`\n👥 *Referrals:* `{u['referrals']}`\n❤️ *Likes Sent:* `{u['likes_sent']}`\n\n📌 10 Credits = 50 Likes", parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "👥 REFER & EARN")
def ref(m):
    bot.reply_to(m, f"🔥 *REFER & EARN*\n\n💎 Per Refer = 5 Credits\n🎯 2 Refer = 50 Likes\n\n🔗 *Link:* `https://t.me/{bot.get_me().username}?start={m.from_user.id}`", parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "🛍️ BUY LIKES PACK")
def buy(m):
    bot.reply_to(m, f"🛍️ *LIKES PRICING*\n\n• 50 Likes = ₹15\n• 100 Likes = ₹25\n• 300 Likes = ₹60\n• 1,000 Likes = ₹150\n\n👉 Contact: @{ADMIN_USER}", parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "❤️‍🔥 FREE LIKES (50 LIKES)")
def ask_l(m):
    if get_user(m.from_user.id)["credits"] < 10:
        bot.reply_to(m, "⚠️ 50 Likes ke liye 10 Credits chahiye! Refer karein ya Buy karein.", parse_mode='Markdown')
        return
    user_states[m.from_user.id] = "likes"
    bot.reply_to(m, "🔢 Apni Free Fire **Numeric UID** bhejein:\n_(Cancel: /cancel)_")

@bot.message_handler(func=lambda m: m.text == "📊 PLAYER STATS CARD")
def ask_s(m):
    user_states[m.from_user.id] = "stats"
    bot.reply_to(m, "🔍 Check karne ke liye **Numeric UID** bhejein:\n_(Cancel: /cancel)_")

@bot.message_handler(func=lambda m: m.text == "🚨 AUTO REPORT PLAYER")
def ask_r(m):
    user_states[m.from_user.id] = "rep"
    bot.reply_to(m, "🚨 Mass report ke liye target **Numeric UID** bhejein:\n_(Cancel: /cancel)_")

@bot.message_handler(func=lambda m: m.text == "🎁 REDEEM GIFT CODE")
def ask_g(m):
    user_states[m.from_user.id] = "gift"
    bot.reply_to(m, "🎁 Apna **Gift Code** yahan enter karein:\n_(Cancel: /cancel)_")

@bot.message_handler(commands=['cancel'])
def can(m):
    user_states.pop(m.from_user.id, None)
    bot.reply_to(m, "❌ Canceled.", reply_markup=main_kb())

# 6. Inputs & Background Tasks
@bot.message_handler(func=lambda m: m.from_user.id in user_states)
def handle_inputs(m):
    uid = m.from_user.id
    st = user_states.pop(uid, None)

    if st == "likes":
        fuid = m.text.strip()
        if not fuid.isdigit() or len(fuid) < 7:
            bot.reply_to(m, "❌ Invalid UID! Valid numeric UID enter karein.")
            return
        u = get_user(uid)
        if u["credits"] < 10: return
        u["credits"] -= 10
        u["likes_sent"] += 50
        save_db(db)
        try: requests.get(f"https://like-api-freefire.vercel.app/api?uid={fuid}&server_name=ind", headers=HDR, timeout=8)
        except: pass
        bot.reply_to(m, f"🎉 *50 Likes Sent!* ❤️‍🔥\n\n🎯 UID: `{fuid}`\n💎 Balance: `{u['credits']}`", parse_mode='Markdown', reply_markup=main_kb())

    elif st == "stats":
        fuid = m.text.strip()
        if not fuid.isdigit(): return
        bot.reply_to(m, f"🔍 Fetching UID `{fuid}`...")
        info = None
        for u in [f"https://www.freefireapi.me/api/info?uid={fuid}", f"https://freefire-virusteam.vercel.app/info?uid={fuid}&region=ind"]:
            try:
                r = requests.get(u, headers=HDR, timeout=6).json()
                if r:
                    info = r.get("AccountInfo") or r.get("basicInfo") or r
                    break
            except: pass
        if info:
            name = info.get("nickname") or info.get("AccountName") or info.get("name") or "Player"
            lvl = info.get("level") or info.get("AccountLevel") or "N/A"
            lik = info.get("likes") or info.get("AccountLikes") or "N/A"
            reg = info.get("region") or "IND"
            bio = info.get("signature") or "None"
            bot.reply_to(m, f"🎮 *PROFILE CARD*\n\n👤 *IGN:* `{name}`\n🆔 *UID:* `{fuid}`\n⭐ *Level:* `{lvl}`\n❤️ *Likes:* `{lik}`\n🌍 *Server:* `{reg}`\n📝 *Bio:* `{bio}`", parse_mode='Markdown', reply_markup=main_kb())
        else:
            bot.reply_to(m, f"⚠️ UID `{fuid}` details fetch nahi ho payi. Server busy hai.", reply_markup=main_kb())

    elif st == "rep":
        fuid = m.text.strip()
        if not fuid.isdigit(): return
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("⚠️ START MASS REPORT", callback_data=f"rp_go_{fuid}"), types.InlineKeyboardButton("❌ CANCEL", callback_data="rp_cx"))
        bot.reply_to(m, f"🚨 *CONFIRM TARGET*\n\n🆔 UID: `{fuid}`\nKya aap automated reporting start karna chahte hain?", parse_mode='Markdown', reply_markup=kb)

    elif st == "gift":
        code = m.text.strip().upper()
        s, codes = str(uid), db.get("gift_codes", {})
        if code not in codes:
            bot.reply_to(m, "❌ Invalid/Expired Code!", reply_markup=main_kb()); return
        gc = codes[code]
        if s in gc["users"]:
            bot.reply_to(m, "⚠️ Pehle hi claim kar chuke hain!", reply_markup=main_kb()); return
        if len(gc["users"]) >= gc["max_claims"]:
            bot.reply_to(m, "⚠️ Code limit full ho gayi!", reply_markup=main_kb()); return
        u = get_user(uid)
        u["credits"] += gc["credits"]
        gc["users"].append(s)
        save_db(db)
        bot.reply_to(m, f"🎉 *Redeemed!* +{gc['credits']} Credits!\nBalance: `{u['credits']}`", parse_mode='Markdown', reply_markup=main_kb())

def run_rep_task(cid, mid, uid, fuid):
    active_rep[uid] = True
    stop_kb = types.InlineKeyboardMarkup()
    stop_kb.add(types.InlineKeyboardButton("🛑 STOP REPORT", callback_data=f"rp_stop_{uid}"))
    for i in range(1, 26):
        if not active_rep.get(uid, False): break
        try: requests.get(f"https://like-api-freefire.vercel.app/api?uid={fuid}&server_name=ind", headers=HDR, timeout=4)
        except: pass
        try: bot.edit_message_text(f"🚨 *REPORTING...*\n\n🎯 UID: `{fuid}`\n📊 Status: `{i}/25 Reports Sent`", chat_id=cid, message_id=mid, parse_mode='Markdown', reply_markup=stop_kb)
        except: pass
        time.sleep(2)
    active_rep.pop(uid, None)
    try: bot.edit_message_text(f"🛑 *Reporting Finished/Stopped for UID `{fuid}`.*", chat_id=cid, message_id=mid, parse_mode='Markdown')
    except: pass

@bot.callback_query_handler(func=lambda c: c.data.startswith("rp_"))
def rep_calls(c):
    if c.data.startswith("rp_go_"):
        fuid = c.data.split("_")[2]
        bot.answer_callback_query(c.id, "🚨 Report Started!")
        threading.Thread(target=run_rep_task, args=(c.message.chat.id, c.message.message_id, c.from_user.id, fuid)).start()
    elif c.data.startswith("rp_stop_"):
        active_rep[c.from_user.id] = False
        bot.answer_callback_query(c.id, "🛑 Stopping...", show_alert=True)
    elif c.data == "rp_cx":
        bot.delete_message(c.message.chat.id, c.message.message_id)

# 7. Admin Commands
@bot.message_handler(commands=['all'])
def admin_all(m):
    if m.from_user.id != ADMIN_ID: return
    p = m.text.split(maxsplit=1)
    if len(p) < 2: return
    s, f = 0, 0
    for u in list(db.get("users", {}).keys()):
        try:
            bot.send_message(int(u), f"📢 *NOTIFICATION*\n\n{p[1]}", parse_mode='Markdown')
            s += 1; time.sleep(0.05)
        except: f += 1
    bot.send_message(m.chat.id, f"✅ Done! Sent: {s}, Failed: {f}")

@bot.message_handler(commands=['gen'])
def admin_gen(m):
    if m.from_user.id != ADMIN_ID: return
    p = m.text.split()
    if len(p) != 4:
        bot.reply_to(m, "Usage: `/gen <NAME> <CREDITS> <MAX_USERS>`")
        return
    code, cred, lim = p[1].upper(), int(p[2]), int(p[3])
    if "gift_codes" not in db: db["gift_codes"] = {}
    db["gift_codes"][code] = {"credits": cred, "max_claims": lim, "users": []}
    save_db(db)
    bot.reply_to(m, f"✅ *Code Created!*\n🎁 Code: `{code}`\n💎 Credits: `{cred}`\n👥 Limit: `{lim}`", parse_mode='Markdown')

if __name__ == '__main__':
    threading.Thread(target=run_web).start()
    bot.infinity_polling()
