from pathlib import Path
import pandas as pd

from pymatgen.core import Lattice, Structure
from pymatgen.core.surface import SlabGenerator


def build_rutile_ruo2() -> Structure:
    """Build a simple rutile RuO2 bulk structure."""
    lattice = Lattice.tetragonal(a=4.49, c=3.11)

    structure = Structure(
        lattice,
        species=["Ru", "Ru", "O", "O", "O", "O"],
        coords=[
            [0.0, 0.0, 0.0],
            [0.5, 0.5, 0.5],
            [0.305, 0.305, 0.0],
            [0.695, 0.695, 0.0],
            [0.805, 0.195, 0.5],
            [0.195, 0.805, 0.5],
        ],
        coords_are_cartesian=False,
    )

    return structure


def generate_slab(
    structure: Structure,
    miller_index=(1, 1, 0),
    min_slab_size=10.0,
    min_vacuum_size=15.0,
):
    """Generate one RuO2 slab from a bulk structure."""
    slabgen = SlabGenerator(
        initial_structure=structure,
        miller_index=miller_index,
        min_slab_size=min_slab_size,
        min_vacuum_size=min_vacuum_size,
        center_slab=True,
    )

    slabs = slabgen.get_slabs(symmetrize=False)
    return slabs[0]


def main():
    output_dir = Path("data/slabs")
    output_dir.mkdir(parents=True, exist_ok=True)

    bulk = build_rutile_ruo2()
    slab = generate_slab(bulk, miller_index=(1, 1, 0))

    slab_path = output_dir / "RuO2_110_slab.cif"
    slab.to(filename=str(slab_path))

    metadata = pd.DataFrame(
        [
            {
                "material": "RuO2",
                "structure_type": "rutile",
                "miller_index": "(1,1,0)",
                "file_path": str(slab_path),
                "num_sites": len(slab),
            }
        ]
    )

    metadata_path = output_dir / "slab_metadata.csv"
    metadata.to_csv(metadata_path, index=False)

    print("RuO2 slab generation completed")
    print(f"Saved slab: {slab_path}")
    print(f"Saved metadata: {metadata_path}")


if __name__ == "__main__":
    main()