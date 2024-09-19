import wave
from functools import cached_property, wraps
from src.waveio.encoding import PCMEncoding
from src.waveio.metadata import WAVMetadata


def reshape(shape):
    if shape not in ("rows", "columns"):
        raise ValueError("Shape must be either 'rows' or 'columns'")

    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            values = method(self, *args, **kwargs)
            reshaped = values.reshape(-1, self.metadata.num_channels)
            return reshaped if shape == "rows" else reshaped.T

        return wrapper

    return decorator


class WAVReader:
    def __init__(self, path):
        self._wav_file = wave.open(str(path))
        self.metadata = WAVMetadata(
            PCMEncoding(self._wav_file.getsampwidth()),
            self._wav_file.getframerate(),
            self._wav_file.getnchannels(),
            self._wav_file.getnframes()
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self._wav_file.close()

    def _read(self, max_frames=None):
        self._wav_file.rewind()
        frames = self._wav_file.readframes(max_frames)
        return self.metadata.encoding.decode(frames)

    @cached_property
    @reshape("rows")
    def frames(self):
        return self._read(self.metadata.num_frames)

    @cached_property
    @reshape("columns")
    def channels(self):
        return self.frames
