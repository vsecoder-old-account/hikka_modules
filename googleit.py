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
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.unrestricted
@loader.ratelimit
@loader.tds
class GoogleItMod(loader.Module):
    """Module for google search"""

    strings = {
        "name": "Google it",
        "cfg_lingva_url": "Look for the answer to your question in Google",
        "answer": "😒 I advise you to start looking in the search engine: ",
        "error": "Error!\n .googleit | text",
    }

    strings_ru = {
        "cfg_lingva_url": "Поищи ответ на свой вопрос в гугле",
        "answer": "😒 Советую поискать для начала в поисковике: ",
        "error": "Ошибка!\n \n .googleit | text",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "search_url",
            "https://www.google.com/search?q={query}",
            lambda m: self.strings("cfg_searc_url", m),
        )
        self.name = self.strings["name"]

    @loader.unrestricted
    @loader.ratelimit
    async def googleitcmd(self, message):
        """
         | text
        Based on... my code)
        """
        args = utils.get_args_raw(message)
        query = args.split("|")[1]
        if args:
            if query:
                url = self.config["search_url"].format(
                    query=query
                ).replace(" ", "+")
            else:
                await utils.answer(message, self.strings["error"])
                await asyncio.sleep(5)
                await message.delete()
                return

            await utils.answer(message, f'{self.strings["answer"]}{url}')
        else:
            await utils.answer(message, self.strings["error"])
            await asyncio.sleep(5)
            await message.delete()
