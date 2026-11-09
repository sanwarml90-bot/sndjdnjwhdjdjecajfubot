import os
from pyrogram import Client, filters, types
from pyrogram.enums import ChatMembersFilter

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

welcome_msgs = {}

def get_user_id(app, message):
    if message.reply_to_message:
        return message.reply_to_message.from_user.id
    if len(message.command) > 1:
        try:
            return int(message.command[1])
        except ValueError:
            return None
    return None

@app.on_message(filters.command("start"))
async def start(app, message):
    await message.reply_text("Hello! Main group me madad karne aaya hu. /help laga kar dekh lo.")

@app.on_message(filters.command("help"))
async def help(app, message):
    help_text = (
        "Main yeh commands deta hu:\n"
        "/start - Hello message\n"
        "/mute <user> - user ko mute karo\n"
        "/unmute <user> - user ko unmute karo\n"
        "/kick <user> - user ko group se nikalo\n"
        "/ban <user> - user ko ban karo\n"
        "/unban <user> - user ko unban karo\n"
        "/promote <user> - user ko admin banao\n"
        "/demote <user> - admin ko normal banao\n"
        "/welcome <text> - group ka welcome message set karo\n"
        "/stats - group ka stats dekhlo\n"
        "/id - tumhara ya reply user ka id dekhlo"
    )
    await message.reply_text(help_text)

@app.on_message(filters.command("mute"))
async def mute(app, message):
    user_id = get_user_id(app, message)
    if user_id is None:
        await message.reply_text("Please reply to a user or provide user ID.")
        return
    try:
        await app.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            permissions=types.ChatPermissions(can_send_messages=False)
        )
        await message.reply_text(f"User {user_id} ko mute kar diya gaya.")
    except Exception as e:
        await message.reply_text(f"Mute karne me error: {e}")

@app.on_message(filters.command("unmute"))
async def unmute(app, message):
    user_id = get_user_id(app, message)
    if user_id is None:
        await message.reply_text("Please reply to a user or provide user ID.")
        return
    try:
        await app.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            permissions=types.ChatPermissions()
        )
        await message.reply_text(f"User {user_id} ko unmute kar diya gaya.")
    except Exception as e:
        await message.reply_text(f"Unmute karne me error: {e}")

@app.on_message(filters.command("kick"))
async def kick(app, message):
    user_id = get_user_id(app, message)
    if user_id is None:
        await message.reply_text("Please reply to a user or provide user ID.")
        return
    try:
        await app.kick_chat_member(chat_id=message.chat.id, user_id=user_id)
        await message.reply_text(f"User {user_id} ko group se nikal diya gaya.")
    except Exception as e:
        await message.reply_text(f"Kick karne me error: {e}")

@app.on_message(filters.command("ban"))
async def ban(app, message):
    user_id = get_user_id(app, message)
    if user_id is None:
        await message.reply_text("Please reply to a user or provide user ID.")
        return
    try:
        await app.ban_chat_member(chat_id=message.chat.id, user_id=user_id)
        await message.reply_text(f"User {user_id} ko ban kar diya gaya.")
    except Exception as e:
        await message.reply_text(f"Ban karne me error: {e}")

@app.on_message(filters.command("unban"))
async def unban(app, message):
    user_id = get_user_id(app, message)
    if user_id is None:
        await message.reply_text("Please reply to a user or provide user ID.")
        return
    try:
        await app.unban_chat_member(chat_id=message.chat.id, user_id=user_id)
        await message.reply_text(f"User {user_id} ko unban kar diya gaya.")
    except Exception as e:
        await message.reply_text(f"Unban karne me error: {e}")

@app.on_message(filters.command("promote"))
async def promote(app, message):
    user_id = get_user_id(app, message)
    if user_id is None:
        await message.reply_text("Please reply to a user or provide user ID.")
        return
    try:
        await app.promote_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            can_change_info=True,
            can_post_messages=True,
            can_edit_messages=True,
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_promote_members=True
        )
        await message.reply_text(f"User {user_id} ko admin banao gaya.")
    except Exception as e:
        await message.reply_text(f"Promote karne me error: {e}")

@app.on_message(filters.command("demote"))
async def demote(app, message):
    user_id = get_user_id(app, message)
    if user_id is None:
        await message.reply_text("Please reply to a user or provide user ID.")
        return
    try:
        await app.promote_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False
        )
        await message.reply_text(f"User {user_id} ko normal banao gaya.")
    except Exception as e:
        await message.reply_text(f"Demote karne me error: {e}")

@app.on_message(filters.command("welcome"))
async def welcome(app, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a welcome message. Usage: /welcome <text>")
        return
    welcome_text = " ".join(message.command[1:])
    welcome_msgs[message.chat.id] = welcome_text
    await message.reply_text(f"Welcome message set for this group: {welcome_text}")

@app.on_message(filters.command("stats"))
async def stats(app, message):
    try:
        chat = await app.get_chat(message.chat.id)
        member_count = chat.members_count if hasattr(chat, "members_count") else "N/A"
        admin_count = 0
        async for member in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
            admin_count += 1
        await message.reply_text(f"Group Stats:\nMembers: {member_count}\nAdmins: {admin_count}")
    except Exception as e:
        await message.reply_text(f"Stats dekhne me error: {e}")

@app.on_message(filters.command("id"))
async def id(app, message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        await message.reply_text(f"Your ID: {message.from_user.id}\nReplied user ID: {user.id} (@{user.username})")
    else:
        await message.reply_text(f"Your Telegram ID: {message.from_user.id}")

app.run()