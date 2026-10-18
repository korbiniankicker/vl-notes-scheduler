import logging
import sys
import os
import shutil
import time
import json


logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("load_slides_from_clouds")

try:
    with open("config.json") as f:
        config = json.load(f)
except FileNotFoundError:
    logging.error("config.json not found")
    sys.exit(1)

googleDrivePath = config["google_drive_path"]
obsidianVaultPath = config["obsidian_vault_path"]
pollingInterval = config["polling_interval"]
valid_folders = config["valid_folders"]


def main():
    had_errors = False
    googleDriveDirs = os.listdir(googleDrivePath)
    obsidianDirs = os.listdir(obsidianVaultPath)

    for course in googleDriveDirs:
        if course.startswith("."):
            continue  
        if course not in obsidianDirs:
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

    return 1 if had_errors else 0

def check_if_file_changed(sec, dst) -> bool:
    if not os.path.exists(dst):
        return True
    src_mtime = os.stat(sec).st_mtime
    dst_mtime = os.stat(dst).st_mtime   
    return src_mtime > dst_mtime

if __name__ == "__main__":
    while True:
        exit_code = main()
        if exit_code == 1:
            log.warning("Some files were not copied due to errors.")
        time.sleep(pollingInterval)
         
