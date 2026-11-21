from datetime import datetime

def save_returns(books, log_name="returns.log"):
    with open(log_name, "a", encoding="utf-8") as log:
        for book in books:
            clean_book = book.strip()
            if clean_book:
                log.write(clean_book + "\n")


def process(day_file):
    try:
        with open(day_file, "r", encoding="utf-8") as source:
            books = source.readlines()

        save_returns(books)

    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as error:
        with open("error.log", "a", encoding="utf-8") as errors:
            errors.write(
                f"{datetime.now().isoformat()} | {day_file} | "
                f"{type(error).__name__}: {error}\n"
            )


if __name__ == "__main__":
    process("day1.txt")
    process("day2.txt")
    process("day3.txt")
