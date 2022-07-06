"""
                                _             
  __   _____  ___  ___ ___   __| | ___ _ __   
  \ \ / / __|/ _ \/ __/ _ \ / _` |/ _ \ '__|  
   \ V /\__ \  __/ (_| (_) | (_| |  __/ |     
    \_/ |___/\___|\___\___/ \__,_|\___|_|     

    Copyleft 2022 t.me/vsecoder                                                            
    This program is free software; you can redistribute it and/or modify 

"""
# meta developer: @vsecoder_m
# meta pic: https://img.icons8.com/color/344/antivirus-scanner--v1.png

__version__ = (3, 3, 0)

import logging
import re
import requests
from .. import loader, utils

logger = logging.getLogger(__name__)


checker_regex = {
    "critical": [
        {"command": r"DeleteAccountRequest", "perms": "delete account"},
        {"command": r"edit_2fa", "perms": "change 2FA password"},
        {"command": r"get_me", "perms": "presumably get your profile account data"},
        {"command": r"disconnect", "perms": "disconnect account"},
        {"command": r"log_out", "perms": "disconnect account"},
        {"command": r"ResetAuthorizationRequest", "perms": "kill account sessions"},
        {"command": r"GetAuthorizationsRequest", "perms": "get telegram api_id and api_hash"},
        {"command": r"AddRequest", "perms": "get telegram api_id and api_hash"},
        {"command": r"pyarmor", "perms": "all(obfuscated script)"},
        {"command": r"pyrogram", "perms": "another tg client"},
        {"command": r"system", "perms": "presumably eval commands"},
        {"command": r"eval", "perms": "presumably eval python code"},
        {"command": r"exec", "perms": "presumably exec python code"},
        {"command": r"sessions", "perms": "get all sessions data, delete sessoins, copy and send sessions"},
        {"command": r"subprocess", "perms": "eval commands"},
        {"command": r"torpy", "perms": "download viruses"},
        {"command": r"httpimport", "perms": "import malicious scripts"},
    ],
    "warn": [
        {"command": r"list_sessions", "perms": "get all account sessions"},
        {"command": r"LeaveChannelRequest", "perms": "leave channel and chats"},
        {"command": r"JoinChannelRequest", "perms": "join channel and chats"},
        {"command": r"ChannelAdminRights", "perms": "edit channel and chats users perms"},
        {"command": r"EditBannedRequest", "perms": "kick and ban users"},
        {"command": r"remove", "perms": "presumably remove files"},
        {"command": r"rmdir", "perms": "presumably remove dirs"},
        {"command": r"telethon", "perms": "telethon funcs"},
        {"command": r"get_response", "perms": "get telegram messages"},
    ],
    "council": [
        {"command": r"requests", "perms": "send requests"},
        {"command": r"get_entity", "perms": "get entities"},
        {"command": r"get_dialogs", "perms": "get dialogs"},
        {"command": r"os", "perms": "presumably get os info"},
        {"command": r"sys", "perms": "presumably get sys info"},
        {"command": r"import", "perms": "import modules"},
        {"command": r"client", "perms": "all client functions"},
        {"command": r"send_message", "perms": "send messages"},
        {"command": r"send_file", "perms": "send files"},
        {"command": r"TelegramClient", "perms": "create new session"},
        {"command": r"download_file", "perms": "download telegram files"},
        {"command": r"ModuleConfig", "perms": "create configs"},
    ]
}


@loader.tds
class CheckModulesMod(loader.Module):
    """Module for check modules"""

    strings = {
        "name": "Check module",
        "cfg_lingva_url": "Check the module for suspicious features, scam, and find out what the module has access to",
        "answer": ("🔍 <b>Module check complete</b>:\n\n⛔️ Criticals:\n{0}\n🟡 Warns:\n{1}\n✅ Councils:\n{2}"),
        "component": (" ▪️ «<code>{0}</code>» in module have permissions on <i>{1}</i>"),
        "error": "Error!\n\n.checkmod <module_link>\n.checkmod https://raw.githubusercontent.com/vsecoder/hikka_modules/main/googleit.py",
    }

    strings_ru = {
        "cfg_lingva_url": "Проверьте модуль на подозрительные возможности, скам, и узнайте к чему есть доступ у модуля",
        "answer": ("🔍 <b>Проверка модуля завершена</b>:\n\n⛔️ Критические:\n{0}\n🟡 Предупреждения:\n{1}\n✅ Советы:\n{2}"),
        "component": (" ▪️ «<code>{0}</code>» в модуле имеет разрешения на <i>{1}</i>"),
        "error": "Ошибка!\n\n.checkmod <module_link>\n.checkmod https://raw.githubusercontent.com/vsecoder/hikka_modules/main/googleit.py",
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

        await self.save_stat("download")

    async def save_stat(self, state):
        bot = "@modules_stat_bot"
        m = await self._client.send_message(bot, f"/{state} checkmods")
        await self._client.delete_messages(bot, m)

    async def on_unload(self):
        await self.save_stat("unload")

    async def check_m(self, args):
        string = args
        critical = ''
        warn = ''
        council = ''
        for command in checker_regex['critical']:
            r = re.search(command['command'], string)
            if r is not None: critical = critical + self.strings["component"].format(command['command'], command['perms']) + '\n'
        if critical == '': critical = ' ▪️ ➖\n'
        for command in checker_regex['warn']:
            r = re.search(command['command'], string)
            if r is not None: warn = warn + self.strings["component"].format(command['command'], command['perms']) + '\n'
        if warn == '': warn = ' ▪️ ➖\n'
        for command in checker_regex['council']:
            r = re.search(command['command'], string)
            if r is not None: council = council + self.strings["component"].format(command['command'], command['perms']) + '\n'
        if council == '': council = ' ▪️ ➖\n'

        return self.strings["answer"].format(critical, warn, council, args)

    @loader.unrestricted
    @loader.ratelimit
    async def checkmodcmd(self, message):
        """
         <module_link> or "reply file" or "send file" - start check module
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
