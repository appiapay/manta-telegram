from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from manta.store import Store
from manta.messages import AckMessage, Status
import qrcode
import io
import logging

logger = logging.getLogger(__name__)

bot = Bot(token='680959216:AAEeTUEDsVJ_wjSG1HwvNEu2_nOB9XS9IU4')
dp = Dispatcher(bot)




@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['pay'])
async def qr_code(message: types.Message):
    amount: float = message.get_args()[0]
    store = Store("dummystore")
    reply = await  store.merchant_order_request(amount, "eur")

    image = qrcode.make(reply.url)
    global output

    with io.BytesIO() as output:
        image.save(output, format="png")
        await message.reply_photo(output.getvalue(), caption=reply.url)

    while True:
        ack: AckMessage = await store.acks.get()
        if ack.status == Status.PAID:
            await message.reply ("Payment Complete")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp)

