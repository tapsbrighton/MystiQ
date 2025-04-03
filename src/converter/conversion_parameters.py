##
# Created by @taps on Wednesday, 02 April 2025.
##

import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class ConversionParameters:
    source: str = ""
    destination: str = ""
    threads: int = 0
    disable_audio: bool = False
    copy_audio: bool = False
    audio_bitrate: int = 0
    audio_sample_rate: int = 0
    audio_keep_sample_rate: bool = False
    audio_channels: int = 0
    audio_volume: int = 0
    disable_video: bool = False
    insert_subtitle: bool = False
    disable_color: bool = False
    vertical_flip: bool = False
    horizontal_flip: bool = False
    rotate_90more: bool = False
    rotate_90less: bool = False
    rotate_180: bool = False
    video_same_quality: bool = False
    video_deinterlace: bool = False
    video_bitrate: int = 0
    video_width: int = 0
    video_height: int = 0
    toCrop: bool = False
    video_crop_top: int = 0
    video_crop_bottom: int = 0
    video_crop_left: int = 0
    video_crop_right: int = 0
    time_begin: int = 0
    time_end: int = 0
    ffmpeg_options: str = ""
    speed_scaling: bool = False
    speed_scaling_factor: float = 1.0

    def copy_configuration_from(self, src: 'ConversionParameters'):
        orig_src = self.source
        orig_dest = self.destination
        self.__dict__.update(src.__dict__)
        self.source = orig_src
        self.destination = orig_dest

    @staticmethod
    def from_ffmpeg_parameters(params_str: str) -> 'ConversionParameters':
        result = ConversionParameters()
        args = params_str.split()

        i = 0
        while i < len(args):
            arg = args[i]
            if arg.startswith('-'):
                if arg == "-threads":
                    result.threads = int(args[i + 1])
                    i += 2
                elif arg == "-an":
                    result.disable_audio = True
                    i += 1
                elif arg == "-ab":
                    result.audio_bitrate = int(re.sub(r'\D', '', args[i + 1]))
                    i += 2
                elif arg == "-ar":
                    result.audio_sample_rate = int(re.sub(r'\D', '', args[i + 1]))
                    i += 2
                elif arg == "-ac":
                    result.audio_channels = int(args[i + 1])
                    i += 2
                elif arg == "-vol":
                    result.audio_volume = int(args[i + 1])
                    i += 2
                elif arg == "-vn":
                    result.disable_video = True
                    i += 1
                elif arg == "-s":
                    match = re.match(r"(\d+)x(\d+)", args[i + 1])
                    if match:
                        result.video_width = int(match.group(1))
                        result.video_height = int(match.group(2))
                        i += 2
                    else:
                        i += 1
                elif arg == "-filter:v":
                    match = re.match(r"crop=(\d+):(\d+):(\d+):(\d+)", args[i + 1])
                    if match:
                        result.video_crop_top = int(match.group(4))
                        result.video_crop_left = int(match.group(3))
                        result.video_crop_right = int(match.group(1)) + int(match.group(3))
                        result.video_crop_bottom = int(match.group(2)) + int(match.group(4))
                        i += 2
                    else:
                        i += 1
                else:
                    i += 1
            else:
                i += 1

        result.ffmpeg_options = " ".join(args)
        return result
