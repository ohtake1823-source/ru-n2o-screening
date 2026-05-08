from pathlib import Path
import pandas as pd


def compute_adsorption_energy(
    slab_ads_energy,
    clean_slab_energy,
    gas_adsorbate_energy,
):
    """
    Compute adsorption energy.

    E_ads =
        E(slab+adsorbate)
        - E(clean slab)
        - E(gas adsorbate)
    """

    return (
        slab_ads_energy
        - clean_slab_energy
        - gas_adsorbate_energy
    )


def main():

    metadata_path = (
        "data/substituted_adsorbates/"
        "substituted_adsorbate_metadata.csv"
    )

    adsorbate_df = pd.read_csv(
        metadata_path
    )

    gas_phase_energies = {
        "O": -5.0,
        "O2": -10.0,
        "N2O": -15.0,
    }

    results = []

    for _, row in adsorbate_df.iterrows():

        adsorbate = row["adsorbate"]

        # Placeholder energies
        clean_slab_energy = (
            -100.0
            + row["Ru_fraction"] * -5.0
            + row["M_fraction"] * -2.0
        )

        slab_ads_energy = (
            clean_slab_energy
            + gas_phase_energies[
                adsorbate
            ]
            - 3.0
        )

        adsorption_energy = (
            compute_adsorption_energy(
                slab_ads_energy,
                clean_slab_energy,
                gas_phase_energies[
                    adsorbate
                ],
            )
        )

        results.append(
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
                "adsorbate":
                    adsorbate,
                "adsorption_energy_eV":
                    adsorption_energy,
                "adsorbate_structure_file":
                    row[
                        "adsorbate_structure_file"
                    ],
                "parent_slab_file":
                    row[
                        "parent_slab_file"
                    ],
                "backend":
                    "placeholder",
                "notes":
                    "placeholder energies",
            }
        )

    results_df = pd.DataFrame(
        results
    )

    output_dir = Path(
        "data/results"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_dir /
        "substituted_descriptors.csv"
    )

    results_df.to_csv(
        output_path,
        index=False,
    )

    print(
        "Substituted descriptor calculation completed"
    )

    print(
        f"Saved: {output_path}"
    )


if __name__ == "__main__":
    main()