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
# meta pic: https://img.icons8.com/cute-clipart/344/wikipedia.png


__version__ = (1, 0, 0)

import logging
import wikipedia
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class WikiMod(loader.Module):
    """Module for wikipedia search"""

    strings = {
        "name": "Wikipedia🌐",
        "answer": ("🌐 <b>{0}</b><a href='{1}'>:</a>\n\n<i>{2}</i>\n\n{3}"),
        "error": ("❗️ <b>{0}</b>"),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "wiki_lang", "en", "Language of wikipedia(en or ru)",
        )

    async def client_ready(self, client, db):
        self._client = client
        

    async def wikicmd(self, message):
        """
         <text> - search in wikipedia
        """
        args = utils.get_args_raw(message)
        result = {
            "title": "",
            "summary": "",
            "url": "",
            "image": ""
        }
        try:
            wikipedia.set_lang(self.config["wiki_lang"])
        except:
            wikipedia.set_lang("en")
        try:
            page = wikipedia.page(args)
            result["title"] = page.title
            result["summary"] = page.summary
            result["url"] = page.url
            result["image"] = page.images[0]
            await utils.answer(message, self.strings['answer'].format(result["title"], result["image"], result["summary"], result["url"]))
        except wikipedia.exceptions.DisambiguationError as e:
            await utils.answer(message, self.strings['error'].format(e))
        except wikipedia.exceptions.PageError as e:
            await utils.answer(message, self.strings['error'].format(e))