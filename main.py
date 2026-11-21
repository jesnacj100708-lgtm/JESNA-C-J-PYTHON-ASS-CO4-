from pathlib import Path
from fest_registration import process_files, write_outputs

if __name__ == "__main__":
    input_files = [
        "inputs/department1.txt",
        "inputs/department2.txt",
        "inputs/department3.txt",
        "inputs/department4.txt",
        "inputs/department5.txt"
    ]

    result = process_files(input_files)
    write_outputs(result, "outputs")

    print("Processing completed.")
    print("Valid unique registrations:", len(result["master"]))
    print("Duplicates:", result["duplicates"])
    print("Invalid e-mails:", result["invalid_emails"])
    print("Damaged lines:", result["damaged"])
    print("Missing files:", result["missing"])
