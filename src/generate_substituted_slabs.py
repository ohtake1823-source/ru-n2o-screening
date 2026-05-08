from pathlib import Path
import pandas as pd

from pymatgen.core import Structure
from pymatgen.core.surface import SlabGenerator


def generate_slab(
    structure: Structure,
    miller_index=(1, 1, 0),
    min_slab_size=10.0,
    min_vacuum_size=15.0,
):
    """Generate slab from bulk structure."""

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

    metadata_path = (
        "data/substituted_structures/"
        "substituted_structure_metadata.csv"
    )

    structures_df = pd.read_csv(
        metadata_path
    )

    output_dir = Path(
        "data/substituted_slabs"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    slab_metadata = []

    for _, row in structures_df.iterrows():

        structure = Structure.from_file(
            row["structure_file"]
        )

        slab = generate_slab(
            structure,
            miller_index=(1, 1, 0),
        )

        slab_file = (
            output_dir /
            f"{row['material_id']}"
            "_110_slab.cif"
        )

        slab.to(
            filename=str(slab_file)
        )

        slab_metadata.append(
            {
                "material_id":
                    row["material_id"],
                "M_element":
                    row["M_element"],
                "Ru_fraction":
                    row["Ru_fraction"],
                "M_fraction":
                    row["M_fraction"],
                "nominal_formula":
                    row["nominal_formula"],
                "miller_index":
                    "(1,1,0)",
                "slab_file":
                    str(slab_file),
                "parent_structure_file":
                    row["structure_file"],
                "notes":
                    "generated substituted slab",
            }
        )

    slab_metadata_df = pd.DataFrame(
        slab_metadata
    )

    metadata_output = (
        output_dir /
        "substituted_slab_metadata.csv"
    )

    slab_metadata_df.to_csv(
        metadata_output,
        index=False,
    )

    print(
        "Substituted slab generation completed"
    )

    print(
        f"Saved metadata: "
        f"{metadata_output}"
    )


if __name__ == "__main__":
    main()