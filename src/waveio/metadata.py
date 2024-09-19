from src.waveio.encoding import PCMEncoding
from dataclasses import dataclass


@dataclass(frozen=True)
class WAVMetadata:
    encoding: PCMEncoding
    frames_per_second: float
    num_channels: int
    num_frames: int | None = None

    @property
    def num_seconds(self):
        if self.num_frames is None:
            raise ValueError("Indeterminate stream of audio frames")
        return self.num_frames / self.frames_per_second
