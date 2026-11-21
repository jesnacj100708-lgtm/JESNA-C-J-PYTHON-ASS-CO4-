# attendance_all.py
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

    return {
        reg: (p_count, a_count,
              p_count / (p_count + a_count) * 100)
        for reg, (p_count, a_count) in counts.items()
    }


def write_report(summary, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for reg, (present, absent, pct) in summary.items():
            file.write(f"{reg},{present},{absent},{pct:.2f}%\n")


if __name__ == "__main__":
    data = read_records("daily")
    result = percentage(data)
    write_report(result, "summary.csv")
