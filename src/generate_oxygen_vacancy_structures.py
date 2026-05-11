from pathlib import Path
import pandas as pd

from pymatgen.core import Structure


MAX_VACANCY_SITES_PER_SLAB = 3


def get_surface_oxygen_indices(structure: Structure):
    """
    Select candidate surface oxygen atoms.

    Simple criterion:
    - oxygen atoms only
    - highest z-coordinate atoms are treated as surface oxygen candidates
    """

    oxygen_indices = [
        i
        for i, site in enumerate(structure)
        if site.specie.symbol == "O"
    ]

    oxygen_indices = sorted(
        oxygen_indices,
        key=lambda i: structure[i].coords[2],
        reverse=True,
    )

    return oxygen_indices[:MAX_VACANCY_SITES_PER_SLAB]


def main():
    metadata_path = (
        "data/substituted_slabs/"
        "substituted_slab_metadata.csv"
    )

    slab_metadata = pd.read_csv(metadata_path)

    output_dir = Path("data/vacancies")
    output_dir.mkdir(parents=True, exist_ok=True)

    vacancy_metadata = []

    for _, row in slab_metadata.iterrows():
        slab = Structure.from_file(row["slab_file"])

        vacancy_indices = get_surface_oxygen_indices(slab)

        for vacancy_site_index, atom_index in enumerate(vacancy_indices):
            vacancy_structure = slab.copy()
            removed_site = vacancy_structure[atom_index]

            vacancy_structure.remove_sites([atom_index])

            file_name = (
                f"{row['material_id']}_"
                f"vacancy_site{vacancy_site_index}.cif"
            )

            file_path = output_dir / file_name
            vacancy_structure.to(filename=str(file_path))

            vacancy_metadata.append(
                {
                    "material_id": row["material_id"],
                    "M_element": row["M_element"],
                    "Ru_fraction": row["Ru_fraction"],
                    "M_fraction": row["M_fraction"],
                    "nominal_formula": row["nominal_formula"],
                    "vacancy_site_index": vacancy_site_index,
                    "removed_atom_index": atom_index,
                    "removed_species": removed_site.specie.symbol,
                    "vacancy_structure_file": str(file_path),
                    "parent_slab_file": row["slab_file"],
                    "notes": "surface oxygen vacancy generated from highest-z oxygen atoms",
                }
            )

    metadata_df = pd.DataFrame(vacancy_metadata)

    metadata_path = output_dir / "vacancy_metadata.csv"
    metadata_df.to_csv(metadata_path, index=False)

    print("Oxygen vacancy structures generated")
    print(f"Number of vacancy structures: {len(metadata_df)}")
    print(f"Saved metadata: {metadata_path}")


if __name__ == "__main__":
    main()