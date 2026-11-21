class InvalidRegistration(Exception):
    pass

def valid_email(email):
    email = email.strip()
    if " " in email or email.count("@") != 1:
        return False
    local, domain = email.split("@")
    if not local or not domain:
        return False
    if "." not in domain or domain.startswith(".") or domain.endswith("."):
        return False
    return True

def parse_line(line):
    parts = [part.strip() for part in line.strip().split(",")]
    if len(parts) != 5:
        raise InvalidRegistration(
            f"expected 5 fields, found {len(parts)}"
        )

    reg_no, name, department, email, event_text = parts
    if not reg_no or not name or not department or not email:
        raise InvalidRegistration("one or more required fields are empty")

    if not valid_email(email):
        raise InvalidRegistration(f"invalid e-mail '{email}'!")

    events = [event.strip() for event in event_text.split(";")
              if event.strip()]

    if not events:
        raise InvalidRegistration("no event selected")

    return {
        "register_number": reg_no,
        "name": name,
        "department": department,
        "email": email,
        "events": events
    }
