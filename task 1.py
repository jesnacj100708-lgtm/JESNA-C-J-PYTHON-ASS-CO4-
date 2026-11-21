from decimal import Decimal, InvalidOperation
def process_mess_file(filename):
    total = Decimal("0.00")
    report_lines = []
    rejected_lines = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    parts = [part.strip() for part in line.split(",")]
                    if len(parts) != 3:
                        raise ValueError("expected exactly 3 fields")
                    reg_no, name, amount_text = parts
                    amount = Decimal(amount_text)
                    if amount < 0:
                        raise ValueError("amount cannot be negative")
                    total += amount
                    report_lines.append(
                        f"{reg_no} | {name} | Rs. {amount:.2f}"
                    )
                except (ValueError, InvalidOperation) as error:
                    rejected_lines.append(
                        f"Line {line_number}: {line!r} - {error}"
                    )
    except FileNotFoundError:
        print(f"Input file not found: {filename}")
        return
    with open("mess_report.txt", "w", encoding="utf-8") as report:
        report.write("\\n".join(report_lines))
        report.write(f"\\nTotal: Rs. {total:.2f}\\n")
    with open("rejected_lines.txt", "w", encoding="utf-8") as error_file:
        error_file.write("\\n".join(rejected_lines))
    print("\\n".join(report_lines))
    print(f"Total: Rs. {total:.2f}")
    print("Rejected records:", len(rejected_lines))
if __name__ == "__main__":
    process_mess_file("mess_oct.txt")
