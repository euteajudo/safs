#!/usr/bin/env python3
"""
Script to run Alembic migrations from the correct directory
"""
import os
import sys
import subprocess
from pathlib import Path

# Change to the backend/backend directory
backend_dir = Path(__file__).parent / "backend" / "backend"
print(f"Changing to directory: {backend_dir}")

try:
    os.chdir(backend_dir)
    print(f"Current directory: {os.getcwd()}")
    
    # Check current migration status
    print("\n=== Checking current Alembic status ===")
    result = subprocess.run([sys.executable, "-m", "alembic", "current"], 
                          capture_output=True, text=True)
    print(f"Return code: {result.returncode}")
    print(f"STDOUT:\n{result.stdout}")
    if result.stderr:
        print(f"STDERR:\n{result.stderr}")
    
    # Show available migrations
    print("\n=== Showing migration history ===")
    result = subprocess.run([sys.executable, "-m", "alembic", "history"], 
                          capture_output=True, text=True)
    print(f"Return code: {result.returncode}")
    print(f"STDOUT:\n{result.stdout}")
    if result.stderr:
        print(f"STDERR:\n{result.stderr}")
    
    # Apply migrations
    print("\n=== Applying migrations ===")
    result = subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], 
                          capture_output=True, text=True)
    print(f"Return code: {result.returncode}")
    print(f"STDOUT:\n{result.stdout}")
    if result.stderr:
        print(f"STDERR:\n{result.stderr}")
    
    # Verify final status
    print("\n=== Verifying final migration status ===")
    result = subprocess.run([sys.executable, "-m", "alembic", "current"], 
                          capture_output=True, text=True)
    print(f"Return code: {result.returncode}")
    print(f"STDOUT:\n{result.stdout}")
    if result.stderr:
        print(f"STDERR:\n{result.stderr}")
        
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)