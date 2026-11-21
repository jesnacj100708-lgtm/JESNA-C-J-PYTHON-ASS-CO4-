import os
import tempfile 
class InvalidRecord(Exception):
    """Raised when an attendance line is not in the expected format."""
    pass
def parse_line(line):
    parts = line.strip().split(",")
    if len(parts) != 3:
        raise InvalidRecord(
            f"expected 3 fields, found {len(parts)}"
        )
    register_number, date, status = parts
    if status not in ("P", "A"):
        raise InvalidRecord(f"invalid status '{status}'")
    if not register_number or not date:
        raise InvalidRecord("register number and date cannot be empty")
    return register_number, date, status
def summarise(path):
    present, absent, errors = 0, 0, []
    try:
        with open(path, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                if not line.strip():
                    continue
                try:
                    register_number, date, status = parse_line(line)
                except InvalidRecord as error:
                    errors.append((line_number, str(error)))
                    continue
                if status == "P":
                    present += 1
                else:
                    absent += 1
    except FileNotFoundError as error:
        raise RuntimeError(f"attendance file not found: {path}") from error
    except PermissionError as error:
        raise RuntimeError(f"permission denied: {path}") from error
    except UnicodeDecodeError as error:
        raise RuntimeError(f"file encoding error: {path}") from error
    else:
        # This block runs when the file is read without a file-level error.
        pass
    finally:
        # The with statement closes the file; finally is useful for
        # cleanup or logging that must happen on every path.
        pass
    return present, absent, errors
data = (
    "192311001,2026-10-08,P\\n"
    "192311002,2026-10-08,A\\n"
    "192311003,2026-10-08\\n"
    "192311004,2026-10-08,L\\n"
)
with tempfile.NamedTemporaryFile(
    "w", suffix=".csv", delete=False, encoding="utf-8"
) as tmp:
    tmp.write(data)
    temp_path = tmp.name
try:
    print(summarise(temp_path))
finally:
    os.remove(temp_path)
