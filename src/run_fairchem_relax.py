from pathlib import Path
import pandas as pd


def is_fairchem_available() -> bool:
    """Check whether fairchem is installed."""
    try:
        import fairchem  # noqa: F401
        return True
    except ImportError:
        return False


def predict_energy_with_fairchem_placeholder_interface(
    structure_file: str,
    adsorbate: str,
):
    """
    Placeholder interface for future fairchem/Open Catalyst energy prediction.

    This function currently returns placeholder energies even when fairchem is
    installed. Later, this is where the real fairchem calculator will be called.
    """

    placeholder_energies = {
        "O": -108.0,
        "O2": -112.0,
        "N2O": -120.0,
    }

    return placeholder_energies.get(adsorbate, None)


def main():
    metadata_path = Path("data/adsorbates/adsorbate_metadata.csv")
    output_dir = Path("data/results")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "fairchem_energies.csv"

    adsorbate_metadata = pd.read_csv(metadata_path)

    fairchem_available = is_fairchem_available()

    if fairchem_available:
        print("fairchem is installed.")
        print("Using placeholder fairchem interface for now.")
    else:
        print("fairchem is not installed.")
        print("Writing placeholder energies instead.")

    results = []

    for _, row in adsorbate_metadata.iterrows():
        adsorbate = row["adsorbate"]
        structure_file = row["file"]

        predicted_energy = (
            predict_energy_with_fairchem_placeholder_interface(
                structure_file=structure_file,
                adsorbate=adsorbate,
            )
        )

        results.append(
            {
                "structure_file": structure_file,
                "adsorbate": adsorbate,
                "predicted_energy_eV": predicted_energy,
                "backend": (
                    "fairchem_placeholder_interface"
                    if fairchem_available
                    else "placeholder"
                ),
                "status": (
                    "fairchem_installed_placeholder_used"
                    if fairchem_available
                    else "placeholder_no_fairchem"
                ),
            }
        )

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_path, index=False)

    print("Energy prediction table created")
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()