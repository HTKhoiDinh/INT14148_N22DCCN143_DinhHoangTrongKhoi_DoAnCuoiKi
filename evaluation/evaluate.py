import sys
import os

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


clean_queries = load_queries("datasets/clean.sql")
malicious_queries = load_queries("datasets/malicious.sql")

tp = 0
tn = 0
fp = 0
fn = 0

print("===== CLEAN QUERY TEST =====")

for query in clean_queries:
    is_blocked = detect(query)

    if is_blocked:
        fp += 1
        print("[FP] Blocked clean query:", query)
    else:
        tn += 1
        print("[TN] Allowed clean query:", query)

print("\n===== MALICIOUS QUERY TEST =====")

for query in malicious_queries:
    is_blocked = detect(query)

    if is_blocked:
        tp += 1
        print("[TP] Blocked malicious query:", query)
    else:
        fn += 1
        print("[FN] Missed malicious query:", query)

print("\n===== EVALUATION RESULT =====")

print("True Positive :", tp)
print("True Negative :", tn)
print("False Positive:", fp)
print("False Negative:", fn)

if (fp + tn) > 0:
    fpr = fp / (fp + tn)
else:
    fpr = 0

if (fn + tp) > 0:
    fnr = fn / (fn + tp)
else:
    fnr = 0

print("False Positive Rate =", fpr)
print("False Negative Rate =", fnr)

accuracy = (tp + tn) / (tp + tn + fp + fn)

print("Accuracy =", accuracy)