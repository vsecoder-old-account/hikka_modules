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
# meta pic: https://img.icons8.com/fluency/344/pen-1.png

__version__ = (1, 0, 0)

import logging
from .. import loader, utils

import datetime as dt
import re

logger = logging.getLogger(__name__)

@loader.tds
class FormatterMod(loader.Module):
    """
    Module for prettyfy formatting messages 🪛

    📌 To sample write:
    --------------------
    Hi, now is {now}, today is {today}, yesterday is {yesterday}, my id is {id}, username is @{username}...

    ⌨️ Keyboard:
    ~
    📥 Modules $ https://t.me/vsecoder_m
    👨‍💻 Dev $ https://t.me/vsecoder
    --------------------

    P.S. "~" is a separator for keyboard and message.
         "/" is a separator for button and link.
    
    """

    strings = {
        "name": "Formatter 🪛",
    }

    async def client_ready(self, client, db):
        self._client = client

        self.me = await client.get_me()
        
        await self.save_stat("download")

    async def save_stat(self, state):
        bot = "@modules_stat_bot"
        m = await self._client.send_message(bot, f"/{state} formatter")
        await self._client.delete_messages(bot, m)

    async def on_unload(self):
        await self.save_stat("unload")

    async def watcher(self, message):
        try:
            if message.from_id != self.me.id:
                return
            self.formats = {
                "now": dt.datetime.now(),
                "today": dt.date.today(),
                "yesterday": dt.date.today() - dt.timedelta(days=1),
                "id": self._client._tg_id,
                "username": self.me.username,
                "phone": self.me.phone,
                "msg": message,
            }

            text = message.text
            for i in self.formats:
                to = "{"+i+"}"
                if to in text:
                    text = text.replace(to, str(self.formats[i]))
            keyboard = []
            if len(text.split('\n~\n')) == 2:
                keyb = text.split('\n~\n')[1]
                keyb = keyb.split('\n')
                for key in keyb:
                    if len(key.split(' $ ')) == 2:
                        button = key.split(' $ ')[0]
                        CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
                        link = re.sub(CLEANR, '', key.split(' $ ')[1])
                        keyboard.append([{'text': button, 'url': link}])
                text = text.split('\n~\n')[0]

            if text != message.text or keyboard != [[]]:
                await utils.answer(message, text, reply_markup=keyboard)
        except Exception as e:
            pass