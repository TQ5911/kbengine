#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import argparse
import subprocess
import glob

def parse_arguments():
    parser = argparse.ArgumentParser(description="Import SQL files from subdirectories into MySQL databases based on config files.")
    parser.add_argument("-h_mysql", "--host", default="localhost", help="MySQL server host (default: localhost)")
    parser.add_argument("-P", "--port", default="3306", help="MySQL server port (default: 3306)")
    parser.add_argument("-u", "--user", required=True, help="MySQL username")
    parser.add_argument("-p", "--password", required=True, help="MySQL password")
    parser.add_argument("-c", "--charset", default="utf8mb4", help="Character set (default: utf8mb4)")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing them")
    
    # Check if -h is used for help or host. argparse uses -h for help by default.
    # To support -h as host, we'd need to conflict_handler='resolve' or similar, but let's stick to standard argparse.
    # The shell script used -h for host. Let's support both if possible or just use --host.
    # Standard argparse: -h is help. Let's use -H for host or just rely on --host to avoid confusion, 
    # BUT the user might expect -h.
    # Let's try to override the default help.
    
    return parser.parse_args()

def get_db_name_from_config(folder_path):
    """
    Scans the folder for .json files and attempts to extract mysql.db.
    Returns the db name if found, otherwise None.
    """
    json_files = glob.glob(os.path.join(folder_path, "*.json"))
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                # Remove comments if any (standard json doesn't support comments but sometimes people add them)
                # A simple way is to use a library that supports comments or just try standard json.load
                # Given the environment, standard json.load is safest.
                try:
                    config = json.load(f)
                except json.JSONDecodeError:
                    print(f"Warning: Could not parse JSON file {json_file}. Skipping.")
                    continue
                
                if "mysql" in config and isinstance(config["mysql"], dict):
                    db_name = config["mysql"].get("db")
                    if db_name:
                        return db_name
        except Exception as e:
            print(f"Warning: Error reading {json_file}: {e}")
            
    return None

def main():
    # Only use basic args to avoid conflict with -h (help) if we want to mimic the shell script exactly 
    # we might need to do manual parsing, but let's use argparse for robustness.
    # ArgumentParser automatically handles --help. 
    # If the user provides -h, argparse shows help. 
    # If the shell script used -h for host, this is a breaking change for the flag shorthand.
    # However, standard linux tools use -h for help and -H or --host for host. 
    # I kept -h_mysql as the DEST in the parser above but the flag is -h_mysql... wait.
    # Let's just use --host and -H to be safe and clear.
    
    parser = argparse.ArgumentParser(description="Import SQL files from subdirectories.")
    parser.add_argument("--host", "-H", default="localhost", help="MySQL Host")
    parser.add_argument("--port", "-P", default="3306", help="MySQL Port")
    parser.add_argument("--user", "-u", required=True, help="MySQL User")
    parser.add_argument("--password", "-p", required=True, help="MySQL Password")
    parser.add_argument("--charset", "-c", default="utf8mb4", help="Charset")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    
    parser.add_argument("--clean", action="store_true", help="Drop all identified databases instead of importing")
    
    args = parser.parse_args()
    
    current_dir = os.getcwd()
    print(f"Scanning directory: {current_dir}")
    print("-" * 40)
    
    processed_count = 0
    skipped_count = 0
    error_count = 0
    
    # List all subdirectories
    dirs = [d for d in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, d))]
    
    for folder in dirs:
        folder_path = os.path.join(current_dir, folder)
        
        # Check for SQL files first
        sql_files = glob.glob(os.path.join(folder_path, "*.sql"))
        
        if not sql_files:
            continue
            
        print(f"\nProcessing folder: {folder}")
        
        # Determine database name
        db_name = get_db_name_from_config(folder_path)
        
        if not db_name:
            print(f"  [Warning] No valid 'mysql.db' configuration found in {folder}. Using folder name '{folder}' as fallback.")
            db_name = folder
        else:
            print(f"  Found database name from config: {db_name}")

        if args.clean:
            # Clean mode: Drop database
            drop_db_sql = f"DROP DATABASE IF EXISTS `{db_name}`;"
            cmd_drop = [
                "mysql", 
                "-h", args.host, 
                "-P", args.port, 
                "-u", args.user, 
                f"-p{args.password}", 
                "-e", drop_db_sql
            ]
            
            if args.dry_run:
                print(f"  [Dry Run] Executing: {' '.join(cmd_drop[:-1])} \"{drop_db_sql}\"")
                processed_count += 1
            else:
                try:
                    subprocess.run(cmd_drop, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                    print(f"  ✓ Database '{db_name}' dropped.")
                    processed_count += 1
                except subprocess.CalledProcessError as e:
                    print(f"  ✗ Failed to drop database {db_name}: {e.stderr.decode()}")
                    error_count += 1
            continue
            
        # 1. Create Database
        create_db_sql = f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET {args.charset} COLLATE {args.charset}_unicode_ci;"
        cmd_create = [
            "mysql", 
            "-h", args.host, 
            "-P", args.port, 
            "-u", args.user, 
            f"-p{args.password}", 
            "-e", create_db_sql
        ]
        
        if args.dry_run:
            print(f"  [Dry Run] Executing: {' '.join(cmd_create[:-1])} \"{create_db_sql}\"")
        else:
            try:
                # hide password in process list? subprocess calls are essentially safe from shell history but 
                # visible in ps. acceptable for this tool.
                subprocess.run(cmd_create, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                print(f"  Database '{db_name}' created (or exists).")
            except subprocess.CalledProcessError as e:
                print(f"  [Error] Failed to create database {db_name}: {e.stderr.decode()}")
                error_count += 1
                continue

        # 2. Import SQL files
        for sql_file in sql_files:
            file_name = os.path.basename(sql_file)
            print(f"  Importing {file_name}...")
            
            # Use shell=True to handle the redirection < properly or read file and pass to stdin
            # Using stdin is safer and cleaner in python
            
            cmd_import = [
                "mysql",
                "-h", args.host,
                "-P", args.port,
                "-u", args.user,
                f"-p{args.password}",
                db_name
            ]
            
            if args.dry_run:
                print(f"  [Dry Run] Executing: {' '.join(cmd_import)} < {sql_file}")
                processed_count += 1
            else:
                try:
                    with open(sql_file, 'r') as f_in:
                        subprocess.run(cmd_import, stdin=f_in, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                    print(f"  ✓ Imported {file_name}")
                    processed_count += 1
                except subprocess.CalledProcessError as e:
                    print(f"  ✗ Failed to import {file_name}: {e.stderr.decode()}")
                    error_count += 1

    print("\n" + "=" * 40)
    print("Execution Summary")
    print("=" * 40)
    print(f"SQL Files Processed: {processed_count}")
    print(f"Errors: {error_count}")
    print("=" * 40)

if __name__ == "__main__":
    main()
