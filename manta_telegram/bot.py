from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from manta.store import Store
from manta.messages import AckMessage, Status
from decimal import Decimal
import qrcode
import io
import logging
import manta_telegram.settings as settings
from manta_telegram.qr_logo import make_logo_qr

logger = logging.getLogger(__name__)

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Welcome to Appia Donation Bot\nPlease type \pay [amount] for your donation")


async def wait_confirmation(message: types.Message, store: Store):
    while True:
        ack: AckMessage = await store.acks.get()
        if ack.status == Status.PAID:
            await message.reply("Payment Complete")
            return
        elif ack.status == Status.CONFIRMING:
            await message.reply('Payment is Confirming')
            await wait_confirmation(message, store)
            return
        elif ack.status == Status.INVALID:
            await message.reply("Invalid Transaction: {}".format(ack.memo))
            return


@dp.message_handler(commands=['pay'])
@dp.async_task
async def qr_code(message: types.Message):
    amount: Decimal = Decimal(message.get_args())
    logger.info ("Creating a request for amount {}".format(amount))
    store = Store(settings.MANTA_APP_ID, host=settings.MANTA_HOST)
    store.mqtt_client.username_pw_set(settings.MANTA_APP_ID, settings.MANTA_APP_TOKEN)
    reply = await store.merchant_order_request(amount, "EUR")

    logo = settings.__dict__.get("LOGO", "")

    with io.BytesIO() as output:
        make_logo_qr(reply.url, logo, output)
        # image.save(output, format="png")
        await message.reply_photo(output.getvalue(), caption=reply.url)
        await wait_confirmation(message, store)


def run():
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp)


if __name__ == '__main__':
    run()

