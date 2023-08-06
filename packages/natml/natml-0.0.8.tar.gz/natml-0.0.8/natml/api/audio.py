#
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from dataclasses import dataclass

@dataclass
class AudioFormat:
    """
    Audio format.

    Members:
        sample_rate (int): Audio sample rate.
        channel_count (int): Audio channel count.
    """
    sample_rate: int
    channel_count: int