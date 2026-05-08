import subprocess
import sys


PIPELINE_STEPS = [
    "src/generate_slabs.py",
    "src/place_adsorbates.py",
    "src/run_fairchem_relax.py",
    "src/compute_descriptors.py",
    "src/generate_catmap_input.py",
]


def run_step(script_path: str):
    print("=" * 60)
    print(f"Running: {script_path}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, script_path],
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Pipeline failed at: {script_path}"
        )


def main():
    print("Starting Ru-M oxide screening pipeline")

    for step in PIPELINE_STEPS:
        run_step(step)

    print("=" * 60)
    print("Pipeline completed successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()