"""
                                _             
  __   _____  ___  ___ ___   __| | ___ _ __   
  \ \ / / __|/ _ \/ __/ _ \ / _` |/ _ \ '__|  
   \ V /\__ \  __/ (_| (_) | (_| |  __/ |     
    \_/ |___/\___|\___\___/ \__,_|\___|_|     

    Copyleft 2022 t.me/vsecoder                                                            
    This program is free software; you can redistribute it and/or modify 

"""

__version__ = (2, 0, 0)

import logging
from aiogram.types import Message as AiogramMessage
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.unrestricted
@loader.ratelimit
@loader.tds
class BioPageMod(loader.Module):
    """Module for create bio page"""

    strings = {
        "name": "Bio Page",
        "answer": ("📦 The configuration of the <b>BioPage</b> is set to <code>\"{0}\"</code>"),
        "error": "❗️ Error, check logs!",
    }

    strings_ru = {
        "answer": ("📦 Конфигурация <b>BioPage</b> установлена <code>\"{0}\"</code>"),
        "error": "❗️ Ошибка, проверьте логи!",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "toggle",
                "off",
                lambda m: "Toggle bio page on/off",
            ),
            loader.ConfigValue(
                "bio_url",
                "https://vsecoder.github.io/tg-web-app/",
                lambda m: "Bio page url(need restart toggle)",
            ),
        )
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self.botfather = "@BotFather"

        await self.save_stat("download")

    async def save_stat(self, state):
        bot = "@modules_stat_bot"
        m = await self._client.send_message(bot, f"/{state} biopage")
        await self._client.delete_messages(bot, m)

    async def on_unload(self):
        await self.save_stat("unload")
        
    async def bot_conifg(self, toggle):
        if toggle == "on":
            async with self._client.conversation(self.botfather) as conv:
                await conv.send_message("/setmenubutton")
                await conv.mark_read()
                await conv.send_message(f"@{self.inline.bot_username}")
                await conv.mark_read()
                await conv.send_message(self.config['bio_url'])
                await conv.mark_read()
                await conv.send_message("🔗 Bio")
                await conv.mark_read()
        elif toggle == "off":
            async with self._client.conversation(self.botfather) as conv:
                await conv.send_message("/setmenubutton")
                await conv.mark_read()
                await conv.send_message(f"@{self.inline.bot_username}")
                await conv.mark_read()
                await conv.send_message('/empty')
                await conv.mark_read()
        
    @loader.unrestricted
    @loader.ratelimit
    async def biotogglecmd(self, message):
        """
         - toggle bio page(default: off)
        Based on... my code)
        """
        try:
            toggle = self.config['toggle']
            if toggle == 'on':
                self.config['toggle'] = 'off'
            else:
                self.config['toggle'] = 'on'
            await self.bot_conifg(self.config['toggle'])
            await utils.answer(message, self.strings["answer"].format(self.config['toggle']))
        except:
            pass