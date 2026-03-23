"""Daylio CSV exports to Markdown converter."""

import argparse
import csv
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, TypedDict, cast

import frontmatter  # type: ignore

TAG_DAYLIO_EXPORT = "daylio-export"


class MoodScore(Enum):
    """Enum representing Daylio mood levels with corresponding numerical scores."""

    AMAZING = 5
    HAPPY = 4
    AVERAGE = 3
    SAD = 2
    HORRIBLE = 1


class CSVRow(TypedDict):
    """Daylio CSV rows."""

    full_date: str
    date: str
    weekday: str
    time: str
    mood: str
    activities: str
    note_title: str | None
    note: str | None


def parse_csv(input_path: Path) -> list[CSVRow]:
    """Parse tCSV file and return list of entry dictionaries."""
    with open(input_path, encoding="utf-8-sig") as f_in:
        reader = csv.DictReader(f_in)

        return [cast(CSVRow, row) for row in reader]


def convert_to_24hr(time_str: str) -> str:
    """Convert 12-hour time format to 24-hour format."""
    return datetime.strptime(time_str.strip(), "%I:%M\u202f%p").strftime("%H:%M")


def parse_activities(activities_str: str) -> list[str]:
    """Parse the activities string into a list of activities."""
    activities_str = activities_str.strip()

    return [a.strip() for a in activities_str.split("|")] if activities_str else []


def format_note_content(row: CSVRow) -> str:
    """Format the note content from a CSVRow's title and body."""
    content_parts: list[str] = []

    note_title = (row["note_title"] or "").strip()
    note_body = (row["note"] or "").strip()

    if note_title:
        content_parts.append(f"# {note_title}")
    if note_body:
        note_body = note_body.replace("nbsp;", " ").replace("<br>", "\n")
        content_parts.append(note_body)

    return "\n\n".join(content_parts)


def process_entry(row: CSVRow) -> tuple[str, str, dict[str, Any]]:
    """Process a CSV row and return date, content, and frontmatter data."""
    full_date = row["full_date"]
    time = convert_to_24hr(row["time"])
    created_at = f"{full_date}T{time}"

    activities = parse_activities(row["activities"])
    mood = row["mood"].strip()
    mood_value = MoodScore[mood.upper()].value
    content = format_note_content(row)

    frontmatter_data = {
        "created_at": created_at,
        "mood": mood,
        "mood-score": mood_value,
        "activities": activities,
        "tags": [TAG_DAYLIO_EXPORT],
    }

    return full_date, content, frontmatter_data


def write_note(
    output_path: Path,
    date_str: str,
    content: str,
    frontmatter_data: dict[str, Any],
) -> None:
    """Write a Markdown file with frontmatter to the output directory.

    If the output exists, a new one will be added with an incremented index."""
    page = frontmatter.Post(content, **frontmatter_data)
    output_file = output_path / f"{date_str}.md"

    if output_file.exists():
        index = 1
        while True:
            candidate = output_path / f"{date_str} {index}.md"
            if not candidate.exists():
                output_file = candidate
                break
            index += 1

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(page))

    print(f"- {output_file}")


def clear_output_directory(output_path: Path) -> None:
    """Remove existing files in the output directory."""
    for path in output_path.iterdir():
        if path.is_file():
            path.unlink()


def convert_csv_to_notes(input_path: Path, output_path: Path) -> None:
    """Convert Daylio CSV export to individual Markdown files."""
    output_path.mkdir(parents=True, exist_ok=True)
    clear_output_directory(output_path)

    entries = parse_csv(input_path)
    print(f"Processing {len(entries)} entries.")

    unique_activities: set[str] = set()

    for row in entries:
        date_str, content, frontmatter_data = process_entry(row)
        unique_activities.update(frontmatter_data.get("activities", []))
        write_note(output_path, date_str, content, frontmatter_data)

    print(f"Created {len(entries)} notes in {output_path}.")
    print()

    sorted_activities = sorted(unique_activities, key=str.casefold)
    print("Unique activities:")
    for activity in sorted_activities:
        print(f"- {activity}")


def main():
    """Main command-line entry-point."""
    parser = argparse.ArgumentParser(
        prog="daylio2md",
        description="Convert Daylio CSV export to individual Markdown files.",
    )
    parser.add_argument(
        "input",
        metavar="INPUT_CSV",
        type=Path,
        help="Path to the input CSV file exported from Daylio.",
    )
    parser.add_argument(
        "output",
        metavar="OUTPUT_DIR",
        type=Path,
        help="Path to an output directory. This will be created if necessary.",
    )

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: Input file '{args.input}' does not exist")
        return

    convert_csv_to_notes(args.input, args.output)


if __name__ == "__main__":
    main()
