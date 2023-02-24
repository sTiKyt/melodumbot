import logging
from glob import glob
from os import environ
from telethon.sync import TelegramClient, events
from youtube_search import YoutubeSearch
from pytube import YouTube

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

bot = TelegramClient('bot', int(environ['APP_API_ID']), environ['APP_API_HASH']).start(bot_token=environ['BOT_TOKEN'])


@bot.on(events.InlineQuery)
async def inline_query_handler(event):
    builder = event.builder
    answer = []
    youtube_search = YoutubeSearch(event.query.query, max_results=1).to_dict() # TODO rewrite to support more than one result
    if glob('audio_archive' + f'/*{event.query.query}*.mp3'):  # TODO needs to be case insensitive
        for file_path in glob('audio_archive' + f'/*{event.query.query}*.mp3'):
            print(file_path)
            answer.append(builder.document( # TODO download cover and name, list before downloading actual song
                title=file_path[14:][:-4],  # TODO loading can be inspired by how it's done in @nowplaybot
                file=file_path,
                text='#TODO add links here'
            ))
    else:
        print(f"No audio files found for query {event.query.query}, searching...")
        #youtube_link = f'https://youtu.be{youtube_search[0]["url_suffix"]}'
        youtube_link = f'https://music.youtube.com/watch?v={youtube_search[0]["url_suffix"]}'

        youtube_name = youtube_search[0]["title"]
        print(f'{youtube_name} | {youtube_link}') #TODO better file naming based on to-be parsed metadata

        YouTube(youtube_link).streams.get_audio_only().download(output_path='audio_archive', filename=f'{youtube_name}.mp3')

        for file_path in glob('audio_archive' + f'/{youtube_name}*.mp3'):
            print(file_path)
            answer.append(builder.document(
                title=file_path[14:][:-4],
                file=file_path,
                text='#TODO add links here'
            ))
    print(f'User id: {event.query.user_id} requested {event.query.query}')
    await event.answer(answer)


bot.run_until_disconnected()
