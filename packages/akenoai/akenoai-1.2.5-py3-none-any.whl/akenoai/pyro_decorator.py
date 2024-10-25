from functools import wraps

from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message

import akenoai.logger as akeno


def with_premium(func):
    async def wrapper(client: Client, message: Message):
        if not client.me.is_premium:
            await message.edit_text("<b>Premium account is required</b>")
        else:
            return await func(client, message)
    return wrapper

def disable_command(command=None):
    def decorator(func):
        @Client.on_message(~filters.command(command))
        async def wrapper(client: Client, message: Message):
            await func(client, message)
        return wrapper
    return decorator

def format_user_info(user) -> str:
    return (
        f"UserID: {user.id if user else 0}\n"
        f"Username: {user.username if user else None}\n"
        f"First Name: {user.first_name if user else ''}\n"
    )

def LogChannel(channel_id=None, is_track: bool = False):
    def decorator(func):
        @wraps(func)
        async def wrapper(client: Client, message: Message):
            if is_track:
                try:
                    formatting = format_user_info(message.from_user)
                    await client.send_message(channel_id, formatting)
                except Exception as e:
                    await akeno.warning(str(e))
            else:
                return False
            return await func(client, message)
        return wrapper
    return decorator

def check_is_admin(status: bool = True):
    def decorator(func):
        @wraps(func)
        async def wrapper(client: Client, message: Message):
            if status:
                try:
                    member = await client.get_chat_member(message.chat.id, "me")
                    if member.status != ChatMemberStatus.ADMINISTRATOR:
                        return await message.reply_text("I am not an administrator in this group.")
                except Exception as e:
                    return await message.reply_text(f"Error while checking admin status: {e}")
                return await func(client, message)
            else:
                return await message.reply_text("Admin check is disabled.")
        return wrapper
    return decorator
