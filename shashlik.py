from .. import loader, utils

@loader.tds
class PersonaBuilder(loader.Module):
    """Создание и управление персонами"""

    strings = {"name": "PersonaBuilder"}

    def __init__(self):
        self.in_progress = {}  # {user_id: {data}}
        self.personas = {}     # {user_id: [persona1, persona2, ...]}

    @loader.command()
    async def создатьп(self, message):
        """Начать создание новой персоны"""
        uid = message.sender_id
        self.in_progress[uid] = {
            "Пол": None,
            "Возраст": None,
            "Что делает": None,
            "Навыки": None
        }
        await message.edit("🆕 Создание новой персоны начато! Используй команды:\n!стать, !возвраст, !чтоделает, !навыки")

    @loader.command()
    async def стать(self, message):
        """Указать пол: !стать девушка/парень"""
        uid = message.sender_id
        if uid not in self.in_progress:
            return await message.edit("❗ Сначала используй !создатьп")
        gender = utils.get_args_raw(message).strip().capitalize()
        if gender not in ["Парень", "Девушка"]:
            return await message.edit("❗ Укажи: парень или девушка")
        self.in_progress[uid]["Пол"] = gender
        await message.edit(f"✅ Пол установлен: {gender}")

    @loader.command()
    async def возвраст(self, message):
        """Установить возраст: !возвраст 18"""
        uid = message.sender_id
        if uid not in self.in_progress:
            return await message.edit("❗ Сначала используй !создатьп")
        age = utils.get_args_raw(message).strip()
        if not age.isdigit():
            return await message.edit("❗ Возраст должен быть числом")
        self.in_progress[uid]["Возраст"] = int(age)
        await message.edit(f"📅 Возраст установлен: {age}")

    @loader.command()
    async def чтоделает(self, message):
        """Описание деятельности: !чтоделает Пишет модули и играет"""
        uid = message.sender_id
        if uid not in self.in_progress:
            return await message.edit("❗ Сначала используй !создатьп")
        text = utils.get_args_raw(message)
        self.in_progress[uid]["Что делает"] = text
        await message.edit("💼 Занятие установлено.")

    @loader.command()
    async def навыки(self, message):
        """Список навыков: !навыки Python, C++, коты"""
        uid = message.sender_id
        if uid not in self.in_progress:
            return await message.edit("❗ Сначала используй !создатьп")
        text = utils.get_args_raw(message)
        self.in_progress[uid]["Навыки"] = text
        await message.edit("🧠 Навыки установлены.")

    @loader.command()
    async def закончить(self, message):
        """Завершить создание и сохранить"""
        uid = message.sender_id
        if uid not in self.in_progress:
            return await message.edit("❗ Сначала используй !создатьп")

        persona = self.in_progress.pop(uid)
        if None in persona.values():
            return await message.edit("❗ Все поля должны быть заполнены перед завершением.")

        if uid not in self.personas:
            self.personas[uid] = []
        self.personas[uid].append(persona)

        text = "✅ Персона создана!\n\n"
        for key, value in persona.items():
            text += f"<b>{key}:</b> {value}\n"
        await message.edit(text, parse_mode="html")

    @loader.command()
    async def списокперсон(self, message):
        """Показать всех твоих персон"""
        uid = message.sender_id
        if uid not in self.personas or not self.personas[uid]:
            return await message.edit("📭 У тебя ещё нет персон.")

        text = "<b>📋 Твои персоны:</b>\n\n"
        for i, p in enumerate(self.personas[uid], 1):
            text += f"<b>Персона {i}:</b>\n"
            for key, val in p.items():
                text += f"• <b>{key}:</b> {val}\n"
            text += "\n"

        await message.edit(text, parse_mode="html")

