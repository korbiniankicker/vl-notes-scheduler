#!/usr/bin/env python3
import json
import logging
import sys
from datetime import date
from pathlib import Path

CONFIG = Path(__file__).resolve().parent / "schedule.json"
WEEKDAYS = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("create_notes")


def is_lecture_day(lecture, today):
    start = date.fromisoformat(lecture["start"])
    end = date.fromisoformat(lecture["end"])
    weekdays = {WEEKDAYS[d.lower()] for d in lecture["weekdays"]}
    skip = {date.fromisoformat(d) for d in lecture.get("skip", [])}
    return start <= today <= end and today.weekday() in weekdays and today not in skip


def create_note(vault, lecture, today):
    name = lecture["name"]
    folder = Path(vault).expanduser() / lecture["folder"]
    folder.mkdir(parents=True, exist_ok=True)
    note_path = folder / f"{today.isoformat()} {name}.md"

    try:
        with open(note_path, "x") as note_file:  # "x" = fail if the file already exists
            note_file.write(f"# {name}\n\n")
            note_file.write(f"Date: {today}\n\n")
            note_file.write("## Notes\n\n")
    except FileExistsError:
        log.info("already exists, skipping: %s", note_path)
        return
    log.info("created %s", note_path)


def main():
    today = date.today()

    try:
        with open(CONFIG) as file:
            data = json.load(file)
    except FileNotFoundError:
        log.error("config not found: %s", CONFIG)
        return 1
    except json.JSONDecodeError as e:
        log.error("invalid JSON in %s: %s", CONFIG, e)
        return 1

    had_errors = False
    vault = data.get("vault")
    if not vault:
        log.error("json not formatted correctly, missing vault path: %r", data)
        had_errors = True

    for lecture in data.get("lectures", []):
        try:
            if is_lecture_day(lecture, today):
                create_note(vault, lecture, today)
        except Exception:
            log.exception("failed for lecture %r", lecture.get("name"))
            had_errors = True

    return 1 if had_errors else 0


if __name__ == "__main__":
    sys.exit(main())    
