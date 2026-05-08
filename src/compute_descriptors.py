from pathlib import Path
import pandas as pd


def compute_adsorption_energy(
    slab_ads_energy,
    clean_slab_energy,
    gas_adsorbate_energy,
):
    """
    Compute adsorption energy.

    E_ads = E(slab+adsorbate)
            - E(clean slab)
            - E(gas adsorbate)
    """
    return (
        slab_ads_energy
        - clean_slab_energy
        - gas_adsorbate_energy
    )


def main():
    adsorbate_metadata = pd.read_csv(
        "data/adsorbates/adsorbate_metadata.csv"
    )

    # Placeholder energies
    clean_slab_energy = -100.0

    gas_phase_energies = {
        "O": -5.0,
        "O2": -10.0,
        "N2O": -15.0,
    }

    slab_adsorption_energies = {
        "O": -108.0,
        "O2": -112.0,
        "N2O": -120.0,
    }

    results = []

    for _, row in adsorbate_metadata.iterrows():

        adsorbate = row["adsorbate"]

        e_ads = compute_adsorption_energy(
            slab_ads_energy=slab_adsorption_energies[
                adsorbate
            ],
            clean_slab_energy=clean_slab_energy,
            gas_adsorbate_energy=gas_phase_energies[
                adsorbate
            ],
        )

        results.append(
            {
                "adsorbate": adsorbate,
                "adsorption_energy_eV": e_ads,
                "structure_file": row["file"],
            }
        )

    results_df = pd.DataFrame(results)

    output_dir = Path("data/results")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = (
        output_dir / "descriptors.csv"
    )

    results_df.to_csv(output_path, index=False)

    print("Descriptor calculation completed")
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()