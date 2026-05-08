from pathlib import Path
import pandas as pd
import yaml


def load_material_config():
    """Load material settings from YAML."""
    with open(
        "configs/materials.yaml",
        "r",
    ) as f:
        return yaml.safe_load(f)


def create_formula(
    ru_fraction,
    m_fraction,
    m_element,
):
    """Generate nominal formula string."""

    if ru_fraction == 1.0:
        return "RuO2"

    if ru_fraction == 0.0:
        return f"{m_element}Ox"

    return (
        f"Ru{ru_fraction:.2f}"
        f"{m_element}{m_fraction:.2f}Ox"
    )


def main():

    config = load_material_config()

    m_elements = (
        config["materials"]["M_elements"]
    )

    ru_ratios = (
        config["materials"]["Ru_ratios"]
    )

    compositions = []

    material_counter = 1

    for m in m_elements:

        for ru_fraction in ru_ratios:

            m_fraction = (
                1.0 - ru_fraction
            )

            # Avoid duplicated RuO2
            if (
                ru_fraction == 1.0
                and m != m_elements[0]
            ):
                continue

            formula = create_formula(
                ru_fraction,
                m_fraction,
                m,
            )

            compositions.append(
                {
                    "material_id":
                        f"MAT_{material_counter:03d}",
                    "M_element": m,
                    "Ru_fraction":
                        ru_fraction,
                    "M_fraction":
                        m_fraction,
                    "nominal_formula":
                        formula,
                    "notes":
                        "Ru-M oxide screening",
                }
            )

            material_counter += 1

    compositions_df = pd.DataFrame(
        compositions
    )

    output_dir = Path(
        "data/compositions"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_dir /
        "composition_list.csv"
    )

    compositions_df.to_csv(
        output_path,
        index=False,
    )

    print(
        "Composition list generated"
    )

    print(
        f"Saved: {output_path}"
    )


if __name__ == "__main__":
    main()