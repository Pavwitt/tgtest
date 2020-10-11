from .. import loader, utils
import logging
import asyncio

logger = logging.getLogger(__name__)


def register(cb):
    cb(UpgradedSpamMod)


class UpgradedSpamMod(loader.Module):
    strings = {"name": "UpgradedSpamMod"}

    def __init__(self):
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self.client = client
        self._db = db
        self.me = await client.get_me(True)

    @loader.owner
    async def spamallcmd(self, message):
        """ Кидает всем участникам чата сообщение в лс
            Формат: <code>.spamall <ссылка на изображение(не обязательно) <текст сообщения></code>"""
        args = utils.get_args(message)
        raw_text = utils.get_args_raw(message)
        spamText = ""
        errors = 0
        if not raw_text:
            await message.edit("<b>Нужны аргументы</b>")
        await message.edit("<b>Отправляем...</b>")
        if "http" in args[0]:
            txt = raw_text.replace(args[0], '')
            spamText = f"<a href={args[0]}>\u2060</a> " + txt
        else:
            spamText = raw_text
        async for user in self.client.iter_participants(message.to_id):
            try:
                if user.id != message.from_id:
                    msg = await self.client.send_message(user.id, spamText)
                    msg.delete(revoke=False)
            except Exception as e:
                errors += 1
            await asyncio.sleep(1)
        if errors > 0:
            result = f"<b>Отправлено! Не получили {errors} участников чата</b>"
        else:
            result = f"<b>Успешно отправлено всем участникам чата! </b>"
        await message.edit(result)
