from __future__ import annotations

from dataclasses import dataclass

import pytest
from graph_pes.core import GraphPESModel
from graph_pes.graphs import keys
from graph_pes.graphs.graph_typing import AtomicGraph
from graph_pes.graphs.operations import (
    neighbour_distances,
    number_of_edges,
    trim_edges,
)
from graph_pes.models import AdditionModel, SchNet
from graph_pes.models.offsets import FixedOffset
from helpers import graph_from_molecule
from torch import Tensor


@dataclass
class Stats:
    n_neighbours: int
    max_edge_length: float


class DummyModel(GraphPESModel):
    def __init__(self, name: str, cutoff: float, info: dict[str, Stats]):
        super().__init__(
            cutoff=cutoff,
            implemented_properties=["local_energies"],
        )
        self.name = name
        self.info = info

    def forward(self, graph: AtomicGraph) -> dict[keys.LabelKey, Tensor]:
        # insert statistics here: `GraphPESModel` should automatically
        # trim the input graph based on the model's cutoff
        self.info[self.name] = Stats(
            n_neighbours=number_of_edges(graph),
            max_edge_length=neighbour_distances(graph).max().item(),
        )
        # dummy return value
        return {"local_energies": graph["atomic_numbers"].float()}


def test_auto_trimming():
    info = {}
    graph = graph_from_molecule("CH3CH2OCH3", cutoff=5.0)

    large_model = DummyModel("large", cutoff=5.0, info=info)
    small_model = DummyModel("small", cutoff=3.0, info=info)

    # forward passes to gather info
    large_model.predict_energy(graph)
    small_model.predict_energy(graph)

    # check that graph remains unchanged
    assert "_rmax" not in graph

    # check that cutoff filtering is working
    assert info["large"].n_neighbours == number_of_edges(graph)
    assert info["small"].n_neighbours < number_of_edges(graph)

    assert (
        info["large"].max_edge_length == neighbour_distances(graph).max().item()
    )
    assert (
        info["small"].max_edge_length < neighbour_distances(graph).max().item()
    )


def test_model_cutoffs():
    model = AdditionModel(
        small=SchNet(cutoff=3.0),
        large=SchNet(cutoff=5.0),
    )

    assert model.cutoff == 5.0

    model = FixedOffset()
    assert model.cutoff == 0


def test_warning():
    graph = graph_from_molecule("CH4", cutoff=3.0)
    trimmed_graph = trim_edges(graph, cutoff=3.0)

    model = SchNet(cutoff=6.0)
    with pytest.warns(UserWarning, match="Graph already has a cutoff of"):
        model.get_all_PES_predictions(trimmed_graph)


def test_cutoff_trimming():
    graph = graph_from_molecule("CH4", cutoff=5)

    trimmed_graph = trim_edges(graph, cutoff=3.0)
    assert graph is not trimmed_graph

    # check that trimming a second time with the same cutoff is a no-op
    doubly_trimmed_graph = trim_edges(trimmed_graph, cutoff=3.0)
    assert doubly_trimmed_graph is trimmed_graph

    # but that if the cutoff is further reduced then the trimming occurs
    doubly_trimmed_graph = trim_edges(trimmed_graph, cutoff=2.0)
    assert doubly_trimmed_graph is not trimmed_graph
    assert doubly_trimmed_graph["_rmax"].item() == 2.0  # type: ignore
