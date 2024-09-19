from waveio.reader import WAVReader


with WAVReader("../audio/Bongo_sound.wav") as wav:
    print(f"Frames: {wav.frames}")
    print(f"Channels: {wav.channels}")
