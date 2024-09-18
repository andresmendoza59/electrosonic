import wave
from waveio.encoding import PCMEncoding


with wave.open("../audio/output.wav") as wave_file:
    metadata = wave_file.getparams()
    frames = wave_file.readframes(metadata.nframes)
    encoding = PCMEncoding(metadata.sampwidth)
    amplitudes = encoding.decode(frames)
