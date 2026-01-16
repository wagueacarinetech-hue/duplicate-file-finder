# Duplicate File Finder

A Python script that automatically detects and organizes duplicate files in your Downloads folder. Uses MD5 hashing to compare file contents, ensuring true duplicates are found even when filenames differ.

## Features

- **Smart Detection**: Uses MD5 hashing to identify duplicates by content, not just filename
- **Safe Organization**: Moves duplicates to a separate folder for review (never auto-deletes)
- **Automated Scheduling**: Can be set to run daily at a specific time
- **Keeps Oldest**: Preserves the original file, moves newer copies
- **Detailed Logging**: Shows exactly what was found and moved

## How It Works

The script scans your Downloads folder and:
1. Calculates an MD5 hash (digital fingerprint) for each file
2. Identifies files with matching hashes as duplicates
3. Keeps the oldest version in Downloads
4. Moves newer duplicates to `Downloads/duplicates/` folder
5. Logs all actions for your review

## Installation

### Prerequisites
- Python 3.x
- macOS (can be adapted for Windows/Linux)

### Setup

1. Clone this repository:
```bash
git clone https://github.com/wagueacarinetech-hue/duplicate-file-finder.git
cd duplicate-file-finder
```

2. Make the script executable:
```bash
chmod +x duplicate_finder.py
```

3. Test it manually:
```bash
python3 duplicate_finder.py
```

## Usage

### Run Manually
```bash
python3 duplicate_finder.py
```

### Schedule Daily Execution (macOS)

To run automatically at 10 AM every day:

1. Create a launch agent plist file:
```bash
nano ~/Library/LaunchAgents/com.user.duplicatefinder.plist
```

2. Add this configuration (replace `YOUR_USERNAME` with your actual username):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.duplicatefinder</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/YOUR_USERNAME/path/to/duplicate_finder.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>10</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/YOUR_USERNAME/Library/Logs/duplicate_finder.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/YOUR_USERNAME/Library/Logs/duplicate_finder_error.log</string>
</dict>
</plist>
```

3. Load the schedule:
```bash
launchctl load ~/Library/LaunchAgents/com.user.duplicatefinder.plist
```

4. Verify it's running:
```bash
launchctl list | grep duplicatefinder
```

## Example Output

```
=== Duplicate File Finder ===
Date: 2026-01-15 10:00:00
Checking: /Users/username/Downloads

Scanning for duplicates...
Found 41 duplicate file(s) in 29 group(s)

Found 6 duplicate(s) of: report.pdf
  Moved: report-1.pdf -> duplicates/
  Moved: report-2.pdf -> duplicates/
  Moved: report (1).pdf -> duplicates/
  ...

=== Summary ===
Moved 41 duplicate file(s) to: /Users/username/Downloads/duplicates
You can review and delete them when ready.
```

## Configuration

You can modify the script to:
- Change the target folder (default: `~/Downloads`)
- Change the duplicates folder name (default: `duplicates`)
- Use a different hash algorithm (SHA256 instead of MD5 for stronger verification)

## Why MD5?

This script uses MD5 hashing for duplicate detection because:
- Fast and efficient for file comparison
- Sufficient for identifying identical files
- Well-suited for non-security applications

For file verification where security matters, consider using SHA256 instead.

## Troubleshooting

**Script doesn't find my duplicates:**
- Ensure files have identical content (not just similar names)
- Check file permissions

**Scheduled task not running:**
- Verify the plist file is loaded: `launchctl list | grep duplicatefinder`
- Check logs: `cat ~/Library/Logs/duplicate_finder.log`

**Permission errors:**
- Ensure script is executable: `chmod +x duplicate_finder.py`
- Grant Terminal full disk access in System Preferences > Privacy & Security

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built to solve the common problem of accumulating duplicate downloads over time. Inspired by the need for a simple, automated solution that doesn't require manual file management.
