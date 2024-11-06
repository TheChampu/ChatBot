import random
import asyncio
import re
from ChampuAPI import api
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.errors import MessageEmpty
from pyrogram.enums import ChatAction, ChatMemberStatus as CMS
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from deep_translator import GoogleTranslator
from Champu.database.chats import add_served_chat
from Champu.database.users import add_served_user
from datetime import datetime, timedelta
from Champu import Champu, mongo, LOGGER, db
from Champu.modules.helpers import chatai, storeai, languages, CHATBOT_ON
from Champu.modules.helpers import (
    ABOUT_BTN, ABOUT_READ, ADMIN_READ, BACK, CHATBOT_BACK, CHATBOT_READ,
    DEV_OP, HELP_BTN, HELP_READ, MUSIC_BACK_BTN, SOURCE_READ, START,
    TOOLS_DATA_READ,
)

translator = GoogleTranslator()
lang_db = db.ChatLangDb.LangCollection
status_db = db.chatbot_status_db.status
replies_cache = []
new_replies_cache = []

blocklist = {}
message_counts = {}


async def get_chat_language(chat_id):
    try:
        chat_lang = await lang_db.find_one({"chat_id": chat_id})
        return chat_lang["language"] if chat_lang and "language" in chat_lang else "en"
    except Exception as e:
        print(f"Error in get_chat_language: {e}")
        return "en"

            

@Champu.on_message(filters.incoming)
async def chatbot_response(client: Client, message: Message):
    global blocklist, message_counts
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        current_time = datetime.now()
        
        blocklist = {uid: time for uid, time in blocklist.items() if time > current_time}

        if user_id in blocklist:
            return

        if user_id not in message_counts:
            message_counts[user_id] = {"count": 1, "last_time": current_time}
        else:
            time_diff = (current_time - message_counts[user_id]["last_time"]).total_seconds()
            if time_diff <= 3:
                message_counts[user_id]["count"] += 1
            else:
                message_counts[user_id] = {"count": 1, "last_time": current_time}
            
            if message_counts[user_id]["count"] >= 4:
                blocklist[user_id] = current_time + timedelta(minutes=1)
                message_counts.pop(user_id, None)
                await message.reply_text(f"**Hey, {message.from_user.mention}**\n\n**You are blocked for 1 minute due to spam messages.**\n**Try again after 1 minute 🤣.**")
                return
        chat_id = message.chat.id
        chat_status = await status_db.find_one({"chat_id": chat_id})
        
        if chat_status and chat_status.get("status") == "disabled":
            return

        if message.text and any(message.text.startswith(prefix) for prefix in ["!", "/", ".", "?", "@", "#"]):
            if message.chat.type == "group" or message.chat.type == "supergroup":
                return await add_served_chat(message.chat.id)
            else:
                return await add_served_user(message.chat.id)
        
        if (message.reply_to_message and message.reply_to_message.from_user.id == shizuchat.id) or not message.reply_to_message:
            reply_data = await get_reply(message.text)

            if reply_data:
                response_text = reply_data["text"]
                chat_lang = await get_chat_language(chat_id)

                if not chat_lang or chat_lang == "nolang":
                    translated_text = response_text
                else:
                    translated_text = GoogleTranslator(source='auto', target=chat_lang).translate(response_text)
                
                if reply_data["check"] == "sticker":
                    await message.reply_sticker(reply_data["text"])
                elif reply_data["check"] == "photo":
                    await message.reply_photo(reply_data["text"])
                elif reply_data["check"] == "video":
                    await message.reply_video(reply_data["text"])
                elif reply_data["check"] == "voice":
                    await message.reply_voice(reply_data["text"])
                elif reply_data["check"] == "audio":
                    await message.reply_audio(reply_data["text"])
                elif reply_data["check"] == "gif":
                    await message.reply_animation(reply_data["text"]) 
                else:
                    await message.reply_text(translated_text)
            else:
                await message.reply_text("**I don't understand. what are you saying??**")
        
        if message.reply_to_message:
            await save_reply(message.reply_to_message, message)

        
    except MessageEmpty as e:
        return await message.reply_text("🙄🙄")
    except Exception as e:
        return


async def save_reply(original_message: Message, reply_message: Message):
    try:
        if reply_message.sticker:
            is_chat = await storeai.find_one({
                "word": original_message.text,
                "text": reply_message.sticker.file_id,
                "check": "sticker",
            })
            if not is_chat:
                await storeai.insert_one({
                    "word": original_message.text,
                    "text": reply_message.sticker.file_id,
                    "check": "sticker",
                })

        elif reply_message.photo:
            is_chat = await storeai.find_one({
                "word": original_message.text,
                "text": reply_message.photo.file_id,
                "check": "photo",
            })
            if not is_chat:
                await storeai.insert_one({
                    "word": original_message.text,
                    "text": reply_message.photo.file_id,
                    "check": "photo",
                })

        elif reply_message.video:
            is_chat = await storeai.find_one({
                "word": original_message.text,
                "text": reply_message.video.file_id,
                "check": "video",
            })
            if not is_chat:
                await storeai.insert_one({
                    "word": original_message.text,
                    "text": reply_message.video.file_id,
                    "check": "video",
                })

        elif reply_message.voice:
            is_chat = await storeai.find_one({
                "word": original_message.text,
                "text": reply_message.voice.file_id,
                "check": "voice",
            })
            if not is_chat:
                await storeai.insert_one({
                    "word": original_message.text,
                    "text": reply_message.voice.file_id,
                    "check": "voice",
                })

        elif reply_message.audio:
            is_chat = await storeai.find_one({
                "word": original_message.text,
                "text": reply_message.audio.file_id,
                "check": "audio",
            })
            if not is_chat:
                await storeai.insert_one({
                    "word": original_message.text,
                    "text": reply_message.audio.file_id,
                    "check": "audio",
                })

        elif reply_message.animation:  
            is_chat = await storeai.find_one({
                "word": original_message.text,
                "text": reply_message.animation.file_id,
                "check": "gif",
            })
            if not is_chat:
                await storeai.insert_one({
                    "word": original_message.text,
                    "text": reply_message.animation.file_id,
                    "check": "gif",
                })

        elif reply_message.text:
            translated_text = reply_message.text
            try:
                translated_text = GoogleTranslator(source='auto', target='en').translate(reply_message.text)
            except Exception as e:
                print(f"Translation error: {e}, saving original text.")
                translated_text = reply_message.text
            is_chat = await storeai.find_one({
                "word": original_message.text,
                "text": translated_text,
                "check": "none",
            })
            if not is_chat:
                await storeai.insert_one({
                    "word": original_message.text,
                    "text": translated_text,
                    "check": "text",
                })
                
    except Exception as e:
        print(f"Error in save_reply: {e}")



async def get_reply(word: str):
    try:
        is_chat = await chatai.find({"word": word}).to_list(length=None)
        if not is_chat:
            is_chat = await storeai.find({"word": word}).to_list(length=None)
            if not is_chat:
                is_chat = await chatai.find().to_list(length=None)
        return random.choice(is_chat) if is_chat else None
    except Exception as e:
        print(f"Error in get_reply: {e}")
        return None


