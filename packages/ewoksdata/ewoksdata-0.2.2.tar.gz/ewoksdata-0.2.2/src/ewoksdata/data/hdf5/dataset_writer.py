from typing import Optional

import h5py
import numpy
from numpy.typing import ArrayLike

from .types import StrictPositiveIntegral
from .config import guess_dataset_config


class DatasetWriter:
    def __init__(
        self,
        parent: h5py.Group,
        name: str,
        npoints: Optional[StrictPositiveIntegral] = None,
        attrs: Optional[dict] = None,
    ) -> None:
        self._parent = parent
        self._name = name
        self._attrs = attrs
        self._dataset_name = f"{parent.name}/{name}"
        self._dataset = None
        self._buffer = list()
        self._npoints_added = 0
        self._npoints = npoints
        self._npoints_chunk = None
        self._dataset_idx = 0

    @property
    def dataset_name(self) -> str:
        return self._dataset_name

    def __enter__(self) -> "DatasetWriter":
        return self

    def __exit__(self, *args) -> None:
        self.flush_buffer()

    @property
    def dataset(self) -> Optional[h5py.Dataset]:
        return self._dataset

    def _create_dataset(self, first_data_point: numpy.ndarray) -> h5py.Dataset:
        scan_shape = (self._npoints,)
        detector_shape = first_data_point.shape
        dtype = first_data_point.dtype
        if self._npoints is None:
            max_shape = scan_shape + detector_shape
            shape = (1,) + first_data_point.shape
        else:
            max_shape = None
            shape = scan_shape + first_data_point.shape

        options = guess_dataset_config(
            scan_shape, detector_shape, dtype=dtype, max_shape=max_shape
        )
        options["shape"] = shape
        options["dtype"] = dtype
        options["fillvalue"] = numpy.nan  # converts to 0 for integers
        if max_shape:
            options["maxshape"] = max_shape
        if options["chunks"]:
            self._npoints_chunk = options["chunks"][0]
        else:
            self._npoints_chunk = 0
        dset = self._parent.create_dataset(self._name, **options)
        if self._attrs:
            dset.attrs.update(self._attrs)
        return dset

    @property
    def npoints_added(self) -> int:
        return self._npoints_added

    def add_point(self, data: ArrayLike) -> bool:
        if self._dataset is None:
            self._dataset = self._create_dataset(data)
        self._buffer.append(data)
        self._npoints_added += 1
        return self.flush_buffer(align=True)

    def add_points(self, data: ArrayLike) -> bool:
        if self._dataset is None:
            self._dataset = self._create_dataset(data[0])
        self._buffer.extend(data)
        self._npoints_added += len(data)
        return self.flush_buffer(align=True)

    def flush_buffer(self, align: bool = False) -> bool:
        nbuffer = len(self._buffer)
        if align and self._npoints_chunk:
            nflush = nbuffer // self._npoints_chunk * self._npoints_chunk
        else:
            nflush = nbuffer
        if nflush == 0:
            return False
        npoints0 = self._dataset.shape[0]
        istart = self._dataset_idx
        npoints1 = istart + nflush
        if self._npoints_chunk and npoints1 > npoints0:
            self._dataset.resize(npoints1, axis=0)
        self._dataset[istart : istart + nflush] = self._buffer[:nflush]
        self._buffer = self._buffer[nflush:]
        self._dataset_idx += nflush
        return True
