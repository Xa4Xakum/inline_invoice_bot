import asyncio
from loguru import logger

from helper import bot, dp
from handlers import r


async def on_startup():
    logger.warning('БОТ ОНЛАЙН')
    logger.warning(await bot.get_me())


def set_loggers():
    logger.add(
        'logs/{time}.log',
        level='INFO',
        backtrace=True,
        diagnose=True,
        rotation='00:00',
        retention='1 week',
        catch=True
    )
    logger.add(
        'errors/{time}.log',
        level='ERROR',
        backtrace=True,
        diagnose=True,
        rotation='00:00',
        retention='1 week',
        catch=True
    )


if __name__ == "__main__":

    set_loggers()
    dp.include_router(r)
    dp.startup.register(on_startup)
    asyncio.run(dp.start_polling(bot))
