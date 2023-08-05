import pytest
from maggma.stores import JSONStore, MemoryStore

from emmet.builders.qchem.molecules import MoleculesAssociationBuilder, MoleculesBuilder
from emmet.builders.molecules.redox import RedoxBuilder
from emmet.builders.molecules.thermo import ThermoBuilder


__author__ = "Evan Spotte-Smith <ewcspottesmith@lbl.gov>"


@pytest.fixture(scope="session")
def tasks_store(test_dir):
    return JSONStore(test_dir / "C2H4.json.gz")


@pytest.fixture(scope="session")
def mol_store(tasks_store):
    assoc_store = MemoryStore(key="molecule_id")
    stage_one = MoleculesAssociationBuilder(tasks=tasks_store, assoc=assoc_store)
    stage_one.run()

    mol_store = MemoryStore(key="molecule_id")
    stage_two = MoleculesBuilder(assoc=assoc_store, molecules=mol_store)
    stage_two.run()

    return mol_store


@pytest.fixture(scope="session")
def redox_store():
    return MemoryStore()


@pytest.fixture(scope="session")
def thermo_store():
    return MemoryStore()


def test_redox_builder(tasks_store, mol_store, thermo_store, redox_store):
    thermo_builder = ThermoBuilder(tasks_store, mol_store, thermo_store)
    thermo_builder.run()

    builder = RedoxBuilder(tasks_store, mol_store, thermo_store, redox_store)
    builder.run()

    assert redox_store.count() == 22
    assert redox_store.count({"deprecated": True}) == 0
