from single_audio import handle_single_audio


async def handle_audio_list(update, entries):
    for entry in entries:
        if not entry:
            continue

        await handle_single_audio(entry, update)
