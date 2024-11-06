import asyncio
import importlib

from pyrogram import idle

from Champu import LOGGER, ChampuBot
from Champu.modules import ALL_MODULES


async def anony_boot():
    try:
        await ChampuBot.start()
    except Exception as ex:
        LOGGER.error(ex)
        quit(1)

    for all_module in ALL_MODULES:
        importlib.import_module("Champu.modules." + all_module)

    LOGGER.info(f"@{ChampuBot.username} Started.")
    await idle()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(anony_boot())
    LOGGER.info("Stopping Champu Bot...")
