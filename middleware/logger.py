from datetime import datetime
import os


LOG_FILE = "logs/query_log.txt"


def write_log(user, sql, result, reason="", site=""):

    os.makedirs("logs", exist_ok=True)

    timestamp = datetime.now()

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp}\n")
        f.write(f"USER: {user}\n")
        f.write(f"SQL: {sql}\n")
        f.write(f"RESULT: {result}\n")

        if reason:
            f.write(f"REASON: {reason}\n")

        if site:
            f.write(f"SITE: {site}\n")

        f.write("-" * 60 + "\n")