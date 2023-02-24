import logging
from glob import glob
from os import environ
from telethon.sync import TelegramClient, events

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

bot = TelegramClient('bot', int(environ['APP_API_ID']),  environ['APP_API_HASH']).start(bot_token=environ['BOT_TOKEN'])


@bot.on(events.InlineQuery)
async def inline_query_handler(event):
    builder = event.builder
    answer = []
    for file_path in glob('audio_archive' + f'/*{event.query.query}*.mp3'):
        answer.append(builder.document(
            title=file_path[14:][:-4],
            file=file_path,
            ))

    await event.answer(answer)

bot.run_until_disconnected()
