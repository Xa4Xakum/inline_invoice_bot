import requests
import asyncio
import json
import emoji


async def get_amount_and_total(text: str):
    text = text.replace(',', '.')
    params = text.split()
    digits = [float(i) for i in params]

    if len(params) == 0:
        digits.append(float(text))

    amount = digits[0]
    digits.remove(amount)

    if len(digits) > 0:
        total = ''
        for i in digits:
            total += f'{round(i)}'
    else:
        total = str(await get_total_amount(amount=amount))

    total_with_tabs = add_tabs(total)

    return amount, total_with_tabs


def get_data():
    data = json.load(open("data.json"))
    # if 'text' in data:
    #     data['text'] = emoji.emojize(data['text'])
    return data


def set_data(data):
    # if 'text' in data:
    #     data['text'] = emoji.demojize(data['text'])
    with open("data.json", "w") as file:
        json.dump(data, file, indent=2, ensure_ascii=True)


def add_admin(uid):
    data = get_data()
    if 'admins' not in data:
        data['admins'] = []
    if uid not in data['admins']:
        data['admins'].append(uid)
    set_data(data)


def del_admin(uid):
    data = get_data()
    if 'admins' not in data:
        data['admins'] = []
    if uid in data['admins']:
        data['admins'].remove(uid)
    set_data(data)


async def make_pay_text(amount, total):
    data = get_data()
    text = (
        f'<b>ЗАЯВКА ДЕЙСТВУЕТ 60 МИНУТ</b>\n\n'

        f'===========================\n'
        f'Вы должны оплатить: {total} сум\n'
        f'Получите LTC: {amount} LTC\n'
        f'===========================\n'
        f'{data["text"]}'
    )

    return text


async def get_ltc_price():
    while True:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
        if response:
            data = response.json()
            return data['litecoin']['usd']
        else:
            await asyncio.sleep(1)


async def get_total_amount(amount):
    data = get_data()
    ltc_price = await get_ltc_price()
    amount_ltc = amount * ltc_price

    if amount_ltc < float(data['limit']):
        exchange_fee = float(data['exfee'])  # 8% комиссия обменника
    else:
        exchange_fee = float(data['lower_exfee'])  # если 100$ и более

    usd_to_uzs_rate = float(data['usduzs'])  # Курс доллара к суму
    hidden_fee = float(data['hiddenfee'])  # Скрытая комиссия
    return round((amount_ltc + hidden_fee + amount_ltc * exchange_fee) * usd_to_uzs_rate)


def add_tabs(total: str):
    total_with_tabs = ''
    iterator = 3 - len(total) % 3
    for i in total:
        total_with_tabs += i
        iterator += 1
        if iterator % 3 == 0:
            total_with_tabs += ' '

    return total_with_tabs
