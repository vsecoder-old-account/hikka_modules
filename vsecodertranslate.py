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

__version__ = (2, 2, 1)

from fnmatch import translate
import logging
import translators as vt
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.unrestricted
@loader.ratelimit
@loader.tds
class VseTranslateMod(loader.Module):

    strings = {
        "name": "💠 Vsecoder Translate",
        "invalid_args": "📥 Invalid arguments!",
        "answer": ("💠 <b>{}</b> <i>from:</i><b>[{}]</b> <i>to:</i><b>[{}]</b>\n\n<code>{}</code>"),
        "error": "📥 Error!",
    }

    strings_ru = {
        "invalid_args": "📥 Неправильные аргументы!",
        "answer": ("💠 <b>{}</b> <i>с:</i><b>[{}]</b> <i>на:</i><b>[{}]</b>\n\n<code>{}</code>"),
        "error": "📥 Ошибка!",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "default_lang",
                "ru",
                lambda: "Which language to translate by default(ru/en/de/fr/es/it/pt/ja/zh/ko)",
            ),
            loader.ConfigValue(
                "default_translator",
                "google",
                lambda: "Which translator to use by default(google/yandex/bing/iciba)",
            ),
        )

    async def client_ready(self, client, db):
        self._client = client
        
        await self.save_stat("download")

    async def save_stat(self, state):
        bot = "@modules_stat_bot"
        m = await self._client.send_message(bot, f"/{state} vsecodertranslate")
        await self._client.delete_messages(bot, m)

    async def on_unload(self):
        await self.save_stat("unload")

    async def translate(self, text, lang_from="auto", lang_to="ru", translator="google"):
        translators = {
            "google": vt.google,
            "yandex": vt.yandex,
            "bing": vt.bing,
            "iciba": vt.iciba,
        }
        if translator not in translators:
            return self.strings("invalid_translator")

        translater = translators[translator]
        result = {
            "translator": translator,
            "from": lang_from,
            "to": lang_to,
            "text": translater(text, from_language=lang_from, to_language=lang_to),
        }
        return result


    async def vsetranslatecmd(self, message):
        """
         [from_language] [to_language] [text]
        .vsetranslate en ru Hello, world!
        """
        args = utils.get_args(message)
        langs = [
            "auto", "ru", "en", "de", "fr", "es", "it", "pt", "ja", "zh", "ko"
        ]
        translators = [
            "google", "yandex", "bing", "iciba"
        ]
        text = message.text.replace(f"{self.get_prefix()}vsetranslate", "")
        t = ""
        if not args:
            return await utils.answer(message, self.strings("invalid_args"))
        if args[0] not in langs:                                # .vsetranslate text
            t = await self.translate(text, translator=self.config["default_translator"], lang_to=self.config["default_lang"])
        elif args[1] not in langs and args[0] in langs:         # .vsetranslate from_language text
            text = message.text.replace(f"{self.get_prefix()}vsetranslate {args[0]}", "")
            t = await self.translate(text, translator=self.config["default_translator"], lang_to=self.config["default_lang"], lang_from=args[0])
        elif args[2] not in translators and args[1] in langs:   # .vsetranslate from_language to_language text
            text = message.text.replace(f"{self.get_prefix()}vsetranslate {args[0]} {args[1]}", "")
            t = await self.translate(
                text, 
                translator=self.config["default_translator"],
                lang_to=args[1], 
                lang_from=args[0]
            )
        else:                                                   # .vsetranslate from_language to_language translator text
            text = message.text.replace(f"{self.get_prefix()}vsetranslate {args[0]} {args[1]} {args[2]}", "")
            t = await self.translate(
                text, 
                translator=args[2],
                lang_to=args[1], 
                lang_from=args[0]
            )
        try:
            return await utils.answer(message, self.strings("answer").format(t["translator"], t["from"], t["to"], t["text"]))
        except:
            return await utils.answer(message, self.strings("error"))