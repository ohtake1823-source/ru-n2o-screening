from pathlib import Path

from pymatgen.core import Structure
from pymatgen.io.ase import AseAtomsAdaptor


def main():
    structure_path = Path("data/adsorbates/RuO2_110_O.cif")

    if not structure_path.exists():
        raise FileNotFoundError(f"Missing structure: {structure_path}")

    structure = Structure.from_file(structure_path)
    atoms = AseAtomsAdaptor.get_atoms(structure)

    try:
        import fairchem  # noqa: F401
    except ImportError:
        print("fairchem is not installed.")
        return

    print("fairchem import OK")
    print(f"Loaded structure: {structure_path}")
    print(f"Number of atoms: {len(atoms)}")
    print("Smoke test completed.")
    print("Real model loading will be added after this import/structure test.")


if __name__ == "__main__":
    main()