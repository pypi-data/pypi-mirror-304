import pytest
import torch
from ase.build import molecule
from graph_pes.data.io import to_atomic_graph
from graph_pes.deploy import LAMMPSModel
from graph_pes.graphs import keys
from graph_pes.graphs.graph_typing import AtomicGraph
from graph_pes.models import LennardJones

CUTOFF = 1.5


@pytest.mark.parametrize(
    "compute_virial",
    [True, False],
)
def test_lammps_model(compute_virial: bool):
    # generate a structure
    structure = molecule("CH3CH2OH")
    if compute_virial:
        # ensure the structure has a cell
        structure.center(vacuum=5.0)
    graph = to_atomic_graph(structure, cutoff=CUTOFF)

    # create a normal model, and get normal predictions
    model = LennardJones(cutoff=CUTOFF)
    props: list[keys.LabelKey] = ["energy", "forces"]
    if compute_virial:
        props.append("stress")
    outputs = model.predict(graph, properties=props)

    # create a LAMMPS model, and get LAMMPS predictions
    lammps_model = LAMMPSModel(model)

    assert lammps_model.get_cutoff() == torch.tensor(CUTOFF)

    lammps_graph: AtomicGraph = {
        **graph,
        "compute_virial": torch.tensor(compute_virial),
        "debug": torch.tensor(False),
    }  # type: ignore
    lammps_outputs = lammps_model(lammps_graph)

    # check outputs
    if compute_virial:
        assert "virial" in lammps_outputs
        assert lammps_outputs["virial"].shape == (6,)
        assert (
            outputs["stress"].shape == lammps_outputs["stress"].shape == (3, 3)
        )

    assert torch.allclose(
        outputs["energy"].float(),
        lammps_outputs["energy"].float(),
    )


def test_debug_logging(capsys):
    # generate a structure
    structure = molecule("CH3CH2OH")
    structure.center(vacuum=5.0)
    graph = to_atomic_graph(structure, cutoff=CUTOFF)

    # create a LAMMPS model, and get LAMMPS predictions
    lammps_model = LAMMPSModel(LennardJones())

    lammps_graph: AtomicGraph = {
        **graph,
        "compute_virial": torch.tensor(True),
        "debug": torch.tensor(True),
    }  # type: ignore
    lammps_model(lammps_graph)

    logs = capsys.readouterr().out
    assert "Received graph:" in logs
