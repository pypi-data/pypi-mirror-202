# 
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from dataclasses import dataclass
from typing import List

@dataclass
class Normalization:
    """
    Feature normalization.

    Members:
        mean (List[float]): Normalization mean.
        std (List[float]): Normalization standard deviation.
    """
    mean: List[float]
    std: List[float]