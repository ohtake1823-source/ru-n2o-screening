from pathlib import Path
import argparse
import pandas as pd

from pymatgen.core import Structure
from pymatgen.io.ase import AseAtomsAdaptor


def load_uma_calculator():

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
    structure_file,
    calculator,
):

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
        "data/substituted_slabs/"
        "substituted_slab_metadata.csv"
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
        "clean_slab_energies.csv"
    )

    if output_path.exists():

        existing = pd.read_csv(
            output_path
        )

        completed = set(
            existing["slab_file"]
        )

    else:

        existing = pd.DataFrame()

        completed = set()

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

        slab_file = row["slab_file"]

        if slab_file in completed:

            print(
                f"[SKIP] {slab_file}"
            )

            continue

        print(
            f"[{idx}/{total}] "
            f"Processing "
            f"{slab_file}"
        )

        try:

            energy = compute_energy(
                slab_file,
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
                "slab_file":
                    slab_file,
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
        "Clean slab UMA calculation completed"
    )

    print(
        f"Saved: {output_path}"
    )


if __name__ == "__main__":
    main()