from send_audio_response import send_audio_response


async def handle_single_audio(info, update):
    title = info.get('title', 'audio')
    performer = info.get('uploader', 'Unknown Artist')
    filename = f"downloads/{title}.mp3"

    await send_audio_response(update, filename, title, performer)
