from pathlib import Path
import argparse
import pandas as pd

from pymatgen.core import Structure
from pymatgen.io.ase import AseAtomsAdaptor


def load_uma_calculator():
    """Load UMA calculator."""

    from fairchem.core import (
        pretrained_mlip,
        FAIRChemCalculator,
    )

    predictor = (
        pretrained_mlip.get_predict_unit(
            "uma-s-1p2",
            device="cpu",
        )
    )

    calculator = FAIRChemCalculator(
        predictor,
        task_name="oc22",
    )

    return calculator


def compute_energy(
    structure_file: str,
    calculator,
):
    """Compute UMA energy."""

    structure = Structure.from_file(
        structure_file
    )

    atoms = (
        AseAtomsAdaptor.get_atoms(
            structure
        )
    )

    atoms.calc = calculator

    energy = (
        atoms.get_potential_energy()
    )

    return energy


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

        subset = subset.iloc[
            :args.limit
        ]

    print(
        "Loading UMA model..."
    )

    calculator = (
        load_uma_calculator()
    )

    print(
        "UMA model loaded."
    )

    results = []

    total = len(subset)

    for idx, (_, row) in enumerate(
        subset.iterrows(),
        start=1,
    ):

        structure_file = row[
            "adsorbate_structure_file"
        ]

        if (
            structure_file
            in completed_files
        ):

            print(
                f"[SKIP] "
                f"{structure_file}"
            )

            continue

        print(
            f"[{idx}/{total}] "
            f"Processing "
            f"{structure_file}"
        )

        try:

            energy = compute_energy(
                structure_file,
                calculator,
            )

            status = "success"

            print(
                f"Energy: "
                f"{energy:.6f} eV"
            )

        except Exception as error:

            energy = None

            status = (
                f"failed: {error}"
            )

            print(
                f"FAILED: {error}"
            )

        results.append(
            {
                "material_id":
                    row["material_id"],
                "nominal_formula":
                    row[
                        "nominal_formula"
                    ],
                "adsorbate":
                    row["adsorbate"],
                "adsorbate_structure_file":
                    structure_file,
                "predicted_energy_eV":
                    energy,
                "backend":
                    "uma-s-1p2",
                "status":
                    status,
            }
        )

        temp_df = pd.DataFrame(
            results
        )

        if not existing.empty:

            combined = pd.concat(
                [
                    existing,
                    temp_df,
                ],
                ignore_index=True,
            )

        else:

            combined = temp_df

        combined.to_csv(
            output_path,
            index=False,
        )

    print(
        "Batch UMA prediction completed"
    )

    print(
        f"Saved: {output_path}"
    )


if __name__ == "__main__":
    main()