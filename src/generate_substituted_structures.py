from pathlib import Path
import pandas as pd

from pymatgen.core import Lattice, Structure


def build_rutile_ruo2() -> Structure:
    """Build a simple rutile RuO2 bulk structure."""
    lattice = Lattice.tetragonal(a=4.49, c=3.11)

    return Structure(
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


def make_supercell(structure: Structure) -> Structure:
    """Create a larger supercell so fractional substitution is possible."""
    supercell = structure.copy()
    supercell.make_supercell([2, 2, 1])
    return supercell


def substitute_ru_sites(
    structure: Structure,
    m_element: str,
    m_fraction: float,
) -> Structure:
    """Substitute a fraction of Ru sites with M."""
    substituted = structure.copy()

    ru_indices = [
        i for i, site in enumerate(substituted)
        if site.specie.symbol == "Ru"
    ]

    n_substitute = round(len(ru_indices) * m_fraction)

    for idx in ru_indices[:n_substitute]:
        substituted[idx] = m_element

    return substituted


def main():
    composition_path = "data/compositions/composition_list.csv"
    compositions = pd.read_csv(composition_path)

    output_dir = Path("data/substituted_structures")
    output_dir.mkdir(parents=True, exist_ok=True)

    metadata = []

    parent = make_supercell(build_rutile_ruo2())

    for _, row in compositions.iterrows():
        material_id = row["material_id"]
        m_element = row["M_element"]
        ru_fraction = row["Ru_fraction"]
        m_fraction = row["M_fraction"]
        nominal_formula = row["nominal_formula"]

        # Skip pure MOx for now because each M oxide has a different parent lattice.
        if ru_fraction == 0.0:
            continue

        structure = substitute_ru_sites(
            parent,
            m_element=m_element,
            m_fraction=m_fraction,
        )

        file_name = f"{material_id}_{nominal_formula}.cif"
        file_path = output_dir / file_name
        structure.to(filename=str(file_path))

        metadata.append(
            {
                "material_id": material_id,
                "M_element": m_element,
                "Ru_fraction": ru_fraction,
                "M_fraction": m_fraction,
                "nominal_formula": nominal_formula,
                "structure_file": str(file_path),
                "parent_lattice": "rutile_RuO2_2x2x1",
                "notes": "single simple substitution pattern",
            }
        )

    metadata_df = pd.DataFrame(metadata)

    metadata_path = output_dir / "substituted_structure_metadata.csv"
    metadata_df.to_csv(metadata_path, index=False)

    print("Substituted structures generated")
    print(f"Saved metadata: {metadata_path}")


if __name__ == "__main__":
    main()