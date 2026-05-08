from pathlib import Path
import pandas as pd


def is_fairchem_available() -> bool:
    """Check whether fairchem is installed."""
    try:
        import fairchem  # noqa: F401
        return True
    except ImportError:
        return False


def main():
    metadata_path = Path("data/adsorbates/adsorbate_metadata.csv")
    output_dir = Path("data/results")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "fairchem_energies.csv"

    adsorbate_metadata = pd.read_csv(metadata_path)

    fairchem_available = is_fairchem_available()

    if not fairchem_available:
        print("fairchem is not installed.")
        print("Writing placeholder energies instead.")

    placeholder_energies = {
        "O": -108.0,
        "O2": -112.0,
        "N2O": -120.0,
    }

    results = []

    for _, row in adsorbate_metadata.iterrows():
        adsorbate = row["adsorbate"]

        results.append(
            {
                "structure_file": row["file"],
                "adsorbate": adsorbate,
                "predicted_energy_eV": placeholder_energies.get(
                    adsorbate, None
                ),
                "backend": "placeholder"
                if not fairchem_available
                else "fairchem",
                "status": "placeholder"
                if not fairchem_available
                else "not_implemented",
            }
        )

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_path, index=False)

    print("Energy prediction table created")
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()