from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def main():
    ranking = pd.read_csv(
        "data/results/candidate_ranking.csv"
    )

    top20 = ranking.head(20)

    output_dir = Path("data/results")
    output_dir.mkdir(parents=True, exist_ok=True)

    top20_path = output_dir / "top20_candidates.csv"
    top20.to_csv(top20_path, index=False)

    plt.figure(figsize=(10, 6))
    plt.barh(
        top20["nominal_formula"],
        top20["ranking_score"],
    )
    plt.xlabel("Ranking score")
    plt.ylabel("Candidate")
    plt.title("Top 20 Ru-M oxide candidates")
    plt.gca().invert_yaxis()
    plt.tight_layout()

    figure_path = output_dir / "candidate_ranking_top20.png"
    plt.savefig(figure_path, dpi=300)

    print("Candidate ranking plot completed")
    print(f"Saved figure: {figure_path}")
    print(f"Saved table: {top20_path}")


if __name__ == "__main__":
    main()