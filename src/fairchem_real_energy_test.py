from pathlib import Path

from pymatgen.core import Structure
from pymatgen.io.ase import AseAtomsAdaptor


def main():
    structure_path = Path("data/adsorbates/RuO2_110_O.cif")

    structure = Structure.from_file(structure_path)
    atoms = AseAtomsAdaptor.get_atoms(structure)

    try:
        from fairchem.core import pretrained_mlip, FAIRChemCalculator
    except ImportError as error:
        print("Failed to import fairchem energy tools.")
        print(error)
        return

    try:
        predictor = pretrained_mlip.get_predict_unit(
             "uma-s-1p2",
            device="cpu",
        )

        calculator = FAIRChemCalculator(
            predictor,
            task_name="oc22",
        )

        atoms.calc = calculator

        energy = atoms.get_potential_energy()

        print("fairchem real energy test completed")
        print(f"Structure: {structure_path}")
        print(f"Number of atoms: {len(atoms)}")
        print(f"Potential energy: {energy:.6f} eV")

    except Exception as error:
        print("fairchem real energy calculation failed.")
        print(error)


if __name__ == "__main__":
    main()