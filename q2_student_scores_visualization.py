
import requests
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:5000/students"

def fetch_scores():
    response = requests.get(API_URL, timeout=15)
    response.raise_for_status()
    return response.json()

def main():
    data = fetch_scores()

    names = [student["name"] for student in data]
    scores = [float(student["score"]) for student in data]

    average = sum(scores) / len(scores)
    print(f"Average score: {average:.2f}")

    plt.figure(figsize=(8, 5))
    plt.bar(names, scores)
    plt.axhline(
        average,
        color="red",
        linestyle="--",
        label=f"Average = {average:.1f}"
    )

    plt.xlabel("Student")
    plt.ylabel("Test Score")
    plt.title("Student Test Scores")
    plt.legend()
    plt.tight_layout()

    plt.savefig("scores_chart.png", dpi=150)
    print("Chart saved as scores_chart.png")

if __name__ == "__main__":
    main()
