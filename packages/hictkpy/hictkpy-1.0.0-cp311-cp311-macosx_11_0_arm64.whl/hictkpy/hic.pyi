from collections.abc import Sequence
import os
import pathlib
from typing import overload

import pd

import hictkpy._hictkpy


class FileWriter:
    """Class representing a file handle to create .hic files."""

    @overload
    def __init__(self, path: str | os.PathLike, chromosomes: dict[str, int], resolution: int, assembly: str = 'unknown', n_threads: int = 1, chunk_size: int = 10000000, tmpdir: str | os.PathLike = ..., compression_lvl: int = 10, skip_all_vs_all_matrix: bool = False) -> None:
        """
        Open a .hic file for writing given a list of chromosomes with their sizes and one resolution.
        """

    @overload
    def __init__(self, path: str | os.PathLike, chromosomes: dict[str, int], resolutions: Sequence[int], assembly: str = 'unknown', n_threads: int = 1, chunk_size: int = 10000000, tmpdir: str | os.PathLike = ..., compression_lvl: int = 10, skip_all_vs_all_matrix: bool = False) -> None:
        """
        Open a .hic file for writing given a list of chromosomes with their sizes and one or more resolutions.
        """

    @overload
    def __init__(self, path: str | os.PathLike, bins: hictkpy._hictkpy.BinTable, assembly: str = 'unknown', n_threads: int = 1, chunk_size: int = 10000000, tmpdir: str | os.PathLike = ..., compression_lvl: int = 10, skip_all_vs_all_matrix: bool = False) -> None:
        """
        Open a .hic file for writing given a BinTable. Only BinTable with a fixed bin size are supported.
        """

    def __repr__(self) -> str: ...

    def path(self) -> pathlib.Path:
        """Get the file path."""

    def resolutions(self) -> list[int]:
        """Get the list of resolutions in bp."""

    def chromosomes(self, include_ALL: bool = False) -> dict[str, int]:
        """Get chromosomes sizes as a dictionary mapping names to sizes."""

    def add_pixels(self, pixels: pd.DataFrame) -> None:
        """
        Add pixels from a pandas DataFrame containing pixels in COO or BG2 format (i.e. either with columns=[bin1_id, bin2_id, count] or with columns=[chrom1, start1, end1, chrom2, start2, end2, count].
        """

    def finalize(self, log_lvl: str = 'WARN') -> None:
        """Write interactions to file."""

