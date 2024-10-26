from __future__ import annotations

from pathlib import Path

import helpers
import pytest
import torch
from ase.build import molecule
from graph_pes.core import GraphPESModel
from graph_pes.data.io import to_atomic_graph
from graph_pes.deploy import deploy_model
from graph_pes.graphs.operations import number_of_atoms
from graph_pes.models.pairwise import LennardJones, SmoothedPairPotential


# ignore warnings about lack of energy labels for pre-fitting: not important
@pytest.mark.filterwarnings("ignore:.*No energy data found in training data.*")
@helpers.parameterise_all_models(expected_elements=["C", "H", "O"])
def test_deploy(model: GraphPESModel, tmp_path: Path):
    dummy_graph = to_atomic_graph(molecule("CH3CH2OH"), cutoff=1.5)
    # required by some models before making predictions
    model.pre_fit_all_components([dummy_graph])

    model_cutoff = float(model.cutoff)
    graph = to_atomic_graph(
        molecule("CH3CH2OH", vacuum=2),
        cutoff=model_cutoff,
    )
    outputs = {
        k: t.double() for k, t in model.get_all_PES_predictions(graph).items()
    }

    # 1. saving and unsaving works
    torch.save(model, tmp_path / "model.pt")
    loaded_model = torch.load(tmp_path / "model.pt")
    assert isinstance(loaded_model, GraphPESModel)
    torch.testing.assert_close(
        model.predict_forces(graph),
        loaded_model.predict_forces(graph),
        atol=1e-6,
        rtol=1e-6,
    )

    # 2. deploy the model
    save_path = tmp_path / "model.pt"
    deploy_model(model, path=save_path)

    # 3. load the model back in
    loaded_model = torch.jit.load(save_path)
    assert isinstance(loaded_model, torch.jit.ScriptModule)
    assert loaded_model.get_cutoff() == model_cutoff

    # 4. test outputs
    loaded_outputs = loaded_model(
        # mock the graph that would be passed through from LAMMPS
        {
            **graph,
            "compute_virial": torch.tensor(True),
            "debug": torch.tensor(False),
        }
    )
    assert isinstance(loaded_outputs, dict)
    assert set(loaded_outputs.keys()) == {
        "energy",
        "local_energies",
        "forces",
        "virial",
        "stress",
    }
    assert loaded_outputs["energy"].shape == torch.Size([])
    torch.testing.assert_close(
        outputs["energy"],
        loaded_outputs["energy"],
        atol=1e-6,
        rtol=1e-6,
    )

    assert loaded_outputs["local_energies"].shape == (number_of_atoms(graph),)
    torch.testing.assert_close(
        outputs["local_energies"],
        loaded_outputs["local_energies"],
        atol=1e-6,
        rtol=1e-6,
    )

    assert loaded_outputs["forces"].shape == graph["_positions"].shape
    torch.testing.assert_close(
        outputs["forces"],
        loaded_outputs["forces"],
        atol=1e-6,
        rtol=1e-6,
    )

    assert loaded_outputs["stress"].shape == (3, 3)
    torch.testing.assert_close(
        outputs["stress"],
        loaded_outputs["stress"],
        atol=1e-6,
        rtol=1e-6,
    )

    assert loaded_outputs["virial"].shape == (6,)


def test_deploy_smoothed_pair_potential(tmp_path: Path):
    model = SmoothedPairPotential(LennardJones(cutoff=2.5))
    test_deploy(model, tmp_path)
