from pathlib import Path
import pandas as pd


def main():

    descriptors = pd.read_csv(
        "data/results/descriptors.csv"
    )

    fairchem = pd.read_csv(
        "data/results/fairchem_energies.csv"
    )

    merged = descriptors.merge(
        fairchem,
        on="adsorbate",
        how="left",
        suffixes=(
            "_descriptor",
            "_fairchem",
        ),
    )

    catmap_rows = []

    for _, row in merged.iterrows():

        catmap_rows.append(
            {
                "surface": "RuO2_110",
                "adsorbate": row["adsorbate"],
                "adsorption_energy_eV":
                    row["adsorption_energy_eV"],
                "source":
                    row["backend"],
            }
        )

    catmap_df = pd.DataFrame(
        catmap_rows
    )

    output_dir = Path("data/catmap")
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_dir /
        "catmap_input.csv"
    )

    catmap_df.to_csv(
        output_path,
        index=False,
    )

    print(
        "CatMAP input generation completed"
    )

    print(
        f"Saved: {output_path}"
    )


if __name__ == "__main__":
    main()