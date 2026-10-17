import logging
import sys
import os
import shutil

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("load_slides_from_clouds")

googleDrivePath = "/Users/korbi/gdrive/GoodNotes/TUM"
obsidianVaultPath = "/Users/korbi/vaults/uni"

courses: list[str]

def main():
    had_errors = False
    googleDriveDirs = os.listdir(googleDrivePath)
    obsidianDirs = os.listdir(obsidianVaultPath)

    for course in googleDriveDirs:
        if course not in obsidianDirs:
            log.info("Course %s is missing in Obsidian vault", course)
            had_errors = True
            continue
        else:
            for file in os.listdir(os.path.join(googleDrivePath, course, "Folien")):
                if file.endswith(".pdf"):
                    
                    dst = os.path.join(obsidianVaultPath, course, "slides", file)
                    src = os.path.join(googleDrivePath, course, "Folien", file)

                    try:
                        shutil.copy2(src, dst)
                    except Exception as e:
                        had_errors = True
                        log.error("Error occurred while copying file %s: %s", src, str(e))
        return 1 if had_errors else 0

if __name__ == "__main__":
    sys.exit(main())