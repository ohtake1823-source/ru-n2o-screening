from pathlib import Path
import pandas as pd

from pymatgen.core import Structure, Molecule
from pymatgen.analysis.adsorption import AdsorbateSiteFinder


def load_slab(path: str) -> Structure:
    """Load slab structure from CIF file."""
    return Structure.from_file(path)


def create_o_adsorbate():
    """Create atomic oxygen adsorbate."""
    return Molecule(["O"], [[0, 0, 0]])


def create_o2_adsorbate():
    """Create O2 molecular adsorbate."""
    return Molecule(
        ["O", "O"],
        [
            [0, 0, 0],
            [0, 0, 1.21],
        ],
    )


def create_n2o_adsorbate():
    """Create N2O molecular adsorbate."""
    return Molecule(
        ["N", "N", "O"],
        [
            [0, 0, 0],
            [0, 0, 1.13],
            [0, 0, 2.32],
        ],
    )


def main():
    slab_path = "data/slabs/RuO2_110_slab.cif"

    slab = load_slab(slab_path)
    asf = AdsorbateSiteFinder(slab)

    adsorbates = {
        "O": create_o_adsorbate(),
        "O2": create_o2_adsorbate(),
        "N2O": create_n2o_adsorbate(),
    }

    output_dir = Path("data/adsorbates")
    output_dir.mkdir(parents=True, exist_ok=True)

    metadata = []

    for name, molecule in adsorbates.items():
        structures = asf.generate_adsorption_structures(molecule)

        if len(structures) == 0:
            continue

        file_path = output_dir / f"RuO2_110_{name}.cif"
        structures[0].to(filename=str(file_path))

        metadata.append(
            {
                "adsorbate": name,
                "file": str(file_path),
                "num_sites": len(structures[0]),
            }
        )

    metadata_df = pd.DataFrame(metadata)
    metadata_path = output_dir / "adsorbate_metadata.csv"
    metadata_df.to_csv(metadata_path, index=False)

    print("Adsorbate placement completed")
    print(f"Saved metadata: {metadata_path}")


if __name__ == "__main__":
    main()