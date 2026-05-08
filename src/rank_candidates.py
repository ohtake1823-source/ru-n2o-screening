from pathlib import Path
import pandas as pd


TARGET_O_ADSORPTION = -2.0


def main():
    descriptors = pd.read_csv(
        "data/results/substituted_descriptors.csv"
    )

    pivot = descriptors.pivot_table(
        index=[
            "material_id",
            "nominal_formula",
            "M_element",
            "Ru_fraction",
            "M_fraction",
        ],
        columns="adsorbate",
        values="adsorption_energy_eV",
        aggfunc="mean",
    ).reset_index()

    pivot["average_adsorption_energy"] = pivot[
        ["O", "O2", "N2O"]
    ].mean(axis=1)

    pivot["ranking_score"] = (
        (pivot["O"] - TARGET_O_ADSORPTION).abs()
        + pivot["O2"].abs() * 0.5
        + pivot["N2O"].abs() * 0.2
    )

    pivot = pivot.sort_values(
        "ranking_score",
        ascending=True,
    )

    pivot["ranking_position"] = range(
        1,
        len(pivot) + 1,
    )

    pivot = pivot.rename(
        columns={
            "O": "O_adsorption_energy",
            "O2": "O2_adsorption_energy",
            "N2O": "N2O_adsorption_energy",
        }
    )

    pivot["notes"] = (
        "placeholder ranking; replace with fairchem/CatMAP descriptors"
    )

    output_dir = Path("data/results")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "candidate_ranking.csv"

    pivot.to_csv(output_path, index=False)

    print("Candidate ranking completed")
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()