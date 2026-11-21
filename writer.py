from pathlib import Path
import csv

def write_outputs(result, output_folder="outputs"):
    folder = Path(output_folder)
    folder.mkdir(parents=True, exist_ok=True)

    # Clean master list
    with (folder / "master_list.csv").open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow([
            "Register Number", "Name", "Department", "Email", "Events"
        ])

        for record in result["master"].values():
            writer.writerow([
                record["register_number"],
                record["name"],
                record["department"],
                record["email"],
                ";".join(record["events"])
            ])

    # Separate participant file for every event
    for event, participants in result["events"].items():
        safe_name = "".join(
            ch if ch.isalnum() or ch in "-_" else "_"
            for ch in event
        )

        with (folder / f"{safe_name}_participants.csv").open(
            "w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow(["Register Number", "Name", "Department"])

            for record in participants:
                writer.writerow([
                    record["register_number"],
                    record["name"],
                    record["department"]
                ])

    # Summary report
    with (folder / "summary_report.txt").open(
        "w", encoding="utf-8"
    ) as file:
        file.write(
            f"Valid unique registrations: {len(result['master'])}\n\n"
        )
        file.write(
            f"Duplicate registrations: {result['duplicates']}\n\n"
        )
        file.write(
            f"Invalid e-mails: {result['invalid_emails']}\n\n"
        )
        file.write(
            f"Damaged/invalid lines: {result['damaged']}\n\n"
        )
        file.write(
            f"Missing department files: {result['missing']}\n\n"
        )

        file.write("Participants per event:\n")
        for event, participants in sorted(result["events"].items()):
            file.write(f"{event}: {len(participants)}\n")

    # Error log
    with (folder / "error_log.csv").open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["File", "Line Number", "Record", "Reason"])
        writer.writerows(result["errors"])
