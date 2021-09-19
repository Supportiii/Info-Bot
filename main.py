# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/Info-Bot/blob/main/LICENSE

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

FayasNoushad = Client(
    "Info-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

START_TEXT = """
Hola {}, Mit diesem Bot kannst du verschiedene tolle Dinge tun!
- Sende /info für deine Info
- Antworte /info auf eine weitergeleitete Nachricht für die ChatInfo/UserInfo
"""
BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⚙ Mein erhärmlicher Kanal ⚙', url='https://t.me/iSupCh')
        ]]
    )

@FayasNoushad.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    text = START_TEXT.format(update.from_user.mention)
    reply_markup = BUTTONS
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )

@FayasNoushad.on_message((filters.private | filters.group) & filters.command(["info", "information"]))
async def info(bot, update):
    if (not update.reply_to_message) and ((not update.forward_from) or (not update.forward_from_chat)):
        info = user_info(update.from_user)
    elif update.reply_to_message and update.reply_to_message.forward_from:
        info = user_info(update.reply_to_message.forward_from)
    elif update.reply_to_message and update.reply_to_message.forward_from_chat:
        info = chat_info(update.reply_to_message.forward_from_chat)
    elif (update.reply_to_message and update.reply_to_message.from_user) and (not update.forward_from or not update.forward_from_chat):
        info = user_info(update.reply_to_message.from_user)
    else:
        return
    try:
        await update.reply_text(
            text=info,
            reply_markup=BUTTONS,
            disable_web_page_preview=True,
            quote=True
        )
    except Exception as error:
        await update.reply_text(error)

def user_info(user):
    text = "--**Nutzer Informationen:**--\n"
    text += f"\n**VorName:** `{user.first_name}`"
    text += f"\n**NachName:** `{user.last_name},`" if user.last_name else ""
    text += f"\n**Nutzername:** @{user.username}" if user.username else ""
    text += f"\n**Link:** {user.mention}" if user.username else ""
    text += f"\n**Id:** `{user.id}`"
    text += f"\n**DC:** `{user.dc_id}`" if user.dc_id else ""
    text += f"\n**Gelöscht:** True" if user.is_deleted else ""
    text += f"\n**Bot:** True" if user.is_bot else ""
    text += f"\n**Verifiziert:** True" if user.is_verified else ""
    text += f"\n**Eingeschränkt:** True" if user.is_verified else ""
    text += f"\n**Betrug:** True" if user.is_scam else ""
    text += f"\n**Fake:** True" if user.is_fake else ""
    text += f"\n**Support:** True" if user.is_support else ""
    text += f"\n**Sprach-Code:** {user.language_code}" if user.language_code else ""
    text += f"\n**Status:** {user.status}" if user.status else ""
    text += f"\n\nGemacht von @TLGRM_Support"
    return text

def chat_info(chat):
    text = "--**Chat-Informationen**--\n" 
    text += f"\n**Titel:** `{chat.title}`"
    text += f"\n**Nutzername:** @{chat.username}" if chat.username else ""
    text += f"\n**Art:** `{chat.type}`"
    text += f"\n**ID:** `{chat.id}`"
    text += f"\n**DC:** `{chat.dc_id}`"
    text += f"\n**Verifiziert:** True" if chat.is_verified else ""
    text += f"\n**Eingeschränkt:** True" if chat.is_verified else ""
    text += f"\n**Ersteller*in:** True" if chat.is_creator else ""
    text += f"\n**Betrug:** True" if chat.is_scam else ""
    text += f"\n**Fake:** True" if chat.is_fake else ""
    text += f"\n\nGemacht von @TLGRM_Support"
    return text

FayasNoushad.run()
