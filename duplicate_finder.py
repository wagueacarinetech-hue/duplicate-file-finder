#!/usr/bin/env python3
"""
Duplicate File Finder for Downloads Folder
Finds duplicate files based on content (hash) and moves them to a duplicates folder
"""

import hashlib
import os
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def get_file_hash(filepath):
    """Calculate MD5 hash of a file to identify duplicates by content"""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            # Read file in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error hashing {filepath}: {e}")
        return None

def find_duplicates(downloads_folder):
    """Find all duplicate files in the downloads folder"""
    hash_map = defaultdict(list)
    
    # Get all files in downloads folder (not subdirectories)
    for item in Path(downloads_folder).iterdir():
        if item.is_file():
            file_hash = get_file_hash(item)
            if file_hash:
                hash_map[file_hash].append(item)
    
    # Return only groups that have duplicates (more than 1 file with same hash)
    duplicates = {h: files for h, files in hash_map.items() if len(files) > 1}
    return duplicates

def move_duplicates(duplicates, duplicates_folder):
    """Move duplicate files to the duplicates folder, keeping the oldest"""
    Path(duplicates_folder).mkdir(exist_ok=True)
    
    moved_count = 0
    
    for file_hash, files in duplicates.items():
        # Sort by modification time (oldest first)
        files_sorted = sorted(files, key=lambda f: f.stat().st_mtime)
        
        # Keep the first (oldest) file, move the rest
        original = files_sorted[0]
        duplicates_to_move = files_sorted[1:]
        
        print(f"\nFound {len(duplicates_to_move)} duplicate(s) of: {original.name}")
        
        for dup_file in duplicates_to_move:
            try:
                # Create unique name if file already exists in duplicates folder
                dest_path = Path(duplicates_folder) / dup_file.name
                counter = 1
                while dest_path.exists():
                    name_parts = dup_file.stem, counter, dup_file.suffix
                    dest_path = Path(duplicates_folder) / f"{name_parts[0]}_copy{name_parts[1]}{name_parts[2]}"
                    counter += 1
                
                shutil.move(str(dup_file), str(dest_path))
                print(f"  Moved: {dup_file.name} -> duplicates/")
                moved_count += 1
            except Exception as e:
                print(f"  Error moving {dup_file.name}: {e}")
    
    return moved_count

def main():
    """Main function to find and move duplicate files"""
    # Set up paths
    home = Path.home()
    downloads_folder = home / "Downloads"
    duplicates_folder = downloads_folder / "duplicates"
    
    print(f"=== Duplicate File Finder ===")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Checking: {downloads_folder}\n")
    
    # Check if Downloads folder exists
    if not downloads_folder.exists():
        print(f"Error: Downloads folder not found at {downloads_folder}")
        return
    
    # Find duplicates
    print("Scanning for duplicates...")
    duplicates = find_duplicates(downloads_folder)
    
    if not duplicates:
        print("No duplicates found! Your Downloads folder is clean.")
        return
    
    # Count total duplicate files
    total_duplicates = sum(len(files) - 1 for files in duplicates.values())
    print(f"Found {total_duplicates} duplicate file(s) in {len(duplicates)} group(s)\n")
    
    # Move duplicates
    moved = move_duplicates(duplicates, duplicates_folder)
    
    print(f"\n=== Summary ===")
    print(f"Moved {moved} duplicate file(s) to: {duplicates_folder}")
    print("You can review and delete them when ready.")

if __name__ == "__main__":
    main()