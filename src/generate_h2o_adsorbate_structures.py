from pathlib import Path
import pandas as pd

from pymatgen.core import Structure, Molecule
from pymatgen.analysis.adsorption import AdsorbateSiteFinder


MAX_SITES_PER_SLAB = 3


def create_h2o_adsorbate():
    """
    Create H2O molecule.
    """

    return Molecule(
        ["O", "H", "H"],
        [
            [0.000, 0.000, 0.000],
            [0.758, 0.000, 0.504],
            [-0.758, 0.000, 0.504],
        ],
    )


def main():

    metadata_path = (
        "data/substituted_slabs/"
        "substituted_slab_metadata.csv"
    )

    slab_metadata = pd.read_csv(
        metadata_path
    )

    output_dir = Path(
        "data/h2o_adsorbates"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    h2o_metadata = []

    h2o = create_h2o_adsorbate()

    for _, row in slab_metadata.iterrows():

        slab = Structure.from_file(
            row["slab_file"]
        )

        asf = AdsorbateSiteFinder(
            slab
        )

        structures = (
            asf.generate_adsorption_structures(
                h2o
            )
        )

        for site_index, structure in enumerate(
            structures[:MAX_SITES_PER_SLAB]
        ):

            file_name = (
                f"{row['material_id']}_"
                f"H2O_site{site_index}.cif"
            )

            file_path = (
                output_dir / file_name
            )

            structure.to(
                filename=str(file_path)
            )

            h2o_metadata.append(
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
                        row[
                            "nominal_formula"
                        ],
                    "adsorption_site_index":
                        site_index,
                    "h2o_structure_file":
                        str(file_path),
                    "parent_slab_file":
                        row["slab_file"],
                    "notes":
                        "H2O adsorption structure",
                }
            )

    metadata_df = pd.DataFrame(
        h2o_metadata
    )

    metadata_output = (
        output_dir /
        "h2o_adsorbate_metadata.csv"
    )

    metadata_df.to_csv(
        metadata_output,
        index=False,
    )

    print(
        "H2O adsorption structures generated"
    )

    print(
        f"Number of structures: "
        f"{len(metadata_df)}"
    )

    print(
        f"Saved metadata: "
        f"{metadata_output}"
    )


if __name__ == "__main__":
    main()