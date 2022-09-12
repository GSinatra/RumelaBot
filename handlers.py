from aiogram.types import Message, ShippingOption, ShippingQuery, LabeledPrice, PreCheckoutQuery
from aiogram.types.message import ContentType

from main import dp, bot, db
from messages import MESSAGES
from config import BANK_TOKEN, item_url

from Buttons.Client import Markups



PRICES = [
    LabeledPrice(label="Мёд донниковый", amount=45000)
]

FAST_SHIPPING_OPTION = ShippingOption(
    id='fast',
    title="Срочная доставка"
).add(LabeledPrice(label="До порога!", amount=50000))

POST_SHIPPING_OPTION = ShippingOption(
    id='post',
    title="Курьер"
)

MAIL_SHIPPING_OPTION = ShippingOption(
    id='mail',
    title="Почта России"
).add(LabeledPrice(label="Почта России", amount=50000))

MAIL_SHIPPING_OPTION.add(LabeledPrice(label="Подарочная упаковка", amount=25000))
MAIL_SHIPPING_OPTION.add(LabeledPrice(label="Срочное отправление!", amount=100000))

PICKUP_SHIPPING_OPTION = ShippingOption(
    id='pickup',
    title="Самовывоз"
)


@dp.message_handler(commands=['start'])
async def start_cmd(message: Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        await message.answer(MESSAGES['start'])
    else:
        await bot.send_message(message.from_user.id, "Добро пожаловать!", reply_markup=Markups.mainMenu)


@dp.message_handler(commands=['help'])
async def start_cmd(message: Message):
    await message.answer(MESSAGES['help'])


@dp.message_handler(commands=['terms'])
async def start_cmd(message: Message):
    await message.answer(MESSAGES['terms'])


@dp.message_handler(commands=['buy'])
async def buy_process(message: Message):
    await bot.send_invoice(chat_id=message.chat.id,
                           title=MESSAGES['item_title'],
                           description=MESSAGES['item_description'],
                           provider_token=BANK_TOKEN,
                           currency='RUB',
                           photo_url=item_url,
                           photo_height=512,
                           photo_width=512,
                           photo_size=512,
                           need_phone_number=True,
                           is_flexible=True,
                           prices=PRICES,
                           start_parameter='example',
                           payload='some_invoice')


@dp.shipping_query_handler(lambda q: True)
async def shipping_process(shipping_querry: ShippingQuery):
    if shipping_querry.shipping_address.country_code != 'RU':
        return await bot.answer_shipping_query(
            shipping_querry.id,
            ok=False,
            error_message=MESSAGES['post_error']
        )

    shipping_option = [FAST_SHIPPING_OPTION]

    if shipping_querry.shipping_address.country_code == 'RU':
        shipping_option.append(POST_SHIPPING_OPTION)

    await bot.answer_shipping_query(
        shipping_querry.id,
        ok=True,
        shipping_options=shipping_option
    )


@dp.pre_checkout_query_handler(lambda q: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    await bot.send_message(
        message.chat.id,
        MESSAGES['successful_payment'].format(total_amount=message.successful_payment.total_amount // 100,
                                              currency=message.successful_payment.currency)
    )
