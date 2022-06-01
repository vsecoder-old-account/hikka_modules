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
import requests
import io
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.unrestricted
@loader.ratelimit
@loader.tds
class GoogleItMod(loader.Module):
    """Module for screenshot web site"""

    strings = {
        "name": "ScreenWeb",
        "answer": "🖥 Screenshot {0} {1}x{2}px:",
        "error": "Error!\n \n .screenweb <url>=str <width>=int <height>=int",
    }

    strings_ru = {
        "answer": "🖥 Скриншот {0} {1}x{2}px:",
        "error": "Ошибка!\n \n .screenweb <url>=строка <width>=число <height>=число",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "url",
            "https://webshot.deam.io/{0}/?width={1}&height={2}?type=png&no_cookie_banners=true&lazy_load=true&destroy_screenshot=true&dark_mode=true&wait_for_event=load&delay=1000&accept_languages=ru&ttl=10",
            lambda m: self.strings("cfg_url", m),
        )
        self.name = self.strings["name"]

    @loader.unrestricted
    @loader.ratelimit
    async def screenwebcmd(self, message):
        """
         <url>=str <width>=int <height>=int
        .screenweb https://google.com/
        .screenweb https://vsecoder.ml/ 1920 1080
        Based on... my code and screenshot api)
        Made with <3 by @vsecoder
        """
        args = utils.get_args_raw(message)
        args = args.split(" ")
        if args:
            try:
                print(args[0])
            except:
                return await utils.answer(message, self.strings["error"])

            try:
                width = args[2]
                height = args[3]
            except:
                width = 1920
                height = 1080

            url = self.config['url'].format(
                args[0],   # url
                width,     # width
                height     # height
            )
            photo = requests.get(url)
            if not photo.ok:
                await message.edit("<b>Что-то пошло не так..</b>")
                return
            photo = io.BytesIO(photo.content)
            photo.name = "screen.png"
            photo.seek(0)
            await message.edit(self.strings["answer"].format(args[0],width,height))
            await message.client.send_file(message.to_id, photo)
        else:
            await utils.answer(message, self.strings["error"])
            await asyncio.sleep(5)
            await message.delete()
