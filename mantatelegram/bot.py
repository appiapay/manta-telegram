from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from manta.store import Store
from manta.messages import AckMessage, Status
from decimal import Decimal
import qrcode
import io
import logging

logger = logging.getLogger(__name__)

bot = Bot(token='680959216:AAEeTUEDsVJ_wjSG1HwvNEu2_nOB9XS9IU4')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Welcome to Appia Pay TestBot")


async def wait_confirmation(message: types.Message, store: Store):
    while True:
        ack: AckMessage = await store.acks.get()
        if ack.status == Status.PAID:
            await message.reply("Payment Complete")
            return


@dp.message_handler(commands=['pay'])
@dp.async_task
async def qr_code(message: types.Message):
    amount: Decimal = Decimal(message.get_args())
    logger.info ("Creating a request for amount {}".format(amount))
    store = Store("2bbfb558-0237-4b06-83f6-0e9a5a97b165", host="95.179.183.144")
    store.mqtt_client.username_pw_set("2bbfb558-0237-4b06-83f6-0e9a5a97b165", "gCkW2EztSAqpLIIUIYyqPw==")
    reply = await store.merchant_order_request(amount, "EUR")

    image = qrcode.make(reply.url)
    global output

    with io.BytesIO() as output:
        image.save(output, format="png")
        await message.reply_photo(output.getvalue(), caption=reply.url)
        await wait_confirmation(message, store)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp)

