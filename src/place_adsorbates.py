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

    o_ads = create_o_adsorbate()
    o2_ads = create_o2_adsorbate()
    n2o_ads = create_n2o_adsorbate()

    output_dir = Path("data/adsorbates")
    output_dir.mkdir(parents=True, exist_ok=True)

    o_structures = asf.generate_adsorption_structures(o_ads)
    o2_structures = asf.generate_adsorption_structures(o2_ads)
    n2o_structures = asf.generate_adsorption_structures(n2o_ads)
    metadata = []

    if len(o_structures) > 0:
        o_file = output_dir / "RuO2_110_O.cif"
        o_structures[0].to(filename=str(o_file))

        metadata.append(
            {
                "adsorbate": "O",
                "file": str(o_file),
                "num_sites": len(o_structures[0]),
            }
        )

    if len(o2_structures) > 0:
        o2_file = output_dir / "RuO2_110_O2.cif"
        o2_structures[0].to(filename=str(o2_file))

        metadata.append(
            {
                "adsorbate": "O2",
                "file": str(o2_file),
                "num_sites": len(o2_structures[0]),
            }
        )

    if len(n2o_structures) > 0:
        n2o_file = output_dir / "RuO2_110_N2O.cif"
        n2o_structures[0].to(filename=str(n2o_file))

        metadata.append(
            {
                "adsorbate": "N2O",
                "file": str(n2o_file),
                "num_sites": len(n2o_structures[0]),
            }
        )

    metadata_df = pd.DataFrame(metadata)

    metadata_path = output_dir / "adsorbate_metadata.csv"
    metadata_df.to_csv(metadata_path, index=False)

    print("Adsorbate placement completed")
    print(f"Saved metadata: {metadata_path}")


if __name__ == "__main__":
    main()