import sys
import os
import csv
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from middleware.detector import detect


def load_queries(file_path):
    queries = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line:
                queries.append(line)

    return queries


def save_csv_result(result):
    output_path = "evaluation/evaluation_result.csv"

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["Metric", "Value"])

        for key, value in result.items():
            writer.writerow([key, value])

    print(f"Saved CSV result to {output_path}")


def draw_confusion_matrix(tp, tn, fp, fn):
    import matplotlib.pyplot as plt

    matrix = [
        [tn, fp],
        [fn, tp]
    ]

    labels = [
        ["TN", "FP"],
        ["FN", "TP"]
    ]

    fig, ax = plt.subplots(figsize=(6, 5))

    im = ax.imshow(matrix, cmap="Blues")

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])

    ax.set_xticklabels(["Predicted Clean", "Predicted Malicious"], fontsize=12)
    ax.set_yticklabels(["Actual Clean", "Actual Malicious"], fontsize=12)

    # Hiển thị số trong từng ô
    for i in range(2):
        for j in range(2):
            value = matrix[i][j]

            # Nếu ô đậm thì chữ trắng, ô nhạt thì chữ đen
            text_color = "white" if value > max(tp, tn, fp, fn) / 2 else "black"

            ax.text(
                j,
                i,
                f"{labels[i][j]}\n{value}",
                ha="center",
                va="center",
                fontsize=16,
                fontweight="bold",
                color=text_color
            )

    ax.set_title("Confusion Matrix", fontsize=18, fontweight="bold", pad=12)

    plt.tight_layout()

    output_path = "evaluation/confusion_matrix.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved confusion matrix to {output_path}")


def draw_metrics_chart(accuracy, precision, recall, f1, fpr, fnr):
    metrics = [
        "Accuracy",
        "Precision",
        "Recall",
        "F1-score",
        "FPR",
        "FNR"
    ]

    values = [
        accuracy,
        precision,
        recall,
        f1,
        fpr,
        fnr
    ]

    plt.figure(figsize=(9, 5))
    plt.bar(metrics, values)

    plt.ylim(0, 1.1)
    plt.title("Evaluation Metrics")
    plt.ylabel("Score")

    for index, value in enumerate(values):
        plt.text(
            index,
            value + 0.03,
            f"{value:.2f}",
            ha="center"
        )

    plt.tight_layout()

    output_path = "evaluation/metrics_chart.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved metrics chart to {output_path}")


def draw_query_distribution(clean_count, malicious_count):
    labels = ["Clean Queries", "Malicious Queries"]
    values = [clean_count, malicious_count]

    plt.figure(figsize=(7, 5))
    plt.bar(labels, values)

    plt.title("Evaluation Dataset Distribution")
    plt.ylabel("Number of Queries")

    for index, value in enumerate(values):
        plt.text(
            index,
            value + 0.5,
            str(value),
            ha="center"
        )

    plt.tight_layout()

    output_path = "evaluation/query_distribution.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved query distribution chart to {output_path}")


def main():
    clean_queries = load_queries("datasets/clean.sql")
    malicious_queries = load_queries("datasets/malicious.sql")

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    print("===== CLEAN QUERY TEST =====")

    for query in clean_queries:
        blocked = detect(query)

        if blocked:
            fp += 1
            print("[FP] Blocked clean query:", query)
        else:
            tn += 1
            print("[TN] Allowed clean query:", query)

    print("\n===== MALICIOUS QUERY TEST =====")

    for query in malicious_queries:
        blocked = detect(query)

        if blocked:
            tp += 1
            print("[TP] Blocked malicious query:", query)
        else:
            fn += 1
            print("[FN] Missed malicious query:", query)

    total = tp + tn + fp + fn

    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
    fnr = fn / (fn + tp) if (fn + tp) > 0 else 0
    accuracy = (tp + tn) / total if total > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    result = {
        "Clean Queries": len(clean_queries),
        "Malicious Queries": len(malicious_queries),
        "True Positive": tp,
        "True Negative": tn,
        "False Positive": fp,
        "False Negative": fn,
        "False Positive Rate": fpr,
        "False Negative Rate": fnr,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1-score": f1
    }

    print("\n===== EVALUATION RESULT =====")

    for key, value in result.items():
        print(f"{key}: {value}")

    save_csv_result(result)
    draw_confusion_matrix(tp, tn, fp, fn)
    draw_metrics_chart(accuracy, precision, recall, f1, fpr, fnr)
    draw_query_distribution(len(clean_queries), len(malicious_queries))


if __name__ == "__main__":
    main()