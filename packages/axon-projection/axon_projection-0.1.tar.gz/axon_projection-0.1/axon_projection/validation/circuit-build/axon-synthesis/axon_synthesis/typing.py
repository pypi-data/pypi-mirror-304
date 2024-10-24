"""Module to define custom types used in axon-synthesis."""
# pylint: disable=unused-import
import os
import sys
from collections.abc import Sequence

import morphio
import neurom
from numpy.random import BitGenerator
from numpy.random import Generator
from numpy.random import SeedSequence
from numpy.typing import ArrayLike  # noqa: F401

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self  # noqa: F401

FileType = str | os.PathLike
LayerNamesType = list[int | str]
RegionIdsType = int | str | list[int | str]
LoadableMorphology = FileType | neurom.core.Morphology | morphio.Morphology | morphio.mut.Morphology
SeedType = None | int | Sequence[int] | SeedSequence | BitGenerator | Generator
