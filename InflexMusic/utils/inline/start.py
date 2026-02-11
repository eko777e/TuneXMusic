from pyrogram.types import InlineKeyboardButton

import config
from InflexMusic import app

def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users",
            )
        ],
        [
            InlineKeyboardButton(text=_["S_B_3"], url=f"https://t.me/BotAzDestek"),
            InlineKeyboardButton(text=_["S_B_6"], url=f"https://t.me/BotAzNews")
        ],
        
    ]
    return buttons
