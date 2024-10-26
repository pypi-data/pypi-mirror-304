from __future__ import annotations

import warnings
from typing import Iterator, Sequence

import torch.utils.data

from graph_pes.graphs import LabelledBatch, LabelledGraph
from graph_pes.graphs.operations import to_batch

from .dataset import LabelledGraphDataset, SequenceDataset


class GraphDataLoader(torch.utils.data.DataLoader):
    r"""
    A data loader for merging :class:`~graph_pes.graphs.AtomicGraph` objects
    into :class:`~graph_pes.graphs.AtomicGraphBatch` objects.

    Parameters
    ----------
    dataset
        The dataset to load.
    batch_size
        The batch size.
    shuffle
        Whether to shuffle the dataset.
    **kwargs:
        Additional keyword arguments to pass to the underlying
        :class:`torch.utils.data.DataLoader`.
    """

    def __init__(
        self,
        dataset: LabelledGraphDataset | Sequence[LabelledGraph],
        batch_size: int = 1,
        shuffle: bool = False,
        **kwargs,
    ):
        if not isinstance(dataset, LabelledGraphDataset):
            dataset = SequenceDataset(dataset)

        if "collate_fn" in kwargs:
            warnings.warn(
                "graph-pes uses a custom collate_fn (`collate_atomic_graphs`), "
                "are you sure you want to override this?",
                stacklevel=2,
            )

        collate_fn = kwargs.pop("collate_fn", to_batch)

        super().__init__(
            dataset,
            batch_size,
            shuffle,
            collate_fn=collate_fn,
            **kwargs,
        )

    def __iter__(self) -> Iterator[LabelledBatch]:  # type: ignore
        return super().__iter__()
