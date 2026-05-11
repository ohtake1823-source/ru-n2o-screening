from pathlib import Path
import pandas as pd

from ase import Atoms


def load_uma_calculator():
    from fairchem.core import pretrained_mlip, FAIRChemCalculator

    predictor = pretrained_mlip.get_predict_unit(
        "uma-s-1p2",
        device="cpu",
    )

    return FAIRChemCalculator(
        predictor,
        task_name="oc22",
    )


def compute_energy(atoms, calculator):
    atoms.calc = calculator
    return atoms.get_potential_energy()


def main():
    output_dir = Path("data/results")
    output_dir.mkdir(parents=True, exist_ok=True)

    calculator = load_uma_calculator()

    gas_molecules = {
        "O2": Atoms(
            "O2",
            positions=[
                [0, 0, 0],
                [0, 0, 1.21],
            ],
            cell=[20, 20, 20],
            pbc=False,
        ),
        "N2O": Atoms(
            "N2O",
            positions=[
                [0, 0, 0],
                [0, 0, 1.13],
                [0, 0, 2.32],
            ],
            cell=[20, 20, 20],
            pbc=False,
        ),
        "H2O": Atoms(
            "H2O",
            positions=[
                [0.000, 0.000, 0.000],
                [0.758, 0.000, 0.504],
                [-0.758, 0.000, 0.504],
            ],
            cell=[20, 20, 20],
            pbc=False,
        ),
        ),
    }

    results = []

    for name, atoms in gas_molecules.items():
        try:
            energy = compute_energy(atoms, calculator)
            status = "success"
            print(f"{name}: {energy:.6f} eV")
        except Exception as error:
            energy = None
            status = f"failed: {error}"
            print(f"{name} FAILED: {error}")

        results.append(
            {
                "molecule": name,
                "predicted_energy_eV": energy,
                "backend": "uma-s-1p2",
                "status": status,
            }
        )

    output_path = output_dir / "gas_reference_energies.csv"
    pd.DataFrame(results).to_csv(output_path, index=False)

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()