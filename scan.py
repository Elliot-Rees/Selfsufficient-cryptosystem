import os
import win32api # type: ignore

# Function to scan for drives
def scan_for_drives(target_drive_name=None):
    found_drives = []
    if os.name == 'nt':  # Windows
        drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]
        potential_drives = [d for d in drives if os.path.exists(d) and os.path.isdir(d)]
    else:  # macOS and Linux
        potential_drives = [f"/media/{os.getlogin()}/{d}" for d in os.listdir(f"/media/{os.getlogin()}") if os.path.isdir(f"/media/{os.getlogin()}/{d}")]
    
    for drive in potential_drives:
        key_file_path = os.path.join(drive, "key.txt")
        if os.path.isfile(key_file_path):
            try:
                with open(key_file_path, "r") as file:
                    key = file.readline().strip()  # Read the first line as the key
                    if target_drive_name and target_drive_name.lower() in drive.lower():
                        key = f"{key}#"
                    found_drives.append({
                        "drive": drive,
                        "key": key
                    })
            except Exception as e:
                print(f"Error reading key file on drive {drive}: {e}")
    return found_drives

# Main program
def scan():
    # print("Scanning for drives with encryption keys")
    target_drive_name = "MyUSBDrive"  
    drives_with_keys = scan_for_drives(target_drive_name)
if __name__ == "__scan__":
    scan()