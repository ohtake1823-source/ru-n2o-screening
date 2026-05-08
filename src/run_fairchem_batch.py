from pathlib import Path
import argparse
import pandas as pd


def placeholder_predict_energy(
    adsorbate: str,
):
    """Placeholder energy predictor."""

    placeholder_energies = {
        "O": -108.0,
        "O2": -112.0,
        "N2O": -120.0,
    }

    return placeholder_energies.get(
        adsorbate,
        None,
    )


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
    )

    parser.add_argument(
        "--start-index",
        type=int,
        default=0,
    )

    args = parser.parse_args()

    metadata_path = (
        "data/substituted_adsorbates/"
        "substituted_adsorbate_metadata.csv"
    )

    metadata = pd.read_csv(
        metadata_path
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
        "fairchem_batch_energies.csv"
    )

    if output_path.exists():
        existing = pd.read_csv(
            output_path
        )

        completed_files = set(
            existing[
                "adsorbate_structure_file"
            ]
        )

    else:
        existing = pd.DataFrame()
        completed_files = set()

    subset = metadata.iloc[
        args.start_index:
    ]

    if args.limit is not None:
        subset = subset.iloc[:args.limit]

    results = []

    total = len(subset)

    for idx, (_, row) in enumerate(
        subset.iterrows(),
        start=1,
    ):

        structure_file = row[
            "adsorbate_structure_file"
        ]

        if structure_file in completed_files:

            print(
                f"[SKIP] "
                f"{structure_file}"
            )

            continue

        adsorbate = row["adsorbate"]

        print(
            f"[{idx}/{total}] "
            f"Processing "
            f"{structure_file}"
        )

        predicted_energy = (
            placeholder_predict_energy(
                adsorbate
            )
        )

        results.append(
            {
                "material_id":
                    row["material_id"],
                "nominal_formula":
                    row["nominal_formula"],
                "adsorbate":
                    adsorbate,
                "adsorbate_structure_file":
                    structure_file,
                "predicted_energy_eV":
                    predicted_energy,
                "backend":
                    "placeholder_batch",
            }
        )

    new_results = pd.DataFrame(
        results
    )

    if not existing.empty:
        final = pd.concat(
            [
                existing,
                new_results,
            ],
            ignore_index=True,
        )

    else:
        final = new_results

    final.to_csv(
        output_path,
        index=False,
    )

    print(
        "Batch energy prediction completed"
    )

    print(
        f"Saved: {output_path}"
    )


if __name__ == "__main__":
    main()