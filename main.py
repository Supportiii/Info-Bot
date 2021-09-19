# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/Info-Bot/blob/main/LICENSE

import os
import requests
from requests.utils import requote_uri
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

FayasNoushad = Client(
    "Info-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

API = "https://api.sumanjay.cf/covid/?country="

START_TEXT = """
Hello {}, I am a Bot for all!

- /info Shows your Info
- /covid Shows covid numbers
"""
BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⚙ Join Channel ⚙', url='https://t.me/iSupCh')
        ]]
    )

@FayasNoushad.on_message(filters.private & filters.command(["info"]))
async def start(bot, update):
    text = START_TEXT.format(update.from_user.mention)
    reply_markup = BUTTONS
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )
    
@FayasNoushad.on_message(filters.private & filters.text)
async def reply_info(bot, update):
    reply_markup = BUTTONS
    await update.reply_text(
        text=covid_info(update.text),
        disable_web_page_preview=True,
        quote=True,
        reply_markup=reply_markup
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

def user_info(user):
    text = "--**User Details:**--\n"
    text += f"\n**First Name:** `{user.first_name}`"
    text += f"\n**Last Name:** `{user.last_name},`" if user.last_name else ""
    text += f"\n**User Id:** `{user.id}`"
    text += f"\n**Username:** @{user.username}" if user.username else ""
    text += f"\n**User Link:** {user.mention}" if user.username else ""
    text += f"\n**DC ID:** `{user.dc_id}`" if user.dc_id else ""
    text += f"\n**Is Deleted:** True" if user.is_deleted else ""
    text += f"\n**Is Bot:** True" if user.is_bot else ""
    text += f"\n**Is Verified:** True" if user.is_verified else ""
    text += f"\n**Is Restricted:** True" if user.is_verified else ""
    text += f"\n**Is Scam:** True" if user.is_scam else ""
    text += f"\n**Is Fake:** True" if user.is_fake else ""
    text += f"\n**Is Support:** True" if user.is_support else ""
    text += f"\n**Language Code:** {user.language_code}" if user.language_code else ""
    text += f"\n**Status:** {user.status}" if user.status else ""
    text += f"\n\nMade by @FayasNoushad"
    return text

def chat_info(chat):
    text = "--**Chat Details**--\n" 
    text += f"\n**Title:** `{chat.title}`"
    text += f"\n**Chat ID:** `{chat.id}`"
    text += f"\n**Username:** @{chat.username}" if chat.username else ""
    text += f"\n**Type:** `{chat.type}`"
    text += f"\n**DC ID:** `{chat.dc_id}`"
    text += f"\n**Is Verified:** True" if chat.is_verified else ""
    text += f"\n**Is Restricted:** True" if chat.is_verified else ""
    text += f"\n**Is Creator:** True" if chat.is_creator else ""
    text += f"\n**Is Scam:** True" if chat.is_scam else ""
    text += f"\n**Is Fake:** True" if chat.is_fake else ""
    text += f"\n\nMade by @FayasNoushad"
    return text

def covid_info(country_name):
    try:
        r = requests.get(API + requote_uri(country_name.lower()))
        info = r.json()
        country = info['country'].capitalize()
        active = info['active']
        confirmed = info['confirmed']
        deaths = info['deaths']
        info_id = info['id']
        last_update = info['last_update']
        latitude = info['latitude']
        longitude = info['longitude']
        recovered = info['recovered']
        covid_info = f"""
--**Covid 19 Information**--
Country : `{country}`
Actived : `{active}`
Confirmed : `{confirmed}`
Deaths : `{deaths}`
ID : `{info_id}`
Last Update : `{last_update}`
Latitude : `{latitude}`
Longitude : `{longitude}`
Recovered : `{recovered}`
Made by @FayasNoushad
"""
        return covid_info
    except Exception as error:
        return error
    await update.reply_text(error)

FayasNoushad.run()
