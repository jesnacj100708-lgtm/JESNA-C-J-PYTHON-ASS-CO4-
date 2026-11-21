from pathlib import Path
from .reader import parse_line, InvalidRegistration

def process_files(paths):
    master = {}
    seen_registers = set()
    event_groups = {}
    errors = []
    duplicate_count = 0
    invalid_email_count = 0
    damaged_count = 0
    missing_count = 0

    for path_value in paths:
        path = Path(path_value)
        try:
            with path.open("r", encoding="utf-8") as file:
                for line_number, line in enumerate(file, start=1):
                    if not line.strip():
                        continue
                    try:
                        record = parse_line(line)
                    except InvalidRegistration as error:
                        message = str(error)
                        errors.append(
                            (str(path), line_number, line.strip(), message)
                        )
                        damaged_count += 1
                        if message.startswith("invalid e-mail"):
                            invalid_email_count += 1
                        continue

                    reg_no = record["register_number"]
                    if reg_no in seen_registers:
                        duplicate_count += 1
                        errors.append((
                            str(path), line_number, line.strip(),
                            f"duplicate registration: {reg_no}"
                        ))
                        continue

                    seen_registers.add(reg_no)
                    master[reg_no] = record

                    for event in record["events"]:
                        event_groups.setdefault(event, []).append(record)

        except FileNotFoundError as error:
            missing_count += 1
            errors.append((str(path), 0, "", f"missing file: {error}"))

        except (PermissionError, UnicodeDecodeError, OSError) as error:
            errors.append((
                str(path), 0, "",
                f"{type(error).__name__}: {error}"
            ))

    return {
        "master": master,
        "events": event_groups,
        "errors": errors,
        "duplicates": duplicate_count,
        "invalid_emails": invalid_email_count,
        "damaged": damaged_count,
        "missing": missing_count
    }
