import asyncio

import coffeehouse
from coffeehouse.lydia import LydiaAI
from telethon import events
from jarvis.utils import admin_cmd, sudo_cmd, edit_or_reply
# Non-SQL Mode
ACC_LYDIA = {}
SESSION_ID = {}

if Var.LYDIA_API_KEY:
    api_key = Var.LYDIA_API_KEY
    api_client = coffeehouse.API(api_key)
    Lydia = LydiaAI(api_client)


@jarvis.on(admin_cmd(pattern="repcf", outgoing=True))
@jarvis.on(sudo_cmd(pattern="repcf",allow_sudo=True))
async def repcf(event):
    if event.fwd_from:
        return
    await edit_or_reply(event,"Processing...")
    try:
        session = Lydia.create_session()
        session_id = session.id
        reply = await event.get_reply_message()
        msg = reply.text
        text_rep = session.think_thought((session_id, msg))
        await edit_or_reply(event," {0}".format(text_rep))
    except Exception as e:
        await edit_or_reply(event,str(e))


@jarvis.on(admin_cmd(pattern="addcf", outgoing=True))
@jarvis.on(sudo_cmd(pattern="addcf",allow_sudo=True))
async def addcf(event):
    if event.fwd_from:
        return
    await edit_or_reply(event,"Running on NON-SQL mode for now...")
    await asyncio.sleep(3)
    await event.edit("Processing...")
    reply_msg = await event.get_reply_message()
    if reply_msg:
        session = Lydia.create_session()
        session_id = session.id
        ACC_LYDIA.update({str(event.chat_id) + " " + str(reply_msg.from_id): session})
        SESSION_ID.update(
            {str(event.chat_id) + " " + str(reply_msg.from_id): session_id}
        )
        await event.edit(
            "Lydia Activated successfully enabled for user: {} in chat: {}".format(
                str(reply_msg.from_id), str(event.chat_id)
            )
        )
    else:
        await event.edit("Reply to a user to activate JARVIS AI on them")


@jarvis.on(admin_cmd(pattern="remcf", outgoing=True))
@jarvis.on(sudo_cmd(pattern="remcf",allow_sudo=True))
async def remcf(event):
    if event.fwd_from:
        return
    await edit_or_reply(event,"Running on NON-SQL mode for now...")
    await asyncio.sleep(3)
    await event.edit("Processing...")
    reply_msg = await event.get_reply_message()
    try:
        del ACC_LYDIA[str(event.chat_id) + " " + str(reply_msg.from_id)]
        del SESSION_ID[str(event.chat_id) + " " + str(reply_msg.from_id)]
        await event.edit(
            "Lydia successfully disabled for user: {} in chat: {}".format(
                str(reply_msg.from_id), str(event.chat_id)
            )
        )
    except KeyError:
        await event.edit("This person does not have Lydia activated on him/her.")


@bot.on(events.NewMessage(incoming=True))
async def user(event):
    event.text
    try:
        session = ACC_LYDIA[str(event.chat_id) + " " + str(event.sender_id)]
        session_id = SESSION_ID[str(event.chat_id) + " " + str(event.sender_id)]
        msg = event.text
        async with event.client.action(event.chat_id, "typing"):
            text_rep = session.think_thought((session_id, msg))
            wait_time = 0
            for i in range(len(text_rep)):
                wait_time = wait_time + 0.1
            await asyncio.sleep(wait_time)
            await event.reply(text_rep)
    except KeyError:
        return