#!/usr/bin/env python3
"""
Migration script to move chat history files to the new chat_sessions/ directory.

This script:
1. Creates the chat_sessions/ directory if it doesn't exist
2. Moves all chat_history_*.json files to chat_sessions/
3. Moves all chat_metadata_*.json files to chat_sessions/
4. Moves settings.json to chat_sessions/
5. Provides a summary of the migration
"""

import os
import shutil
import glob
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def main():
    print_header("Chat Sessions Migration Script")
    
    # Configuration
    CHAT_SESSIONS_DIR = 'chat_sessions'
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print_error("Error: app.py not found!")
        print_info("Please run this script from the project root directory.")
        return 1
    
    print_info(f"Current directory: {os.getcwd()}")
    
    # Create chat_sessions directory if it doesn't exist
    if not os.path.exists(CHAT_SESSIONS_DIR):
        print_info(f"Creating {CHAT_SESSIONS_DIR}/ directory...")
        os.makedirs(CHAT_SESSIONS_DIR)
        print_success(f"Created {CHAT_SESSIONS_DIR}/ directory")
    else:
        print_info(f"{CHAT_SESSIONS_DIR}/ directory already exists")
    
    # Track migration statistics
    stats = {
        'chat_history': 0,
        'chat_metadata': 0,
        'settings': 0,
        'errors': 0
    }
    
    # Migrate chat history files
    print_header("Migrating Chat History Files")
    chat_history_files = glob.glob('chat_history_*.json')
    
    if chat_history_files:
        print_info(f"Found {len(chat_history_files)} chat history file(s)")
        for file in chat_history_files:
            try:
                dest = os.path.join(CHAT_SESSIONS_DIR, file)
                if os.path.exists(dest):
                    print_warning(f"Skipping {file} (already exists in destination)")
                else:
                    shutil.move(file, dest)
                    print_success(f"Moved {file}")
                    stats['chat_history'] += 1
            except Exception as e:
                print_error(f"Error moving {file}: {e}")
                stats['errors'] += 1
    else:
        print_info("No chat history files found in root directory")
    
    # Migrate metadata files
    print_header("Migrating Metadata Files")
    metadata_files = glob.glob('chat_metadata_*.json')
    
    if metadata_files:
        print_info(f"Found {len(metadata_files)} metadata file(s)")
        for file in metadata_files:
            try:
                dest = os.path.join(CHAT_SESSIONS_DIR, file)
                if os.path.exists(dest):
                    print_warning(f"Skipping {file} (already exists in destination)")
                else:
                    shutil.move(file, dest)
                    print_success(f"Moved {file}")
                    stats['chat_metadata'] += 1
            except Exception as e:
                print_error(f"Error moving {file}: {e}")
                stats['errors'] += 1
    else:
        print_info("No metadata files found in root directory")
    
    # Migrate settings file
    print_header("Migrating Settings File")
    settings_file = 'settings.json'
    
    if os.path.exists(settings_file):
        try:
            dest = os.path.join(CHAT_SESSIONS_DIR, settings_file)
            if os.path.exists(dest):
                print_warning(f"Skipping {settings_file} (already exists in destination)")
            else:
                shutil.move(settings_file, dest)
                print_success(f"Moved {settings_file}")
                stats['settings'] += 1
        except Exception as e:
            print_error(f"Error moving {settings_file}: {e}")
            stats['errors'] += 1
    else:
        print_info("No settings.json file found in root directory")
    
    # Print summary
    print_header("Migration Summary")
    
    total_moved = stats['chat_history'] + stats['chat_metadata'] + stats['settings']
    
    print(f"Chat history files moved:  {stats['chat_history']}")
    print(f"Metadata files moved:      {stats['chat_metadata']}")
    print(f"Settings files moved:      {stats['settings']}")
    print(f"{Colors.BOLD}Total files moved:         {total_moved}{Colors.END}")
    
    if stats['errors'] > 0:
        print(f"\n{Colors.RED}Errors encountered:        {stats['errors']}{Colors.END}")
    
    # Verify migration
    print_header("Verification")
    
    # Check what's in the chat_sessions directory
    chat_sessions_files = os.listdir(CHAT_SESSIONS_DIR)
    print_info(f"Files in {CHAT_SESSIONS_DIR}/: {len(chat_sessions_files)}")
    
    # Count each type
    history_count = len([f for f in chat_sessions_files if f.startswith('chat_history_')])
    metadata_count = len([f for f in chat_sessions_files if f.startswith('chat_metadata_')])
    settings_count = 1 if 'settings.json' in chat_sessions_files else 0
    
    print(f"  - Chat history files: {history_count}")
    print(f"  - Metadata files: {metadata_count}")
    print(f"  - Settings file: {settings_count}")
    
    # Check for remaining files in root
    remaining_history = glob.glob('chat_history_*.json')
    remaining_metadata = glob.glob('chat_metadata_*.json')
    remaining_settings = os.path.exists('settings.json')
    
    if remaining_history or remaining_metadata or remaining_settings:
        print_warning("\nRemaining files in root directory:")
        if remaining_history:
            print(f"  - Chat history files: {len(remaining_history)}")
        if remaining_metadata:
            print(f"  - Metadata files: {len(remaining_metadata)}")
        if remaining_settings:
            print(f"  - Settings file: 1")
    else:
        print_success("\nNo chat-related files remaining in root directory")
    
    # Final message
    print_header("Migration Complete!")
    
    if total_moved > 0:
        print_success(f"Successfully migrated {total_moved} file(s) to {CHAT_SESSIONS_DIR}/")
        print_info("\nYou can now start the application:")
        print(f"  {Colors.BOLD}python app.py{Colors.END}")
    else:
        print_info("No files needed to be migrated")
        print_info("Your chat sessions are already organized!")
    
    if stats['errors'] > 0:
        print_warning(f"\n{stats['errors']} error(s) occurred during migration")
        print_info("Please check the error messages above")
        return 1
    
    return 0

if __name__ == '__main__':
    try:
        exit_code = main()
        exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Migration cancelled by user{Colors.END}")
        exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.END}")
        exit(1)

