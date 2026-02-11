from typing import Union

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from InflexMusic import app


def help_pannel():
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="⬅️ Geri",
                    callback_data="settingsback_helper",
                )
            ]
        ]
    )

    text = """
<b>Mənim Əmrlərim:</b>

/play - musiqi oxudar
/skip - musiqini keçər
/stop • /end - musiqini dayandırar.
"""

    return text, buttons

def help_back_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data=f"settings_back_helper",
                ),
            ]
        ]
    )
    return upl


def private_help_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                url=f"https://t.me/{app.username}?start=help",
            ),
        ],
    ]
    return buttons
