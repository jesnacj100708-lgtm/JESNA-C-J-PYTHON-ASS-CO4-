# attendance_utils.py
from pathlib import Path

def read_records(folder):
    records = []
    for path in Path(folder).glob("*.csv"):
        with path.open(encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 3 and parts[2] in ("P", "A"):
                    records.append(tuple(parts))
    return records


def percentage(records):
    counts = {}
    for reg, date, status in records:
        counts.setdefault(reg, [0, 0])
        counts[reg][0 if status == "P" else 1] += 1

    return {reg: (a, b, a / (a + b) * 100)
            for reg, (a, b) in counts.items()}


def write_report(summary, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for reg, (p_count, a_count, pct) in summary.items():
            file.write(f"{reg},{p_count},{a_count},{pct:.2f}%\n")
