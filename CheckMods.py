"""
                                _             
  __   _____  ___  ___ ___   __| | ___ _ __   
  \ \ / / __|/ _ \/ __/ _ \ / _` |/ _ \ '__|  
   \ V /\__ \  __/ (_| (_) | (_| |  __/ |     
    \_/ |___/\___|\___\___/ \__,_|\___|_|     

    Copyleft 2022 t.me/vsecoder                                                            
    This program is free software; you can redistribute it and/or modify 

"""

__version__ = (1, 0, 0)

import logging
import asyncio
import re
import requests
from .. import loader, utils

logger = logging.getLogger(__name__)


checker_regex = {
    "critical": [
        {"command": r"DeleteAccountRequest", "perms": "delete account"},
        {"command": r"edit_2fa", "perms": "change 2FA password"},
        #{"command": r"phone", "perms": "get your account phone number"},
        {"command": r"get_me", "perms": "get your profile account data"},
        {"command": r"disconnect", "perms": "disconnect account"},
        {"command": r"log_out", "perms": "disconnect account"},
        {"command": r"ResetAuthorizationRequest", "perms": "kill account sessions"},
        {"command": r"GetAuthorizationsRequest", "perms": "get telegram api_id and api_hash"},
        {"command": r"AddRequest", "perms": "get telegram api_id and api_hash"},
        {"command": r"pyarmor", "perms": "all(obfuscated script)"},
        {"command": r"pyrogram", "perms": "another tg client"},
        {"command": r"system", "perms": "eval commands"},
        {"command": r"eval", "perms": "eval python code"},
        {"command": r"sessions", "perms": "get all sessions data, delete sessoins, copy and send sessions"},
        {"command": r"subprocess", "perms": "eval commands"},
    ],
    "warn": [
        {"command": r"list_sessions", "perms": "get all account sessions"},
        {"command": r"LeaveChannelRequest", "perms": "leave channel and chats"},
        {"command": r"JoinChannelRequest", "perms": "join channel and chats"},
        {"command": r"ChannelAdminRights", "perms": "edit channel and chats users perms"},
        {"command": r"EditBannedRequest", "perms": "kick and ban users"},
        {"command": r" os ", "perms": "full OS access"},
        {"command": r" sys ", "perms": "full system access"},
        {"command": r" remove ", "perms": "remove files"},
        {"command": r"rmdir", "perms": "remove dirs"},
    ],
    "council": [
        {"command": r"requests", "perms": "send requests"},
        {"command": r"get_entity", "perms": "get entities"},
        {"command": r"get_dialogs", "perms": "get dialogs"},
        {"command": r" os ", "perms": "get os info"},
        {"command": r" sys ", "perms": "get sys info"},
        {"command": r"import", "perms": "import modules"},
        {"command": r"client", "perms": "all client functions"},
        {"command": r"send_message", "perms": "send messages"},
        {"command": r"send_file", "perms": "send files"},
        {"command": r"TelegramClient", "perms": "create new session"},
    ]
}



@loader.unrestricted
@loader.ratelimit
@loader.tds
class CheckModulesMod(loader.Module):
    """Module for check modules"""

    strings = {
        "name": "Check module",
        "cfg_lingva_url": "Check the module for suspicious features, scam, and find out what the module has access to",
        "answer": ("""🔍 <b>Module check complete</b>:

⛔️ Criticals:
{0}
🟡 Warns:
{1}
✅ Councils:
{2}"""),
        "component": (" ▪️ «<code>{0}</code>» in module have permissions on <i>{1}</i>"),
        "error": "Error!\n\n.checkmod <module_link>\n.checkmod https://raw.githubusercontent.com/vsecoder/hikka_modules/main/googleit.py",
    }

    strings_ru = {
        "cfg_lingva_url": "Проверьте модуль на подозрительные возможности, скам, и узнайте к чему есть доступ у модуля",
        "answer": ("""🔍 <b>Проверка модуля завершена</b>:

⛔️ Критические:
{0}
🟡 Предупреждения:
{1}
✅ Советы:
{2}"""),
        "component": (" ▪️ «<code>{0}</code>» в модуле имеет разрешения на <i>{1}</i>"),
        "error": "Ошибка!\n\n.checkmod <module_link>\n.checkmod https://raw.githubusercontent.com/vsecoder/hikka_modules/main/googleit.py",
    }

    async def check_m(self, args):
        string = args
        critical = ''
        warn = ''
        council = ''
        for command in checker_regex['critical']:
            r = re.search(command['command'], string)
            if r != None: critical = critical + self.strings["component"].format(command['command'], command['perms']) + '\n'
        if critical == '': critical = ' ▪️ ➖\n'
        for command in checker_regex['warn']:
            r = re.search(command['command'], string)
            if r != None: warn = warn + self.strings["component"].format(command['command'], command['perms']) + '\n'
        if warn == '': warn = ' ▪️ ➖\n'
        for command in checker_regex['council']:
            r = re.search(command['command'], string)
            if r != None: council = council + self.strings["component"].format(command['command'], command['perms']) + '\n'
        if council == '': council = ' ▪️ ➖\n'

        return self.strings["answer"].format(critical, warn, council, args)

    @loader.unrestricted
    @loader.ratelimit
    async def checkmodcmd(self, message):
        """
         <module_link> or "reply file" or "send file" - start check module
        Based on... my code code)
        Made with <3 by @vsecoder
        """
        args = ''
        try:
            args = utils.get_args_raw(message)
        except:
            pass
        if args:
            try:
                r = requests.get(args)
                string = r.text
                return await utils.answer(message, await self.check_m(string))
            except:
                pass
        try:
            code_from_message = (
                await self._client.download_file(message.media, bytes)
            ).decode("utf-8")
        except Exception:
            code_from_message = ""

        try:
            reply = await message.get_reply_message()
            code_from_reply = (
                await self._client.download_file(reply.media, bytes)
            ).decode("utf-8")
        except Exception:
            code_from_reply = ""

        args = code_from_message or code_from_reply
        return await utils.answer(message, await self.check_m(args))