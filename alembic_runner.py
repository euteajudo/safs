#!/usr/bin/env python3
"""
Comprehensive Alembic migration runner for SAFS project
"""
import os
import sys
import subprocess
from pathlib import Path
import traceback

def run_command(command, cwd=None):
    """Run a command and return the result"""
    try:
        print(f"\n>>> Running: {' '.join(command)}")
        if cwd:
            print(f">>> In directory: {cwd}")
        
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            cwd=cwd,
            shell=False
        )
        
        print(f">>> Return code: {result.returncode}")
        
        if result.stdout.strip():
            print(">>> STDOUT:")
            print(result.stdout)
        
        if result.stderr.strip():
            print(">>> STDERR:")
            print(result.stderr)
            
        return result
        
    except Exception as e:
        print(f">>> Error running command: {e}")
        traceback.print_exc()
        return None

def main():
    # Get the project root directory
    project_root = Path(__file__).parent
    backend_dir = project_root / "backend" / "backend"
    
    print(f"Project root: {project_root}")
    print(f"Backend directory: {backend_dir}")
    print(f"Backend directory exists: {backend_dir.exists()}")
    
    if not backend_dir.exists():
        print("ERROR: Backend directory not found!")
        return 1
    
    # Check if virtual environment exists
    venv_dir = backend_dir / "venv"
    venv_python = venv_dir / "Scripts" / "python.exe"
    venv_alembic = venv_dir / "Scripts" / "alembic.exe"
    
    if venv_python.exists():
        print(f"Using virtual environment Python: {venv_python}")
        python_cmd = str(venv_python)
        alembic_cmd = str(venv_alembic) if venv_alembic.exists() else [str(venv_python), "-m", "alembic"]
    else:
        print("Using system Python")
        python_cmd = sys.executable
        alembic_cmd = [python_cmd, "-m", "alembic"]
    
    # Ensure alembic_cmd is a list
    if isinstance(alembic_cmd, str):
        alembic_cmd = [alembic_cmd]
    
    print(f"Python command: {python_cmd}")
    print(f"Alembic command: {alembic_cmd}")
    
    # Check if .env file exists
    env_file = backend_dir / ".env"
    print(f".env file exists: {env_file.exists()}")
    
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            env_content = f.read()
            print("Environment file content:")
            for line in env_content.split('\n'):
                if line.strip() and not line.startswith('#'):
                    if 'PASSWORD' in line:
                        key, _ = line.split('=', 1)
                        print(f"  {key}=****")
                    else:
                        print(f"  {line}")
    
    # Step 1: Check current migration status
    print("\n" + "="*60)
    print("STEP 1: Checking current Alembic status")
    print("="*60)
    
    result = run_command(alembic_cmd + ["current"], cwd=backend_dir)
    if result is None or result.returncode != 0:
        print("WARNING: Could not check current status. Continuing...")
    
    # Step 2: Show migration history
    print("\n" + "="*60)
    print("STEP 2: Showing migration history")
    print("="*60)
    
    result = run_command(alembic_cmd + ["history"], cwd=backend_dir)
    if result is None or result.returncode != 0:
        print("WARNING: Could not show history. Continuing...")
    
    # Step 3: Show pending migrations
    print("\n" + "="*60)
    print("STEP 3: Showing pending migrations")
    print("="*60)
    
    result = run_command(alembic_cmd + ["show", "head"], cwd=backend_dir)
    if result is None or result.returncode != 0:
        print("WARNING: Could not show head. Continuing...")
    
    # Step 4: Apply migrations
    print("\n" + "="*60)
    print("STEP 4: Applying migrations to head")
    print("="*60)
    
    result = run_command(alembic_cmd + ["upgrade", "head"], cwd=backend_dir)
    if result is None:
        print("ERROR: Could not run upgrade command!")
        return 1
    elif result.returncode != 0:
        print("ERROR: Migration failed!")
        print("This could be due to:")
        print("1. Database connection issues")
        print("2. PostgreSQL server not running")
        print("3. Database credentials incorrect")
        print("4. Migration conflicts")
        return 1
    else:
        print("SUCCESS: Migrations applied successfully!")
    
    # Step 5: Verify final status
    print("\n" + "="*60)
    print("STEP 5: Verifying final migration status")
    print("="*60)
    
    result = run_command(alembic_cmd + ["current"], cwd=backend_dir)
    if result is None or result.returncode != 0:
        print("WARNING: Could not verify final status")
    else:
        print("Migration verification completed!")
    
    print("\n" + "="*60)
    print("MIGRATION PROCESS COMPLETED")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)