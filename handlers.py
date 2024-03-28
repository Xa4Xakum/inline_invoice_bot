
from aiogram import Router, F
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.filters import Command
from aiogram.types import Message

from filters import NumericInput, AdminInline, Admin, WordsCount, NumericSecParam
from operations import make_pay_text, get_amount_and_total, add_admin, del_admin, set_data, get_data, get_total_amount, add_tabs

r = Router()
r.message.filter(Admin())


@r.message(F.text, Command('start'))
async def start(msg: Message):
    await msg.answer('Я нужен для того, чтобы создавать квитанции')


@r.inline_query(NumericInput(), AdminInline())
async def invoice(iq: InlineQuery):

    amount, total_amount = await get_amount_and_total(iq.query)
    pay_text = await make_pay_text(amount=amount, total=total_amount)

    await iq.answer(
        cache_time=1,
        results=[
            InlineQueryResultArticle(
                id='0',
                title='Создать квитанцию',
                description=f'{total_amount} сум',
                input_message_content=InputTextMessageContent(
                    message_text=pay_text,
                    parse_mode="HTML"
                )
            )
        ]
    )


# добавить админа
@r.message(Command('addadmin'), WordsCount(2))
async def addadmin(msg: Message):
    params = msg.text.split()
    add_admin(int(params[1]))
    await msg.answer('Готово')


# удалить админа
@r.message(Command('deladmin'), WordsCount(2))
async def deladmin(msg: Message):
    params = msg.text.split()
    del_admin(int(params[1]))
    await msg.answer('Готово')


# установить комиссию обменника
@r.message(Command('setexfee'), WordsCount(2), NumericSecParam())
async def setexfee(msg: Message):
    params = msg.text.split()
    data = get_data()
    data['exfee'] = params[1].replace(',', '.')
    set_data(data)
    await msg.answer('Готово')


# установить курс usdt к сумам
@r.message(Command('usdtuzs'), WordsCount(2), NumericSecParam())
async def setusduzs(msg: Message):
    params = msg.text.split()
    data = get_data()
    data['usduzs'] = params[1].replace(',', '.')
    set_data(data)
    await msg.answer('Готово')


# установить скрытую комиссию
@r.message(Command('sethiddenfee'), WordsCount(2), NumericSecParam())
async def sethiddenfee(msg: Message):
    params = msg.text.split()
    data = get_data()
    data['hiddenfee'] = params[1].replace(',', '.')
    set_data(data)
    await msg.answer('Готово')


# установить текст после =====
@r.message(Command('settext'))
async def setcard(msg: Message):
    data = get_data()
    data['text'] = msg.text.split('/settext')[1]
    set_data(data)
    await msg.answer('Готово')


# показать список админов
@r.message(Command('admins'))
async def admins(msg: Message):
    data = get_data()
    text = f'Список админов(всего {len(data["admins"])}):\n\n'

    for admin in data['admins']:
        text += f'{admin}\n'

    await msg.answer(text)


@r.message(Command('const'))
async def const(msg: Message):
    data = get_data()
    text = (
        f'Комиссия обменника: {data["exfee"]}\n'
        f'Лимит: {data["limit"]}\n'
        f'Пониженная комиссия: {data["lower_exfee"]}\n'
        f'Курс доллара к суму: {data["usduzs"]}\n'
        f'Скрытая комиссия: {data["hiddenfee"]}\n'
    )
    await msg.answer(text)


@r.message(Command('cost'), WordsCount(2), NumericSecParam())
async def cost(msg: Message):
    text = msg.text.replace(',', '.')
    params = text.split()
    total = await get_total_amount(float(params[1]))
    total_with_tabs = add_tabs(str(total))
    await msg.answer(f'UZS: {total_with_tabs}')


@r.message(Command('setlimit'), WordsCount(2), NumericSecParam())
async def setlimit(msg: Message):
    params = msg.text.split()
    data = get_data()
    data['limit'] = params[1].replace(',', '.')
    set_data(data)
    await msg.answer('Готово')


@r.message(Command('setlowerexfee'), WordsCount(2), NumericSecParam())
async def setlowerexfee(msg: Message):
    params = msg.text.split()
    data = get_data()
    data['lower_exfee'] = params[1].replace(',', '.')
    set_data(data)
    await msg.answer('Готово')
