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

valid_folders = {"Folien", "Übungen"}

def main():
    had_errors = False
    googleDriveDirs = os.listdir(googleDrivePath)
    print("gdrive:", googleDriveDirs)
    obsidianDirs = os.listdir(obsidianVaultPath)
    print("obsidian:", obsidianDirs)

    for course in googleDriveDirs:
        if course.startswith("."):
            continue  
        if course not in obsidianDirs:
            log.info("Course %s is missing in Obsidian vault", course)
            had_errors = True
            continue
        else:
            for folder in os.listdir(os.path.join(googleDrivePath, course)):
                if folder in valid_folders:
                    for file in os.listdir(os.path.join(googleDrivePath, course, folder)):
                        if file.startswith("."):
                            continue
                        if file.endswith(".pdf"):
                            src = os.path.join(googleDrivePath, course, folder, file)
                            dst = os.path.join(obsidianVaultPath, course, folder, file)
                            if check_if_file_changed(src, dst):
                                log.info("Copying %s to %s", src, dst)
                                try:
                                    shutil.copy2(src, dst)
                                except Exception as e:
                                    had_errors = True
                                    log.error("Error occurred while copying file %s: %s", src, str(e))
                            else:
                                log.info("File %s is up to date, skipping copy", file)
    return 1 if had_errors else 0

def check_if_file_changed(sec, dst) -> bool:
    if not os.path.exists(dst):
        return True
    src_mtime = os.stat(sec).st_mtime
    dst_mtime = os.stat(dst).st_mtime   
    return src_mtime > dst_mtime

if __name__ == "__main__":
    sys.exit(main())