from pathlib import Path
import pandas as pd

from pymatgen.core import Structure, Molecule
from pymatgen.analysis.adsorption import AdsorbateSiteFinder


def create_adsorbate(name: str) -> Molecule:
    if name == "O":
        return Molecule(["O"], [[0, 0, 0]])

    if name == "O2":
        return Molecule(["O", "O"], [[0, 0, 0], [0, 0, 1.21]])

    if name == "N2O":
        return Molecule(
            ["N", "N", "O"],
            [[0, 0, 0], [0, 0, 1.13], [0, 0, 2.32]],
        )

    raise ValueError(f"Unknown adsorbate: {name}")


def main():
    slab_metadata = pd.read_csv(
        "data/substituted_slabs/substituted_slab_metadata.csv"
    )

    output_dir = Path("data/substituted_adsorbates")
    output_dir.mkdir(parents=True, exist_ok=True)

    adsorbates = ["O", "O2", "N2O"]
    metadata = []

    for _, row in slab_metadata.iterrows():
        slab = Structure.from_file(row["slab_file"])
        asf = AdsorbateSiteFinder(slab)

        for adsorbate_name in adsorbates:
            adsorbate = create_adsorbate(adsorbate_name)
            structures = asf.generate_adsorption_structures(adsorbate)

            if len(structures) == 0:
                continue

            file_name = (
                f"{row['material_id']}_"
                f"{adsorbate_name}_adsorbed.cif"
            )
            file_path = output_dir / file_name

            structures[0].to(filename=str(file_path))

            metadata.append(
                {
                    "material_id": row["material_id"],
                    "M_element": row["M_element"],
                    "Ru_fraction": row["Ru_fraction"],
                    "M_fraction": row["M_fraction"],
                    "nominal_formula": row["nominal_formula"],
                    "adsorbate": adsorbate_name,
                    "adsorbate_structure_file": str(file_path),
                    "parent_slab_file": row["slab_file"],
                    "notes": "first generated adsorption structure",
                }
            )

    metadata_df = pd.DataFrame(metadata)

    metadata_path = (
        output_dir / "substituted_adsorbate_metadata.csv"
    )
    metadata_df.to_csv(metadata_path, index=False)

    print("Adsorbates placed on substituted slabs")
    print(f"Saved metadata: {metadata_path}")


if __name__ == "__main__":
    main()