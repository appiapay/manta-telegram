# Manta Telegram Bot
This is a demo Telegram Bot enabled to receive payments through Manta protocol.

For Manta protocol, visit https://appia.co

## Install
```bash
pip install git+git://github.com/appiapay/manta-telegram.git
```

## Run
Some environment variables need to be setup before launching:

```dotenv
BOT_TOKEN={YOUR BOT TOKEN}
MANTA_APP_TOKEN={MANTA APP TOKEN}
MANTA_APP_ID={MANTA APP ID}
MANTA_HOST=manta.beappia.com
API_BASEURL=https://developer.beappia.com
```

Then you can simply launch:
```bash
mtbot
```
